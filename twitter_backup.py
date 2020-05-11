import twitter
import json

with open("twitter.json") as json_data:
    data = json.load(json_data)
    print(data)
    api = twitter.Api(
        consumer_key=data["consumer_key"],
        consumer_secret=data["consumer_secret"],
        access_token_key=data["access_token_key"],
        access_token_secret=data["access_token_secret"],
    )

print(api.VerifyCredentials())

users = api.GetFriends()
print([{u.name, "@{}".format(u.screen_name)} for u in users])
