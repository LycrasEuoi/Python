import webbrowser, pyperclip, sys


if len(sys.argv) > 1:
    address = ' '.join(sys.argv[1:])

else:
    address = pyperclip.paste

BASE_URL = 'https://www.google.com/maps/place/'

webbrowser.open(BASE_URL + address)



