#!/usr/bin/python3.8


class DNSRecord:
    def __init__(self, auth, domain_name, query_type, query_class, ttl, rdlength):
        if(type(domain_name) != str):
            domain_name = self.convert_domain_to_string(domain_name)
        self.auth = auth
        self.domain_name = domain_name
        self.query_type = query_type
        self.query_class = query_class
        self.ttl = ttl
        self.rdlength = rdlength

    def convert_domain_to_string(self, domain_name):
        domain_name = b'.'.join(domain_name[0])
        return domain_name.decode()