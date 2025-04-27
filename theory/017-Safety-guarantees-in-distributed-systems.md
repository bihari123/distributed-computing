## Introduction to Safety Guarantees

When designing distributed systems, we need certain safety guarantees to ensure that our system behaves correctly despite the challenges inherent to distributed computing. These guarantees serve as the foundation for reliable distributed systems, providing assurances about how the system will behave even under problematic conditions.

## The Three Core Safety Properties

The three fundamental safety properties that distributed systems strive to provide are:

1. **Atomicity**
2. **Consistency**
3. **Isolation**

Let's examine each of these properties in detail and understand why they're challenging to achieve in distributed environments.

## Understanding Atomicity

**Atomicity** ensures that a transaction is treated as a single, indivisible unit of work. This means that either all operations within a transaction complete successfully, or none of them do. There is no middle ground – we never end up in a state where only some of the operations have been applied.

The term "atomicity" comes from the Greek word "atomos," meaning indivisible. Just as an atom was once thought to be the smallest indivisible unit of matter, an atomic transaction is indivisible from the perspective of the system.

For example, when transferring money between two bank accounts, either both the debit and credit operations must succeed, or neither should be applied. We should never end up in a state where money has been debited from one account but not credited to the other.

### Why Atomicity is Challenging in Distributed Systems

Achieving atomicity in distributed systems is difficult primarily because of **partial failures**. In a distributed system, components can fail independently of one another. For instance:

- A server might crash in the middle of processing a transaction
- A network partition might separate parts of the system
- Some nodes might experience timeouts while others continue operating

When such partial failures occur, the system must have mechanisms to either complete the transaction fully or roll back all its effects as if it never started. This often requires complex protocols like two-phase commit or distributed sagas.

## Understanding Consistency

In the context described (related to the CAP theorem), **consistency** refers to the guarantee that all nodes in a distributed system see the same data at the same time. When a write operation completes, all subsequent read operations should reflect that write, regardless of which node handles the read.

Consistency ensures that the distributed system behaves as if it were a single, coherent system, even though it's composed of multiple nodes that might be geographically dispersed.

### Why Consistency is Challenging in Distributed Systems

Consistency is difficult to achieve because of **network asynchrony**. This refers to the fact that nodes in a distributed system:

- May have different internal clocks that drift apart
- Experience varying network delays when communicating
- Cannot perfectly synchronize their understanding of "now"

Due to these timing discrepancies, nodes might receive updates in different orders, leading to inconsistent views of the system state. For example, if Node A receives an update before Node B, then for some period, clients interacting with Node A will see different data than clients interacting with Node B.

Addressing these challenges often requires consensus protocols like Paxos or Raft, or eventual consistency models that provide weaker but more attainable guarantees.

## Understanding Isolation

**Isolation** ensures that concurrent transactions do not interfere with each other. Even when multiple transactions are executing simultaneously, the system behaves as if transactions are executed one after another (serially).

Proper isolation prevents problems like dirty reads (reading uncommitted data), non-repeatable reads (getting different results when reading the same data multiple times within a transaction), and phantom reads (where a transaction re-executes a query and finds newly added records).

### Why Isolation is Challenging in Distributed Systems

Isolation is challenging because distributed systems are inherently **concurrent**. Multiple operations can occur simultaneously across different nodes, making it difficult to coordinate their effects.

When multiple processes attempt to access and modify shared data concurrently (like two pens trying to write on the same resource), several issues can arise:

- Race conditions, where the outcome depends on the timing of operations
- Lost updates, where one change might overwrite another
- Inconsistent reads, where a transaction sees partial effects of other transactions

Systems typically address these challenges using concurrency control mechanisms like locking, multi-version concurrency control (MVCC), or optimistic concurrency control.

## The Interconnection Between Safety Properties and System Challenges

It's important to recognize how each safety property directly addresses one of the fundamental challenges of distributed systems:

1. **Atomicity** addresses the challenge of partial failures
2. **Consistency** addresses the challenge of network asynchrony
3. **Isolation** addresses the challenge of concurrency

Understanding these relationships helps system designers focus on the right techniques and protocols when building robust distributed systems.

## Looking Ahead

The next two lessons will delve deeper into these safety guarantees, exploring the specific techniques, algorithms, and trade-offs involved in achieving them. These concepts are not merely theoretical but have profound practical implications for building reliable distributed applications.

By mastering these safety properties, you'll gain the foundational knowledge needed to design distributed systems that can withstand the challenges of partial failures, network asynchrony, and concurrency.