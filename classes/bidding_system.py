from user import User
from nicegui import ui

class BiddingSystem:
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def display_available_restaurants(self, party_size):
        party_size = int(party_size)
        available_restaurants = [
            restaurant
            for restaurant in self.restaurants
            if party_size <= restaurant.max_party_size
        ]

        # Display available restaurants on the GUI
        with ui.column():
            with ui.row():
                ui.label(f"Available Restaurants for Party Size {party_size}")
            for idx, restaurant in enumerate(available_restaurants, start=1):
                with ui.row():
                    ui.label(f"{idx}. {restaurant.name} - Max Party Size: {restaurant.max_party_size} - Current Bid: ${restaurant.current_bid}")

    def place_bid(self, user, restaurant_name, bid_amount):
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                user.bidding_history.append(
                    {
                        "restaurant": restaurant_name,
                        "time": "now",
                        "bid_amount": bid_amount,
                    }
                )
                restaurant.current_bid = bid_amount
                print(
                    f"Bid placed successfully for {restaurant_name} at ${bid_amount}."
                )
                return
        else:
            print(
                f"Invalid restaurant name. Please choose a valid restaurant from the list."
            )


#! Implement methods for placing bids, updating bids, and handling bidding countdown.
