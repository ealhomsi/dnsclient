from .dns_record import DNSRecord

class SOARecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, primary, responsible, serialNumber, refreshInterval, retryInterval, expireLimit, minimumTTL):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.primary = primary
        self.responsible = responsible
        self.serialNumber = serialNumber
        self.refreshInterval = refreshInterval
        self.retryInterval = retryInterval
        self.expireLimit = expireLimit
        self.minimumTTL = minimumTTL

    def __str__(self):
        return (f"NS\t{self.domain_name}\t{self.ttl}\t{self.auth}")
