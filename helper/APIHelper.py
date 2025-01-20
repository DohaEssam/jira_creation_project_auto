import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv()
class APIHelper:
    def __init__(self):
  
        self.base_url = os.getenv("BASE_URL").rstrip("/")
        username = os.getenv("API_USERNAME")
        api_token = os.getenv("API_TOKEN")
        self.headers = self._generate_headers(username, api_token)
        
    @staticmethod
    def _generate_headers(username, api_token):
    
        auth_token = base64.b64encode(f"{username}:{api_token}".encode()).decode()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_token}"
        }

    def get(self, endpoint, params=None):
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GET request failed: {e}")
            return None

    def post(self, endpoint, json=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.post(url, headers=self.headers, json=json)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                # Extract detailed error messages
                error_details = response.json()
                print(f"POST request failed: {error_details}")
            except ValueError:
                # Fallback to plain response text if JSON parsing fails
                print(f"POST request failed with raw response: {response.text}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"POST request failed: {req_err}")
            return None

    def put(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.put(url, json=json, headers=self.headers)
            response.raise_for_status()  # Raise an error for 4xx/5xx status codes
            return response  # Return the full response object
        except requests.exceptions.RequestException as e:
            print(f"PUT request failed: {e}")
            return None


    @staticmethod
    def read_config_from_file(file_path):

        config = {}
        try:
            with open(file_path, "r") as file:
                for line in file:
                    # Skip empty lines or lines starting with a comment (#)
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    # Split the line into key and value
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Only include non-empty values in the config dictionary
                        if value:
                            config[key] = value
                        else:
                            print(f"Warning: Value for '{key}' is empty. Skipping.")
        
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}")
        return config
    

    @staticmethod
    def update_project_key_in_config(file_path, project_key):
        """Updates the PROJECT_KEY in the configuration file."""
        # Read the current configuration
        config = APIHelper.read_config_from_file(file_path)

        # Update the project key in the configuration
        config['PROJECT_KEY'] = project_key  # Add or update the project key entry

        # Write the updated configuration back to the file
        with open(file_path, 'w') as f:
            for key, value in config.items():
                f.write(f"{key}='{value}'\n")    