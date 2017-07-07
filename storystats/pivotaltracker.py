import json
import requests

class PivotalTracker:
    def __init__(self, url, token, project_id):
        self._url = url
        self._token = token
        self._project_id = project_id
        self._base_url = '{}/projects/{}'.format(self._url, self._project_id)
        self._headers = {'X-TrackerToken': self._token}

    def _make_request(self, api_endpoint):
        return requests.get(api_endpoint, headers=self._headers)

    def _request_and_get_data(self, api_endpoint):
        response = self._make_request(api_endpoint)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        return json.loads(response.text)

    def get_project_bugs(self, filter_accepted=False):
        api_endpoint = '{}/stories?filter=story_type:bug'.format(
            self._base_url
        )
        # investigate why this was not working
        # if filter_accepted:
        #     api_endpoint = '{} current_state:accepted'.format(api_endpoint)

        return self._request_and_get_data(api_endpoint)

    def get_story_comments(self, story_id):
        api_endpoint = '{}/stories/{}/comments'.format(self._base_url, story_id)
        return self._request_and_get_data(api_endpoint)
