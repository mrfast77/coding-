import math
def main():
    num = int(input("Enter a number: "))

    print(is_perfect_square(num))


def is_perfect_square(num):
    if math.sqrt(num).is_integer():
        return True
    return False

if __name__ == "__main__":
    main()