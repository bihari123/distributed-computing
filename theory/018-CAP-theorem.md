# ACID Transactions

Let's see the ACID properties.

 

**ACID** is a set of properties of traditional database transactions that provide guarantees around the expected behavior of transactions during errors, power failures, etc. More specifically, these properties are the following.

## Atomicity (A)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/4804539597979648#Atomicity-A)

**Atomicity** guarantees that a transaction that comprises multiple operations is treated as a single unit. This means that either _all_ operations of the transaction are executed or _none_ of them are.

This concept of atomicity extends to distributed systems, where the system might need to execute the same operation in multiple nodes of the system in an atomic way. So, the operation is either executed to all the nodes or none.

## Consistency (C)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/4804539597979648#Consistency-C)

**Consistency** guarantees that a transaction only transitions the database from one valid state to another valid state, while maintaining any database invariants. However, these invariants are application-specific and defined by every application accordingly.

For example, consider an application that has a table A with records that refer to records in table B through a [foreign key relationship](https://en.wikipedia.org/wiki/Foreign_key). The database prevents a transaction from deleting a record from table A, unless any records in table B referenced from this record are already deleted.

> Note that this is not the concept of consistency we refer to in the context of distributed systems.

## Isolation (I)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/4804539597979648#Isolation-I)

**Isolation** guarantees that even though transactions might run concurrently and have data dependencies, the result is as if one of them was executed at a time and there was no interference between them. This prevents a large number of anomalies.

## Durability (D)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/4804539597979648#Durability-D)

**Durability** guarantees that once a transaction is committed, it remains committed even in the case of failure.

In the context of single-node, centralized systems, this usually means that completed transactions and their effects are recorded in non-volatile storage.

In the context of distributed systems, this means that transactions need to be durably stored in multiple nodes. This way, recovery is possible even in the presence of total failures of a node, alongside its storage facilities.

 
# The CAP Theorem: Understanding Fundamental Trade-offs in Distributed Systems

## Core Principles of the CAP Theorem

The CAP Theorem represents one of the most fundamental principles in distributed systems design. Initially, it stated that a distributed data store cannot simultaneously provide more than two of these three properties:

1. **Consistency** - Every read receives the most recent write or an error. This ensures all nodes see the same data at the same time.
    
2. **Availability** - Every request receives a non-error response, though it might not contain the most recent data.
    
3. **Partition Tolerance** - The system continues to operate despite network failures between nodes.
    

An important clarification is that partition tolerance isn't optional in real-world distributed systems—network partitions will inevitably occur. Therefore, the theorem essentially presents a binary choice: when a network partition occurs, a system must sacrifice either consistency or availability.

## Refined Understanding of CAP

The more accurate statement of the CAP Theorem is: **In the presence of a network partition, a distributed system can be either consistent or available, but not both simultaneously.**

To understand this intuitively, consider a simple two-node distributed system storing a value X. If a network partition separates these nodes and a write occurs on one node followed by a read on the other node, the system faces an impossible dilemma:

- It can reject one operation (breaking availability)
- It can process both operations but return stale data (breaking consistency)
- It cannot maintain both properties because the network partition prevents synchronization

## Distributed System Classifications Under CAP

Based on this understanding, distributed systems are generally classified as:

- **CP systems** - Prioritize consistency over availability during partitions
- **AP systems** - Prioritize availability over consistency during partitions

This classification has guided distributed system design by making explicit the unavoidable trade-offs that engineers must consider.

## The PACELC Extension

The PACELC theorem extends CAP by acknowledging that even during normal operations (without partitions), trade-offs still exist. Its name encodes its principle:

- **P**: In case of network Partition
- **A/C**: choose between Availability and Consistency
- **E**: Else (normal operation)
- **L/C**: choose between Latency and Consistency

This creates four possible system classifications:

1. **AP/EL** - Prioritizes availability during partitions and low latency during normal operations
2. **CP/EL** - Prioritizes consistency during partitions but low latency during normal operations
3. **AP/EC** - Prioritizes availability during partitions and consistency during normal operations
4. **CP/EC** - Prioritizes consistency both during partitions and normal operations

Most real-world systems fall into either AP/EL (favoring performance and availability) or CP/EC (favoring data consistency) categories, reflecting their overall design philosophy.

## Practical Implications

The significance of these theorems lies in their power to guide system design decisions. For instance, a system requiring strong consistency (like a banking application) might adopt a CP/EC approach, accepting higher latency or reduced availability to ensure data correctness. Conversely, a system where immediate access is critical (like a content delivery network) might adopt an AP/EL approach, accepting occasional data inconsistency to maintain responsiveness.

Understanding these inherent trade-offs helps system designers make informed choices aligned with their specific application requirements, rather than pursuing an impossible ideal of perfect consistency, availability, and performance simultaneously.