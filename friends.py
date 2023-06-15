import discord
from unidecode import unidecode
import argparse

client = discord.Client()

def graph_from_dict(graph_dict):
    filename = "graph.dot"
    graph_items = graph_dict.items()

    with open(filename, "w", encoding="utf-8") as file:
        file.write("strict graph{\n")
        for (k, v) in graph_items:
            file.write(f"{k}[label=\"{k}\n{len(v)}\"]\n")
        file.write("\n")

        for (k, v) in graph_items:
            for name in v:
                file.write(f"{k} -- {name}\n")
        file.write("}\n")

def normalize(s):
    special_chars = "&~#{}()[]-'\"@^$£€<>*+=|_,;:!?./%"
    s = unidecode(s) # Remove accents, emojis...
    for c in special_chars:
        s = s.replace(c, '')
    return s


@client.event
async def on_ready():
    global filename
    friends_graph = dict()
    

    print(f'We have logged in as {client.user}')

    with open(filename, "w", encoding="utf-8") as file:

        # Treating each separate friend
        for friend in client.friends:
            mutual_friends_list = []
            friend_name = normalize(friend.user.name)

            print(f"Treating {friend_name}")
            file.write(f"{friend_name}: ")

            profile = await client.fetch_user_profile(friend.user.id)
            for mutual_friend in profile.mutual_friends:
                mutual_friend_name = normalize(mutual_friend.name)
                mutual_friends_list.append(mutual_friend_name)
                file.write(f"{mutual_friend_name}, ")
            friends_graph[friend_name] = mutual_friends_list
            file.write("\n")

    print("Finished!")
    graph_from_dict(friends_graph)


if __name__ == "__main__":
    # argparse the user token
    parser = argparse.ArgumentParser(description='Get the friends graph of a discord user.')
    parser.add_argument('token', metavar='token', type=str, help='The discord user token')
    parser.add_argument('--output', metavar='output', type=str, help='The output file name', default="friends.txt")

    args = parser.parse_args()
    if args.output:
        filename = args.output
    else:
        filename = "friends.txt"
    client.run(args.token)


