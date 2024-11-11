import re

message = 'Call me at 415-555-1234 tomorrow or at 415-555-2341 for my office line'

phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
foundNumbers = phoneNumRegex.findall(message)

for number in foundNumbers:
    print(number)

