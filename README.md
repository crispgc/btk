# btk

New Test

## Run dockers

docker run -dit --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management; docker run --name testneo4j -p7474:7474 -p7687:7687 -d -v $HOME/neo4j/data:/data -v $HOME/neo4j/logs:/logs -v $HOME/neo4j/import:/var/lib/neo4j/import -v $HOME/neo4j/plugins:/plugins --env NEO4J_AUTH=neo4j/test neo4j:latest
