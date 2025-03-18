import requests
import csv
import os

# Replace with your Kakao API key
api_key = '5ac23e3f4a305df669580f00637c8459'

# Define search areas: west, middle, and east of Jeju
search_areas = [
    {'x': 126.1628, 'y': 33.3946, 'area_name': 'West Jeju'},   # West Jeju
    {'x': 126.570667, 'y': 33.450701, 'area_name': 'Middle Jeju'},  # Middle Jeju
    {'x': 126.9748, 'y': 33.5097, 'area_name': 'East Jeju'}    # East Jeju
]

# Define the request headers
headers = {
    'Authorization': f'KakaoAK {api_key}'
}

# Define the CSV file name
csv_file = 'jeju_restaurants.csv'

# Create a set to track unique place IDs
unique_place_ids = set()

# Check if the CSV file already exists
file_exists = os.path.isfile(csv_file)

# Open the CSV file in append mode
with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header only if the file is newly created
    if not file_exists:
        writer.writerow(['Place Name', 'Longitude', 'Latitude', 'Phone', 'Average Rating', 'Average Price'])

    for area in search_areas:
        print(f"Searching in {area['area_name']}...")
        
        # Define the search parameters for each area
        params = {
            'query': 'restaurant',
            'x': area['x'],  # Longitude
            'y': area['y'],  # Latitude
            'radius': 20000  # Search radius in meters
        }

        # Make the API request to search for places
        try:
            response = requests.get('https://dapi.kakao.com/v2/local/search/keyword.json', headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching search results: {e}")
            continue

        # Process the data
        data = response.json()
        for document in data.get('documents', []):
            place_name = document.get('place_name')
            place_id = document.get('id')
            longitude = document.get('x')
            latitude = document.get('y')
            phone = document.get('phone')

            # Skip if the place has already been processed
            if place_id in unique_place_ids:
                continue
            unique_place_ids.add(place_id)

            # Note: Kakao Local API doesn't provide detailed reviews/prices directly.
            # The detailed endpoint you used seems incorrect. For simplicity, we'll skip it here.
            # If you have a valid detail endpoint, replace this section.
            average_rating = 'N/A'  # Placeholder
            average_price = 'N/A'  # Placeholder

            # Write to the CSV file
            writer.writerow([place_name, longitude, latitude, phone, average_rating, average_price])

print("Data collection complete. Results have been saved to", csv_file)