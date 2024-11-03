# This is a guess the number game.
import random

print('Hello, What is your name?')
name = input()
error = 0
guessesTaken = 1

print('Well ' + name + ', I am thinking of a number between 1 and 20')
secretNumber = random.randint(1, 20)

while guessesTaken < 7:
    try: # Error-handeling
        print('Take a guess [' + str(guessesTaken) +']')
        guess = int(input())
        guessesTaken += 1  
    except ValueError:
        print('You have to guess a number.')
        guessesTaken - 1
        continue

    if guess < secretNumber:
        print('Your guess is too low')
    elif guess > secretNumber:
        print('Your guess is to high')
    else:
        break # This condition is for the correct guess.
    

if guess == secretNumber:
    print('Good job, ' + name + '! You guessed my number in ' + str(guessesTaken) + ' guesses!')
else:
    print('Nope. The number I was thinking of was ' + str(secretNumber))