# enter the ip here
ip = input("Enter an IPv4 address: ")

# split by dots
parts = ip.split(".")

# assume it valid 
valid = True

# check parts
if len(parts) != 4:
        valid = False
else:
    # check each part
    for part in parts:
        # check cont only digitsS
        if not part.isdigit():
            valid = False
            break

        # convert to integer
        number = int(part)

        # between 0 and 255?
        if number < 0 or number > 255:
            valid = False
            break

# result
if valid:
    print("The IP address is valid.")
else:
    print("The IP address is invalid.")
    