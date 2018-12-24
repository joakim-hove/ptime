import sys
import json
import os
import requests
import datetime
from ptime.util import parse_input_date, parse_input_time
from argparse import ArgumentParser


class BaseClient(object):
    PTIME_URL = os.environ["PTIME_URL"]
    PTIME_USER = os.environ["PTIME_USER"]


    def __init__(self, options):
        self.project = options.project
        self.activity = options.activity

        self.data = {"user" : self.PTIME_USER }
        if options.start:
            self.data["start"] = options.start

        if options.end:
            self.data["end"] = options.end



    def url(self):
        raise NotImplementedError("Each inherited class must implement the url() method")


class GetClient(BaseClient):

    def __init__(self, options):
        super().__init__(options)

    def run(self):
        try:
            r = requests.get(self.url(), params=self.data)
        except:
            sys.exit("GET request to server:{} failed".format(self.PTIME_URL))

        status_code = r.status_code
        return (status_code, r.text)




class PostClient(BaseClient):

    def __init__(self, options):
        super().__init__(options)

    def run(self):
        try:
            r = requests.post(self.url(), json=self.data)
        except:
            sys.exit("POST request to server:{} failed".format(self.PTIME_URL))

        status_code = r.status_code
        return (status_code, r.text)



class StartClient(PostClient):

    def __init__(self, options):
        super().__init__(options)
        if self.project is None:
            raise ValueError("Missing project id")

        if self.activity:
            self.data["activity"] = options.activity

    def url(self):
        return "{0}/api/task/start/{1}/".format(self.PTIME_URL, self.project_id)



class StopClient(PostClient):

    def __init__(self, options):
        super().__init__(options)

    def url(self):
        return "{0}/api/task/stop/".format(self.PTIME_URL)


class StatusClient(GetClient):

    def __init__(self, options):
        super().__init__(options)

    def url(self):
        return "{0}/api/status/".format(self.PTIME_URL)


class TaskListClient(GetClient):

    def __init__(self, options):
        super().__init__(options)
        if self.project:
            self.data["project"] = self.project


    def url(self):
        return "{0}/api/get/".format(self.PTIME_URL)


class SummaryClient(TaskListClient):
    pass



class PTimeClient(object):
    commands = {"start" : StartClient,
                "stop" : StopClient,
                "status" : StatusClient,
                "list" : TaskListClient,
                "sum" : SummaryClient }

    def __init__(self, cmd, options):
        self.client = self.commands[cmd](options)

    def data(self):
        return self.client.data

    def run(self):
        return self.client.run()



def parse_args(cmd, argv):
    argparser = ArgumentParser()
    if cmd in ["start", "stop"]:
        argparser.add_argument("project", nargs="?")
        argparser.add_argument("activity", nargs="?")
        argparser.add_argument("--start", type=parse_input_time, dest="start", help="Start time")
        argparser.add_argument("--end", type=parse_input_time, dest="end", help="End time")

    if cmd in ["list", "sum"]:
        argparser.add_argument("project", nargs="?")
        argparser.add_argument("--start", type=parse_input_date, dest="start", help="Start time")
        argparser.add_argument("--end", type=parse_input_date, dest="end", help="End time")

    return argparser.parse_args( argv )


def run(argv):
    cmd = argv[0]
    if not cmd in PTimeClient.commands:
        sys.exit("No such subcommand:{}".format(cmd))

    options = parse_args(cmd, argv[1:])


    client = PTimeClient(cmd, options)
    status_code, text = client.run()
    if status_code in [200,201]:
        return json.loads(text)
    else:
        sys.exit("{} ({})".format(text, status_code))
