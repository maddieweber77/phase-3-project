class Restaurant:
    def __init__(self, name, max_party_size, current_bid, neighborhood):
        self.name = name
        self.max_party_size = max_party_size
        self.current_bid = current_bid
        self.neighborhood = neighborhood

    #! need to do @property and setter for all of the above

    def display_info(self, user_neighborhood):
        if self.neighborhood.lower() == user_neighborhood.lower():
            print(f"{self.name} - Max Party Size: {self.max_party_size} - Current Bid: ${self.current_bid} - Neighborhood: {self.neighborhood}")

#! Implement methods for managing restaurant information and releasing canceled reservations.