from .dns_record import DNSRecord

class SOARecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, primary, responsible, serialNumber, refreshInterval, retryInterval, expireLimit, minimumTTL):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.primary = super().process_list(primary)
        self.responsible = super().process_list(responsible)
        self.serialNumber = serialNumber
        self.refreshInterval = refreshInterval
        self.retryInterval = retryInterval
        self.expireLimit = expireLimit
        self.minimumTTL = minimumTTL

    def __str__(self):
        return (f"SOA\t{self.primary}\t{self.ttl}\t{self.auth}")
