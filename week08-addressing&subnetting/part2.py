import ipaddress

net = ipaddress.IPv4Network("192.168.10.0/24")
subnets = list(net.subnets(prefixlen_diff=2))  # add 2 bits → /26

print("=== Subnetting 192.168.10.0/24 into four /26s ===\n")

for i, s in enumerate(subnets):
    hosts = list(s.hosts())
    print(f"Subnet {i}: {s}")
    print(f"  Network address:  {s.network_address}")
    print(f"  Broadcast:        {s.broadcast_address}")
    print(f"  Usable hosts:     {hosts[0]} – {hosts[-1]}")
    print(f"  Total usable:     {len(hosts)}")
    print()