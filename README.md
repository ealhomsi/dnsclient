# DNS Client Python
This is a network tool similar to nslookup

## McGill University Assignment
- Assignment 1 
- ECSE 316
- Signals and network

## Requirements
Please download python3.8 or the latest version of python3 you can find and run `app.py`.

## Instructions
```
usage: app.py [-h] [-t TIMEOUT] [-r MAXRETRIES] [-p PORT] [-mx | -ns] address name
For example: ./DnsClient.py -mx -t 10 -r 7 @8.8.8.8 mcgill.ca 
```

### Parameters
- timeout(optional): gives how long to wait, in seconds, before retransmitting an unanswered query. Default value: 5.
- max-retries(optional): is the maximum number of times to retransmit an unanswered query before giving up. Default value: 3.
- port(optional): is the UDP port number of the DNS server. Default value: 53.
- -mx or -ns flags (optional): indicate whether to send a MX (mail server) or NS (name server). Those are mutually exclusive flags.
- address (required) is the IPv4 address of the DNS server, in @a.b.c.d.format
- name (required) is the domain name to query for.

## Run
```bash
    chmod u+x DnsClient.py
    ./DnsClient.py @8.8.8.8 mcgill.ca -mx 
    ./DnsClient.py @8.8.8.8 google.ca -ns  
    ./DnsClient.py @8.8.8.8 mcgill.ca -ns   
    ./DnsClient.py @8.8.8.8 mcgill.ca
```

you can alternatively `python3 app.py` when running the program
