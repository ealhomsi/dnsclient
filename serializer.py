from query_type import QueryType
import struct
import random

class Serializer:
    def __init__(self):
        pass

    def build_packet(self, url, qtype):
        packet = struct.pack(">H", random.getrandbits(16)) # ID
        packet += struct.pack(">H", 256) # Flags
        packet += struct.pack(">H", 1)  # Questions
        packet += struct.pack(">H", 0)  # Answers
        packet += struct.pack(">H", 0)  # Authorities
        packet += struct.pack(">H", 0)  # Additional
        
        split_url = url.split(".")
        for part in split_url:
            parts = part.encode('utf-8')
            packet += struct.pack("B", len(part))
            for byte in part:
                packet += struct.pack("c", byte.encode('utf-8'))
    
        packet += struct.pack("B", 0)  # End of String
        packet += struct.pack(">H", int(qtype))  # Query Type
        packet += struct.pack(">H", 1)  # Query Class
        return packet