# Read and download database

# Create database in Neo4j if it does not exists
from db_controller import neo
neo.GraphDatabase()

driver = neo.GraphDatabase.driver("bolt://localhost:7687", 
        auth=("neo4j", "test"), encrypted=False)

with driver.session() as session:
    session.write_transaction(neo.add_friend, "Arthur", "Guinevere")
    session.write_transaction(neo.add_friend, "Arthur", "Lancelot")
    session.write_transaction(neo.add_friend, "Arthur", "Merlin")
    session.read_transaction(neo.print_friends, "Arthur")

driver.close()

# If exists, continue

# Check if data in Neo4j

# Add data to Neo4j

# 