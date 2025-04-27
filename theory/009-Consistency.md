Whenever the data is being replicated from the leader to the follower, there is a lag as the data has to travel over the network and each follower has to process the write-request on their side. This lag is known as **replication lag**.
There are two levels of data consistency: the disk caching level and database level. In the context of distributed system, we will only discuss consistency on the database level.
### Consistency models
If a system is strongly consistent, then all the nodes have the exact copy of data when the read request is fired. In these systems, when the write request arrives, the followers start processing that on their own and until the follower are on the consistent state, they don't process the read request. In such scenarios, the followers can choose to keep the request waiting until it reaches the consistent state or it might also give an error telling the user to try again after some time.  Although it ensures strong consistency, the availability hurts.
### Eventual consistency
In this type of consistency, the node doesn't wait to be in the consistent state to process read request. Instead, it  just gives the data that is available at the moment and let itself be consistent eventually.
## Which consistency model should you choose?[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/4856372201259008#Which-consistency-model-should-you-choose)

Strong consistency for the services which need to have correct data. Like financial systems.
Eventual consistency where you need high availability.

## Tunable Consistency
Databases like apache cassandra have largely popularized this consistency model. 
some of the most important terms from tunable consistency are as follows:
- **R**: Read consistency level. the minimum replicas of the node that must to the read request with the latest data they have.
- **W**: Write consistency. How many replicas nodes should acknowledge that the request has been processed on their side.
- ***RF***: The replication factor. This is the number of nodes the partition will be replicated to.
- **Quorum**: The number of majority nodes derived from the replication factor.![[Quorum.png]]
At the heart of the tunable consistency is the ***coordinator node***. It aggregates the responses from replicas defined by read/write consistency level and checks if the consistency requirements are met. If there is a conflict, then it reconciles the data using various strategies.
For example, if there is a read request then it first determines which replica nodes are responsible for the requested data and the wait for the response from the appropriate number of replicas ( ONE: read from one replica, QUORUM: read from majority of replicas or ALL: read from all replicas). Then it reconciles the data, if required:
- Last-write-wins (based on timestamps)
- Vector clocks for more complex version resolution
- Application-specific merge functions
At last, it prepares the response after the consistency level is satisfied and then send the response to the client.
#### Tuning consistency
- Strong consistency: we set `R+W >RF` . Assume that RF is 3. So, the data is replicated into 3 nodes - n<sub>0</sub> , n<sub>1</sub> and n<sub>2</sub> . So Quorum is 2. If R=2 and W=2 then the write for a key is acknowledged by n<sub>0</sub> and n<sub>1</sub> , and the read is responded from n<sub>1</sub> and n<sub>2</sub> . So, there is node n<sub>1</sub> that will have the latest update.  Now we can set RR and WW in a way that either read is optimized, or write is optimized, or both are balanced. For instance:

	- Setting both the values as QUORUM gives a balanced performance.
	- Setting R=1 and W=RF makes read-requests fast but write-requests slow.
	- Similarly, R=RF and W=1 gives us a fast write performance but a slow read performance.
- Eventual Consistency: `R+W <= RF`.Given the formula above, we can set RR and WW loosely. For example, R=1,W=1R=1,W=1. This gives us no guarantee that we can always get the latest update after a write. But since RF=3RF=3, eventually, all nodes will be in sync.
# Understanding Quorum Systems in Distributed Computing

## Introduction to Quorum Systems

A quorum system represents one of the fundamental concepts in distributed computing, providing a mathematical framework for managing consistency and availability in systems where data is replicated across multiple nodes. The word "quorum" comes from Latin, originally referring to the minimum number of members required to conduct business in an assembly. In distributed systems, this concept has been adapted to ensure reliable operation even when some nodes fail or become unreachable.

## The Basic Principle

At its core, a quorum system divides the set of replicas into overlapping subsets. For any operation to proceed, it must receive acknowledgment from at least one such subset—a quorum. The critical insight is that these subsets are designed to always intersect, ensuring that operations can detect the most recent updates.

Consider a system with N replicas. We define:

- A write quorum (W): the minimum number of replicas that must acknowledge a write operation
- A read quorum (R): the minimum number of replicas that must respond to a read operation

For consistency to be maintained, we require: W + R > N

This inequality guarantees that any read operation will overlap with any previous write operation in at least one replica, ensuring that the read can access the most up-to-date data.

## A Concrete Example

Let's imagine a distributed database with 5 replicas (servers) storing the same data. If we set W=3 and R=3:

- Any write must be confirmed by at least 3 servers
- Any read must gather responses from at least 3 servers

Since 3+3=6, which is greater than our total of 5 servers, the quorum constraint (W+R>N) is satisfied. This means that among the 3 servers involved in a read, at least one must have participated in the most recent write.

What if we chose W=2 and R=3 instead? Then W+R=5, which equals N but doesn't exceed it. This doesn't guarantee an overlap—we could have a situation where a write is confirmed by servers 1 and 2, while a subsequent read retrieves data from servers 3, 4, and 5, missing the updated data entirely.

## Trade-offs in Quorum Systems

Quorum systems allow us to make deliberate trade-offs between different system properties:

1. **Read vs. Write Performance**: If we set W=1 and R=5, writes become very fast (needing acknowledgment from just one replica) while reads become slower and more robust (requiring responses from all replicas). Conversely, W=5 and R=1 optimizes for fast reads at the expense of slower writes.
    
2. **Consistency vs. Availability**: Stronger consistency requirements (larger quorums) reduce the system's ability to operate during network partitions, while smaller quorums improve availability but may compromise consistency.
    
3. **Fault Tolerance**: The system can tolerate up to (N-W) replica failures for writes and (N-R) failures for reads. Setting appropriate quorum sizes helps balance these concerns.
    

## Beyond Simple Majority Quorums

While the simplest approach uses uniform quorums (where any subset of a given size constitutes a quorum), more sophisticated quorum schemes exist:

### Weighted Voting

In weighted voting systems, each replica receives a "vote weight." A quorum is achieved when the sum of votes exceeds a threshold. This allows us to give more importance to more reliable or powerful nodes.

### Grid Quorums

Replicas are arranged in a logical grid. A quorum consists of a full row plus a representative from each other row, or a similar pattern. This reduces the quorum size while maintaining the intersection property.

### Hierarchical Quorums

Replicas are organized in a tree structure, with quorums defined recursively. For instance, a quorum might require a majority of replicas at each level of the hierarchy.

## Practical Applications

Quorum systems appear in many real-world distributed systems:

1. **Distributed Databases**: Systems like Cassandra and DynamoDB use quorum-based approaches to balance consistency and availability.
    
2. **Consensus Protocols**: Algorithms like Paxos and Raft implicitly implement quorum systems to reach agreement.
    
3. **Distributed File Systems**: Systems like Google's GFS and Hadoop's HDFS use quorum techniques for replication.
    
4. **Blockchain Systems**: Many blockchain implementations rely on quorum-like mechanisms where a majority of nodes must agree on the validity of transactions.
    

## Quorum Systems and the CAP Theorem

The CAP theorem states that a distributed system cannot simultaneously provide all three of:

- Consistency: all nodes see the same data at the same time
- Availability: every request receives a response
- Partition tolerance: the system continues to operate despite network failures

Quorum systems allow us to precisely tune where a system falls in this trade-off space. By adjusting W and R, we can favor consistency over availability or vice versa, depending on application requirements.

## Conclusion

Quorum systems represent a powerful abstraction for managing replicated data. They provide a mathematical foundation for reasoning about consistency and availability in distributed systems, allowing system designers to make explicit trade-offs based on application requirements. Whether prioritizing read performance, write performance, or fault tolerance, the quorum approach offers a flexible framework that continues to be relevant in modern distributed computing.

Understanding quorums is essential for anyone working with distributed databases, consensus protocols, or any system where data is replicated across multiple nodes. By carefully selecting quorum sizes, system designers can achieve the right balance of consistency, availability, and performance for their specific use cases.