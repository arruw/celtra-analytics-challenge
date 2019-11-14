# Celtra Analytics Engineer Challenge
Challenge description is located [here](https://gist.github.com/anzebrvar/6b137727997c1e20bcd67c92666cbafd).

# Requirements
- docker (tested on v19.03.3)
- docker-compose (tested on v1.24.1)
- make (tested on GNU Make v4.2.1)

# Commands
**Start local environment**

Start Apache Spark cluster, MySQL database (with fake data), dummy data generator (over TCP socket), Apache Spark driver program & REST API

*NOTE:* First run can take some time because dependant Docker images are pulled and build.
```bash
$ make up
```

**Scale Apache Spark worker nodes**

```bash
$ make scale n=3 
```

**Stop local environment**

```bash
$ make down
``` 

*OPTIONAL:* Data is still persisted in the named volume, remove it with following command:
```bash
$ make clean
``` 

# Solution Architecture
![arhitecture.drawop.png](resources/arhitecture.drawio.png)

# Demo APIs

**Question 1: How many impressions were trafficked each day for each campaign?**

```bash
curl http://localhost:8080/api/campaigns/timeseries
```

**Question 2: How many impressions, interactions and swipes were trafficked for each ad in the specific campaign?**

```bash
curl http://localhost:8080/api/campaigns/1/ads
```

**Question 3: How many unique users and impressions were trafficked each day for each ad in the last 7 days?**

```bash
curl http://localhost:8080/api/campaigns/ads/lastweek
```

# TODOs
- Split driver program into smaller functions
- Move hard coded configurations to environment variables
- Add unit tests