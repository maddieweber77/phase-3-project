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
bid_placed = False 

# Global Variables
name_input_widget = None
address_input_widget = None
party_size_input_widget = None
submit_button = None
your_reservations_button = None

bidding_input_widget = None
bidding_amount_input_widget = None
submit_button_2 = None
available_restaurants_num = None
available_restaurants_label = None
start_over_button = None

restaurant_buttons = []
reservations = []
bidding_amount_widgets = []
submit_button_widgets = []


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
        hide_components_initally()
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
        
def hide_start_over_button():
    global start_over_button
    if start_over_button:
        start_over_button.visible = False

def show_start_over_button():
    global start_over_button
    if start_over_button:
        start_over_button.visible = True

def create_start_over_button():
    global start_over_button
    start_over_button = ui.button('Start Over', on_click=lambda: start_over()).classes('nice-button')

def start_over():
    global completion_counter, completion_counter_2, data, data_2, current_screen, available_restaurants_num, restaurant_buttons, bidding_amount_widgets, submit_button_widgets

    completion_counter = 0
    completion_counter_2 = 0
    data = {'user': None, 'latitude': None, 'longitude': None, 'party_size': None}
    data_2 = {'restaurant_name': None, 'bid_amount': None}
    current_screen = SCREEN_1
    available_restaurants_num = None

    # Clear the existing restaurant buttons without re-initializing the list
    for button in restaurant_buttons:
        button.visible = False
    
    restaurant_buttons = []

    hide_all_components()
    hide_start_over_button()
    show_screen_1()

def hide_components_initally():
    global name_input_widget, address_input_widget, party_size_input_widget, submit_button

    hide_start_over_button()

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
    # set_buttons_visibility(True)

    prompt_bid(restaurant, bidding_system)

def prompt_bid(restaurant, bidding_system):
    global bidding_amount_input_widget, submit_button_2, bidding_amount_widgets, submit_button_widgets
    # Display a prompt for the user to enter a bid for the specific restaurant
    with ui.row():
        bidding_amount_input_widget = ui.input(f"Bid Amount:")
        bidding_amount_widgets.append(bidding_amount_input_widget)
    with ui.row():
        submit_button_2 = ui.button('Submit', on_click=lambda: submit_bid(restaurant, bidding_system)).classes('nice-button')
        submit_button_widgets.append(submit_button_2)

def submit_bid(restaurant, bidding_system):
    global data_2, completion_counter_2, bid_placed, reservations

    bid_amount = bidding_amount_input_widget.value

    #! this is where we need to check bid amount
    try:
        bid_amount = float(bid_amount)
    except ValueError:
        ui.notify("Please enter a valid numeric bid amount.")
        return  # Don't proceed if the input is not a valid number
    
    # Convert party_size to an integer
    try:
        party_size = int(data['party_size'])
    except ValueError:
        ui.notify("Invalid party size. Please enter a valid number.")
        return  # Don't proceed if party_size is not a valid number

    # Check if the bid amount meets the criteria
    if bid_amount < restaurant.current_bid + 10 * party_size:
        ui.notify("Bid amount must be at least $10 more per person than the current bid.")
        return  # Don't proceed if the bid amount is too low

    data_2['restaurant_name'] = restaurant.name
    data_2['bid_amount'] = bid_amount

    bidding_system.place_bid(data['user'], data_2['restaurant_name'], data_2['bid_amount'])

    # Add the reservation to the global reservations list
    reservation = {'name': data_2['restaurant_name'], 'bid_amount': data_2['bid_amount']}
    reservations.append(reservation)

    bid_placed = True

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
        submit_button = ui.button('Next', on_click=lambda: submit_all(data)).classes('nice-button')

# Screen Variables
SCREEN_1 = 1
SCREEN_2 = 2
SCREEN_3 = 3
SCREEN_4 = 4
current_screen = SCREEN_1

def switch_to_screen(screen):
    global current_screen
    current_screen = screen


#! hide all components 

def hide_all_components():
    global name_input_widget, address_input_widget, party_size_input_widget, submit_button, available_restaurants_label, submit_button_2, bidding_amount_input_widget, bidding_amount_widgets, submit_button_widgets

    hide_start_over_button()

    for widget in bidding_amount_widgets:
        widget.visible = False
    for widget in submit_button_widgets:
        widget.visible = False

    # Hide all components from Screen 1
    name_input_widget.visible = False
    address_input_widget.visible = False
    party_size_input_widget.visible = False
    submit_button.visible = False

    #Hide all from screen 2

    if available_restaurants_label is not None:
        available_restaurants_label.visible = False

    # Check and hide restaurant buttons if they exist
    global restaurant_buttons
    if restaurant_buttons:
        for button in restaurant_buttons:
            button.visible = False
    
    if bid_placed:
        available_restaurants_label = ui.html("")
    
    #hide all from screen 3
    if bidding_amount_input_widget is not None:
        bidding_amount_input_widget.visible = False
    
    if submit_button_2 is not None:
        submit_button_2.visible = False
    
    # Hide bid success message
    if bid_placed:
        with ui.row():
            ui.html("")  # This is an empty html element to clear the bid success message


def show_screen_1():
    hide_all_components()
    hide_start_over_button()
    name_input_widget.visible = True
    address_input_widget.visible = True
    party_size_input_widget.visible = True
    submit_button.visible = True

def show_screen_2():
    global available_restaurants_label
    hide_all_components()

    if available_restaurants_label is None:
        available_restaurants_label = ui.html("")

    party_size = data['party_size']
    
    #! I only want this to show once
    available_restaurants_label.visible = True
    show_start_over_button()

    #! change below to get_fancy_restaurants when pulling from the API
    available_restaurants = get_hardcoded_restaurants(data['latitude'], data['longitude'])
    for idx, restaurant in enumerate(available_restaurants, start=1):
        on_click_handler = lambda restaurant=restaurant: handle_button_click(restaurant, bidding_system)
        with ui.column().classes('main-container'):
            button = ui.button(f"{idx}. {restaurant.name} - Max Party Size: {restaurant.max_party_size} - Current Bid: ${restaurant.current_bid}", on_click=on_click_handler)
            restaurant_buttons.append(button)


def show_screen_3(restaurant_name, bid_amount):
    global bid_placed_label
    hide_all_components()
    # Display Screen 3 components
    bid_placed_label = ui.notify(f'Bid placed successfully for {restaurant_name} for ${bid_amount}.')
    
    show_start_over_button()
    show_screen_4()

def show_screen_4():
    hide_all_components()
    
    # Display Screen 4 components
    with ui.column():
        # Header for Your Reservations
        with ui.row():
            ui.html('<strong>Your Reservations</strong>')

        # Display reservations
        with ui.row():
            # Assuming you have a list of reservations, modify this part accordingly
            reservations = [
                {'name': 'Restaurant 1', 'time': '2024-01-01 18:00'},
                {'name': 'Restaurant 2', 'time': '2024-01-02 19:30'},
                # Add more reservations as needed
            ]
            for idx, reservation in enumerate(reservations, start=1):
                ui.label(f"{idx}. {reservation['name']} - Time: {reservation['time']}")

    # Include the Start Over button on Screen 4
    show_start_over_button()

def create_your_reservations_button():
    global your_reservations_button
    if your_reservations_button is None:
        your_reservations_button = ui.button('Your Reservations', on_click=lambda: switch_to_screen(SCREEN_4)).classes('nice-button')

#! might be one of the functions below
def submit_all(data):
    # Get the values from the input widgets
    name_input = name_input_widget.value
    address_input = address_input_widget.value
    party_size_input = party_size_input_widget.value

    
    # Validate the "Number of People in Party" input
    try:
        party_size = int(party_size_input)
    except ValueError:
        ui.notify("Please enter a valid number for the 'Number of People in Party'.")
        return  # Don't proceed if the input is not a valid number

    # Check if any of the required inputs is empty
    if not name_input or not address_input or not party_size_input:
        ui.notify("Please fill out all the prompts before proceeding.")
        return  # Don't proceed if any input is empty
    
    data['party_size'] = party_size
    submit_name(data)
    submit_address(data)
    submit_party_size(data)

    # Switch to Screen 2 after submitting Screen 1
    switch_to_screen(SCREEN_2)
    show_start_over_button()

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


    # Show Screen 1 initially
    show_screen_1()
    create_start_over_button()
    create_your_reservations_button()

if __name__ in {"__main__", "__mp_main__"}:
    ui.add_head_html('''
    <style>
        /* Style all buttons to look more sleek */
        .nice-button {
            background-color: #808080 !important; /* Grey background color */
            color: white; /* White text color */
            border: 2px solid #808080; /* Grey border */
            text-align: center; /* Center text */
            text-decoration: none; /* Remove underline */
            display: inline-block; /* Make it inline block */
            font-size: 16px; /* Font size */
            margin: 4px 2px; /* Margin around the button */
            cursor: pointer; /* Cursor style */
            border-radius: 8px; /* Rounded corners */
            transition-duration: 0.3s; /* Animation duration */
        }

        /* Hover effect */
        .nice-button:hover {
            background-color: white !important; /* White background on hover */
            color: #808080 !important; /* Grey text color on hover */
        }
        
        /* Style for the column of restaurant buttons */
        .restaurant-buttons-column {
            display: flex;
            flex-direction: column;
            align-items: center; /* Center the buttons horizontally */
            margin-top: 20px; /* Adjust the top margin as needed */
        }
        
        /* Style for the main container */
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center; /* Center all elements horizontally */
            justify-content: center; /* Center all elements vertically */
            
        }
    </style>
    ''')

    m()
    ui.run(native=True)
