If you have multiple nodes in your distributed system, you will need to distribute the load evenly on all the nodes. It is done to avoid the situation where all the work is done by a single node whereas all other nodes are sitting idle. 
![[Pasted image 20241002154211.png]]
In this diagram, when the client tries to connect to your system, it will have to go through the load balancer. The node balancer will have an algorithm to direct the client request to one of the servers. These algorithms are of various types. Two of the most popular algorithms are 1. Round Robin ( we switch through the nodes serial like first node1 then for the next request node2 then for the next request node3) and 2. Weighted routing (we send to the node with least workload at the moment)
Because of the load balancer, it is now easier to control the traffic and distribute the workload.

Now we also need to keep an eye on the nodes that have crashed so that we can avoid sending the requests to those nodes and the user don't see the **server error**. 
![[Pasted image 20241002154947.png]]
As shown in the diagram above, the LB can send a request to all the servers every 30 seconds to ensure whether the node is healthy or not. It can be some `/status` endpoint that the LB can hit and then check the response code. Based on the response, the LB can declare a node as healthy or unhealthy, and take further actions to make sure the system remains highly available. Some of these actions can include:

- Stopping the forwarding of requests to the unhealthy node. Users won’t see a longer response time due to retry and node failures.
- Triggering alerts for the system owners.
- If required, initiating the process of spinning up a new node automatically. This helps to achieve high availability in the system when node failures occur.
- At the same time, LBs can help to scale out the system based on load. If the LB sees more requests than a particular threshold, it can trigger the initiation of more nodes.
- Periodically checking the status of the unhealthy node whether it’s back again. Many times, only the network between the LB and the seemingly faulty node is the issue. Originally, the node can be healthy.
## Can a load balancer be a single point of failure?[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/4925763085402112#Can-a-load-balancer-be-a-single-point-of-failure)

If you have already noticed this, give yourself a pat on the back!

Yes. A single load balancer is actually a single point of failure. If it is down, then essentially the whole system is down.

One simple solution to this is to have two or more load balancers in a cluster node. Then, let the IP addresses of these balancer nodes propagate to DNS servers. When clients try to connect to your backend, they get all the three IPs, and randomly connect to one of them. If one is down, clients can try to connect to the other one.

## Load Balancing Algorithms
There are two types of load balancing algorithms: application layer algorithm and network layer algorithm.
### Application Layer algorithms
In application layer load balancing, the load balancer has the access to the data of the request. It can take decisions based on the request header as well as the request body. 
- Hashing: 
	- A common application-layer algorithm is **hashing**. The LB can hash a set of predefined attributes and generate a hash value. The hash value is then mapped to one of the server nodes. Let’s give a simple example.
	- Assume that the request body from a client contains a `user_ID`. Upon receiving the request, the LB can do the following steps
		1. Hash the `user_ID` using any pre-configured hash function. Say for `user_ID = abc123`, the hash function returns a value `981723123`.
		2. Take the returned value and map it to a server node. This can be done by using the modulo operation `981723123 % 5` which equals `3`. Here, we are taking a modulo by `5` as this is the count of nodes in the system.
		3. Route the request to node `3`.
		![[Pasted image 20241002155533.png]]
- Endpoint Evaluation:
	- In this mechanism, the endpoint of the request is considered and routed accordingly. For example, let's say we have two incoming requests. One hits the endpoint `/v1/app/photos` and the other hits `/v1/app/videos`. In such a setup, you might have two sets of servers for serving photos and videos respectively. The load balancer will evaluate the endpoints and route the request to the respective servers.
	- ![[Pasted image 20241002155713.png]]
### Network Layer Algorithm
In network-layer load balancing, the load balancer does not access the data of the request. It can see the source and destination of the request but not what is there in the request. There are a couple of common algorithms based on the network layer.
#### Random selection[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6505047742742528#Random-selection)

This is a very simple algorithm to send the request to any one of the server nodes randomly. The LB calculates a probability for choosing server nodes and decides accordingly. Sometimes a sophisticated random number generation is used to choose a node.

#### Round robin[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6505047742742528#Round-robin)

In this algorithm, the requests are routed to servers in a round-robin manner. Say you have three servers numbered 11, 22 and 33, and 5 requests.

Upon receiving the first request, it is routed to server 11. The next request will go to server 22. Then the next one to 33. 4th4th and 5th5th request will go to server 11 and 22.

The LB will keep a state of the server and route the request accordingly.
#### Least connection[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6505047742742528#Least-connection)

In this algorithm, LBs keep track of how many persistent connections there are in the server nodes and choose the one with the least number of connections. In systems where persistent connections are common (think of chat application backends), least connection can be a beneficial choice for load balancing.

#### IP hashing[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6505047742742528#IP-hashing)

In this algorithm, the source IP is hashed using a good and fast hash function. Based on the hashed value, the request is routed to a specific server.

#### Least pending requests[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6505047742742528#Least-pending-requests)

In this algorithm, the load balancer monitors the count of the pending requests in a server and routes the incoming request to the server with the least pending requests. This essentially means that the load balancer is evaluating how long a request is taking to be resolved in a server. If requests are taking too long, the server will have more pending requests. As a result, the load balancer will try to optimize requests by sending new incoming requests to the less busy servers.

## Which algorithm should you choose?
- If the system has very short request-response pattern, then round-robin or random both can be suitable algorithm.
- if the system does not have a uniform pattern ( some requests may take longer time to respond to) then the round robin or random algorithm won't be suitable at all. This is because one of the servers could be streched thin with a few requests and these algorithms would continuously add more load on to them. In such systems, the least connection or the least response time algorithms make more sense.

## How to measure the load of the distributed system?
1. Query per second: How many queries can the server process per sec. If you process 10 million requests every day then the query per second is (10 million % 86400 secs in a day). Sometimes the nodes need to handle higher QPS during busy hours like Christmas, black Friday . using QPS and user behavior, we can measure the load of a system. With this insight, it’s now easier to decide when to scale the system.
2. Read-to-write ratio (r/w): With this ratio, we can define whether a system is read-heavy or write-heavy.
	1. Read-heavy systems:This means the value of r/w is higher. In case of a higher load, we are likely to serve more and more reads.In read-heavy systems, adding one or more read-replicas to the database cluster will serve the higher count of read-requests.A read-replica in a database is a node that contains a copy of the original data. Read requests can generally be forwarded to read replicas so that the reads are evenly distributed, and do not overload the node that primarily handles write requests.
	2. write-heavy system: This is indicated by the low r/w value. When the load increases, the system will see a similar amount of writes compared to reads. Or sometimes, more writes than reads.Scaling a write-heavy system is more complicated compared to a read-heavy system. The general intuition we have is to add more nodes to handle writes. But this requires careful synchronization between the nodes that are handling writes. We cannot just randomly write one request to one node, and the next one to another. We have to follow a strict pattern.
	3. Measure performance: If our system follow a request-response pattern, then we measure the performance using the **average response time**.
		1. Percentiles: If a system has 99th99th percentile as 500ms500ms, it means out of 100100 requests sent to the system, 9999 are served in less than 500ms500ms time. The 11 request left may take more than 500ms500ms, or 1s1s, or even more.It’s pretty common for distributed systems to evaluate higher percentiles, like 95th95th, 99th99th, or 99.9th99.9th.