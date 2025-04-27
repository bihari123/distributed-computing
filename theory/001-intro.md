A distributed system is a collection of autonomous computing elements that appear to its users as a single coherent system.
There are two important aspects of this definition:
-> Autonomous: a machine in the distributed network is called a **node**.  These nodes are capable of running and dying independently of each other. But that doesn't mean that we can just run these nodes and they'll achieve our purpose. These nodes have to be programmed so that they interact with each other and server the users of the system. They can perform their duties autonomously.
-> Single Coherent System: The users should see what they expect. All the nodes collaborate as expected. No glitches.
### Wait?? does it mean that micro-services are also distributed systems???
No, microservices can have one service down and rest of the services running smoothly. This exposes the part of the microservices that a part of the service is running on one set of nodes whereas other part was running on different sets of nodes. This is what we call a state of incoherence.A distributed system aims at avoiding such inconsistent behavior. It wants to be coherent. And, of course, this is a difficult task by nature. In easy words, A microservice is typically part of a single application, while a distributed system can span multiple applications or services.

[###] NOTE: Don't make a distributed system from the scratch. Take into consideration the amount of money and effort required to build this. 
### Why do we need a distributed system?
- Fault Tolerance:
	- If there is something in your system not functioning as expected, you possibly have a fault.
	- Distributed systems have to be able to tolerate faults so that they can continue to function even if faults appear.
	- As a system owner, you should always expect faults and remain prepared accordingly. In the case of handling faults, prevention is better than cures.
	- Distributed systems have to be fault tolerant by nature.
- Reliability:
	- According to M Kleppmann, who put it in simple words in Designing Data Intensive Application, a reliable system is capable of “continuing to work correctly, even when things go wrong.”
	- in a distributed system, faults are inevitable. Hardware withers away with time. Networks drop and fluctuate randomly. Power outages happen now and then. When the system is built, scenarios like these have to be kept in mind. A reliable system can operate correctly in times of such failure scenarios.
	- When faults occur, a reliable system is capable of identifying, isolating, and potentially correcting it by itself. If correction is not possible, it should trigger a higher-level recovery mechanism, for example, triggering fallbacks to replacement hardware or software components. If that does not work, it should halt the affected program, and stop the entire system if required. And notify the system owner or developers accordingly.
	- When you build a distributed system, it makes hardly any sense if your system is not capable of handling the following:
		- The system can serve users’ expectations, for example, if My Cool App is a photo-sharing app, then users should be able to share photos. If someone uploads a photo and the photo is not shown on their profile, then this leads to a bad user experience.
		- If users make mistakes, the system should be able to tolerate the mistake. If a user of My Cool App uploads a video whereas the expectation is only photos, then the system should not break but handle it correctly. For instance, maybe the app will show some error message to the user that the operation is not allowed.
		- The system should be performant. If your user opens the feed of My Cool App and waits for 2 minutes for it to load, your users won’t be very happy.
		- If some malicious user tries to abuse your system, the system should endure it.
	- What hinders reliability?
		- Hardware faults: There are many hardware components in a single machine. The chance of failures just increases when you have tens of thousands of machines. Apart from the hardware components of the nodes, there is the network that binds the nodes. And networks are also unpredictable.
		- Software Faults: A bug in your server software code can be critical or mild. Sometimes it will randomly cause the server program to crash and restart, such as when some null pointer dereferences due to some specific logical flow which is probably rare. Sometimes it will keep the program crashing every single time it tries to restart, maybe due to some misconfiguration in server startup parameters.
			Sometimes the bugs are not generic. You won’t encounter them until a very specific set of parameters are passed to a particular function. If you don’t know the specific set of inputs, it may be even impossible to reproduce the bug.
			In your system, as the developer, you are probably responsible for a software bug. But sometimes it can be due to some third-party library that you are using. Maybe they have some misplaced condition that caused a set of side effects which affected your system.
	- Availability:
		- Availability is a property of a distributed system that ensures that the system is ready to serve users whenever users need it.
		- In practice, it’s easier to define availability in a mathematical formula.
		- Say, the backend system of the My Cool App was up for U time and down for D time since its launch. Then availability A is defined as
		 >  ![[Pasted image 20241002122343.png]]
		 - So basically, availability is the percentage of time a system was up for a given time range. For example, a system that is 99%99% available for a year means it will be down for 3.65 days over the period.
		 - For many systems, around 4 days of downtime over a year is bad.
	 - Scalability: **Scalability** is the ability of a system to handle the increased load of its usage.
## Challenges in Distributed system 
- Network asynchrony : Network unpredictability can lead to delays and messages being delivered out of order, making it hard to ensure all parts of the system are synchronized.
- partial failure : how do we ensure that the system is running fine if some of the parts are not working 
- concurrency: 
## Measure of Correctness in Distributed system
The correctness measures for distributed systems are the two properties they must satisfy. These are the following : 
- Safety  
- Liveness


>