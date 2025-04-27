# Serializability in Database Systems: A Comprehensive Guide

## Introduction to Serializability

When multiple users interact with a database simultaneously, their transactions can interfere with each other in ways that compromise data integrity. Serializability provides a framework for ensuring that concurrent transactions produce results as if they had executed one after another in some sequential order.

Think of serializability as a traffic control system for database operations. Just as traffic lights prevent collisions at intersections, serializability prevents data inconsistencies when multiple transactions run concurrently.

## The Problem of Concurrent Transactions

Imagine two bank transactions occurring simultaneously:

- Transaction A: Transfer $100 from Account 1 to Account 2
- Transaction B: Calculate the total balance of Account 1 and Account 2

Without proper isolation, Transaction B might read Account 1 after the deduction but before Account 2 is credited, temporarily "losing" $100 from the system. This illustrates why we need mechanisms to control how transactions interact.

## Isolation Levels and Their Trade-offs

Database systems offer various isolation levels that provide different guarantees about transaction behavior:

1. **Read Uncommitted** (weakest): Allows transactions to see uncommitted changes from other transactions
2. **Read Committed**: Prevents dirty reads but allows non-repeatable reads and phantom reads
3. **Repeatable Read**: Prevents dirty and non-repeatable reads but allows phantom reads
4. **Serializable**: Prevents all anomalies but may reduce concurrency
5. **Strict Serializability** (strongest): Combines serializability with real-time ordering constraints

Each stronger level prevents more anomalies but typically comes with performance costs. The appropriate level depends on your application's requirements for data consistency versus throughput.

## Understanding Serializability

Serializability guarantees that the outcome of concurrent transactions matches some possible serial execution of those same transactions. In other words, even though transactions might overlap in time, the final database state will be as if they had run one after another in some order.

### Types of Serializability

#### 1. View Serializability

Two schedules are view equivalent when:

- They start with the same initial database state
- Every read operation in each schedule observes the same data values
- They produce the same final database state

View serializability is theoretically elegant but computationally expensive to verify—it's an NP-complete problem. This makes it impractical for database systems to implement directly.

#### 2. Conflict Serializability

Two schedules are conflict equivalent when all conflicting operations are ordered the same way in both schedules.

Operations conflict when they:

- Belong to different transactions
- Operate on the same data item
- At least one operation is a write

There are three types of conflicts:

- **Read-Write (RW) Conflict**: One transaction reads a value, another writes to it
- **Write-Read (WR) Conflict**: One transaction writes a value, another reads it
- **Write-Write (WW) Conflict**: Two transactions write to the same value

Conflict serializability is more restrictive than view serializability, but it's much easier to verify and implement, making it the practical choice for most database systems.

## Determining Conflict Serializability

### The Precedence Graph Method

A precedence graph provides an elegant way to check if a schedule is conflict serializable:

1. Create a node for each transaction
2. Draw a directed edge from Ti to Tj if an operation in Ti conflicts with and precedes an operation in Tj
3. Check for cycles in the graph

If the graph contains no cycles, the schedule is conflict serializable. If there are cycles, it's not.

### Example 1: Non-Serializable Schedule

Consider this schedule with transactions T1, T2, and T3:

```
T1: R(A) → W(A)
T2: R(A) → W(A) → R(B) → W(B)
T3: R(B) → W(B)
```

The corresponding precedence graph would contain a cycle between T1 and T2, indicating this schedule is not conflict serializable. This means there's no equivalent serial execution order.

### Example 2: Serializable Schedule

Now consider this modified schedule:

```
T1: R(A) → W(A)
T2: R(B) → W(B)
T3: R(A) → W(A) → R(B) → W(B)
```

The precedence graph for this schedule is acyclic, showing edges from T1 to T3 and from T3 to T2. This means the schedule is conflict serializable, equivalent to the serial order T1 → T3 → T2.

## Methods for Achieving Serializability

Databases use two primary approaches to ensure serializability:

### 1. Pessimistic Concurrency Control

This approach assumes conflicts are likely and prevents them before they occur. The most common implementation is through locking:

- **Shared locks** for reads (multiple transactions can hold shared locks simultaneously)
- **Exclusive locks** for writes (only one transaction can hold an exclusive lock)
- **Two-Phase Locking (2PL)**: Transactions acquire all necessary locks before releasing any locks

Pessimistic control provides strong guarantees but can reduce concurrency due to lock contention.

#### When Pessimistic Control Excels

- High-contention workloads with many transactions accessing the same data
- Short transactions where lock overhead is minimal compared to transaction duration
- Critical systems where transaction failures are costly
- Write-intensive applications where conflicts are common

### 2. Optimistic Concurrency Control

This approach assumes conflicts are rare and allows transactions to proceed without blocking. Instead, it validates transactions before they commit:

1. **Read Phase**: Transaction reads data and keeps track of read/write sets
2. **Validation Phase**: System checks if committing would violate serializability
3. **Write Phase**: If validation passes, changes are made permanent; otherwise, the transaction is aborted and restarted

Optimistic control allows higher concurrency but can waste work if many transactions abort.

#### When Optimistic Control Excels

- Read-heavy workloads with few writes
- Low-contention scenarios where different transactions access different data
- Long-running read transactions that would hold locks for extended periods
- Systems where the cost of occasionally restarting transactions is acceptable

## Making the Right Choice

The decision between pessimistic and optimistic concurrency control depends on your workload characteristics:

- **Data access patterns**: How likely are transactions to access the same data?
- **Read/write ratio**: More reads favor optimistic approaches
- **Transaction duration**: Longer transactions may benefit from optimistic approaches
- **Contention level**: Higher contention favors pessimistic approaches
- **Cost of retries**: If aborts are expensive, pessimistic approaches may be better

Many modern databases use hybrid approaches or allow configuration based on workload needs.

## Beyond Basic Serializability

Advanced database systems offer additional techniques:

- **Multiversion Concurrency Control (MVCC)**: Maintains multiple versions of data to allow reads without blocking writes
- **Predicate Locking**: Locks based on data properties rather than specific items
- **Timestamp Ordering**: Uses timestamps to order transactions
- **Snapshot Isolation**: Provides each transaction a consistent snapshot of the database

These techniques offer various trade-offs between consistency guarantees and performance.

## Conclusion

Serializability provides the theoretical foundation for transaction isolation in database systems. By understanding both the theory and practical implementations, database designers can choose appropriate concurrency control mechanisms for their specific requirements, balancing the need for data consistency with performance considerations.

Whether through pessimistic locking or optimistic validation, the goal remains the same: to make concurrent transactions behave as if they executed in some serial order, preserving the integrity and consistency of the database.

# Pessimistic Concurrency Control (PCC)

In this lesson, we will explore the 2-phase locking, a pessimistic concurrency control protocol.

## 2-Phase locking (2PL)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#2-Phase-locking-2PL)

**2-phase locking (2PL)** is a pessimistic concurrency control protocol that uses locks to prevent concurrent transactions from interfering. These locks indicate that a record is being used by a transaction, so that other transactions can determine whether it is safe to use it or not.

### Types of locks[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Types-of-locks)

There are two basic types of locks used in this protocol:

- **Write (exclusive) locks**: These locks are acquired when a record is going to be written (inserted/updated/deleted).
- **Read (shared) locks**: These locks are acquired when a record is read.

## Interaction between write (exclusive) locks and read (shared) locks[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Interaction-between-write-exclusive-locks-and-read-shared-locks)

- A _read lock_ does not block a _read_ from another transaction. This is why it is also called _shared_ because multiple read locks can be acquired at the same time.
- A _read lock_ blocks a _write_ from another transaction. The other transaction will have to wait until the read operation is completed and the read lock is released. Then, it will have to acquire a write lock and perform the write operation.
- A _write_ lock blocks both _reads_ and _writes_ from other transactions, which is also the reason it’s also called _exclusive_. The other transactions will have to wait for the write operation to complete and the write lock to be released; then, they will attempt to acquire the proper lock and proceed.

> If a lock blocks another lock, they are called **incompatible**. Otherwise, they are called **compatible**.

As a result, the relationships described above can be visualized in a compatibility matrix, as shown in the following illustration.

Each type of conflict is represented by an incompatible entry in the above matrix.

## Phases where transactions acquire or release locks[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Phases-where-transactions-acquire-or-release-locks)

In 2-phase locking protocol, transactions acquire and release locks in two distinct phases:

### Expanding phase[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Expanding-phase)

In this phase, a transaction is allowed to only _acquire_ locks, but not _release_ any locks.

### Shrinking phase[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Shrinking-phase)

In this phase, a transaction is allowed to only _release_ locks, but not _acquire_ any locks.

The following illustration shows these phases.
> It’s been implied so far that locks are held per record. However, it’s important to note that if the associated database supports operations based on predicates, there must also be a way to lock ranges of records (predicate locking), e.g., all the customers of ages between 23 and 29. This is to prevent anomalies like phantom reads.

As proven by Franking, this protocol only allows serializable executions to happen.

> A schedule generated by two-phase locking will be conflict equivalent to a serial schedule, where transactions are serialized in the order they completed their expanding phase.

There are some slight variations of the protocol that can provide some additional properties, such as:

- Strict two-phase locking (S2PL)
- Strong strict two-phase locking (SS2PL)

## Deadlocks[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Deadlocks)

The locking mechanism introduces the risk for deadlocks, where two transactions might wait on each other for the release of a lock, thus never making progress. 

### Ways to deal with deadlocks[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Ways-to-deal-with-deadlocks)

In general, there are two ways to deal with these deadlocks.

#### Prevention[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Prevention)

This method prevents the deadlocks from being formed in the first place.

For example, this can be done if transactions know all the locks they need in advance and acquire them in an ordered way. This is typically done by the application since many databases support interactive transactions and are thus unaware of all the data a transaction will access.

#### Detection[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/5680722571689984#Detection)

This method detects deadlocks that occur, and breaks them. For example, this can be achieved by keeping track of which transaction a transaction waits on, using this information to detect cycles that represent deadlocks, and then forcing one of these transactions to abort. This is typically done by the database, without the application having to do anything extra.

# Optimistic Concurrency Control (OCC)

In this lesson, we will describe a way through which the optimistic concurrency control method controls concurrent operations.

**Optimistic concurrency control** **(OCC)** is a concurrency control method that was first proposed in 1981 by Kung et al., where transactions can access data items without acquiring locks on them.

In this method, transactions execute in the following three phases:

- Begin
- Read & modify
- Validate & commit/rollback

## Begin phase[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/6092480030965760#Begin-phase)

In this phase, transactions are assigned a unique timestamp that marks the beginning of the transaction referred to as the **start timestamp**.

## Read & modify phase[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/6092480030965760#Read--modify-phase)

During this phase, transactions execute their read and write operations _tentatively_. This means that when an item is modified, a copy of the item is written to a temporary, local storage location. A read operation first checks for a copy of the item in this location and returns this one, if it exists. Otherwise, it performs a regular read operation from the database.

## Validate & commit/rollback phase[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/6092480030965760#Validate--commitrollback-phase)

The transaction enters this phase when all operations have been executed.

During this phase, the transaction checks whether there are other transactions that have modified the data this transaction has accessed, and have started after this transaction’s start time. If there are, then the transaction is aborted and restarted from the beginning, acquiring a new timestamp. Otherwise, the transaction can be committed.
The commit of a transaction is performed by copying all the values from write operations, from the local storage to the common database storage that other transactions access.

> It’s important to note that the validation checks and the associated commit operation need to be performed in a single atomic action as part of a critical section.

This requires some form of locking mechanism, so there are various optimizations of this approach that attempt to reduce the duration of this phase to improve performance.

### Ways to implement validation logic[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/6092480030965760#Ways-to-implement-validation-logic)

There are two ways to implement validation logic.

#### Version checking[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/6092480030965760#Version-checking)

One way is via version checking, where every data item is marked with a version number. Every time a transaction accesses an item, it can keep track of the version number it had at that point.

During the validation phase, the transaction can check if the version number is the same. If it is, it would mean that no other transaction has accessed the item in the meanwhile.

#### Timestamp ordering[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/4830481670209536/6092480030965760#Timestamp-ordering)

Another way is by using timestamps assigned to transactions, a technique also known as timestamp ordering, since the timestamp indicates the order in which a transaction must occur relative to the other transaction.

In this approach, each transaction keeps track of the items that are accessed by read or write operations, known as the **read set** and the **write set**.

During validation, a transaction performs the following inside a critical section:

It records a fresh timestamp, called the **finish timestamp**, and iterates over all the transactions that have been assigned a timestamp between the transaction’s start and finish timestamp.

> These are essentially all transactions that have started after the running transaction and have already been committed.

For each of those transactions, the running transaction checks if their _write set_ intersects with its own _read set_. If that’s true for any of these transactions, it means that the transaction essentially reads a value “from the future.”

As a result, the transaction is invalid and must be aborted and restarted from the beginning with a fresh timestamp. Otherwise, the transaction is committed, and is assigned the next timestamp.

# Achieving Snapshot Isolation Through Multi-Version Concurrency Control

## Understanding the Foundation of MVCC

**Multi-version Concurrency Control (MVCC)** transforms how database systems manage data updates. Rather than overwriting existing records with new values, MVCC creates and maintains multiple versions of each data item. This fundamental approach allows read operations to access specific versions of data, including historical versions that might otherwise be lost in traditional single-version systems.

The brilliance of this approach lies in its ability to let readers and writers operate without blocking each other. While traditional systems often force readers to wait for writers to finish (or vice versa), MVCC enables concurrent operations by separating what different transactions can see.

Reed introduced this revolutionary concept in his 1978 dissertation, with significant refinements later developed by Silberschatz and Stearns. Though MVCC can theoretically work with both optimistic and pessimistic concurrency control schemes, it particularly shines when paired with optimistic methods. This combination leverages the multiple versions to maximize concurrency among transactions.

## The Connection Between MVCC and Snapshot Isolation

Snapshot Isolation (SI) represents one of the most important practical applications of MVCC. Under snapshot isolation, each transaction operates on a consistent database snapshot from the moment it begins. This means all read operations within a transaction see the database as it existed at a single point in time—regardless of changes made by other concurrent transactions.

For a transaction to successfully commit under snapshot isolation, no other transaction can have modified the same data since the original snapshot was taken. This elegantly prevents many concurrency problems while maintaining high performance.

## How MVCC Implements Snapshot Isolation: The Mechanism

The implementation relies on three critical elements:

1. **Transaction Timestamping**: Each transaction receives a unique timestamp when it begins, establishing its place in the temporal sequence of operations.
2. **Version Tracking**: Every data item version is tagged with the timestamp of the transaction that created it, forming a historical timeline of changes.
3. **Environmental Awareness**: At startup, each transaction records:
    - The timestamp of the most recently committed transaction (let's call this Ts)
    - A list of all transactions that have started but not yet committed

### Reading Data Under MVCC

When a transaction reads a data item, it doesn't simply grab the latest version. Instead, it applies these precise rules:

The transaction retrieves the version with the highest timestamp that:

- Is older than or equal to Ts (the highest committed timestamp when this transaction began)
- Was NOT created by any transaction that was active (uncommitted) when this transaction started

This approach ensures the transaction only sees data from transactions that had already committed when it began—creating a consistent snapshot and preventing dirty reads.

There's one important exception: if the current transaction has already modified the item being read, it will see its own changes rather than an older version.

This reading strategy effectively prevents fuzzy (non-repeatable) reads because all read operations consistently access the same snapshot throughout the transaction's lifetime.

### Writing Data Under MVCC

Write operations involve crucial validation checks that determine whether the transaction can proceed:

Before writing a data item, the transaction examines existing versions to see if either:

- Any version has a timestamp higher than this transaction's timestamp (meaning a "future" transaction has already written this data)
- Any version has a lower timestamp but was created by a transaction that was still active when this transaction began

If either condition is true, the transaction must abort and can restart with a new, later timestamp.

The first condition prevents temporal inconsistencies—we can't have a transaction with timestamp Tj committing before a transaction with timestamp Ti if Ti < Tj.

The second condition specifically targets the lost update anomaly, where two transactions might otherwise unknowingly overwrite each other's changes.

## Limitations: The Write Skew Problem

Despite its sophistication, MVCC with snapshot isolation cannot prevent all concurrency anomalies. The most notable weakness is its vulnerability to **write skew anomalies**.

A write skew occurs when two transactions:

1. Read overlapping data sets
2. Make disjoint updates based on what they read
3. Both commit successfully
4. Together violate a constraint that would have been maintained had the transactions executed serially

This happens because snapshot isolation focuses on direct write-write conflicts but doesn't detect all logical conflicts that might arise from concurrent operations.

For example, two doctors might simultaneously schedule themselves on-call, each checking that at least one other doctor remains available (based on their snapshot), but together leaving no doctors available—violating a hospital requirement that at least one doctor must always be on-call.

Understanding these limitations helps database designers implement additional safeguards when full serializability is required.

# Understanding Serializable Snapshot Isolation: A Comprehensive Guide

## Introduction to the Problem

Database systems must handle multiple transactions occurring simultaneously while maintaining data consistency. This is no small challenge. Traditional approaches often force a difficult choice between performance and correctness. Many systems use _Snapshot Isolation_ (SI) as a compromise, which prevents many but not all concurrency anomalies.

The critical issue with basic Snapshot Isolation is that it cannot prevent certain subtle anomalies like _write skew_, which can lead to database inconsistencies in real-world applications. This limitation has motivated the development of more sophisticated approaches.

## The Evolution to Serializable Snapshot Isolation

Significant research by Ports and others has led to an enhanced algorithm called _Serializable Snapshot Isolation_ (SSI). This breakthrough maintains the performance benefits of standard snapshot isolation while providing full serializability guarantees—the gold standard for transaction correctness.

### The Theoretical Foundation of SSI

SSI is built upon a crucial observation about non-serializable executions under snapshot isolation: they all share a specific pattern in their transaction dependency graphs. Understanding this pattern is key to preventing non-serializable behavior.

**The Fundamental Insight:**

In any non-serializable execution under snapshot isolation, the precedence graph will contain at least one dangerous structure: two read-write dependency edges (rw-dependencies) that form consecutive edges in a cycle, involving transactions that were active concurrently.

To visualize this concept, consider three concurrent transactions: T₀, T₁, and Tₙ (where Tₙ could be any other transaction, like T₃). The dangerous structure occurs when:

1. T₀ has a read-write dependency with T₁
2. Tₙ has a read-write dependency with T₀
3. These dependencies create a cycle in the transaction graph

_What exactly is a read-write dependency?_ It occurs when transaction T₀ reads a version of an item x, and transaction T₁ later writes a newer version of that same item x. This creates a dependency where T₀'s behavior is based on data that T₁ later modified.

## How SSI Works in Practice

Rather than allowing problematic transactions to complete and then trying to repair inconsistencies, SSI takes a preventive approach. It actively monitors for dangerous structures and intervenes before they can cause problems.

### The Detection and Prevention Mechanism

The algorithm works through these key steps:

1. **Track Dependencies**: For each active transaction, the system maintains records of incoming and outgoing read-write dependencies.
2. **Identify Dangerous Patterns**: A transaction that has both incoming and outgoing read-write dependencies represents a potential dangerous structure.
3. **Take Preventive Action**: When such a pattern is detected, the system aborts one of the involved transactions and reschedules it to execute later, effectively breaking the potential cycle.

### Implementation Details

The SSI algorithm uses a surprisingly simple mechanism to track these complex interactions:

1. **Boolean Flags**: Each transaction T maintains just two boolean flags:
    - T.inConflict: Indicates whether T has incoming rw-dependencies
    - T.outConflict: Indicates whether T has outgoing rw-dependencies
2. **Detection Methods**:
    - **Read-time Detection**: When a transaction T reads an item, it checks if another transaction U has written a newer version of that item. If so, this creates a rw-dependency, and the system sets T.outConflict and U.inConflict to true.
    - **Write-time Detection**: For cases where the write happens after the read, the system uses SIREAD locks. These are special "soft locks" that don't block operations but serve as signals. When a transaction reads an item, it places a SIREAD lock on it. Later, when another transaction attempts to write to that item, it can see the SIREAD lock and update the appropriate conflict flags.

It's important to note that unlike traditional locks, SIREAD locks don't prevent other transactions from proceeding. This preserves the optimistic nature of snapshot isolation while adding the ability to detect and prevent dangerous structures.

### Potential Overprotection

One interesting aspect of SSI is that it may sometimes abort transactions that wouldn't actually cause serialization problems. This happens because the algorithm doesn't try to determine if there's a complete cycle in the dependency graph—it simply identifies potential dangerous structures and takes action.

This conservative approach is a deliberate design choice that avoids the computational expense of tracking and analyzing complete dependency cycles. In practice, the rate of unnecessary aborts is acceptable in most workloads, and the guarantee of serializable behavior justifies this trade-off.

## A Concrete Example: Preventing Write Skew

Let's see how SSI prevents the classic write skew anomaly that basic snapshot isolation cannot handle:

1. Transaction T₁ reads items I₁ and I₂, placing SIREAD locks on both.
2. Concurrently, transaction T₂ also reads I₁ and I₂, placing its own SIREAD locks.
3. T₁ updates I₂, which doesn't conflict with any writes from T₂.
4. T₂ attempts to update I₁. At this point, the system detects that T₁ has a SIREAD lock on I₁.
5. The system recognizes a potential dangerous structure and updates the conflict flags:
    - T₂.inConflict is set to true (because T₂ is writing to an item that T₁ has read)
    - If T₂ already has its outConflict flag set to true (from a previous operation), then T₂ is aborted to prevent a potential cycle.

By aborting one of the transactions, SSI prevents the write skew anomaly and ensures serializable behavior.

## The Practical Impact of SSI

The implementation of SSI in commercial database systems has been a significant advancement in concurrency control. It allows databases to provide the strongest consistency guarantees while maintaining much of the performance advantage of snapshot isolation.

Modern systems that implement SSI can handle complex transactional workloads with confidence that the results will be consistent and correct, regardless of the interleaving of concurrent operations. This removes a significant burden from application developers, who no longer need to design around the limitations of weaker isolation levels.

## Conclusion

Serializable Snapshot Isolation represents an elegant solution to a challenging problem in database systems. By identifying and preventing specific patterns of transaction dependencies that lead to non-serializable behavior, SSI achieves the best of both worlds: the performance benefits of optimistic concurrency control with the correctness guarantees of full serializability.

This approach demonstrates how theoretical insights about transaction behaviors can lead to practical improvements in database system design, benefiting applications that require both high performance and strong consistency guarantees.