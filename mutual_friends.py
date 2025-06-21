from pyspark import SparkContext

def parse_line(line):
    # Ligne : "1 Sidi 2,3,4"
    parts = line.strip().split()
    if len(parts) < 3:
        return None
    user_id = parts[0]
    user_name = parts[1]
    friends = parts[2].split(',') if parts[2] else []
    return (user_id, (user_name, friends))

def make_pairs(user_id, friends_list):
    pairs = []
    for friend_id in friends_list:
        pair_key = tuple(sorted([user_id, friend_id]))
        pairs.append((pair_key, set(friends_list)))
    return pairs

if __name__ == "__main__":
    sc = SparkContext(appName="MutualFriendsWithIDs")

    input_file = "hdfs://localhost:9000/social_network.txt"
    output_dir = "hdfs://localhost:9000/output_mutual_friends"

    # Charger et parser les lignes
    lines = sc.textFile(input_file)
    parsed = lines.map(parse_line).filter(lambda x: x is not None)

    # Récupérer le dictionnaire id -> nom
    id_name_rdd = parsed.map(lambda x: (x[0], x[1][0]))
    id_name_dict = id_name_rdd.collectAsMap()

    # Préparer les paires
    user_friends_rdd = parsed.map(lambda x: (x[0], x[1][1]))  # (id, [amis])
    pairs = user_friends_rdd.flatMap(lambda x: make_pairs(x[0], x[1]))

    # Calculer les amis communs
    mutual_friends = pairs.reduceByKey(lambda a, b: a.intersection(b))

    # Format final : ID<Nom>ID<Nom>ami_communs_ids
    def format_result(pair, friends_set):
        id1, id2 = pair
        name1 = id_name_dict.get(id1, "Unknown")
        name2 = id_name_dict.get(id2, "Unknown")
        mutual_ids = sorted(friends_set)
        return f"{id1}<{name1}>{id2}<{name2}>{','.join(mutual_ids) if mutual_ids else 'Aucun'}"

    result = mutual_friends.map(lambda x: format_result(x[0], x[1]))

    # Sauvegarde dans HDFS
    result.saveAsTextFile(output_dir)

    # Affichage console
    for line in result.collect():
        print(line)

    sc.stop()

