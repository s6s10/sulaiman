# function checks if ipaddress?
def check_ip(ip):
    # split ip by dots same day 1
    parts = ip.split(".")

    # ip have 4 parts
    if len(parts) != 4:
        raise ValueError("invalid ipaddress")

    # Check ip parts
    for part in parts:
        # change from str to int
        num = int(part)

        # ip between 0 and 255
        if num < 0 or num > 255:
            raise ValueError("invalid ipaddress")


# checks if CIDR valid
def check_cidr(cidr):
    # CIDR from 0 to 32
    if cidr < 0 or cidr > 32:
        raise ValueError("invalid CIDR prefix")


# changes ipaddress to binary
def ip_to_binary(ip):
    # split 4 parts
    parts = ip.split(".")
    binary_ip = ""

    # change to 8-bit binary && add in one_string
    for part in parts:
        binary_ip += format(int(part), "08b")

    return binary_ip


# changes binary back to ipaddress
def binary_to_ip(binary_ip):
    ip_parts = []

    # binary string 8 bits
    for i in range(0, 32, 8):
        part = binary_ip[i:i+8]

        # 8bit part to decimal
        ip_parts.append(str(int(part, 2)))

    # join the 4 parts && .
    return ".".join(ip_parts)


# finds the network address
def get_network_address(binary_ip, cidr):
    # make the rest 0
    network_binary = binary_ip[:cidr] + "0" * (32 - cidr)

    # binary to IP address
    return binary_to_ip(network_binary)


# finds the broadcast address
def get_broadcast_address(binary_ip, cidr):
    # make the rest 1
    broadcast_binary = binary_ip[:cidr] + "1" * (32 - cidr)

    # binary to IP address
    return binary_to_ip(broadcast_binary)


# calculates the number of hosts
def get_usable_hosts(cidr):
    # /31 and /32 do not have usable hosts
    if cidr >= 31:
        return 0

    # Formula: 2^(host bits) - 2
    return (2 ** (32 - cidr)) - 2


# print the title
print("--- Subnet Calculator ---")

try:
    # enter IP address
    ip = input("Enter an IP address: ")

    # enter CIDR 
    cidr = int(input("Enter CIDR prefix: "))

    # ip and CIDR are ok ??
    check_ip(ip)
    check_cidr(cidr)

    # ipaddress to binary
    binary_ip = ip_to_binary(ip)

    # network address
    network_address = get_network_address(binary_ip, cidr)

    # broadcast address
    broadcast_address = get_broadcast_address(binary_ip, cidr)

    # Gusable hosts
    usable_hosts = get_usable_hosts(cidr)

    # results
    print("network address:", network_address)
    print("broadcast address:", broadcast_address)
    print("number of usable hosts:", usable_hosts)

# any error??, error message
except Exception as e:
    print("Error: Invalid IP address or CIDR prefix provided. Details:", e)
