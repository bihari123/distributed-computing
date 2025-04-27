### Data Collection
Not all data is same in type and value. We can divide the data into three categories.
1. Personal data: Personal data is sensitive info about a user. Like date of birth, credit card credentials and the places you have been to. If the system is dealing with this type of data, there are a lot of rules, regulations and compliance matters that have to be followed.
2. User interaction data: Modern system also collect user-interaction data in their system as **events**. Things you do on the website are generally logged as events and later processed to generate insights.Note that events do not only mean user interaction. Things happening in your system may also be logged as events and propagated to other parts for storage and processing. For example, if your system blocks a user for some fraudulent activities, that may also be logged as an event.
3. Data storage: Collected data has to be stored somewhere for it to be usable. This is where system owner decide what type of storage they would use and which database to choose from among the numerous options available.
	- If the data you have is transactional (for example money transactions between users), it’s likely you will choose a SQL database like MySQL or PostgreSQL.
	- If your data requires very fast retrieval to support queries from users, key-value stores are a feasible option.
	- If the volume is high and the retrieval speed may be slow, then block storage is a viable option. In block storage, data is stored in files and broken up into multiple 
	- parts if required.
4.  Data processing: The data your system receives may not necessarily be used in its exact form it is received in. In the backend server you will need to process the data by filtering, extending or updating schemas, adding or removing attributes etc. 
5. Insight generation: The last common step in distributed system is gathering insights from data. Whatever data you collect and process, is fed into some part of the system which is responsible for generating useful information and insights for driving business and growth. For instance, some business may want to predict user behavior to choose a proper marketing strategy. If your business is subscription based and users have a certain quota every month, you will need to generate insights from user-interaction to make sure they are capped to the usage limit.
### Data Replication
Replication ensures data is correctly available in every part of the system so that requests distributed in different replica nodes have a consistent response. This directly increases the system’s scalability.If a new row gets added, or a column is updated, or some rows are deleted, we see all these changes reflected in every node. If one or a few nodes do not contain these changes in them, then requests served from these nodes will have outdated information, which basically hurts the reliability of the system altogether. As an owner, you will definitely not want this in your system.
#### Techniques of replication
##### Single-leader replication
Each node storing a copy of the database is called a replica. A database system may have many replicas. With replication, these replica are in sync and they remain consistent over time. In single-leader replication, one of the replicas is called the leader. All writes from clients are handled by the leader. Other replicas are called **followers**. Followers don't handle writes at all. They keep in sync with the leader and server the read requests to the client. 
Many databases, such as MySQL, use a single-leader replication mechanism. This means all writes in MySQL will be done via the leader node, and reads can be served by any node. This is why in many cases MySQL is suitable for read-heavy systems. This is also the reason why MySQL is difficult to scale for a large volume of data.

The drawback of single-leader replication is that if clients are unable to connect to the leader, then the writes cannot proceed.

##### Multi-leader replication
In multi-leader replication, there is more than one leader in the system. The mechanism is pretty much the same as single leader mechanism. There are multiple leaders with their own set of followers.  When the write request arrives, it gets forwarded to the leader node which then writes the data and tells its followers to replicate. It also informs other leaders to proceed.
One common use case of multi-leader replication is a cross-datacenter database system. Some systems are so big that data centers are set up in different geographical locations. In each such location, there can be one leader. Inside a single data center, writes are synced the same way a single-leader system would. After that, multiple leaders sync among themselves across data centers.
##### Leaderless replication
There are some systems that go for leaderless replication. The name suggests the mechanism: there is no leader. Any replica can handle write operation. Upon receiving a write-request, a replica will store it in its local storage and communicate the writes to the other replicas. All the replicas that receive the write will process it on their sides.One example of such a system is DynamoDB by AWS. This is a key-value store with very high performance, and many companies heavily rely on this database.

## Replication Types
##### Synchronous or asynchronous replication
In synchronous replication, a write is successful only when all the followers have successfully processed the write-request (leader waits until all the followers have written the changes). In asynchronous replication, a write is successful as soon as the leader has processed the write-request, after which the followers can process it asynchronously.
Synchronous replication becomes problematic when the follower node crashes before successfully writing the changes. In that case, the leader will keep waiting unless the node is back.
On the other hand, asynchronous replication might lead to follower nodes lagging behind in writes which means they don't have the latest data.
In real world, distributed systems are built using a hybrid approach.  In a hybrid approach, one or a few nodes are made synchronous, whereas other nodes are asynchronous. This means a write-request is successful as soon as a fixed number of followers have processed the write on their sides. Other followers can process it asynchronously.

### How to handle follower outages?
In such a scenario, the follower will have to catch up with the leader when it comes back. Briefly, the process is as follows:

- Each follower has a log in its storage. The log keeps all the data changes from the leader.
    
- When a follower comes back after a temporary outage, it can look up its log and decide from which point the follower needs to begin catching up.
    
- The follower then requests corresponding changes from the leader and recovers from the outage.
### How to handle leader outages?
1. Detect the leader failure: First we have to detect the leader failure. Generally, a **timeout** is used to detect a failure in a node. A timeout is a way to limiting how long a client will wait for a response from a server.To detect a failure, we can use a separate controller node, which sends a simple request to the node periodically. For example for a leader, if a timeout occurs for a request from the controller, the leader is deemed to have failed and the next steps are triggered to do a failover.
2. Promote a follower: The next step is to promote one of the followers to the new leader. If the system uses synchronous replication, any of the follower nodes could be promoted to the new leader. Generally, the most up-to-date follower should be the new leader.
3. Route write-request: Since the leader handles the write-requests, the clients should be able to send these to the new leader. This means all the write-requests coming to the system should now go to the new leader. If the old leader comes back, the system should not treat it as the leader. Generally, after electing the new leader, the load balancer should be made aware of the new leader. Then write requests will be handled accordingly.