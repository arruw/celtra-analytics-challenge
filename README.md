# Celtra Analytics Engineer Challenge
Challange description is located [here](https://gist.github.com/anzebrvar/6b137727997c1e20bcd67c92666cbafd).

# Requirements
- docker (tested on v19.03.3)
- docker-compose (tested on v1.24.1)
- make (tested on GNU Make v4.2.1)

# Setup
- `$ make up`             - Start Apache Spark cluster, MySQL database (with fake data) & REST API
- `$ make scale n=3`      - Scale Apache Spark worker nodes
- `$ make agg`            - Run Apache Spark Driver application to calculate aggregations

# Other commands
- `$ make gen`            - Generate few tousond impressions for current day
- `$ make down`           - Stop Apache Spark cluster, MySQL database & REST API