"""
read the output of this command 
aws ec2 describe-vpn-connections --vpn-connection-ids <your aws vpn-id>
on stdin, and convert the customer gateway part from xml to json
which can be easily read by ansible
"""
import sys
import json
import xmltodict

j = json.load(sys.stdin)
cgc = j['VpnConnections'][0]['CustomerGatewayConfiguration']
d = xmltodict.parse(cgc)
print(json.dumps(d['vpn_connection']['ipsec_tunnel'], indent=4))
