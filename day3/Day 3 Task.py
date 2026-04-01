import re # for regex
import csv # for save file
import json # for save JSON

# this list will store all valid log entries
entries = []

# counters for ACCEPT and DROP
accept_count = 0
drop_count = 0

# count bad lines
malformed_count = 0

# to count ports and IPs
port_count = {}
source_ip_count = {}

# this pattern helps me check if the line is correct
pattern = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(ACCEPT|DROP) "
    r"(TCP|UDP|ICMP) "
    r"SRC=([\d.]+) "
    r"SPT=(\d+) "
    r"DST=([\d.]+) "
    r"DPT=(\d+) "
    r"LEN=(\d+)"
)

# open the log file and read all lines
with open("firewall.log", "r") as file:
    lines = file.readlines()

# loop through each line
for line in lines:
    line = line.strip()

    # try to match the pattern
    match = pattern.match(line)

    if match:
        # get all data from the line
        timestamp = match.group(1)
        action = match.group(2)
        protocol = match.group(3)
        source_ip = match.group(4)
        source_port = match.group(5)
        destination_ip = match.group(6)
        destination_port = match.group(7)
        packet_size = match.group(8)

        # save data in dictionary
        entry = {
            "timestamp": timestamp,
            "action": action,
            "protocol": protocol,
            "source_ip": source_ip,
            "source_port": source_port,
            "destination_ip": destination_ip,
            "destination_port": destination_port,
            "packet_size": packet_size
        }

        # add it to the list
        entries.append(entry)

        # count ACCEPT and DROP
        if action == "ACCEPT":
            accept_count += 1
        else:
            drop_count += 1

        # count destination ports
        if destination_port in port_count:
            port_count[destination_port] += 1
        else:
            port_count[destination_port] = 1

        # count how many times each IP appears
        if source_ip in source_ip_count:
            source_ip_count[source_ip] += 1
        else:
            source_ip_count[source_ip] = 1

    else:
        # if line is wrong, skip it
        malformed_count += 1

# sort ports to get top 3
top_ports = sorted(port_count.items(), key=lambda x: x[1], reverse=True)[:3]

# find suspicious IPs (3 or more times)
suspicious_ips = {}
for ip, count in source_ip_count.items():
    if count >= 3:
        suspicious_ips[ip] = count

# save CSV file
with open("output.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)

    # write header
    writer.writerow([
        "Timestamp", "Action", "Protocol", "Source IP",
        "Source Port", "Destination IP", "Destination Port", "Packet Size"
    ])

    # write data
    for entry in entries:
        writer.writerow([
            entry["timestamp"],
            entry["action"],
            entry["protocol"],
            entry["source_ip"],
            entry["source_port"],
            entry["destination_ip"],
            entry["destination_port"],
            entry["packet_size"]
        ])

# save JSON file
with open("output.json", "w") as json_file:
    json.dump(entries, json_file, indent=4)

# save threats file
with open("threats.txt", "w") as threat_file:
    threat_file.write("THREAT REPORT\n")
    threat_file.write("========================\n")

    for ip, count in suspicious_ips.items():
        threat_file.write(f"{ip} - {count} times\n")

# print results in terminal
print("===== REPORT =====")
print("Total lines:", len(lines))
print("Valid lines:", len(entries))
print("Bad lines:", malformed_count)

print("\nACCEPT:", accept_count)
print("DROP:", drop_count)

print("\nTop Ports:")
for port, count in top_ports:
    print(port, "->", count)

print("\nSuspicious IPs:")
for ip, count in suspicious_ips.items():
    print(ip, "->", count)
    ##test