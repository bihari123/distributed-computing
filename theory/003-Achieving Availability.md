## How to achieve availability in distributed systems?[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6450589906239488#How-to-achieve-availability-in-distributed-systems)

This is somewhat answered already—add redundancy in your system.

> Build your system in such a way that when things go wrong, redundant resources can handle the load and continue serving your users.

In this context, let’s introduce the concept of **SPoF**.

> **S**ingle **P**oint **o**f **F**ailure (SPoF) in a distributed system means a component that can bring the entire system down if there is any failure in the node itself.

For example, your home router can be a SPoF. If the router is down, you lose access to the internet.
![[Pasted image 20241002123344.png]]If there are redundant routers, failure of one router is easily tolerated
To build an available system, you need to avoid any possible SPoF so that the system can continue to function even when there are failures.

Expectations
In practice, distributed systems define some set of expectations and communicate them to their clients. That’s where the availability percentage measurements are used. In the case of My Cool App, you can define that the availability will be 2-nines (9999).
### Service Level Agreement (SLA)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6450589906239488#Service-Level-Agreement-SLA)

> SLA is an agreement between the system and its clients on specific requirements, for example, response time or availability.

As a system owner, you can set up an agreement with your clients that:

- The system will have at most 2 days of downtime over a year (99.599.5 availability).
- The system will respond to client requests within 100ms100ms.

When your system makes an agreement with such objectives, this is called a Service Level Agreement (SLA).

In the tech industry, such agreements are common between a vendor and a paying customer. Say, for example, Visa can come to an agreement with one of its paying customers that the system will be up 99.9999.99 time. This objective will be part of the SLA. If the agreement is breached, there will be some actions taken based on the agreement. For instance, Visa could pay the client as a penalty.

### Service Level Objective (SLO)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6450589906239488#Service-Level-Objective-SLO)

Individual promise in SLA is called an SLO. For example, one of My Cool App’s SLOs could be loading users’ feeds within 200ms200ms.

Similarly, Visa could have an SLO of processing each transaction within 2s2s.

### Service Level Indicators (SLI)[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/6450589906239488#Service-Level-Indicators-SLI)

SLA and SLO are agreements and promises between a service and its clients. SLI is the actual measurement in reality.

For example, if Visa promises its clients an uptime of 99.9999.99, and in reality, the uptime is 99.9599.95, the SLO is 4-nines, but SLI is 3-and-a-half nines.

In the real world, it’s not straightforward to perfectly stick to the SLAs and act upon them. Generally, the service and its client tune their expectations over the course of time.