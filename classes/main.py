from geopy.geocoders import Nominatim
from user import User
from bidding_system import BiddingSystem
from restaurant import Restaurant
from current_location import get_fancy_restaurants
import random

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
    user, latitude, longitude = User("M W", "2", 2).register()
    
    # Get fancy restaurants
    fancy_restaurants = get_fancy_restaurants(latitude, longitude)

    #checking to make sure that fancy restaurants are being pulled through
    #! this needs to be the # of fancy restaurants that can accomodate the given party size
    print(len(fancy_restaurants), " Fancy Restaurants")

    # Initialize restaurants based on the obtained fancy restaurants
    restaurants = [
        Restaurant(
            name=restaurant.get('name'),
            max_party_size=random.randint(2,10)
        )
        for restaurant in fancy_restaurants
    ]

    

    # Bidding system now has access to the restaurants object
    bidding_system = BiddingSystem(restaurants)

    # Display available restaurants based on a user's location
    bidding_system.display_available_restaurants(party_size=user.party_size)

    # Get user bid info
    restaurant_name = get_user_input(
        "Which restaurant do you want to bid on? ",
        data_type=str,
        # validation_function=is_valid_restaurant
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