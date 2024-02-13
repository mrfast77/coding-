import random
import sys

colors = ['red', 'blue', 'green', 'yellow']
solution = [random.choice(colors) for i in range(4)]

print(f"SOLTUTION = {solution}")

while True:
    guess = [input(f"Make a guess\nColor {i}: ") for i in range(1,5)]

    if guess == solution:
        print("\n\nYou win!!")
        sys.exit()

    answer = []
    for i in range(4):
        if guess[i] in solution:
            if guess[i] == solution[i]:
                answer.append('yes')
            else:
                answer.append('right color, wrong space')
        else:
            answer.append('no')
    if answer == ['yes', 'yes', 'yes', 'yes']:
        print("\n\nYou win!!")
        sys.exit()

    print(answer)

