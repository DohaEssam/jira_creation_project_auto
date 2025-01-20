from src.modify_fields import ModifyScreenFields
from src.get_user_id import UserSearchAPI
from helper.APIHelper import APIHelper
from src.create_project import CreateProjectAPI
from src.get_user_id import UserSearchAPI
import requests

def main():

    try:
        # Initialize the helper and create_project instance
        api_helper = APIHelper()
        # for testing
        # add_fields_to_new_screen=  ModifyScreenFields(api_helper)
        # add_fields_to_new_screen.apply_fields_to_new_project("TES012")


        # Create the project API instance (This will raise an error if project name or lead email is invalid)
        create_project_api = CreateProjectAPI(api_helper)

        # Create the project
        response = create_project_api.create_project()
        print("Response:", response)

        # Handle the response
        if response:
            print("Project created successfully:", response)
        else:
            print("Failed to create project.")


    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


    
        #TEST
        # call api to get user_id from user email
    def get_user_id(email:str):
        JIRA_BASE_URL = "https://istnetworks-dev.atlassian.net"  # or https://jira.your-company.com
        JIRA_USER_EMAIL = "akhamis@istnetworks.com"  # For Jira Cloud basic auth
        JIRA_API_TOKEN = "ATATT3xFfGF0vdueykvU3RPNPLXFB889pdZUrZSyXQvpDyST1VUuZFW0o-NWJIaWdg8fAjhZM4L7RRywxjlG5P1fXsmvwgF-a-g31qVXYK8B0GHgZOCnIP-LgcAooCKqGNgxDBMGAetuQNVK-6UZYcVi9NDiwb28HAFMXl8xBO5_8SYzLN5iWmo=262BD91F"


        # Authentication for Jira (basic auth example)
        AUTH = (JIRA_USER_EMAIL, JIRA_API_TOKEN)

        # Headers for JSON content
        HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        url = f"{JIRA_BASE_URL}/rest/api/3/user/search"
        
        params = {"query": email}
        try:
            # Perform GET request
            response = requests.get(url, headers=HEADERS, auth=AUTH,params=params)
            response.raise_for_status()  # Raise an error for HTTP codes >= 400
            data = response.json()
            
            if data and isinstance(data, list):
                # Assuming the first result is the correct one
                user = data[0]
                return user.get("accountId")
            
            print("User not found or invalid response.")
            return None
        
        
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    email = 'akhamis@istnetworks.com'
    user_id = get_user_id(email)
    print(user_id)
    

if __name__ == "__main__":
    main()
