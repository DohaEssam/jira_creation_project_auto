from helper.APIHelper import APIHelper

class ModifyScreenFields:
    def __init__(self, api_helper):
        self.api_helper = api_helper
        self.TJM_SCREEN_ID = 11065  # Fixed value for source screen
        self.TJM_TAB_ID = 11068     # Fixed value for source tab
        # Define the specific fields to be added in new project
        self.fields_to_add = [
        {"id": "duedate", "name": "Due date"},
        {"id": "customfield_10015", "name": "Start date"},
        {"id": "timetracking", "name": "Time tracking"},
        {"id": "customfield_10136", "name": "Country"},
        {"id": "customfield_10137", "name": "Net Revenue"},
        {"id": "customfield_10069", "name": "PBS ID"},
         {"id": "customfield_10014", "name": "Epic Link"}
         ]
    def get_screen_ids(self, project_key):
        """Fetch all screen IDs for the given project key and screen name across all pages."""
        print(f"Fetching the screen IDs for project key: {project_key}")
        endpoint = "/screens"
        start_at = 0
        max_results = 50  # Adjust if needed, default is usually 50
        screen_ids = []

        while True:
            # Add pagination parameters
            paginated_endpoint = f"{endpoint}?startAt={start_at}&maxResults={max_results}&orderBy=name"
            response = self.api_helper.get(paginated_endpoint)

            if response:
                # Check if the response contains screens
                screens = response.get("values")  # Replace "values" with the correct key holding screen data
                if not screens:
                    print("No screens found in the response.")
                    break

                # Filter screens by name starting with the project key
                matching_screens = [
                    screen for screen in screens
                    if screen.get("name", "").startswith(f"{project_key}:")
                ]

                # Collect the screen IDs that start with the project key
                for screen in matching_screens:
                    print(f"Found screen: {screen}")
                    screen_ids.append(screen.get("id"))

                # Check if there's another page to fetch
                if response.get("isLast", True):  # Replace "isLast" if the field has a different name
                    print("No more pages left to process.")
                    break

                # Move to the next page
                start_at += max_results
            else:
                print("Failed to retrieve screens.")
                break

        return screen_ids

    def get_tab_id(self, screen_id):
        """Fetch the tab ID for the given screen ID."""
        print("Fetching the tab ID for the given screen ID.")
        endpoint = f"/screens/{screen_id}/tabs"
        response = self.api_helper.get(endpoint)

        if isinstance(response, list):  # Check if response is a list
            # Assuming the first tab is desired; adjust logic if needed
            for tab in response:
                return tab.get("id")
            print(f"No tabs found for screen ID: {screen_id}")
        else:
            print(f"Unexpected response format: {type(response)}")
        return None


    def get_fields_from_source(self):
        """Retrieve fields from the source screen and tab."""
        print("Retrieve fields from the source screen and tab.")
        endpoint = f"/screens/{self.TJM_SCREEN_ID}/tabs/{self.TJM_TAB_ID}/fields"
        response = self.api_helper.get(endpoint)

        if response:
            return [field.get("id") for field in response]  # Return list of field IDs
        else:
            print("Failed to retrieve fields from source.")
        return []

    def add_fields_to_new_project(self, new_screen_id, new_tab_id, fields):
        """Add fields to the new screen and tab."""
        print("Add fields to the new screen and tab.")
        for field_id in fields:
            endpoint = f"/screens/{new_screen_id}/tabs/{new_tab_id}/fields"
            data = {"fieldId": str(field_id)}

            try:
                response = self.api_helper.post(endpoint, json=data)

                # Check if the response indicates the field already exists
                if response and isinstance(response, dict):
                    if "errors" in response and "fieldId" in response["errors"]:
                        error_message = response["errors"]["fieldId"]
                        if "already exists on the screen" in error_message:
                            print(f"Field {field_id} already exists on the screen. Skipping to the next field.")
                            continue

                if response:  # Successful addition
                    print(f"Successfully added field {field_id} to screen {new_screen_id}, tab {new_tab_id}.")
                else:
                    print(f"Failed to add field {field_id}. Error: No response or unknown error.")

            except Exception as e:
                print(f"Unexpected error while adding field {field_id}: {e}")

    def apply_fields_to_new_project(self, project_key):
        """Main method to add specific fields to a new project's screens and tabs."""
        print("Main method to add specific fields to a new project's screens and tabs.")
        
        # Fetch all screen IDs for the new project
        screen_ids = self.get_screen_ids(project_key)
        print(f"Found screen IDs: {screen_ids}")
        if not screen_ids:
            print("Could not find screens for the new project.")
            return

        # Iterate over all the screen IDs
        for new_screen_id in screen_ids:
            print(f"Processing screen {new_screen_id}")

            # Fetch tab ID for the new screen
            new_tab_id = self.get_tab_id(new_screen_id)
            print(f"new_tab_id == {new_tab_id}")
            if not new_tab_id:
                print(f"Could not find tab for screen {new_screen_id}.")
                continue

            # Prepare the list of field IDs to add
            fields_to_add = [field["id"] for field in self.fields_to_add]
            
            # Add fields to the new screen and tab
            self.add_fields_to_new_project(new_screen_id, new_tab_id, fields_to_add)