import ipaddress

def same_subnet(host_a, host_b, prefix_len):
    """Return True if host_a and host_b share the same network prefix."""
    a = int(ipaddress.IPv4Address(host_a))
    b = int(ipaddress.IPv4Address(host_b))
    mask = int(ipaddress.IPv4Address("255.255.255.255")) << (32 - prefix_len) & 0xFFFFFFFF
    return (a & mask) == (b & mask)

def same_subnet_pythonic(host_a, host_b, prefix_len):
    """Return True using ipaddress module's built-in containment."""
    net_a = ipaddress.IPv4Interface(f"{host_a}/{prefix_len}").network
    net_b = ipaddress.IPv4Interface(f"{host_b}/{prefix_len}").network
    return net_a == net_b

print("=== Same-Subnet Checks (Prefix /26) ===\n")

tests = [
    ("192.168.10.75", "192.168.10.100"),
    ("192.168.10.75", "192.168.10.130"),
    ("10.0.0.5", "10.0.0.200"),
    ("172.16.5.1", "172.16.6.1"),
]

for host_a, host_b in tests:
    result = same_subnet(host_a, host_b, 26)
    result2 = same_subnet_pythonic(host_a, host_b, 26)
    status = "SAME subnet" if result else "DIFFERENT subnets"
    print(f"{host_a} and {host_b}: {status} (bitwise: {result}, pythonic: {result2})")