#!/usr/bin/python3.8


class DNSRecord:
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength):
        self.auth = auth
        self.domain_name = self.process_list(domain_name)
        self.query_type = query_type
        self.query_class = query_class
        self.ttl = ttl
        self.rdlength = rdlength

    def flatten(self , lst):
        if not isinstance(lst, list):
            return [lst]
        
        res = []
        for el in lst:
            if isinstance(el, list):  
                res += self.flatten(el)
            elif not isinstance(el, int):
                res.append(el)

        return res

    def process_list(self, l):
        flat_list = self.flatten(l)
        flat_list = b'.'.join(flat_list)
        return flat_list.decode()