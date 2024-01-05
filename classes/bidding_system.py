from user import User
from nicegui import ui

class BiddingSystem:
    def __init__(self, restaurants):
        self.restaurants = restaurants

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
                    f"Bid placed successfully for {restaurant_name} for ${bid_amount}."
                )
                return
        else:
            print(
                f"Invalid restaurant name. Please choose a valid restaurant from the list."
            )


#! Implement methods for placing bids, updating bids, and handling bidding countdown.
