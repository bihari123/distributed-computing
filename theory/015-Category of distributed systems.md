## Categories of distributed systems 
There are two main categories of distributed system that depends on the nature of the communication:
1. Synchronous systems
2. Asynchronous systems
### Synchronous system
A **synchronous system** is one where each node has an accurate clock, and there is a known upper bound on the message transmission delay and processing time. As a result, the execution is split into rounds. This way, every node sends a message to another node, the messages deliver, and every node computes based on the messages it receives. During this, all nodes run in lock-step.
### Asynchronous system 
An **asynchronous system** is one where there is no fixed upper bound on how long it takes for a node to deliver a message, or how much time elapses between consecutive steps of a node. The system nodes do not have a common notion of time and, thus, run at independent rates.
