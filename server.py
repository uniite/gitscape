import git
import json
from flask import Flask, session, redirect, url_for, escape, request
from functools import wraps

import controllers.git
import settings


app = Flask(__name__)


def view(func):
    """
    Turns functions into "views" for GitScape by doing a few things:
     - Name the route after the function name (ie. def foo -> /foo)
     - Pass in the session as the first argument
     - Pass in the current repo and request parameters as keyword arguments
     - Convert the function's output into JSON
    """
    @wraps(func)
    def _route():
        repo = git.Repo(session.get("repo_path") or repo_list[0])
        return json.dumps(func(session, repo=repo, **(request.args)))
    return app.route("/%s" % func.__name__)(_route)


@app.route("/")
def index():
    """ Our main client-side page. """
    return open("static/index.html").read()

@view
def repos(session, repo=None):
    return json.dumps(repo_list)


view(controllers.git.branches)
view(controllers.git.branch_diff)



if __name__ == "__main__":
    global repo_list
    repo_list = [x.strip() for x in
                  open(settings.config_path("repos.lst"), "r").read().splitlines()
                  if x.strip()]
    app.debug = True
    app.run()
