from urllib.request import urlopen

def get_temperature(city):
  city = city.replace(" ", "+")
  url = "https://wttr.in/"+ city + "?format=%t"
  page = urlopen(url)
  raw = page.read()
  temperature = raw.decode("utf-8")
  return temperature

city = input("City: ")

print(get_temperature(city))