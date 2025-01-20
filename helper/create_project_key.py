#it must not exceed 10 characters
#Project keys must start with an uppercase letter, followed by one or more uppercase alphanumeric characters.
import random
import string
import json
import os

class ProjectKeyGenerator:
    def __init__(self, json_file="keys.json"):
        self.json_file = json_file
        self._ensure_file_exists()

    def generate_key(self, project_name):
        """
        Generate a unique project key based on the project name.
        """
        # Extract the base part of the key from the project name
        base_key = self._derive_key_from_name(project_name)

        # Fetch existing keys from the JSON file
        existing_keys = self._fetch_existing_keys()

        # Generate a unique key with random logic
        new_key = self._generate_unique_key(base_key, existing_keys)

        # Save the new key to the JSON file
        self._save_key(new_key)

        return new_key

    def _derive_key_from_name(self, project_name):
        """
        Extract the first 3 uppercase letters from the project name.
        """
        base_key = ''.join(filter(str.isalpha, project_name.upper()))[:3]
        if len(base_key) < 3:
            raise ValueError("Project name must have at least three alphabetic characters.")
        return base_key

    def _generate_unique_key(self, base_key, existing_keys):
        """
        Generate a unique project key using random 4-digit numbers.
        """
        while True:
            # Generate a random 4-digit number
            random_suffix = f"{random.randint(1000, 9999)}"

            # Combine the base key and random suffix
            new_key = (base_key + random_suffix)[:10]

            # Ensure the key is unique and does not exist in the existing keys
            if new_key not in existing_keys:
                return new_key

    def _fetch_existing_keys(self):
        """
        Fetch existing keys from the JSON file.
        """
        with open(self.json_file, "r") as file:
            return set(json.load(file).get("keys", []))

    def _save_key(self, new_key):
        """
        Save the new key to the JSON file.
        """
        with open(self.json_file, "r") as file:
            data = json.load(file)

        # Append the new key
        data["keys"].append(new_key)

        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=4)

    def _ensure_file_exists(self):
        """
        Ensure the JSON file exists and initialize it if not.
        """
        if not os.path.exists(self.json_file):
            with open(self.json_file, "w") as file:
                json.dump({"keys": []}, file, indent=4)
