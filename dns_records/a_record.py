from .dns_record import DNSRecord


class ARecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, address):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.address = address

    def __str__(self):
        return (f"IP\t{self.address}\t{self.ttl}\t{self.auth}")
