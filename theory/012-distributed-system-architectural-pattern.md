## Replicated Load-Balanced Services
### Stateless services
In the state less service, a node doesn't need additional data pre-populated to serve a request. When the request comes in a stateless service, it checks the request, fetch some data from the database , respond with the data and forgets about it. It doesn't take into account any pre-populated data, possibly from any previous request. The service does not store any state in it. In a stateless service, the nodes do not have any state-related context. As the user base grows, we just put more nodes. There is a load balancer before them obviously.
### Session-tracked service
In some cases, the stateless services are not always enough. Suppose that you are having a grocery app. You keep adding the items in your bucket. Now each time a new item is added, the request has to go to the same node which has the session data. In session-tracked services, all the users' requests go to a specific node where some states of the user's session are cached. The session tracked services look almost the same as stateless services, except that sessions are stateful for the users on a specific node. In case the node crashes, the cached state data is gone. The user will have to reconnect to the application and send new requests.Note that user session tracking is not always implemented by caching states in service nodes. Some systems offload the session data onto high-performance key-value databases, such as DynamoDB. As a result, any node can serve any request from a user during the same session. Also, if a machine crashes, there is no state loss.

This was replicated load balanced services. The gist of the idea is that each node will have the whole application hosted in it. As a result, each node can serve _any_ request coming from _any_ client.

## Sharded Services Pattern
When we use sharded services, we have shards instead of multiple replicas of the system. Each shard serves a portion of the requests from the users.

The difference between replicated load-balanced services and sharded services is that in sharded services, each node can only serve a _subset_ of requests, not all of them. In replicated load-balanced services, each node can serve any request coming to the system.

Suppose we are developing instagram, we have three apis:  /photos, /videos and /thumbnail. We have distributed the load of /photos  to node 1 , the load of /videos to node2 and the load of /thumbnail to node3. Now we can also have replicas of these nodes in case the load on a particular api increases so much that it can't be handles by a single node. We might have to deploy another load balancer to that cluster of nodes, resulting in a multi-load balancer deployement

## Lambda Architecture
Lambda architecture provides both realtime and batch processing. There are three layers to it: 1. Speed layer 2. Batch processing layer and 3.  Serving layer. The Speed layer processes the real time stream data . The Batch processing layer have a master copy of the database and it processes the data periodically. Last the serving layer, it combines the  results from the batch and the speed layer to respond to the queries. The details about the layers are as follows:
### Lambda Architecture Layers

#### 1. Batch Layer

The batch layer is responsible for processing large volumes of historical data.

Key characteristics:
- Handles immutable, append-only sets of raw data
- Precomputes batch views (results) from the master dataset
- Typically runs on a distributed system like Hadoop

Functions:
- Stores the master copy of the dataset
- Recomputes results periodically (e.g., daily or hourly)
- Generates batch views for querying

Technologies often used:
- Hadoop Distributed File System (HDFS) for storage
- Apache Hadoop MapReduce or Apache Spark for processing
- Apache Hive or Apache Pig for querying

Advantages:
- High accuracy and completeness of results
- Ability to reprocess data if errors are found
- Scalability to handle very large datasets

Challenges:
- High latency due to periodic processing
- Requires significant computational resources

#### 2. Speed Layer

The speed layer processes data in real-time as it arrives.

Key characteristics:
- Handles recent data only
- Compensates for the high latency of the batch layer
- Uses incremental algorithms to update real-time views

Functions:
- Processes streams of incoming data
- Creates and updates real-time views
- Provides low-latency, approximate results

Technologies often used:
- Apache Kafka or Apache Pulsar for data ingestion
- Apache Flink, Apache Storm, or Apache Spark Streaming for stream processing
- Apache Cassandra or Redis for storing real-time views

Advantages:
- Low latency for real-time data
- Provides up-to-date results
- Can handle high-velocity data streams

Challenges:
- Limited to recent data
- May produce less accurate or incomplete results
- More complex to implement and maintain

#### 3. Serving Layer

The serving layer combines results from the batch and speed layers to respond to queries.

Key characteristics:
- Indexes batch views for fast reads
- Merges batch and real-time views
- Provides a unified interface for querying data

Functions:
- Loads and serves batch views
- Combines batch views with real-time views
- Responds to ad-hoc queries from applications

Technologies often used:
- ElasticSearch or Apache Druid for indexing and serving batch views
- Custom middleware to merge batch and real-time results
- RESTful APIs or GraphQL for query interfaces

Advantages:
- Provides a unified view of data
- Supports low-latency random reads
- Can serve complex queries efficiently

Challenges:
- Needs to handle the complexity of merging different views
- Requires careful design to ensure consistency between batch and real-time data
- May need to manage multiple versions of batch views during updates

The serving layer acts as the bridge between the processed data and the end-users or applications, providing a seamless interface to query both historical and real-time data.
#### Pros of lambda architecture 

- The speed layer provides fast data processing, which is a must in many systems.
    
    - But note that it cannot guarantee 100% correctness. It is challenging to ensure once delivery of events is at scale in a message queue. The speed layer cannot guarantee 100% accuracy as there could be duplicate or late events in the system. That is why we also have a batch layer in the system.
- The batch layer is slow, but it provides 100% correctness in the result.
    
- If there is some bug or some failure in the system, the batch layer can smoothly backfill and provide correct data.
    

#### Cons of lambda architecture 

- The lambda architecture is complicated. It can be difficult to manage for small teams.
    
- As we can see, both the speed and the batch layer are almost doing the same thing. It means the business logic gets duplicated in both layers. It is inconvenient for the maintainability of the system.
    
- There are three distinct components in this architecture. More components mean more work for the engineers working on the system. As a result, engineering time is consumed more in this pattern.