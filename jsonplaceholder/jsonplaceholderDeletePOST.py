#!/usr/bin/python3

import requests

# define the URL we want to use
DELETEURL = "https://jsonplaceholder.typicode.com/posts/1"

def main():
    # use requests library to send an HTTP DELETE
    resp = requests.delete(DELETEURL)

    # display the status code
    if resp.status_code == 200 or resp.status_code == 204:
        print("Post deleted successfully!")
    else:
        print(f"Failed to delete post. Status code: {resp.status_code}")

if __name__ == "__main__":
    main()
