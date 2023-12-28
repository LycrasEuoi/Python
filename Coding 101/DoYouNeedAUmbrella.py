from urllib.request import urlopen

def get_condition(city):
  city = city.replace(" ", "+")
  url = "https://wttr.in/"+ city + "?format=%C"
  page = urlopen(url)
  raw = page.read()
  condition = raw.decode("utf-8")
  return condition

city = input("City: ")

condition = get_condition(city)

if condition == "Clear":
  print("It's " + condition.lower() + " today, so no umbrella needed!")
else:
  print("There is " + condition.lower() + " today, so you should bring a umbrella")