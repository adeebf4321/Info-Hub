import dns.resolver
import socket
from ipwhois import IPWhois
import requests

SHODAN_API_KEY = 'Enter_Your_Shodan_API_Key'
NUMVERIFY_API_KEY = 'Enter_Your_Numverify_API_Key'

def get_info_from_domain(domain):
    ip_addresses = socket.gethostbyname_ex(domain)[2]

    # Subdomain discovery using Shodan
    shodan_url = f"https://api.shodan.io/dns/domain/{domain}?key={SHODAN_API_KEY}"
    res = requests.get(shodan_url).json()
    subdomains = res.get('subdomains', [])
    return {
        'domain': domain,
        'ips': ip_addresses,
        'subdomains': [f"{s}.{domain}" for s in subdomains]
    }

def get_info_from_ip(ip):
    # IP info
    obj = IPWhois(ip)
    result = obj.lookup_rdap()
    domains = result.get('network', {}).get('name', 'N/A')

    # Shodan reverse DNS
    shodan_url = f"https://api.shodan.io/dns/reverse?ips={ip}&key={SHODAN_API_KEY}"
    res = requests.get(shodan_url).json()
    hostnames = res[0].get('hostnames', []) if isinstance(res, list) else []

    return {
        'ip': ip,
        'domains': hostnames or domains,
        'subdomains': hostnames
    }

def get_info_from_phone(number):
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={number}"
    res = requests.get(url).json()
    if not res.get("valid"):
        return {'error': 'Invalid phone number'}
    return {
        'number': number,
        'country': res.get('country_name'),
        'location': res.get('location'),
        'carrier': res.get('carrier'),
        'line_type': res.get('line_type')
    }
