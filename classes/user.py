class User:
    def __init__(self, user, location):
        self.user = user
        self.location = location
        self._bidding_history = []

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        USER_NOT_EMPTY = user is not None
        USER_OBJECT_TYPE = isinstance(user, User)
        if USER_NOT_EMPTY and USER_OBJECT_TYPE:
            self._user = user
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, location):
        if not isinstance(location, str):
            raise ValueError("Location must be a string")
        MAX_LOCATION_LENGTH = 50
        if not isinstance(location, str) or len(location) > MAX_LOCATION_LENGTH:
            raise ValueError("Location must be a string with a maximum length of {}".format(MAX_LOCATION_LENGTH))
        SUPPORTED_LOCATIONS = ["Upper West Side","Upper East Side", "Midtown","Chelsea","Greenwich Village","SoHo","Tribeca","Financial District","Harlem","East Village"]
        if location not in SUPPORTED_LOCATIONS:
            raise ValueError("Invalid location. Supported locations: {}".format(SUPPORTED_LOCATIONS))
        if not location.strip():
            raise ValueError("Location cannot be empty")
        self._location = location.lower()

    @property
    def bidding_history(self):
        return self._bidding_history

    @bidding_history.setter
    def bidding_history(self, bid):
        self._bidding_history.append(bid)

    def view_bidding_history(self):
        if not self._bidding_history:
            print("No bidding history available.")
        else:
            print("Bidding History:")
            for bid in self._bidding_history:
                print("- Restaurant: {}, Time: {}, Bid Amount: {}".format(bid['restaurant'], bid['time'], bid['bid_amount']))

    def register(self):
        print("Welcome to the registration process!")
        name_input = input("What is your first and last name? ")
        
        email = input("What is your email? ")
        # Removed email validation logic
        
        password = input("Please make a password: ")
        phone_number = input("What is your phone number? ")

        print(f"Thank you, {name_input}! Your registration is complete.")

# Create a user instance
user1 = User(user="user123", location="East Village")

# Register the user
user1.register()

# Implement methods for user registration, authentication, and viewing bidding history.
# (These methods need to be added based on your application's requirements)
# Authenticate
# Bidding History
