#!/usr/bin/python3

import requests

# define the URL we want to use
POSTURL = "https://jsonplaceholder.typicode.com/posts"

def main():
    # test data to send
    mydata = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }

    # use requests library to send an HTTP POST
    resp = requests.post(POSTURL, json=mydata)

    # strip off JSON response
    # and convert to PYTHONIC LIST / DICT
    respjson = resp.json()

    # display our PYTHONIC data (LIST / DICT)
    print(respjson)

    # JUST display the value of "id"
    print(f"Newly created post ID: {respjson['id']}")

if __name__ == "__main__":
    main()
