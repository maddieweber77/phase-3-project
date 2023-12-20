from geopy.geocoders import Nominatim
from current_location import get_neighborhood

class User:
    def __init__(self, name, location, party_size, neighborhood=None):
        self.name = name
        self.location = location
        self.neighborhood = neighborhood
        self.bidding_history = []

    @property
    def party_size(self):
        return self._party_size

    @party_size.setter
    def party_size(self, party_size):
        PARTY_IS_NUM = isinstance(party_size, int)
        PARTY_LIMIT_SIZE = (10 >= party_size >= 1)
        if PARTY_IS_NUM and PARTY_LIMIT_SIZE:
            self._party_size = party_size
        else:
            raise ValueError("Party size must be an integer between 1 and 10.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        NAME_NOT_EMPTY = name is not None
        if NAME_NOT_EMPTY:
            self._name = name

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        if not isinstance(location, str):
            raise ValueError("Location must be a string")
        MAX_LOCATION_LENGTH = 50
        if not isinstance(location, str) or len(location) > MAX_LOCATION_LENGTH:
            raise ValueError(
                "Location must be a string with a maximum length of {}".format(
                    MAX_LOCATION_LENGTH
                )
            )
        
        if not location.strip():
            raise ValueError("Location cannot be empty")
        self._location = location

    def view_bidding_history(self):
        if not self.bidding_history:
            print("No bidding history available.")
        else:
            print("Bidding History:")
            for bid in self.bidding_history:
                print(
                    "- Restaurant: {}, Time: {}, Bid Amount: ${}".format(
                        bid["restaurant"], bid["time"], bid["bid_amount"]
                    )
                )

    def validate_name_input(self, name_input):
        if " " not in name_input:
            raise Exception(
                "Invalid name. Please include a space between the first and last name."
            )

        if any(char.isdigit() for char in name_input):
            raise ValueError("Invalid name. Numbers are not allowed in the name.")

    def register(self):
        valid_neighborhoods = [
            "Upper West Side",
            "Upper East Side",
            "Midtown",
            "Chelsea",
            "Greenwich Village",
            "SoHo",
            "Tribeca",
            "Financial District",
            "Harlem",
            "East Village",
        ]

        name_input = input("What is your first and last name? ")
        self.validate_name_input(name_input)
        self.name = name_input

        address = input("What is your current location address?")

        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(address)

        if getLoc: 
            self.location =get_neighborhood(getLoc.latitude, getLoc.longitude)
            print(f"You are in the neighborhood: {self.location}")
        else:
            print('Invalid address, try again')
            return self.register()

        # # Print numbered list of valid neighborhoods
        # print("Select your neighborhood:")
        # for i, neighborhood in enumerate(valid_neighborhoods, start=1):
        #     print(f"{i}. {neighborhood}")

        # # Get user input for neighborhood selection
        # while True:
        #     try:
        #         selected_index = int(
        #             input("Enter the number corresponding to your neighborhood: ")
        #         )
        #         if 1 <= selected_index <= len(valid_neighborhoods):
        #             #! location attribute needs to be set to neighborhood instead
        #             self.location = valid_neighborhoods[selected_index - 1]
        #             print('printing location:')
        #             print(self.location)
        #             break
        #         else:
        #             print("Invalid selection. Please enter a valid number.")
        #     except ValueError:
        #         print("Invalid input. Please enter a number.")
        
        while True:
            try:
                party_size_input = int(input("How many people are in your party? "))
                self.party_size = party_size_input
                break
            except ValueError:
                print("Invalid input. Please enter a valid party size (an integer between 1 and 10).")


        # phone_number = input("What is your phone number? ")

        # print(f"Thank you, {name_input}! Your registration is complete.")

        return self

    def get_bid_amount(self):
        while True:
            try:
                bid_amount = float(
                    input(
                        "Enter your bid amount (must be $10 greater than the last bid): $"
                    )
                )
                return bid_amount
            except ValueError:
                print("Invalid input. Please enter a valid bid amount.")


# Create a user instance


# Implement methods for user registration, authentication, and viewing bidding history.
# (These methods need to be added based on your application's requirements)
# Authenticate
# Bidding History
