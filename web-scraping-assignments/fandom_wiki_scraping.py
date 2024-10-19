import requests
from bs4 import BeautifulSoup
import csv
import os

# URL of the fandom wiki page containing the NFL teams
url = 'https://americanfootball.fandom.com/wiki/List_of_NFL_Teams'

# Send a GET request to fetch the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a folder for images
    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
    os.makedirs(images_folder, exist_ok=True)  # Create folder if it doesn't exist

    # List to hold the image file names
    image_files = []
    
    # Find all images on the page
    images = soup.find_all('img')

    # Download images
    for i, img_tag in enumerate(images):
        img_url = img_tag['src']
        
        # Filter out base64 placeholder images
        if "data:image" in img_url:
            continue
        
        # Fetch the content of the image
        try:
            print(f"Downloading image from: {img_url}")  # Debug: Show URL being fetched
            img_data = requests.get(img_url).content
            
            # Determine the file extension (default to png if not found)
            if img_url.endswith('.webp'):
                img_extension = '.webp'
            elif img_url.endswith('.png'):
                img_extension = '.png'
            elif img_url.endswith('.jpg') or img_url.endswith('.jpeg'):
                img_extension = '.jpg'
            else:
                img_extension = '.png'  # Default extension if none found

            img_filename = f"image_{i + 1}{img_extension}"  # File names will start from image_1
            img_path = os.path.join(images_folder, img_filename)

            # Download and save the image
            with open(img_path, 'wb+') as img_file:
                img_file.write(img_data)
                image_files.append(img_filename)  # Store the image filename
                print(f"Downloaded: {img_filename}")  # Confirm download
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

    # Now we'll save the original CSV with images linked to each row
    # Extract NFL team data for the CSV
    nfl_teams = []
    # Find the table on the page (assuming the first table is the one you need)
    table = soup.find('table', {'class': 'wikitable'})  # Adjust class if necessary

    # Iterate through the table rows (skip the header)
    rows = table.find_all('tr')[1:]  # Skip the first row which is the header

    for row in rows:
        cols = row.find_all('td')

        if len(cols) >= 3:  # Ensure the row has at least 3 columns
            # Extract the team name from the second column
            team_name_tag = cols[1].find('a')
            team_name = team_name_tag.text if team_name_tag else 'No team name'

            # Extract the year founded from the third column
            year_founded = cols[2].text.strip()

            # Append the extracted data to the list
            nfl_teams.append([team_name, year_founded])

    # Define the filename and full path for the CSV
    csv_filename = 'nfl_teams_with_images.csv'
    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_filename)

    # Save the data to a CSV file, mapping images starting from the third image
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Team Name', 'Year Founded', 'Image Path'])
        
        for i, team in enumerate(nfl_teams):
            # Start mapping images from the third image
            image_index = i + 1  # Adjust index to start from the third image
            image_path = f"images/{image_files[image_index]}" if image_index < len(image_files) else 'No image available'
            writer.writerow(team + [image_path])

    print(f"CSV with images saved at {csv_file_path}")

else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
