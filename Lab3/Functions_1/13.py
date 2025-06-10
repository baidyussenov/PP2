import random
print("Hello! What is your name?")
name=input()
print(name)
print(f"Well, {name}, I am thinking of a number between 1 and 20.")
print("Take a guess.")
guessed_number=random.randint(1, 20)
def guess(guessed_number):
    number_of_fails=1
    while(True):
        my_number=int(input())
        if my_number < guessed_number:
            print("Your guess is too low.")
            print("Take a guess")
            number_of_fails += 1
        elif my_number > guessed_number:
            print("Your guess is too high.")
            print("Take a guess")
            number_of_fails += 1
        else:
            break
    print(f"Good job, {name}! You guessed my number in {number_of_fails} guesses!")
guess(guessed_number)