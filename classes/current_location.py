

from geopy.geocoders import Nominatim

loc = Nominatim(user_agent="GetLoc")
address = input("What is your address? ")
getLoc = loc.geocode(address)

#print(getLoc.address)

Latitude = getLoc.latitude
Longitude = getLoc.longitude

print("Latitude = ", getLoc.latitude, "\n")
print("Longitude = ", getLoc.longitude)

# need to get lat and long coordinates and classify them into neighborhood categories