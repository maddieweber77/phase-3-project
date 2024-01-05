# Import Statements
from geopy.geocoders import Nominatim
from user import User
from bidding_system import BiddingSystem
from restaurant import Restaurant
from current_location import get_fancy_restaurants, get_hardcoded_restaurants
import random
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

# Function to Display Notifications
def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')  

## Data Storage #############################################################

data = {'user': None, 'latitude': None, 'longitude': None, 'party_size': None}
completion_counter = 0
completion_counter_2 = 0
data_2 = {'restaurant_name': None, 'bid_amount': None}

# Global Variables
name_input_widget = None
address_input_widget = None
party_size_input_widget = None
submit_button = None

bidding_input_widget = None
bidding_amount_input_widget = None
submit_button_2 = None

restaurant_buttons = []

## Section: User Input Submission ###########################################

def submit_name(data):
    global completion_counter
    name_input = name_input_widget.value
    user = User(name_input, "558 Broome Street", 2)
    print(f"Name: {name_input}")

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

        data['latitude'] = latitude
        data['longitude'] = longitude
        completion_counter += 1
        check_completion()

    else:
        print('Invalid address, try again')

def submit_party_size(data):
    global completion_counter
    party_size_input = party_size_input_widget.value

    print(f"Party Size: {party_size_input}")

    data['party_size'] = party_size_input
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

## Section: Bidding System Operations ######################################

def check_completion_2(bidding_system):
    global completion_counter_2
    if completion_counter_2 == 2:
        bidding_system.place_bid(data['user'], data_2['restaurant_name'], data_2['bid_amount'])
        completion_counter_2 = 0
        hide_bidding_questions()

def hide_bidding_questions():
    global bidding_input_widget, bidding_amount_input_widget, submit_button_2
    if bidding_input_widget:
        bidding_input_widget.visible = False
    if bidding_amount_input_widget:
        bidding_amount_input_widget.visible = False
    if submit_button_2:
        submit_button_2.visible = False

    # Clear the existing restaurant buttons without re-initializing the list
    for button in restaurant_buttons:
        button.visible = True

## Section: GUI Component Operations #######################################

def hide_components():
    global name_input_widget, address_input_widget, party_size_input_widget, submit_button
    # Hide the three prompts and the submit button
    name_input_widget.visible = False
    address_input_widget.visible = False
    party_size_input_widget.visible = False
    submit_button.visible = False

def handle_button_click(restaurant, bidding_system):
    global completion_counter_2

    completion_counter_2+=1
    print('from handle button click, completion counter')
    print(completion_counter_2)
    #! want this to be true initially, but once I click on a button, I want it to become false
    set_buttons_visibility(True)

    # Now handle the click event for the specific restaurant
    prompt_bid(restaurant, bidding_system)

def set_buttons_visibility(visibility):
    global completion_counter_2

    for idx in range(completion_counter_2):
        # Set the visibility of the button to the specified value
        restaurant_buttons[idx].visible = visibility

def prompt_bid(restaurant, bidding_system):
    global bidding_amount_input_widget, submit_button_2
    # Display a prompt for the user to enter a bid for the specific restaurant
    with ui.row():
        bidding_amount_input_widget = ui.input(f"Bid Amount for {restaurant.name} (must be $10 greater than last bid)")
    with ui.row():
        submit_button_2 = ui.button('Submit', on_click=lambda: submit_bid(restaurant, bidding_system))

def submit_bid(restaurant, bidding_system):
    global data_2, completion_counter_2
    bid_amount = bidding_amount_input_widget.value

    data_2['restaurant_name'] = restaurant.name
    data_2['bid_amount'] = bid_amount

    bidding_system.place_bid(data['user'], data_2['restaurant_name'], data_2['bid_amount'])

    # Switch to Screen 3 after submitting bid
    switch_to_screen(SCREEN_3)

    # Display Screen 3
    show_screen_3(data_2['restaurant_name'], data_2['bid_amount'])


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

# Screen Variables
SCREEN_1 = 1
SCREEN_2 = 2
SCREEN_3 = 3
current_screen = SCREEN_1

def switch_to_screen(screen):
    global current_screen
    current_screen = screen

def hide_all_components():
    global name_input_widget, address_input_widget, party_size_input_widget, submit_button
    # Hide all components from Screen 1
    name_input_widget.visible = False
    address_input_widget.visible = False
    party_size_input_widget.visible = False
    submit_button.visible = False

    #! we need to check to see if the restaurant buttons exist, and if they do, then we need to make them hidden
    # Check and hide restaurant buttons if they exist
    global restaurant_buttons
    if restaurant_buttons:
        for button in restaurant_buttons:
            button.visible = False

def show_screen_1():
    hide_all_components()
    name_input_widget.visible = True
    address_input_widget.visible = True
    party_size_input_widget.visible = True
    submit_button.visible = True

def show_screen_2():
    hide_all_components()
    # Display Screen 2 components
    with ui.row():
        reSearch_button = ui.button('Re-Search', on_click=lambda: re_search(bidding_system))

    party_size = data['party_size']
    #! change below to get_fancy_restaurants when pulling from the API
    available_restaurants = get_hardcoded_restaurants(data['latitude'], data['longitude'])
    ui.html(f"<strong>Available Restaurants for Party Size {party_size}</strong>")
    for idx, restaurant in enumerate(available_restaurants, start=1):
        on_click_handler = lambda restaurant=restaurant: handle_button_click(restaurant, bidding_system)
        with ui.row():
            button = ui.button(f"{idx}. {restaurant.name} - Max Party Size: {restaurant.max_party_size} - Current Bid: ${restaurant.current_bid}", on_click=on_click_handler)
            restaurant_buttons.append(button)

    # Call display_available_restaurants to show the buttons only if not on Screen 3
    if current_screen != SCREEN_3:
        display_available_restaurants(available_restaurants, party_size, bidding_system)

def show_screen_3(restaurant_name, bid_amount):
    hide_all_components()
    # Display Screen 3 components
    with ui.row():
        ui.html(f'<strong>Bid placed successfully for {restaurant_name} for ${bid_amount}.</strong>')

def submit_all(data):
    submit_name(data)
    submit_address(data)
    submit_party_size(data)

    # Switch to Screen 2 after submitting Screen 1
    switch_to_screen(SCREEN_2)

    # Display Screen 2
    show_screen_2()

def n():
    global reSearch_button, bidding_system

    # Access the stored values in data
    print("User:", data['user'])
    print("Latitude:", data['latitude'])
    print("Longitude:", data['longitude'])
    print("Party Size:", data['party_size'])

    # Instantiate the bidding system with the list of restaurants
    #! change below to get_fancy_restaurants when pulling from the API
    fancy_restaurants = get_hardcoded_restaurants(data['latitude'], data['longitude'])
    bidding_system = BiddingSystem(restaurants=fancy_restaurants)

    # Adding button to re-search if you want
    with ui.row():
        reSearch_button = ui.button('Re-Search', on_click=lambda: show_screen_1())

    # Hide the "Re-Search" button (if it exists)
    if reSearch_button:
        reSearch_button.visible = False

    # Show Screen 1 initially
    show_screen_1()

if __name__ in {"__main__", "__mp_main__"}:
    m()
    ui.run(native=True)
