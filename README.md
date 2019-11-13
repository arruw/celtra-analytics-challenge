# Celtra Analytics Engineer Challenge
Challenge description is located [here](https://gist.github.com/anzebrvar/6b137727997c1e20bcd67c92666cbafd).

# Requirements
- docker (tested on v19.03.3)
- docker-compose (tested on v1.24.1)
- make (tested on GNU Make v4.2.1)

# Commands
- `$ make up`             - Start Spark cluster, MySQL db (with fake data), Dummy data generator (over TCP socket), Spark driver program & REST API
- `$ make scale n=3`      - Scale Spark worker nodes
- `$ make down`           - Stop all dependencies 

# Solution overview
![arhitecture.drawop.png](resources/arhitecture.drawio.png)

# TODOs
- Implement REST APIs
- Add unit tests
- Move hard coded configurations to environment variables