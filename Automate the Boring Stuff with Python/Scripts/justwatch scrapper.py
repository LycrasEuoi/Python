import re

with open(r'C:\Users\YClae\OneDrive\Documenten\JustWatch.html', 'r', encoding='utf-8') as textFile: # Opens the to scrape file via with, for correct file handeling
    data = textFile.read().lower() 

movieNameRegex = re.compile(r'<h2.*?> (.*?) <span.*?> \((.*?)\) </span') # Create regex based on following string: <h2 data-v-ad8cc64e="" class="title-card-heading"> Movie name <span data-v-ad8cc64e="" class="title-card-heading__info"> Date </span>

list = movieNameRegex.findall(data)

with open(r'C:\Users\YClae\OneDrive\Documenten\scraped_list.txt', 'w') as scrappedFile: # Create file to store scrapped file
    for item in list:
        scrappedFile.write('Movie: ' + item[0].ljust(80, ' ').title() + 'Year: ' + item[1] + '\n') # Format: Movie: NAME    Year: YEAR



