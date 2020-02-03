from .dns_record import DNSRecord

class NSRecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, name_server):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.name_server = super().process_list(name_server)

    def __str__(self):
        return (f"NS\t{self.name_server}\t{self.ttl}\t{self.auth}")
