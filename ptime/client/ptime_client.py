import sys
import json
import os
import requests

class BaseClient(object):
    PTIME_URL = os.environ["PTIME_URL"]
    PTIME_USER = os.environ["PTIME_USER"]


class GetClient(BaseClient):

    def __init__(self):
        self.get_data = {"user" : self.PTIME_USER }

    def run(self):
        try:
            r = requests.get(self.url(), params=self.get_data)
        except:
            sys.exit("Request to server:{} failed".format(PTIME_URL))

        status_code = r.status_code
        return (status_code, r.text)


    def url(self):
        raise NotImplementedError("Each inherited class must implement the url() method")



class PostClient(BaseClient):

    def __init__(self):
        self.post_data = {"user" : self.PTIME_USER }

    def run(self):
        try:
            r = requests.post(self.url(), json=self.post_data)
        except:
            sys.exit("Request to server:{} failed".format(PTIME_URL))

        status_code = r.status_code
        return (status_code, r.text)


    def url(self):
        raise NotImplementedError("Each inherited class must implement the url() method")



class StartClient(PostClient):

    def __init__(self, argv):
        super().__init__()
        if len(argv) == 0:
            raise ValueError("Missing project argument")

        self.project_id = argv[0]
        if len(argv) >= 2:
            self.post_data["activity"] = argv[1]

    def url(self):
        return "{0}/api/task/start/{1}/".format(PTIME_URL, self.project_id)



class StopClient(PostClient):

    def __init__(self, argv):
        super().__init__()

    def url(self):
        return "{0}/api/task/stop/".format(PTIME_URL)


class StatusClient(GetClient):

    def __init__(self, argv):
        super().__init__()

    def url(self):
        return "{0}/api/status/".format(PTIME_URL)



class PTimeClient(object):
    commands = {"start" : StartClient,
                "stop" : StopClient,
                "status" : StatusClient }

    def __init__(self, argv):
        if len(argv) == 0:
            raise ValueError("Empty argv vector - invalid")

        cmd = argv[0]
        self.client = self.commands[cmd](argv[1:])


    def post_data(self):
        return self.client.post_data

    def get_data(self):
        return self.client.get_data()

    def run(self):
        return self.client.run()


def run(argv):
    client = PTimeClient(argv)
    status_code, text = client.run()
    if status_code in [200,201]:
        return json.loads(text)
    else:
        sys.exit("{} ({})".format(text, status_code))
