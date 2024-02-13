import math


try:
    x = int(input("Type in a positive integer: "))
    if x < 0:
        print("That number is not positive")
    if math.log(x,2).is_integer():
        print("This number is a power of 2!")
    else:
        print("This number is not a power of two :(")
    


except:
    print("Please enter a valid, positive number")

# Hello there
