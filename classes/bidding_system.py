class BiddingSystem:
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def display_available_restaurants(self, party_size, user_neighborhood):
        available_restaurants = [restaurant for restaurant in self.restaurants
            if party_size <= restaurant.max_party_size
            and restaurant.neighborhood.lower() == user_neighborhood.lower()]

        if not available_restaurants:
            print(f"No available restaurants in {user_neighborhood} for the specified party size.")
            return

        print(f"Available Restaurants in {user_neighborhood}: ")
        for restaurant in available_restaurants:
            restaurant.display_info(user_neighborhood)

    def place_bid(self, user, restaurant_name, bid_amount):
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_name:
                user.bidding_history = {'restaurant': restaurant_name, 'time': 'now', 'bid_amount': bid_amount}
                restaurant.current_bid = bid_amount
                print(f"Bid placed successfully for {restaurant_name} at ${bid_amount}.")
                return
        else:
            print(f"Invalid restaurant name. Please choose a valid restaurant from the list.")


#! Implement methods for placing bids, updating bids, and handling bidding countdown.