#!/usr/bin/python3

import requests

# define the URL we want to use
PUTURL = "https://jsonplaceholder.typicode.com/posts/1"

def main():
    # updated data for the post
    updated_data = {
        "id": 1,
        "title": "Updated Title",
        "body": "This is the updated body of the post.",
        "userId": 1
    }

    # use requests library to send an HTTP PUT
    resp = requests.put(PUTURL, json=updated_data)

    # strip off JSON response
    # and convert to PYTHONIC LIST / DICT
    respjson = resp.json()

    # display our PYTHONIC data (LIST / DICT)
    print(respjson)

    # JUST display the value of "title"
    print(f"Updated post title: {respjson['title']}")

if __name__ == "__main__":
    main()
