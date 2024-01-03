import random
class Restaurant:

    
    def __init__(self, name, max_party_size, current_bid=None):
        self.name = name
        self.max_party_size = max_party_size
        self.current_bid = current_bid if current_bid is not None else random.randint(10, 100) * max_party_size

    #! need to do @property and setter for all of the above

    def display_info(self):
        print(f"{self.name} - Max Party Size: {self.max_party_size} - Current Bid: ${self.current_bid}")

#! Implement methods for managing restaurant information and releasing canceled reservations.