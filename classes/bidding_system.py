from user import User
class BiddingSystem:
    def __init__(self, restaurants):
        self.restaurants = restaurants


    def display_available_restaurants(self, party_size):
        party_size = int(party_size)
        for restaurant in self.restaurants:
            if party_size <= restaurant.max_party_size:
                print(f"Restaurant: {restaurant.name}, Max Party Size: {restaurant.max_party_size}, Current Bid: ${restaurant.current_bid}")
        while True:
            available_restaurants = [
                restaurant
                for restaurant in self.restaurants
                if (
                party_size <= restaurant.max_party_size
                )
            ]

            if not available_restaurants:
                print(
                    f"No available restaurants available in your area for the specified party size. Please try again"
                )
                
                # Re-prompt user for neighborhood and party size
                user = User("dummy", "dummy", 0)
                user.register()
                
                # Update party size and neighborhood
                party_size = user.party_size
            else:
                # print(f"Available Restaurants: ")
                # for restaurant in available_restaurants:
                #     restaurant.display_info(user_neighborhood)
                break  # Break out of the loop when there are available restaurants

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
