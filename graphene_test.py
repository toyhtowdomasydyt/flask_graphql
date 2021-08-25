from graphene import ObjectType, String, Schema, List
from requests import get

_BASE_URL = "https://api.github.com/users"


def get_user_data(username):
    user_info = get(f"{_BASE_URL}/{username}").json()
    repos_info = get(f"{_BASE_URL}/{username}/repos").json()

    name = user_info["name"]
    repos = sorted([repo["name"] for repo in repos_info])

    return {
        "name": name,
        "repos": repos
    }


class Query(ObjectType):
    user_name = String()
    user_repos = List(String)

    def resolve_user_name(self, info):
        return get_user_data(info.context.get("username"))["name"]

    def resolve_user_repos(self, info):
        return get_user_data(info.context.get("username"))["repos"]


schema = Schema(query=Query)

query_string = '{ userName }'
result = schema.execute(query_string, context={"username": "serwios"})
print(result.data["userName"])

