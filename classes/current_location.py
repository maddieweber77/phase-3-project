from geopy.geocoders import Nominatim

def get_neighborhood(latitude, longitude):
    # Neighborhood latitude and longitude ranges
    neighborhood_ranges = {
        "Upper West Side": {"lat_range": (40.772, 40.808), "lon_range": (-74.018, -73.972)},
        "Upper East Side": {"lat_range": (40.765, 40.782), "lon_range": (-73.958, -73.941)},
        "Midtown": {"lat_range": (40.754, 40.775), "lon_range": (-73.992, -73.977)},
        "Chelsea": {"lat_range": (40.742, 40.753), "lon_range": (-74.001, -73.988)},
        "Greenwich Village": {"lat_range": (40.729, 40.739), "lon_range": (-74.005, -73.994)},
        "SoHo": {"lat_range": (40.720, 40.726), "lon_range": (-74.005, -73.999)},
        "Tribeca": {"lat_range": (40.716, 40.727), "lon_range": (-74.014, -74.005)},
        "Financial District": {"lat_range": (40.703, 40.713), "lon_range": (-74.017, -74.006)},
        "Harlem": {"lat_range": (40.796, 40.815), "lon_range": (-73.954, -73.931)},
        "East Village": {"lat_range": (40.721, 40.734), "lon_range": (-73.991, -73.978)}
    }

    for neighborhood, ranges in neighborhood_ranges.items():
        lat_range = ranges["lat_range"]
        lon_range = ranges["lon_range"]
        if lat_range[0] <= latitude <= lat_range[1] and lon_range[0] <= longitude <= lon_range[1]:
            return neighborhood

    return "Unknown"

def main():
    loc = Nominatim(user_agent="GetLoc")
    address = input("What is your address? ")
    getLoc = loc.geocode(address)

    if getLoc:
        latitude = getLoc.latitude
        longitude = getLoc.longitude

        print("Latitude =", latitude)
        print("Longitude =", longitude)

        neighborhood = get_neighborhood(latitude, longitude)
        print(f"You are in the neighborhood: {neighborhood}")
    else:
        print("Invalid address. Please try again.")

if __name__ == "__main__":
    main()
