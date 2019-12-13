"""
Implements the functions necessary to access every mailer
function without actually needing a visual interface.
"""


import sys
import json
import requests


def index(link):
    """Wakes up the server by asking for its root page."""
    return requests.get(f'{link}/')


def send(link, mailer_key, email, title, body):
    """Sends a mail."""
    payload = {
        "mailer_key": mailer_key,
        "email": email,
        "title": title,
        "body": body
    }
    return requests.get(f'{link}/send').json()


if __name__ == "__main__":
    LINK = "http://127.0.0.1:5000"
    COMMANDS = {
        "index": index,
        "send":  send
    }
    try:
        RESPONSE = COMMANDS[sys.argv[1]](LINK, *sys.argv[2:])
    except IndexError:
        if len(sys.argv) <= 1:
            print("\n\n\n\tInvalid script call. To use the script, run:")
            print("\tpython3 ghost_client.py command *args")
            print("\tWhere *args are the arguments separated by space and "
                  "command corresponds to one of the following:")
            print(f'\t\t{", ".join(COMMANDS.keys())}\n\n')
            sys.exit(1)
    try:
        print(json.dumps(RESPONSE, indent=2, sort_keys=False))
    except TypeError:
        print(RESPONSE.text)
