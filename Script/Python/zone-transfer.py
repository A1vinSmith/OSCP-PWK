#!/bin/python3

import dns.query
import dns.resolver
import dns.zone
import sys


domain=sys.argv[1]
soa_answer = dns.resolver.resolve(domain, 'SOA')

print("NS servers found:")
for ns in soa_answer.response.authority[0]:
    print(ns) # print ns server
    master_answer = dns.resolver.resolve(ns.target,'A')
    try:
        zone=dns.zone.from_xfr(dns.query.xfr(master_answer[0].address, domain))
        print("Zone Transfer Successed on " + str(ns))
    except:
        print("Zone Transfer Failed on " + str(ns))
        continue

    print(f"Zone file of {ns.target}:")
    for n in sorted(zone.nodes.keys()):
        print(str(n) + "." + sys.argv[1] + ": " + zone[n].to_text(n))