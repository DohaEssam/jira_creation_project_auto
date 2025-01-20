from helper.APIHelper import APIHelper
import os

class UserSearchAPI:
    def __init__(self, api_helper):
        self.api_helper = api_helper

        # Path to the configuration file
        file_path = os.path.abspath("configuration.txt")

        # Read configuration
        config = APIHelper.read_config_from_file(file_path)
        # Extract email value and sanitize it
        raw_email = config.get("PROJECT_LEAD_EMAIL")
        if not raw_email:
            raise ValueError("PROJECT_LEAD_EMAIL is missing in the configuration file.")

        # Remove surrounding quotes, if present
        self.email = raw_email.strip("'\"")


    def search_user_by_email(self):
       
        endpoint = "user/search"
        params = {"query": self.email}
        response = self.api_helper.get(endpoint, params=params)

        if response and isinstance(response, list):
            # Assuming the first result is the correct one
            user = response[0]
            return user.get("accountId")
        
        print("User not found or invalid response.")
        return None
