import ipaddress

# Define a network
net = ipaddress.IPv4Network("192.168.10.0/24")

print("=== Basic Network Arithmetic ===")
print(f"Network:            {net}")
print(f"Network address:    {net.network_address}")
print(f"Broadcast address:  {net.broadcast_address}")
print(f"Netmask:            {net.netmask}")
print(f"Prefix length:      /{net.prefixlen}")
print(f"Total addresses:    {net.num_addresses}")

# Usable hosts (excludes network and broadcast addresses)
hosts = list(net.hosts())
print(f"Usable hosts:       {len(hosts)}")
print(f"First usable host:  {hosts[0]}")
print(f"Last usable host:   {hosts[-1]}")