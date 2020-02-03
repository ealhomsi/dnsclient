from .dns_record import DNSRecord


class OTHERRecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, data):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.data = data

def __str__(self):
        return (f"OTHER\t{self.domain_name}\t{self.ttl}\t{self.auth}")