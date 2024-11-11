import re

message = 'Call me at 415-555-1234 tomorrow or at 415-555-2341 for my office line'

batRegex = re.compile(r'Bat(wo){2}man')
mo = batRegex.search('Batwowoman has won the battle')
print(mo.group())

phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
mo = phoneNumRegex.search('My number is 415-555-4312')

print(mo.group())

digitRegex = re.compile(r'(\d){3,5}?')
mo = digitRegex.search('1234567890')

print(mo.group())

vowelRegex = re.compile(r'[^aeiouAEIOU]')
