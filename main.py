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

if __name__ == "__main__":
    main()
