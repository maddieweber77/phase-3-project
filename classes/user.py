from geopy.geocoders import Nominatim

class User:
    def __init__(self, name, location, party_size):
        self.name = name
        self.location = location
        self.party_size = party_size
        self.bidding_history = []

    @property
    def party_size(self):
        return self._party_size

    @party_size.setter
    def party_size(self, party_size):
        try:
            party_size = int(party_size)
            PARTY_LIMIT_SIZE = (10 >= party_size >= 1)
            if PARTY_LIMIT_SIZE:
                self._party_size = party_size
            else:
                raise ValueError("Party size must be an integer between 1 and 10.")
        except ValueError:
            raise ValueError("Invalid party size. Please enter a valid integer.")


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
