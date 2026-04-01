#enter the input manul
user = input("enter a number: ")

try:
    # convert input to integer?
    number = int(user) 
    
    # Ok
    print(f"you entered the number: {number}") # f for enter the number

except ValueError:
    # invalid input//
    print("error!!!: Plz enter a valid integer number.")