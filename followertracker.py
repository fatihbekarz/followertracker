import instaloader
import time
import requests

# Define the IFTTT webhook address
address = "https://maker.ifttt.com/trigger/XXX/with/key/XXX"

# Define the Instagram account to retrieve follower list from
username = "XXX"

# Define the Instagram account credentials
user = "XXX"
password = "XXX"

# Create an Instaloader instance and log in to Instagram
L = instaloader.Instaloader()
L2 = instaloader.Instaloader()
L.context.log("Logging in to Instagram...")
L.login(user, password)
L2.login(user, password)


# Retrieve the follower list and write old followers to file
profile = instaloader.Profile.from_username(L.context, username)
followers = set(profile.get_followers())
file = open("oldfollowers.txt", "w")
for follower in followers:
    print(follower.username)
    oldfollower = follower.username
    file.write(follower.username + "\n")
file.close()

# Wait 5 seconds
time.sleep(5)

# Retrieve the follower list and write new followers to file
profile2 = instaloader.Profile.from_username(L2.context, username)
followers2 = set(profile2.get_followers())
file = open("newfollowers.txt", "w")
for follower in followers2:
    print(follower.username)
    newfollower = follower.username
    file.write(follower.username + "\n")
file.close()

# Compare old and new followers and write missing followers to file
with open("oldfollowers.txt", "r") as file:
    old_followers = set(file.read().splitlines())

with open("newfollowers.txt", "r") as file:
    new_followers = set(file.read().splitlines())

missing_follower = old_followers - new_followers

with open("missing_followers.txt", "w") as file:
    for follower in missing_follower:
        file.write(follower + "\n")

# Send missing followers to IFTTT
response = requests.post(address, data={"value1": missing_follower})