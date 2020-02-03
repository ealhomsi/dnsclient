#!/usr/bin/python3.8

import argparse
from query_type import QueryType
import socket
import time
import ipaddress
from serializer import Serializer
from deserializer import Deserializer


class DNSClient:
    def __init__(self, params):
        self.name = params.name
        self.address = params.address
        self.maxRetries = params.maxRetries
        self.timeout = params.timeout
        self.port = params.port

        self.qtype = QueryType.A

        if(params.mx):
            self.qtype = QueryType.MX
        elif(params.ns):
            self.qtype = QueryType.NS

    def makeRequest(self):
        print(f"DnsClient sending request for {self.name}")
        print(f'Server: {self.address}')
        print(f'Request type: {str(self.qtype).split(".")[1]}')
        self.requestHelper(1)

    def requestHelper(self, retry):
        if retry > self.maxRetries:
            print(
                f'ERROR\tMaximum number of retries {self.maxRetries} exceeded')
            return

        try:
            # open socket
            dnsSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dnsSocket.settimeout(self.timeout)

            # send & recv
            startTime = time.time_ns()
            dnsSocket.sendto(Serializer().build_packet(
                self.name, self.qtype), (self.address, self.port))
            recvBuff = dnsSocket.recvfrom(1024)
            endTime = time.time_ns()

            # close socket
            dnsSocket.close()

            print(
                f'Response received after {(endTime - startTime)//1000000000} seconds {retry -1} retries')
            dns_response = Deserializer().build_response(recvBuff[0])
            if(dns_response['rcode'] == 3):
                print("NOT FOUND")
                return

            self.beautify_dns_response(dns_response)
        except socket.timeout as e:
            print(f"ERROR\tSocket Timeout: {e}")
            print("Reattempting request...")
            self.requestHelper(retry+1)
        except socket.error as e:
            print(f'ERROR\tCould not create socket: {e}')
        except (socket.gaierror, socket.herror) as e:
            print(f"ERROR\tUnknown host: {e}")
        except Exception as e:
            print(e)

    def beautify_dns_response(self, dns_response):
        ancount = dns_response['ancount']
        arcount = dns_response['arcount']
        nscount = dns_response['nscount']

        if(ancount + arcount + nscount <= 0):
            print("NOT FOUND")
            return


        if(ancount > 0):
            print(f"***Answer Section ({ancount} answerRecords)***")
            for item in dns_response['answers']:
                print(str(item))

        print()

        if(arcount > 0):
            print(f"***Additional Section ({arcount} answerRecords)***")
            for item in dns_response['answers']:
                print(str(item))

        print()

        if(nscount > 0):
            print(f"***Authoritative Section ({nscount} answerRecords)***")
            for item in dns_response['authoritative']:
                print(str(item))
