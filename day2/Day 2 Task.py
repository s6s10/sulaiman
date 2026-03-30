# This function checks if the IP address is valid
def check_ip(ip):
    # Split the IP address using dots
    parts = ip.split(".")

    # IP address must have 4 parts
    if len(parts) != 4:
        raise ValueError("Invalid IP address")

    # Check each part of the IP
    for part in parts:
        # Change the part from string to integer
        num = int(part)

        # Each number in IP must be between 0 and 255
        if num < 0 or num > 255:
            raise ValueError("Invalid IP address")


# This function checks if the CIDR is valid
def check_cidr(cidr):
    # CIDR must be from 0 to 32
    if cidr < 0 or cidr > 32:
        raise ValueError("Invalid CIDR prefix")


# This function changes the IP address to binary
def ip_to_binary(ip):
    # Split the IP into 4 parts
    parts = ip.split(".")
    binary_ip = ""

    # Change each part to 8-bit binary and add it to one string
    for part in parts:
        binary_ip += format(int(part), "08b")

    return binary_ip


# This function changes binary back to normal IP address
def binary_to_ip(binary_ip):
    ip_parts = []

    # Take the binary string 8 bits at a time
    for i in range(0, 32, 8):
        part = binary_ip[i:i+8]

        # Change each 8-bit part to decimal and save it
        ip_parts.append(str(int(part, 2)))

    # Join the 4 parts with dots
    return ".".join(ip_parts)


# This function finds the network address
def get_network_address(binary_ip, cidr):
    # Keep the network bits and make the rest 0
    network_binary = binary_ip[:cidr] + "0" * (32 - cidr)

    # Change binary result to IP address
    return binary_to_ip(network_binary)


# This function finds the broadcast address
def get_broadcast_address(binary_ip, cidr):
    # Keep the network bits and make the rest 1
    broadcast_binary = binary_ip[:cidr] + "1" * (32 - cidr)

    # Change binary result to IP address
    return binary_to_ip(broadcast_binary)


# This function calculates the number of usable hosts
def get_usable_hosts(cidr):
    # /31 and /32 do not have usable hosts in this program
    if cidr >= 31:
        return 0

    # Formula: 2^(host bits) - 2
    return (2 ** (32 - cidr)) - 2


# Print the title
print("--- Subnet Calculator ---")

try:
    # Ask the user to enter IP address
    ip = input("Enter an IP address: ")

    # Ask the user to enter CIDR and change it to integer
    cidr = int(input("Enter CIDR prefix: "))

    # Check if IP and CIDR are valid
    check_ip(ip)
    check_cidr(cidr)

    # Change the IP address to binary
    binary_ip = ip_to_binary(ip)

    # Get the network address
    network_address = get_network_address(binary_ip, cidr)

    # Get the broadcast address
    broadcast_address = get_broadcast_address(binary_ip, cidr)

    # Get the number of usable hosts
    usable_hosts = get_usable_hosts(cidr)

    # Print the results
    print("Network Address:", network_address)
    print("Broadcast Address:", broadcast_address)
    print("Number of Usable Hosts:", usable_hosts)

# If there is any error, print the error message
except Exception as e:
    print("Error: Invalid IP address or CIDR prefix provided. Details:", e)

# Print the ending line
print("-------------------------")