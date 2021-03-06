import requests


def _project_url(project: str):
    return '/projects/{0}'.format(project.replace('/', '%2F'))


class GitlabAPI:
    def __init__(self, api_url=None, token=None, verbose=False):
        self.api_url = (api_url or 'https://gitlab.com/api/v4/').rstrip('/') + '/{0}'
        self.token = token
        self.verbose = verbose

    def _get(self, path: str, **kwargs):
        headers = None
        if self.token:
            headers = {'PRIVATE-TOKEN': self.token}
        url = self.api_url.format(path.lstrip('/'))
        params = {k: v for k, v in kwargs.items() if v is not None}
        r = requests.get(url, headers=headers, params=params)
        if self.verbose:
            print('URL: {0}'.format(r.request.url))
        return r.json()

    def commits(self, project: str, ref_name=None, since=None, until=None):
        return self._get(_project_url(project) + '/repository/commits', ref_name=ref_name, since=since, until=until)

    def tags(self, project: str, name: str=None):
        url = _project_url(project) + '/repository/tags'
        if name:
            url = url + '/' + name
        return self._get(url)

    def pipelines(self, project: str, pipeline_id=None, ref=None):
        url = _project_url(project) + '/pipelines'
        if pipeline_id:
            url = url + '/' + pipeline_id
        return self._get(url, ref=ref)

    def pipeline_jobs(self, project: str, pipeline_id: str):
        url = _project_url(project) + '/pipelines/{0}/jobs'.format(pipeline_id)
        return self._get(url)
