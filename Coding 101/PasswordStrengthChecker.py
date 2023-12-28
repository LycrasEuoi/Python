def check(password):
  special_characters = "!@#$%^&*()-+?_=,<>/\\\""
  has_number = False
  has_capital = False
  has_special = False
  has_lenght = False
  for i in password:
    if i.isdigit():
      has_number = True
    if i.isupper():
      has_capital = True
    if any(i in special_characters for j in special_characters):
      has_special = True
  if len(password) >= 12:
    has_lenght = True  
  return [has_number, has_capital, has_special, has_lenght]

while 1:
    password = input("Password: ")
    strengthcheck = check(password)
    print("has it got a number? " + str(strengthcheck[0]))
    print("has it got a capital character? " + str(strengthcheck[1]))
    print("has it got a special character? " + str(strengthcheck[2]))
    print("has it got a the right length? " + str(strengthcheck[3]))