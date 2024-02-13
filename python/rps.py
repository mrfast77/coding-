import random

user_score = 0
computer_score = 0
round_count = 1
username = ""

def main():
    global username
    username = start_game()
    play_game(username)

    
def start_game():
    print("\nHello, welcome to the classic Rock, Paper, Scissors\n")
    name = input("What is your name? ")
    return name


def users_turn():

    while True:
        users_move = input("Type in your move: (rock, paper, or scissors)\n\n").lower()
        if users_move in ["rock", "paper", "scissors"]:
            break

    print(f"\n\nYou played: {users_move}")
    return users_move


def computers_turn():
    plays = ["rock", "paper", "scissors"]
    computers_move = random.choice(plays)
    print(f"The computer played: {computers_move}\n")
    return computers_move


def find_winner(users_move, computers_move, user_name):
    if users_move == computers_move:
        return "Tie"

    moves = [users_move, computers_move]
    if all(x in moves for x in ["rock", "paper"]):
        if users_move == "paper":
            return user_name
        if computers_move == "paper":
            return "computer"
    if all(x in moves for x in ["rock", "scissors"]):
        if users_move == "rock":
            return user_name
        if computers_move == "rock":
            return "computer"
    if all(x in moves for x in ["paper", "scissors"]):
        if users_move == "scissors":
            return user_name
        if computers_move == "scissors":
            return "computer"
        
def score(winner, user):

    if winner == user:
        global user_score
        user_score += 1

    if winner == "computer":
        global computer_score
        computer_score += 1

    if winner == "Tie":
        user_score += 1
        computer_score += 1

    print(f"{user}: {user_score}\nComputer: {computer_score}\n")


def play_again():
    answer = input("Play again? (y/n): ").lower()

    while answer not in ["y", "n"]:
        answer = input("Please answer only with y or n: ")

    if answer == "y":
        global round_count
        round_count += 1
        play_game(username)
    if answer == "n":
        end_game()
        


def play_game(user_name):
    print(f"\nRound {round_count}...\n")
    users_move = users_turn()
    computers_move = computers_turn()
    
    winner = find_winner(users_move, computers_move, user_name)
    print(f"\nThe winner is... {winner}!\n")

    score(winner, user_name)

    play_again()


def end_game():
    print(f"\nFinal Scores...\n{username}: {user_score}\nComputer: {computer_score}\n")
    print("Thanks for playing!\n")
         

if __name__ == "__main__":
    main()


