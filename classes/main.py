from geopy.geocoders import Nominatim
from user import User
from bidding_system import BiddingSystem
from restaurant import Restaurant
from current_location import get_neighborhood, get_fancy_restaurants

# Make sure all files are imported

def get_user_input(prompt, data_type=str, validation_function=None, **kwargs):
    while True:
        try:
            user_input = data_type(input(prompt))
            
            # Check if a validation function is provided
            if validation_function is not None and not validation_function(user_input):
                raise ValueError("Invalid input. Please enter a valid value.")
            
            return user_input
        except ValueError as e:
            print(str(e))

def is_valid_bid(bid_amount, minimum_bid):
    return bid_amount>= minimum_bid


def main():
    # Initialize user
    user = User("M W", "2", 2).register()

    # Get user location
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(user.location)

    latitude = 0
    longitude= 0

    if getLoc:
        user_location = get_neighborhood(getLoc.latitude, getLoc.longitude)
        print(f"You are in the neighborhood: {user_location}")
        latitude = getLoc.latitude
        longitude = getLoc.longitude
        print(f"latitude: {getLoc.latitude}" )
        print(f"longitude: {getLoc.longitude}" )

        response = get_fancy_restaurants(latitude, longitude)

        # Check if the API request was successful
        if response.get('status') == 'OK':
            restaurants = response.get('data', {}).get('places', [])
            
            if restaurants:
                print("\nFancy Restaurants:")
                for restaurant in restaurants:
                    print(restaurant.get('name'))
            else:
                print("No fancy restaurants found.")
        else:
            print(f"Error: {response.get('message', 'Unknown error')}")
    
    else:
        print('Invalid address, try again')
        return  # You might want to handle this case appropriately

    # Get fancy restaurants based on user's location
    fancy_restaurants = get_fancy_restaurants(latitude, longitude)

    # Initialize restaurants based on the obtained fancy restaurants
    restaurants = [
        Restaurant(
            name=restaurant.get('name'),
            max_party_size=10,
            current_bid=15,     
            neighborhood=user_location
        )
        for restaurant in fancy_restaurants
    ]

    # Bidding system now has access to the restaurants object
    bidding_system = BiddingSystem(restaurants)

    # Display available restaurants based on a user's location
    bidding_system.display_available_restaurants(party_size=user.party_size, user_neighborhood=user_location)

    # Get user bid info
    restaurant_name = get_user_input(
        "Which restaurant do you want to bid on? ",
        data_type=str,
        validation_function=is_valid_restaurant
    )
    
    # How to make sure that this amount is greater than the previous bid, if a previous bid exists?
    #! what does next do?
    current_bid = next((restaurant.current_bid for restaurant in restaurants if restaurant.name == restaurant_name), None)
    
    while True:
        bid_amount = get_user_input(f"Enter your bid amount (must be $10 greater than last bid of ${current_bid}): $", float)
        if bid_amount >= current_bid +10:
            break
        else:
            print("Your bid is too low. Please enter a higher bid that is at least $10 more than the last bid")
    
    # Place bid in bidding system
    bidding_system.place_bid(user, restaurant_name, bid_amount)

    # View user's bidding history
    user.view_bidding_history()

if __name__ == "__main__":
    main()



#! If I type in the uncapitalized name of a neighborhood, it should still accept it
    
#! make some random function that is randomly either true / false (to recreate a second bidder) and depending what it returns, the original user will either be outbid (or will be allowed to have the reservation)
    
#! Needs to ask the user for party size
    

#! Make tests for first and last name
    
#! downplay the login info
#! rather, need to emphasize bidding process:
    # pull restaurants API

#! if there aren't any restaurant reservations with the specific inputted # of people, we need to tell them that and ask them if they would like to look elsewhere