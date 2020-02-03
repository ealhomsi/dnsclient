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
For example: ./app.py -mx -t 10 -r 7 @8.8.8.8 mcgill.ca 
```

## Run
```bash
    chmod u+x app.py
    ./app.py @8.8.8.8 mcgill.ca -mx 
    ./app.py @8.8.8.8 google.ca -ns  
    ./app.py @8.8.8.8 mcgill.ca -ns   
    ./app.py @8.8.8.8 mcgill.ca
```