from .dns_record import DNSRecord


class MXRecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, preference, exchange):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.preference = preference
        self.exchange = self.collapse(exchange).decode()

    def collapse(self, l):
        flat_list = []
        for sublist in l:
            if type(sublist) is list:
                for item in sublist:
                    flat_list.append(item)
            elif type(sublist) is not int:
                flat_list.append(sublist)

        return b'.'.join(flat_list)

    def __str__(self):
        return (f"MX\t{self.exchange}\t{self.preference}\t{self.ttl}\t{self.auth}")