from geopy.geocoders import Nominatim
from user import User
from bidding_system import BiddingSystem
from restaurant import Restaurant
from current_location import get_fancy_restaurants
import random
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

# Make sure all files are imported

def show(event):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

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

def register():
        with ui.row():
            name_input = ui.input("What is your first and last name? ").value

            user = User(name_input,"558 Broome Street",2)

            user.validate_name_input(name_input)
            # User.self.name = name_input

        while True:
            with ui.row():
                address = ui.input("What is your current location address? ").value

                loc = Nominatim(user_agent="GetLoc")
                getLoc = loc.geocode(address)

                if getLoc: 
                    latitude = getLoc.latitude
                    longitude = getLoc.longitude
                    print("printing from user.py")
                    ui.label(f"latitude: {latitude}" )
                    ui.label(f"longitude: {longitude}" )
                    break
                else:
                    print('Invalid address, try again')
                    # return self.register()

            
            try:
                with ui.row():
                    party_size_input = int(ui.input("How many people are in your party? ").value)
                # self.party_size = party_size_input
                break
            except ValueError:
                print("Invalid input. Please enter a valid party size (an integer between 1 and 10).")


        return user, latitude, longitude

def is_valid_bid(bid_amount, minimum_bid):
    return bid_amount>= minimum_bid


def main():
    
    # Initialize user
    user, latitude, longitude = register()
    
    # Get fancy restaurants
    fancy_restaurants = get_fancy_restaurants(latitude, longitude)

    #checking to make sure that fancy restaurants are being pulled through
    #! this needs to be the # of fancy restaurants that can accomodate the given party size
    ui.label(f"{len(fancy_restaurants)} Fancy Restaurants")

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
            ui.label("Your bid is too low. Please enter a higher bid that is at least $10 more than the last bid")
    
    # Place bid in bidding system
    bidding_system.place_bid(user, restaurant_name, bid_amount)

    # View user's bidding history 
    user.view_bidding_history()

    ui.run(native=True)


def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')  



#! ################   niceGUI code below  ################ 
##########################################################
#! ################   niceGUI code below  ################ 



def submit_name(name_input_widget):
    name_input = name_input_widget.value
    user = User(name_input, "558 Broome Street", 2)
    print(f"Name: {name_input}")

def submit_address(address_input_widget):
    address_input = address_input_widget.value
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(address_input)

    if getLoc: 
        latitude = getLoc.latitude
        longitude = getLoc.longitude
        print("printing from main.py")
        print((f"latitude: {latitude}" ))
        print((f"longitude: {longitude}" ))

        with ui.row():
            ui.label(f"latitude: {latitude}" )
            ui.label(f"longitude: {longitude}" )
    else:
        print('Invalid address, try again')
        # return self.register()

def submit_party_size(party_size_input_widget):
    party_size_input = party_size_input_widget.value

    print(f"Party Size: {party_size_input}")



def m():

    latitude = 0
    longitude = 0
    
    with ui.row():
        name_input_widget = ui.input("First & Last Name")
        ui.button('Next', on_click=lambda: submit_name(name_input_widget))

    with ui.row():
        address_input_widget = ui.input("Current Address")
        ui.button('Next', on_click=lambda: submit_address(address_input_widget))
    
    
    with ui.row():
        party_size_input_widget = ui.input("# People in Party")
        ui.button('Next', on_click=lambda: submit_party_size(party_size_input_widget))
        
            

        # party_size_input = ui.input("# People in Party").value


        # #! need to also return latitude and logitude somehow
        # return name_input, address_input, party_size_input


if __name__ in {"__main__", "__mp_main__"}:
    # main()
    m()
    ui.run(native=True)
    



#! If I type in the uncapitalized name of a neighborhood, it should still accept it
    
#! make some random function that is randomly either true / false (to recreate a second bidder) and depending what it returns, the original user will either be outbid (or will be allowed to have the reservation)
    
#! Needs to ask the user for party size
    

#! Make tests for first and last name
    
#! downplay the login info
#! rather, need to emphasize bidding process:
    # pull restaurants API

#! if there aren't any restaurant reservations with the specific inputted # of people, we need to tell them that and ask them if they would like to look elsewhere