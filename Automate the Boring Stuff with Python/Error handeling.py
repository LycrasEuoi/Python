print('How many cats do you have?')
while True:
    numCats = input()
    try:
        if int(numCats) >= 4:
            print('That is a lot of cats')
        elif int(numCats) < 0:
            print('You can not have negatief cats')
        else:
            print('That is not  that many cats')
    except ValueError:
        print('You did not enter a number')
