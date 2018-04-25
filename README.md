# Testing AWS Managed VPN service with a Linux peer

Cloudformation stacks and Ansible to configure a Linux server (tested on Ubuntu 16.04.3 only) to act as a peer to a AWS Managed VPN. Installs StrongSwan and Quagga and uses the output of describe-vpn-connections to configure them. The jinja2 templates are based on https://gist.github.com/heri16/2f59d22d1d5980796bfb


## Steps

1. Create Ubuntu 16.04 server. It can be an instance in AWS with a public IP and you can use `linux-host-stack.yml`, but it needs to be in a different VPC than the VPN. You can use the default VPCs in different regions or create new VPCs with `vpc.yml`.

1. Create the AWS VPN with dynamic routing. You can use `aws-vpn-stack.yml`

1. Get the VPN connection id (vpn-...) with `aws cloudformation describe-stack-resource --stack-name vpn-stack --logical-resource-id VPNConnection`

1. Some of the output of `aws describe-vpn-connections` is xml. Convert it to json so Ansible can read it.
    * pip install xml2dict
    * aws ec2 describe-vpn-connections --vpn-connection-ids <vpn-conn-id> | python vpn-xml2json.py > vpn-conns.json   

1. Add the public IP of Ubuntu server to Ansible `hosts`

1. Run the Ansible playbook, it reads variables from `vpn-conns.json`
    * ansible-playbook -i hosts site.yml

1. Ssh to instance and check status
    * sudo ipsec status
    * ip a
    * ip r

1. Check tunnel status
    * aws ec2 describe-vpn-connections | jq '.["VpnConnections"][0]["VgwTelemetry"]'
