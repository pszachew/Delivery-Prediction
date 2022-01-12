#!/usr/bin/env python3

from flask import Flask, request, json
import requests

app = Flask(__name__)


def main():
    data = {"name": "df"}
    print("Sending request:\n", data)
    response = requests.get("http://127.0.0.1:5000/", json=data)
    print("Got response:")
    print(response.json())


if __name__ == '__main__':
    main()
