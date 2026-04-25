import ipaddress

print("=== Special-Purpose IPv4 Address Identification ===\n")

addresses = [
    ("10.0.0.1", "RFC 1918 private (10.0.0.0/8)"),
    ("172.16.5.1", "RFC 1918 private (172.16.0.0/12)"),
    ("192.168.1.42", "RFC 1918 private (192.168.0.0/16)"),
    ("127.0.0.1", "Loopback"),
    ("169.254.23.45", "Link-local (APIPA)"),
    ("224.0.0.5", "Multicast (OSPF all routers)"),
    ("8.8.8.8", "Public (Google DNS)"),
    ("100.64.0.1", "Carrier-Grade NAT (RFC 6598)"),
]

for addr_str, description in addresses:
    addr = ipaddress.IPv4Address(addr_str)
    print(f"{addr_str:16s} — {description}")
    print(f"    is_private:     {addr.is_private}")
    print(f"    is_loopback:    {addr.is_loopback}")
    print(f"    is_link_local:  {addr.is_link_local}")
    print(f"    is_multicast:   {addr.is_multicast}")
    print(f"    is_global:      {addr.is_global}")
    print()