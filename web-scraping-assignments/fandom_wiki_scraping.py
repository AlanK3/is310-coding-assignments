import requests
from bs4 import BeautifulSoup
import csv

# URL of the fandom wiki page containing the NFL teams
url = 'https://americanfootball.fandom.com/wiki/List_of_NFL_Teams'

# Send a GET request to fetch the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table on the page (assuming the first table is the one you need)
    table = soup.find('table', {'class': 'wikitable'})  # or use the correct class name if different

    # List to hold the scraped data
    nfl_teams = []

    # Iterate through the table rows (skip the header)
    rows = table.find_all('tr')[1:]  # Skip the first row which is the header

    for row in rows:
        cols = row.find_all('td')

        if len(cols) >= 3:  # Ensure the row has at least 3 columns
            # Extract the image URL from the first column
            helmet_img_tag = cols[0].find('img')
            helmet_url = helmet_img_tag['src'] if helmet_img_tag else 'No image'

            # Extract the team name from the second column
            team_name_tag = cols[1].find('a')
            team_name = team_name_tag.text if team_name_tag else 'No team name'

            # Extract the year founded from the third column
            year_founded = cols[2].text.strip()

            # Append the extracted data to the list
            nfl_teams.append([helmet_url, team_name, year_founded])

    print(nfl_teams)

else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
