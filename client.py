#!/usr/bin/env python3

from flask import Flask, request, json
import requests
from argparse import ArgumentParser

app = Flask(__name__)


def parse_arguments():
    p = ArgumentParser("Client for sending requests to prediction server")
    p.add_argument('-c',
                   '--city',
                   help="Target city for delivery.",
                   type=str,
                   default="Warszawa",
                   choices=[
                       "Warszawa", "Wrocław", "Poznań", "Szczecin", "Kraków",
                       "Radom", "Gdynia"
                   ])
    p.add_argument('-d',
                   '--delivery-company',
                   help="Delivery company.",
                   type=int,
                   default=620,
                   choices=[254, 360, 516, 620])
    p.add_argument('-t',
                   '--time',
                   help="Date of purchase.",
                   type=str,
                   default="2021-03-13T15:20:42")
    return p.parse_args()


def main():
    args = parse_arguments()
    data = {
        "purchase_timestamp": "2021-03-13T15:20:42",
        "city": "Szczecin",
        "delivery_company": 620
    }


    print("Sending request:\n", data)
    response = requests.get("http://127.0.0.1:5000/", json=data)
    print("Got response:")
    print(response.json())


if __name__ == '__main__':
    main()
