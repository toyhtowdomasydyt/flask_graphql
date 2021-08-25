from flask import Flask, render_template, request
from graphene import ObjectType, String, Schema, List
from requests import get

app = Flask(__name__)

_BASE_URL = "https://api.github.com/users"


def get_user_name(username):
    return get(f"{_BASE_URL}/{username}").json()["name"]


def get_user_repos(username):
    repos_info = get(f"{_BASE_URL}/{username}/repos").json()

    return sorted([repo["name"] for repo in repos_info])


class Query(ObjectType):
    user_name = String()
    user_repos = List(String)

    def resolve_user_name(self, info):
        return get_user_name(info.context.get("username"))

    def resolve_user_repos(self, info):
        return get_user_repos(info.context.get("username"))


@app.route('/')
def display_home():
    return render_template("index.html", phrase="Hello")


@app.route("/form", methods=["post", "get"])
def display_form():
    schema = Schema(query=Query)

    username = ""

    name = "No name"
    user_repos = "No repos"

    if request.method == "POST":
        username = request.form["username"]

    if username:
        query_string = '{ userName }'
        result = schema.execute(query_string, context={"username": username})
        name = result.data["userName"]

        query_string = '{ userRepos }'
        result = schema.execute(query_string, context={"username": username})
        user_repos = result.data["userRepos"]

    return render_template(
        "form.html",
        name=name,
        repos=user_repos
    )


if __name__ == '__main__':
    app.run()
