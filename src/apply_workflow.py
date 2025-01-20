class WorkflowSchemeAPI:
    def __init__(self, api_helper):
        self.api_helper = api_helper

    def update_workflow_scheme(self, project_id):
        endpoint = "/workflowscheme/project"
        data = {
            "workflowSchemeId": 10383,
            "projectId": project_id,
        }

        try:
            print(f"Updating workflow scheme for project ID: {project_id}")
            response = self.api_helper.put(endpoint, json=data)
            
            if response is None:
                print("No response received from API helper.")
                return

            # Handle 204 or other successful status codes
            if response.status_code == 204:
                print(f"Workflow scheme successfully updated for project: {project_id}")
            else:
                print(f"Unexpected status code: {response.status_code}")
                print(f"Response body: {response.text}")

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
