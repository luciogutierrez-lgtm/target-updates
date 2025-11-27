from api.api_client import ApiClient
from api.pagination import PhraseTmsPagination
import config

import time


class TMS:
    def __init__(self, base_url="https://cloud.memsource.com/web"):
        self._base_url = base_url
        self._api_client = ApiClient()
        self.login()
        self._pagination = PhraseTmsPagination(self._api_client)

    def combine_url_with_query_params(self, url, params):
        if params:
            query_params = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{url}?{query_params}"
        else:
            return url


    def set_token(self, authorization_header):
        self._api_client.set_token(authorization_header)

    def who_am_i(self):
        url = f"{self._base_url}/api2/v1/auth/whoAmI"
        return self._api_client.get_request(url)

    def login(self):
        payload = {"userName": config.USERNAME,
                   "password": config.PASSWORD}
        url = f"{self._base_url}/api2/v3/auth/login"
        token = self._api_client.post_request(url, payload=payload)["token"]
        self._api_client.set_token({"Authorization": f"ApiToken {token}"})

    def list_users(self, params=None):
        url = f"{self._base_url}/api2/v1/users?role=PROJECT_MANAGER"
        return self._pagination.get_all_content_on_all_pages(url)

    def get_user(self, user_uid):
        url = f"{self._base_url}/api2/v3/users/{user_uid}"
        return self._api_client.get_request(url)

    def edit_user(self, user):
        url = f"{self._base_url}/api2/v3/users/{user['uid']}"
        return self._api_client.put_request(url, user)

    def get_project(self, project_uid):
        url = f"{self._base_url}/api2/v1/projects/{project_uid}"
        print(url)
        return self._api_client.get_request(url)

    def _check_pending_requests(self):
        return self._api_client.get_request(f"{self._base_url}/api2/v1/async")

    def async_check(self, number=0):
        pending_requests = self._check_pending_requests()
        if pending_requests["totalElements"] <= number:
            return True
        else:
            time.sleep(10)
            return self.async_check()

    def create_job(self, project, headers, file):
        url = f"{self._base_url}/api2/v1/projects/{project['uid']}/jobs"
        return self._api_client.post_content(url=url, request_headers=headers, file=file)

    def create_user(self, user):
        url = f"{self._base_url}/api2/v3/users"
        return self._api_client.post_request(url, payload=user)

    def update_target(self, project, file_to_import, headers):
        url = f"{self._base_url}/api2/v1/projects/{project['uid']}/jobs/target"

        return self._api_client.post_content(url=url, request_headers=headers, file=file_to_import)
    
    def list_jobs(self, project, params):
        url = f"{self._base_url}/api2/v1/projects/{project['uid']}/jobs"
        url = self.combine_url_with_query_params(url, params)
        return self._pagination.get_all_content_on_all_pages(url)
    
