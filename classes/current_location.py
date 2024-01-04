from geopy.geocoders import Nominatim
import sqlite3
import requests
from restaurant import Restaurant
import random

def get_fancy_restaurants(lat, lng):
    url = "https://maps-data.p.rapidapi.com/searchmaps.php"

    querystring = {f"query":"fancy restaurants","limit":"10","country":"us","lang":"en","lat":{lat},"lng":{lng},"offset":"0","zoom":"13"}

    headers = {
        "X-RapidAPI-Key": "4578ad90c0msh7185e76eb4a1d1ap1676a0jsn80fa8c573e3d",
        "X-RapidAPI-Host": "maps-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.ok:
        data = response.json()
        places = data.get('data', [])

        # # print("Raw Data:")
        # # print(data)

        # print("\nRestaurant Names:")
        # print("printing from current_location")
        # for place in places:
        #     print(place.get('name'))

        return [
        Restaurant(
            name=place.get('name'),
            max_party_size=random.randint(2, 10)
        )
        for place in places
    ]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

def fetch_reservations_from_db():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()

    # Fetch all data from the reservations table
    cursor.execute('SELECT * FROM reservations')
    reservations = cursor.fetchall()

    conn.close()

    return reservations

def main(latitude, longitude):
    # loc = Nominatim(user_agent="GetLoc")
    # address = input("What is your address? ")
    # getLoc = loc.geocode(address)

    # if getLoc:
    #     latitude = getLoc.latitude
    #     longitude = getLoc.longitude

    #     print("Latitude =", latitude)
    #     print("Longitude =", longitude)

        # Get fancy restaurants
        response = get_fancy_restaurants(latitude, longitude)

        # Fetch reservations from the database
        reservations = fetch_reservations_from_db()

        # Check if the API request was successful
        if response.get('status') == 'OK':
            restaurants = response.get('data', {}).get('places', [])
            
        else:
            print(f"Error: {response.get('message', 'Unknown error')}")
    # else:
    #     print("Invalid address. Please try again.")

if __name__ == "__main__":
    main()