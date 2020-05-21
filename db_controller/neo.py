from neo4j import GraphDatabase


def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend)" +
                         " WHERE a.name = {name}"
                         " RETURN friend.name" +
                         " ORDER BY friend.name"):
        print(record["friend.name"])