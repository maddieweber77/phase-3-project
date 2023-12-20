from user import User
from bidding_system import BiddingSystem
from restaurant import Restaurant

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
    # Initialize restaurants
    restaurants = [
        Restaurant(name="Riverside Lounge", max_party_size=5, current_bid=20, neighborhood="Upper West Side"),
        Restaurant(name="Parkside Grill", max_party_size=8, current_bid=15, neighborhood="Upper West Side"),
        Restaurant(name="Elegance on the East", max_party_size=8, current_bid=22, neighborhood="Upper East Side"),
        Restaurant(name="Cafe Serenity", max_party_size=10, current_bid=25, neighborhood="Upper East Side"),
        Restaurant(name="City Lights Bistro", max_party_size=8, current_bid=22, neighborhood="Midtown"),
        Restaurant(name="Metropolis Eats", max_party_size=10, current_bid=25, neighborhood="Midtown"),
        Restaurant(name="Highline Haute Cuisine", max_party_size=10, current_bid=18, neighborhood="Chelsea"),
        Restaurant(name="Artisan Alley", max_party_size=12, current_bid=30, neighborhood="Chelsea"),
        Restaurant(name="Greenwich Gem", max_party_size=6, current_bid=18, neighborhood="Greenwich Village"),
        Restaurant(name="Village Vittles", max_party_size=8, current_bid=25, neighborhood="Greenwich Village"),
        Restaurant(name="Soho Social", max_party_size=6, current_bid=18, neighborhood="SoHo"),
        Restaurant(name="Arty Appetites", max_party_size=8, current_bid=25, neighborhood="SoHo"),
        Restaurant(name="Tribeca Treats", max_party_size=10, current_bid=22, neighborhood="Tribeca"),
        Restaurant(name="Downtown Delights", max_party_size=12, current_bid=30, neighborhood="Tribeca"),
        Restaurant(name="Financial Fusion", max_party_size=6, current_bid=18, neighborhood="Financial District"),
        Restaurant(name="Wall Street Bites", max_party_size=8, current_bid=25, neighborhood="Financial District"),
        Restaurant(name="Harlem Harvest", max_party_size=10, current_bid=22, neighborhood="Harlem"),
        Restaurant(name="Soulful Supper", max_party_size=12, current_bid=30, neighborhood="Harlem"),
        Restaurant(name="Village Vittles", max_party_size=6, current_bid=18, neighborhood="East Village"),
        Restaurant(name="Eclectic Eats", max_party_size=8, current_bid=25, neighborhood="East Village"),
        # Add more restaurants with their respective neighborhoods
    ]


    # Bidding system now has access to the restaurants object
    bidding_system = BiddingSystem(restaurants)

    # Create a user instance and register
    user = User("M W", "2", 2).register()
    
    def is_valid_restaurant(restaurant):
        valid_restaurant_names = [r.name for r in restaurants]
        return restaurant in valid_restaurant_names


    

    # Display available restaurants based on a user's location
    bidding_system.display_available_restaurants(party_size=user.party_size, user_neighborhood=user.location)


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
    
    # User("M W", "2", 3).register()

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