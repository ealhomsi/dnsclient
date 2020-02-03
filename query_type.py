#!/usr/bin/python3.8
import enum

class QueryType(enum.IntEnum): 
    A=1,
    MX=15,
    NS=13,
    SOA=6,
    CNAME=5,
    OTHER=100