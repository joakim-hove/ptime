import sys
import json
import os
import requests


PTIME_URL = os.environ["PTIME_URL"]
PTIME_USER = os.environ["PTIME_USER"]

class GetClient(object):

    def __init__(self):
        pass

    def run(self):
        data = self.get_data()
        data["user"] = PTIME_USER
        try:
            r = requests.get(self.url(), params=data)
        except:
            sys.exit("Request to server:{} failed".format(PTIME_URL))

        status_code = r.status_code
        return (status_code, r.text)


    def get_data(self):
        return {}


    def url(self):
        raise NotImplementedError("Each inherited class must implement the url() method")



class PostClient(object):

    def __init__(self):
        pass

    def run(self):
        data = self.post_data()
        data["user"] = PTIME_USER
        try:
            r = requests.post(self.url(), json=data)
        except:
            sys.exit("Request to server:{} failed".format(PTIME_URL))

        status_code = r.status_code
        return (status_code, r.text)

    def post_data(self):
        return {}

    def url(self):
        raise NotImplementedError("Each inherited class must implement the url() method")



class StartClient(PostClient):

    def __init__(self, argv):
        if len(argv) == 0:
            raise ValueError("Missing project argument")

        self.project_id = argv[0]


    def url(self):
        return "{0}/api/task/start/{1}/".format(PTIME_URL, self.project_id)



class StopClient(PostClient):

    def __init__(self, argv):
        pass

    def url(self):
        return "{0}/api/task/stop/".format(PTIME_URL)


class StatusClient(GetClient):

    def __init__(self, argv):
        pass

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


    def run(self):
        return self.client.run()


def run(argv):
    client = PTimeClient(argv)
    status_code, text = client.run()
    if status_code in [200,201]:
        return json.loads(text)
    else:
        sys.exit("{} ({})".format(text, status_code))
