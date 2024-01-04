from geopy.geocoders import Nominatim
from user import User
from bidding_system import BiddingSystem
from restaurant import Restaurant
from current_location import get_fancy_restaurants
import random
from nicegui import ui
from nicegui.events import ValueChangeEventArguments


def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')  

# Use a dictionary to store values
data = {'user': None, 'latitude': None, 'longitude': None, 'party_size': None}
completion_counter = 0  # Counter to track the completion of steps
completion_counter_2 = 0 #this is to show the questions about bidding on a restaurant
data_2 = {'restaurant_name': None, 'bid_amount': None}

# Define global variables
name_input_widget = None
address_input_widget = None
party_size_input_widget = None
submit_button = None

bidding_input_widget = None
bidding_amount_input_widget = None
submit_button_2 = None

def submit_name(data):
    global completion_counter
    name_input = name_input_widget.value
    user = User(name_input, "558 Broome Street", 2)
    print(f"Name: {name_input}")

    # Store the user value in the data dictionary
    data['user'] = user
    completion_counter += 1
    check_completion()

def submit_address(data):
    global completion_counter
    address_input = address_input_widget.value
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(address_input)

    if getLoc: 
        latitude = getLoc.latitude
        longitude = getLoc.longitude
        print("printing from main.py")
        print(f"latitude: {latitude}")
        print(f"longitude: {longitude}")

        # Store latitude and longitude in the data dictionary
        data['latitude'] = latitude
        data['longitude'] = longitude
        # Increment the completion counter
        completion_counter += 1
        
        check_completion()

    else:
        print('Invalid address, try again')

def submit_party_size(data):
    global completion_counter
    party_size_input = party_size_input_widget.value

    print(f"Party Size: {party_size_input}")

    # Store party_size in the data dictionary
    data['party_size'] = party_size_input
    # Increment the completion counter
    completion_counter += 1
    check_completion()

def check_completion():
    global completion_counter
    # Check if all three steps are completed
    if completion_counter == 3:
        # Reset the completion counter for future runs
        completion_counter = 0
        hide_components()
        n()

def submit_bidding(bidding_system, data_2): 
    global completion_counter_2
    restaurant_name = bidding_input_widget.value
    bid_amount = bidding_amount_input_widget.value

    # Validate bid amount (must be $10 greater than last bid, add your logic)
    # ...

    # Store bidding data in the data_2 dictionary
    data_2['restaurant_name'] = restaurant_name
    data_2['bid_amount'] = bid_amount

    #! is there a way to now hide the bidding questions?
    completion_counter_2 += 1
    check_completion_2(bidding_system)

def check_completion_2(bidding_system):
    global completion_counter_2
    if completion_counter_2 == 1:
        show_bidding_questions(bidding_system)
    if completion_counter_2==2:
         bidding_system.place_bid(data['user'], data_2['restaurant_name'], data_2['bid_amount']) 

def show_bidding_questions(bidding_system):
    global bidding_amount_input_widget, bidding_input_widget, submit_button_2
    with ui.row():
        bidding_input_widget = ui.input("Enter Restaurant to Bid On?")
    with ui.row():
        bidding_amount_input_widget = ui.input("Bid Amount (must be $10 greater than last bid)")
    with ui.row():
        submit_button_2 = ui.button('Submit', on_click=lambda: submit_bidding(bidding_system, data_2))

def hide_components():
    global name_input_widget, address_input_widget, party_size_input_widget, submit_button
    # Hide the three prompts and the submit button
    name_input_widget.visible = False
    address_input_widget.visible = False
    party_size_input_widget.visible = False
    submit_button.visible = False

def display_available_restaurants(restaurants, party_size, bidding_system):
        global completion_counter_2
        completion_counter_2 +=1
        party_size = int(party_size)
        available_restaurants = [
            restaurant
            for restaurant in restaurants
            if party_size <= restaurant.max_party_size
        ]

        #! After this shows up, there needs to be a prompt that asks which restaurant you want to bid on and for how much 
        # Display available restaurants on the GUI
        with ui.column():
            with ui.row():
                ui.label(f"Available Restaurants for Party Size {party_size}")
            for idx, restaurant in enumerate(available_restaurants, start=1):
                with ui.row():
                    ui.label(f"{idx}. {restaurant.name} - Max Party Size: {restaurant.max_party_size} - Current Bid: ${restaurant.current_bid}")
        check_completion_2(bidding_system)

def m():
    global name_input_widget, address_input_widget, party_size_input_widget, submit_button
    latitude = 0
    longitude = 0

    with ui.row():
        name_input_widget = ui.input("First & Last Name")

    with ui.row():
        address_input_widget = ui.input("Current Address")

    with ui.row():
        party_size_input_widget = ui.input("# People in Party")

    with ui.row():
        submit_button = ui.button('Next', on_click=lambda: submit_all(data))

def submit_all(data):
    submit_name(data)
    submit_address(data)
    submit_party_size(data)

    reSearch_button.visible = True
    name_input_widget.visible = False
    address_input_widget.visible = False
    party_size_input_widget.visible = False
    submit_button.visible = False


def re_search():
    global name_input_widget, address_input_widget, party_size_input_widget, submit_button
    # Reset the visibility of the input widgets and the submit button
    name_input_widget.visible = True
    address_input_widget.visible = True
    party_size_input_widget.visible = True
    submit_button.visible = True
    # hide research button
    reSearch_button.visible = False

def n():
    global reSearch_button, bidding_system

    # Access the stored values in data
    print("User:", data['user'])
    print("Latitude:", data['latitude'])
    print("Longitude:", data['longitude'])
    print("Party Size:", data['party_size'])

    # Instantiate the bidding system with the list of restaurants
    fancy_restaurants = get_fancy_restaurants(data['latitude'], data['longitude'])
    bidding_system = BiddingSystem(restaurants=fancy_restaurants)

    # Adding button to re-search if you want
    with ui.row():
        reSearch_button = ui.button('Re-Search', on_click=lambda: re_search(bidding_system))

    # Hide the "Re-Search" button (if it exists)
    if reSearch_button:
        reSearch_button.visible = False

    # Reset the visibility of the input widgets and the submit button
    name_input_widget.visible = True
    address_input_widget.visible = True
    party_size_input_widget.visible = True
    submit_button.visible = True

    # Display available restaurants based on a user's location
    display_available_restaurants(
        fancy_restaurants,
        party_size=data['party_size'],
        bidding_system=bidding_system  # Pass the bidding system
    )


if __name__ in {"__main__", "__mp_main__"}:
    m()
    ui.run(native=True)
