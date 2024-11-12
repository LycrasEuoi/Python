while(True):
    print("Enter a string to count: ")
    inputString = input()
    if(inputString == ":q"):
        break
    print(len(inputString))