import discord
from unidecode import unidecode
import argparse
import random
import time
import networkx as nx

# Little functions for clustering

def guild_with_most_common_friends(friend_list, guild_list, guild_graph):
    guilds_scores = dict()
    for guild in guild_list:
        score = 0
        for friend in friend_list:
            if guild in guild_graph[friend]:
                score += 1
        guilds_scores[guild] = score

    if len(guilds_scores) == 0:
        return "sansserveur"

    # Returns guild with maximum score
    return max(guilds_scores, key=guilds_scores.get)

def get_guild_clusters(friend_graph, guild_graph):
    clusters = dict()

    for (friend, guild_list) in guild_graph.items():
        friend_list = friend_graph[friend]
        cluster = guild_with_most_common_friends(friend_list, guild_list, guild_graph)
        if cluster in clusters:
            clusters[cluster].append(friend)
        else:
            clusters[cluster] = [friend]

    return clusters

# Louvain clustering 
def get_louvain_clusters(friends_graph):
    G = nx.Graph(friends_graph)
    return nx.community.louvain_communities(G)

# Graph drawing

def random_color():
    return '#' + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])

def graph_from_dict(graph_dict, clusters={}, filename="graph.dot"):
    graph_items = graph_dict.items()

    with open(filename, "w", encoding="utf-8") as file:
        file.write("strict graph{\n")
        for (k, v) in graph_items:
            file.write(f"{k}[label=\"{k}\n{len(v)}\"]\n")
        file.write("\n")

        for (k, v) in graph_items:
            for name in v:
                file.write(f"{k} -- {name}\n")

        for (i, members) in enumerate(clusters):
            file.write(f"subgraph cluster_{i}" + "{\n")
            for member in members:
                file.write(f"{member};\n")

            #file.write(f"label=\"{cluster_name}\"\n")
            file.write(f"color=\"{random_color()}\"\n")
            file.write("}\n")

        file.write("}\n")


# Parse graphs from 'friends.txt' file
def parse_graph(filename):
    graph = dict()
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.readlines():
            friend, mutual_friends_string = line.split(':')
            mutual_friends = mutual_friends_string.strip().split(',')[:-1]
            graph[friend] = [s.strip() for s in mutual_friends]

    return graph

# Discord part

client = discord.Client()

def normalize(s):
    special_chars = "&~#{}()[]-'\"@^$£€<>*+=|_,;:!?./% "
    s = unidecode(s) # Remove accents, emojis...
    for c in special_chars:
        s = s.replace(c, '')
    return s.lower()


@client.event
async def on_ready():
    global filename
    friends_graph = dict()

    print(f'We have logged in as {client.user}')

    with open(filename, "w", encoding="utf-8") as file:

        # Treating each separate friend
        n_friends = len(client.friends)
        for (i, friend) in enumerate(client.friends):
            mutual_friends_list = []
            #mutual_guilds_list = []
            friend_name = normalize(friend.user.name)

            print(f"Treating {friend_name} ({i+1}/{n_friends})")
            file.write(f"{friend_name}: ")

            time.sleep(abs(random.gauss(1, 1/3)))
            profile = await client.fetch_user_profile(friend.user.id)

            # Fetch mutual friends
            #file.write("- Mutual friends:\n\t")
            for mutual_friend in profile.mutual_friends:
                mutual_friend_name = normalize(mutual_friend.name)
                mutual_friends_list.append(mutual_friend_name)
                file.write(f"{mutual_friend_name},")
            friends_graph[friend_name] = mutual_friends_list
            file.write("\n")

            # Fetch mutual guilds
            # file.write("- Mutual guilds:\n\t")
            # for mutual_guild in profile.mutual_guilds:
            #     mutual_guild_name = normalize(mutual_guild.guild.name)
            #     mutual_guilds_list.append(mutual_guild_name)
            #     file.write(f"{mutual_guild_name}, ")
            # guilds_graph[friend_name] = mutual_guilds_list
            # file.write("\n")

    print("Finished!")
    print("Unlogging...")
    await client.close()

def generate_graphs(filename):
    friends_graph = parse_graph(filename)

    graph_from_dict(friends_graph, clusters={}, filename="friends_graph_no_clusters.dot")

    clusters = get_louvain_clusters(friends_graph)
    graph_from_dict(friends_graph, clusters=clusters, filename="friends_graph_clusters.dot")
    print("Graphs generated!")




if __name__ == "__main__":
    # argparse the user token
    parser = argparse.ArgumentParser(description='Get the friends graph of a discord user.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--token', metavar='token', type=str,
                        help='The discord user token')
    group.add_argument('-i', '--input', metavar='input', type=str,
                       help = "The input file name")

    parser.add_argument('--output', metavar='output', type=str,
                        help='The output file name', default="friends.txt")

    args = parser.parse_args()
    if args.output:
        filename = args.output
    else:
        filename = "friends.txt"

    if args.token:
        client.run(args.token)

    else:
        filename = args.input

    generate_graphs(filename)
