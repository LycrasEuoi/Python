import pprint
import json

count = {}

with open(r'C:\Users\YClae\OneDrive\Documenten\Bijbel in Text.txt', 'r', encoding='utf-8') as textFile:
    data = textFile.read().lower()


dataWordList = data.replace('\n',' ').split(' ')


#for character in data:
#    count.setdefault(character, 0)
#    count[character] += 1

for character in dataWordList:
    count.setdefault(character, 0)
    count[character] += 1

sorted_count = dict(sorted(count.items()))

output_file_path = r'C:\Users\YClae\OneDrive\Documenten\word_count_output.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(json.dumps(dataWordList))

#    for word in sorted_count:
#        file.write(word + '\n')

pprint.pprint(sorted_count)