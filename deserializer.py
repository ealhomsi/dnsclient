
import struct
from query_type import QueryType
from dns_records import ARecord, CNAMERecord, MXRecord, OTHERRecord, SOARecord, NSRecord


class Deserializer:
    DNS_QUERY_MESSAGE_HEADER = struct.Struct("!6H")
    DNS_QUERY_SECTION_FORMAT = struct.Struct("!2H")
    DNS_QUERY_TTL_FORMAT = struct.Struct("!I")
    DNS_QUERY_RDLENGTH_FORMAT = struct.Struct("!H")
    DNS_QUERY_MX_PREFERENCE = struct.Struct("!H")

    def __init__(self):
        pass

    def build_response(self, message):
        id, misc, qdcount, ancount, nscount, arcount = self.DNS_QUERY_MESSAGE_HEADER.unpack_from(
            message)


        qr = (misc & 0x8000) != 0
        opcode = (misc & 0x7800) >> 11
        aa = (misc & 0x0400) != 0
        tc = (misc & 0x200) != 0
        rd = (misc & 0x100) != 0
        ra = (misc & 0x80) != 0
        z = (misc & 0x70) >> 4
        rcode = misc & 0xF

        offset = self.DNS_QUERY_MESSAGE_HEADER.size

        questions, offset = self.get_questions_section(
            message, offset, qdcount)

        answers, offset = self.get_section(message, offset, ancount, aa)
        authoritative, offset = self.get_section(message, offset, nscount, aa)
        additional, offset = self.get_section(message, offset, arcount, aa)

        result = {"id": id,
                  "qr": qr,
                  "op": opcode,
                  "aa": aa,
                  "tc": tc,
                  "rd": rd,
                  "ra": ra,
                  "z": z,
                  "rcode": rcode,
                  "qdcount": qdcount,
                  "ancount": ancount,
                  "nscount": nscount,
                  "arcount": arcount,
                  "questions": questions,
                  "answers": answers,
                  "authoritative": authoritative,
                  "additional": additional
                  }

        return result

    def get_labels(self, message, offset):
        labels = []

        while True:
            length, = struct.unpack_from("!B", message, offset)

            if (length & 0xC0) == 0xC0:
                pointer, = struct.unpack_from("!H", message, offset)
                offset += 2

                return (list(labels) + list(self.get_labels(message, pointer & 0x3FFF))), offset

            if (length & 0xC0) != 0x00:
                raise StandardError("unknown label encoding")

            offset += 1

            if length == 0:
                return labels, offset

            labels.append(*struct.unpack_from("!%ds" %
                                              length, message, offset))
            offset += length

    def get_questions_section(self, message, offset, qdcount):
        questions = []

        for _ in range(qdcount):
            qname, offset = self.get_labels(message, offset)

            qtype, qclass = self.DNS_QUERY_SECTION_FORMAT.unpack_from(
                message, offset)
            offset += self.DNS_QUERY_SECTION_FORMAT.size

            questions.append({
                "qname": qname,
                "qtype": qtype,
                "qclass": qclass
            })
        return questions, offset

    def get_section(self, message, offset, count, aa):
        records = []

        for _ in range(count):
            aname, offset = self.get_labels(message, offset)
            atype, aclass = self.DNS_QUERY_SECTION_FORMAT.unpack_from(
                message, offset)
            offset += self.DNS_QUERY_SECTION_FORMAT.size

            ttl, = self.DNS_QUERY_TTL_FORMAT.unpack_from(message, offset)
            offset += self.DNS_QUERY_TTL_FORMAT.size

            rdlength, = self.DNS_QUERY_RDLENGTH_FORMAT.unpack_from(
                message, offset)
            offset += self.DNS_QUERY_RDLENGTH_FORMAT.size
            
            auth = 'noauth'
            if(aa):
                auth = 'auth'
            record_dict = {
                "auth": auth,
                "domain_name": aname,
                "query_type": atype,
                "query_class": aclass,
                "ttl": ttl,
                "rdlength": rdlength
            }

            if(atype == QueryType.MX):
                record, offset = self.process_MX_record(
                    record_dict, message, offset)

            elif(atype == QueryType.NS):
                record, offset = self.process_NS_record(record_dict, message, offset)

            elif(atype == QueryType.A):
                record, offset = self.process_A_record(
                    record_dict, message, offset)

            elif(atype == QueryType.CNAME):
                record, offset = self.process_CNAME_record(
                    record_dict, message, offset)

            elif(atype == QueryType.SOA):
                record, offset = self.process_SOA_record(
                    record_dict, message, offset)

            else:
                record, offset = self.process_OTHER_record(
                    record_dict, message, offset)

            records.append(record)

        return records, offset

    def process_A_record(self, record_dict, message, offset):
        a, b, c, d = struct.unpack_from("!4B", message, offset)
        offset += struct.Struct("!4B").size

        record_dict.update({
            "address": f"{a}.{b}.{c}.{d}"
        })
        return ARecord(**record_dict), offset

    def process_CNAME_record(self, record_dict, message, offset):
        cname, offset = self.get_labels(message, offset)

        record_dict.update({
            "cname": cname
        })
        return CNAMERecord(**record_dict), offset

    def process_OTHER_record(self, record_dict, message, offset):
        rdlength = record_dict['rdlength']
        rdata = message[offset:offset+rdlength]
        offset += rdlength

        record_dict.update({
            "rdata": rdata
        })
        return OTHERRecord(**record_dict), offset

    def process_MX_record(self, record_dict, message, offset):
        preference, = self.DNS_QUERY_MX_PREFERENCE.unpack_from(message, offset)
        offset += self.DNS_QUERY_MX_PREFERENCE.size

        exchange, offset = self.get_labels(message, offset)

        record_dict.update({
            "preference": preference,
            "exchange": exchange
        })
        return MXRecord(**record_dict), offset

    def process_SOA_record(self, record_dict, message, offset):
        primary, offset = self.get_labels(message, offset)
        responsible, offset = self.get_labels(message, offset)
        serialNumber, = struct.unpack_from("!I", message, offset)
        offset += 4
        refreshInterval, = struct.unpack_from("!I", message, offset)
        offset += 4
        retryInterval, = struct.unpack_from("!I", message, offset)
        offset += 4
        expireLimit, = struct.unpack_from("!I", message, offset)
        offset += 4
        minimumTTL, = struct.unpack_from("!I", message, offset)
        offset += 4

        record_dict.update({
            "primary": primary,
            "responsible": responsible,
            "serialNumber": serialNumber,
            "refreshInterval": refreshInterval,
            "retryInterval": retryInterval,
            "expireLimit": expireLimit,
            "minimumTTL": minimumTTL
        })

        return SOARecord(**record_dict), offset
    
    def process_NS_record(self, record_dict, message, offset):
        name_server, offset = self.get_labels(message, offset)

        record_dict.update({
            "name_server": name_server,
        })

        return NSRecord(**record_dict), offset
        