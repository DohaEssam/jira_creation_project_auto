import os
from helper.create_project_key import ProjectKeyGenerator
from src.modify_fields import ModifyScreenFields
from src.apply_permission_scheme import PermissionSchemeAPI
from src.apply_workflow import WorkflowSchemeAPI
from src.get_user_id import UserSearchAPI
from helper.APIHelper import APIHelper

class CreateProjectAPI:
    def __init__(self, api_helper):
        self.api_helper = api_helper

        # Path to the configuration file
        file_path = os.path.abspath("configuration.txt")

        # Read configuration
        config = APIHelper.read_config_from_file(file_path)
        if not config:
            print("Error: No valid configuration found in 'configuration.txt'.")
            raise ValueError("Configuration file is missing or invalid.")

        # Extract and validate the project name
        raw_project_name = config.get("PROJECT_NAME", "").strip()  # Default to empty string if not found
        raw_project_lead_email = config.get("PROJECT_LEAD_EMAIL", "").strip()

        # Explicit checks for invalid or empty project name or lead email
        if not raw_project_name or raw_project_name in ["''", '""']:
            print("Error: PROJECT_NAME is missing, empty, or invalid in the configuration file.")
            raise ValueError("PROJECT_NAME is invalid or empty.")

        if not raw_project_lead_email:
            print("Error: PROJECT_LEAD_EMAIL is missing or empty in the configuration file.")
            raise ValueError("PROJECT_LEAD_EMAIL is missing or empty.")

        # Clean up the project name
        self.project_name = raw_project_name.strip("'\"")
        self.project_lead_email = raw_project_lead_email.strip("'\"")

        print("Loaded configuration:", config)

        # Instantiate the key generator
        generator = ProjectKeyGenerator()

        # Generate a key for the new project
        self.new_key = generator.generate_key(self.project_name)
        print(f"Generated project key: {self.new_key}")

        # Initialize API instances
        self.user_search_api = UserSearchAPI(api_helper)
        self.workflow_scheme_api = WorkflowSchemeAPI(api_helper)
        self.permission_scheme_api = PermissionSchemeAPI(api_helper)
        self.add_customized_fields = ModifyScreenFields(api_helper)

    def create_project(self):
        try:
            # Call the search_user_by_email method to get the leadAccountId
            account_id = self.user_search_api.search_user_by_email()
            if not account_id:
                print(f"Error: Failed to retrieve account ID for {self.project_lead_email}.")
                return None

            print(f"Account ID for {self.project_lead_email}: {account_id}")

            # Get the payload with the retrieved account ID
            payload = self.get_payload(account_id, self.new_key, self.project_name)

            # Make the POST request to create the project
            endpoint = "project"
            response = self.api_helper.post(endpoint, json=payload)
            print("Response when creating project:", response)

            # If project creation was successful, update workflow scheme
            if response:
                project_id = response.get("id")  # Assuming response contains the 'id' of the created project
                self.workflow_scheme_api.update_workflow_scheme(project_id)

                project_key = response.get("key")
                # Get permission scheme for the project
                permission_scheme = self.permission_scheme_api.get_permission_scheme(project_key)
                if permission_scheme:
                    permission_scheme_id = permission_scheme.get("id")  # Extract the permission scheme ID
                    # Now update the permission scheme
                    self.permission_scheme_api.update_permission_scheme(project_key, permission_scheme_id)

                # After the project creation, update the configuration file with the generated project key
                config_file_path = os.path.abspath("configuration.txt")
                APIHelper.update_project_key_in_config(config_file_path, project_key)
                print(f"Project key {project_key} updated in the configuration file.")

                # add new fields to new project created
                self.add_customized_fields.apply_fields_to_new_project(project_key) ## should be tested first
            else:
                print("Failed to create project.")
                return None
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
            raise  # Re-raise the exception to handle it elsewhere if needed
        
        return response

    @staticmethod
    def get_payload(account_id, key, name):
        return {
            "key": key,  # Should set into external file but apply algorithm before storing
            "name": name,  # Should read from external file
            "projectTypeKey": "software",
            "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-kanban-template",
            "leadAccountId": str(account_id),  # Use the retrieved account ID
            "assigneeType": "PROJECT_LEAD"
        }
