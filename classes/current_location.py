from geopy.geocoders import Nominatim
import sqlite3
import requests
from restaurant import Restaurant
import random

def get_hardcoded_restaurants(lat, lng):
    # Hardcoded list of 10 restaurants
    return [
        Restaurant(name="Restaurant A", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant B", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant C", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant D", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant E", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant F", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant G", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant H", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant I", max_party_size=random.randint(2, 10)),
        Restaurant(name="Restaurant J", max_party_size=random.randint(2, 10)),
    ]


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
    # conn = sqlite3.connect('reservations.db')
    # cursor = conn.cursor()

    # # Fetch all data from the reservations table
    # cursor.execute('SELECT * FROM reservations')
    # reservations = cursor.fetchall()

    # conn.close()

    # return reservations
     pass

def main(latitude, longitude):

    #     # Get fancy restaurants
    #     response = get_fancy_restaurants(latitude, longitude)

    #     # Fetch reservations from the database
    #     reservations = fetch_reservations_from_db()

    #     # Check if the API request was successful
    #     if response.get('status') == 'OK':
    #         restaurants = response.get('data', {}).get('places', [])
            
    #     else:
    #         print(f"Error: {response.get('message', 'Unknown error')}")
    # # else:
    # #     print("Invalid address. Please try again.")

    # Fetch hardcoded restaurants
    restaurants = get_hardcoded_restaurants()

    # Fetch reservations from the database
    reservations = fetch_reservations_from_db()

    # Use the 'restaurants' list for further processing
    print("Hardcoded Restaurants:")
    for restaurant in restaurants:
        print(f"{restaurant.name} - Max Party Size: {restaurant.max_party_size}")

if __name__ == "__main__":
    # Sample latitude and longitude (replace with actual values)
    main(latitude=40.7128, longitude=-74.0060)



if __name__ == "__main__":
    main()