### Vertical scaling aka scaling up[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/4554710928588800#Vertical-scaling-aka-scaling-up)

The idea of vertical scaling is to replace the existing machine with a more powerful machine.

![[Pasted image 20241002153725.png]]


In vertical scaling, a node is upgraded with more resources

The diagram above shows why another name for vertical scaling is **scaling up**.

Vertical scaling can mean different things in the context of different systems. For example:

- A node unable to handle many connections can be scaled up by adding more RAM and CPU.
- A database node unable to store more data can be scaled up by adding more storage.
- A router incapable of supporting an increased count of devices could be scaled up by replacing it with a more powerful router.

This scaling technique may work for small systems with a not-so-heavy increased load. Maybe a bigger machine would suffice for the system for the next 2 years or more.

Some systems adopt this technique at earlier stages due to its simplicity. But eventually, it becomes infeasible with the system’s growth:

- Continuously buying or renting a bigger machine is expensive. Hardware also has its own limitations.
- One machine is a single point of failure (SPoF).

The bottom line is that the scope of vertical scaling is limited.

### Horizontal scaling aka scaling out[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/4554710928588800#Horizontal-scaling-aka-scaling-out)

The other technique we will talk about is called horizontal scaling, aka **scaling out**.
![[Pasted image 20241002153747.png]]

In horizontal scaling, load is distributed among multiple nodes

The idea is simple. Add more nodes to handle the increased load. For different systems, this has different implications:

- A node running a server program can be scaled out by running the same program in multiple nodes and distributing the load among them evenly.
    
- A database is scaled out by adding replica nodes, commonly for reads.
    
- A network is scaled out by setting up multiple routers to work in sync.
    

Horizontal scaling is more or less the industry standard. Large systems depend on this method of scalability. There are many benefits that naturally come with this technique, like:

- It’s cost effective. You can basically run your system on cheap hardware with added redundancy.
- You have seemingly infinite scaling capacity if it can be maintained.
- You easily avoid single points of failure in the system. We just talked about evenly distributing load among horizontally scaled nodes. This is where we should discuss another important concept of distributed systems—load balancers.