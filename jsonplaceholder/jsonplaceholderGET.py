#!/usr/bin/python3

import requests

# define the URL we want to use
GETURL = "https://jsonplaceholder.typicode.com/posts/1"

def main():
    # use requests library to send an HTTP GET
    resp = requests.get(GETURL)

    # strip off JSON response
    # and convert to PYTHONIC LIST / DICT
    respjson = resp.json()

    # display our PYTHONIC data (LIST / DICT)
    print(respjson)

    # JUST display the value of "title"
    print(f"The title of the post is --> {respjson['title']}")

if __name__ == "__main__":
    main()
