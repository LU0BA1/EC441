import ipaddress

print("=== Alignment Rule Verification ===\n")

# These are valid
valid_attempts = [
    "192.168.1.0/26",
    "192.168.1.64/26",
    "192.168.1.128/26",
    "192.168.1.192/26",
]

print("Valid /26 networks:")
for addr in valid_attempts:
    net = ipaddress.IPv4Network(addr)
    print(f"  {addr}: network = {net.network_address} (block multiple ✓)")

# This would raise an error
invalid_addr = "192.168.1.10/26"
print(f"\nAttempting invalid network: {invalid_addr}")
try:
    net = ipaddress.IPv4Network(invalid_addr, strict=False)
    print(f"  strict=False allows it, but network portion is .0, not .10")
    print(f"  Actual network: {net.network_address}")
    print(f"  Host bits present: {int(net.network_address) & 0x3F} ≠ 0 (violates alignment)")
except Exception as e:
    print(f"  Error (strict=True): {e}")