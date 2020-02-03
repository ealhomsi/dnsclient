from .dns_record import DNSRecord

class SOARecord(DNSRecord):
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength, primary, responsible, serialNumber, refreshInterval, retryInterval, expireLimit, minimumTTL):
        super().__init__(auth, domain_name, query_class, query_class, ttl, rdlength)
        self.primary = self.collapse(primary).decode()
        self.responsible = responsible
        self.serialNumber = serialNumber
        self.refreshInterval = refreshInterval
        self.retryInterval = retryInterval
        self.expireLimit = expireLimit
        self.minimumTTL = minimumTTL

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
        return (f"NS\t{self.primary}\t{self.ttl}\t{self.auth}")
