class PermissionSchemeAPI:
    def __init__(self, api_helper):
        self.api_helper = api_helper

    def get_permission_scheme(self, project_id):
        # Fetch the permission scheme for the project
        endpoint = f"/project/{project_id}/permissionscheme"
           
        response = self.api_helper.get(endpoint)
        if response:
            print(f"Permission Scheme retrieved: {response}")
            return response
        else:
            print(f"Failed to retrieve permission scheme for project {project_id}.")
            return None

    def update_permission_scheme(self, project_key, permission_scheme_id):
        # Update the permission scheme for the project
        endpoint = f"/project/{project_key}/permissionscheme"
      
        data = {
            "id": permission_scheme_id
        }
        
        response = self.api_helper.put(endpoint, json=data)
        if response:
            print(f"Permission Scheme successfully updated for project {project_key}.")
        else:
            print(f"Failed to update permission scheme for project {project_key}.")
