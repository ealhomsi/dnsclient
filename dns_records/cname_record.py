from .dns_record import DNSRecord


class CNAMERecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, cname):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.cname = cname

    def __str__(self):
        return (f"CNAME\t{self.cname}\t{self.ttl}\t{self.auth}")