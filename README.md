# kafka-docker-cluster
 
 A kafka cluster using docker, base on images provided by Confluent inc.
 * `confluentinc/cp-zookeeper:6.0.0`
 * `confluentinc/cp-kafka:6.0.0`

# Cluster Details:
the cluster is composed of:
* One Zookeeper instance:
* Three Kafka brokers:
  * broker 1: available at `localhost:9091`
  * broker 2: available at `localhost:9092`
  * broker 3: available at `localhost:9093`

# How to use it:

1. Clone the repository to your local machine:
`git clone https://github.com/mhamedLmarbouh/kafka-docker-cluster.git`

2. navigate to the folder:
`cd kafka-docker-cluster`

3. Run the cluster:
`docker-compose -f docker-compose.yaml up`

4. Test everything is up and running correctly:
`python -m unittest test`
you should see an output that looks like:
```
Ran 1 test in 2.735s
OK
```
**Congrats the cluster is up and working correctly. 
Now you can use it for whatever you want**
# After you are done:
**NOTE: the following commands should be run from the kafka-docker-cluster directory**
* to stop the cluster use `docker-compose stop`
* to stop and remove the cluster use `docker-compose down -v`