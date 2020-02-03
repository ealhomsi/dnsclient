from .dns_record import DNSRecord


class MXRecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, preference, exchange):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.preference = preference
        self.exchange = super().process_list(exchange)

    def __str__(self):
        return (f"MX\t{self.exchange}\t{self.preference}\t{self.ttl}\t{self.auth}")