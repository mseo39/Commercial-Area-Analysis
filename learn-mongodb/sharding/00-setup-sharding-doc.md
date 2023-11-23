## Set up Sharding using Docker Containers

### Config servers
Start config servers (3 member replica set)
```
docker-compose -f config-server/docker-compose.yaml up -d
```
Initiate replica set
```
mongo mongodb://220.69.209.126:40001
```
```
rs.initiate(
  {
    _id: "cfgrs",
    configsvr: true,
    members: [
      { _id : 0, host : "220.69.209.126:40001" },
      { _id : 1, host : "220.69.209.126:40002" },
      { _id : 2, host : "220.69.209.126:40003" }
    ]
  }
)

rs.status()
```

### Shard 1 servers
Start shard 1 servers (3 member replicas set)
```
docker-compose -f shard1/docker-compose.yaml up -d
```
Initiate replica set
```
mongo mongodb://220.69.209.126:50001
```
```
rs.initiate(
  {
    _id: "shard1rs",
    members: [
      { _id : 0, host : "220.69.209.126:50001" },
      { _id : 1, host : "220.69.209.126:50002" },
      { _id : 2, host : "220.69.209.126:50003" }
    ]
  }
)

rs.status()
```

### Mongos Router
Start mongos query router
```
docker-compose -f mongos/docker-compose.yaml up -d
```

### Add shard to the cluster
Connect to mongos
```
mongo mongodb://220.69.209.126:60000
```
Add shard
```
mongos> sh.addShard("shard1rs/220.69.209.126:50001,220.69.209.126:50002,220.69.209.126:50003")
mongos> sh.status()
```
## Adding another shard
### Shard 2 servers
Start shard 2 servers (3 member replicas set)
```
docker-compose -f shard2/docker-compose.yaml up -d
```
Initiate replica set
```
mongo mongodb://220.69.209.126:50004
```
```
rs.initiate(
  {
    _id: "shard2rs",
    members: [
      { _id : 0, host : "220.69.209.126:50004" },
      { _id : 1, host : "220.69.209.126:50005" },
      { _id : 2, host : "220.69.209.126:50006" }
    ]
  }
)

rs.status()
```
### Add shard to the cluster
Connect to mongos
```
mongo mongodb://220.69.209.126:60000
```
Add shard
```
mongos> sh.addShard("shard2rs/220.69.209.126:50004,220.69.209.126:50005,220.69.209.126:50006")
mongos> sh.status()
```
