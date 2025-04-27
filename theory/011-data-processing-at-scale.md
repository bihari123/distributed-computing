## Batch processing
Generally, the server executes the client request, connects to some database and sends the response. The user expects to be served that response as quickly as possible. A system like this is popularly known as an online system.
On the other hand, we have batch processing systems which takes a large amount of input data, runs a job periodically and then produces some output. One important aspect of batch processing is the execution of the job by using many processes, typically using a cluster of nodes.
### An example of batch processing
You have a social media site where the interaction of the users are logged as events and sent to the servers. The servers read the events, parse the events using any predefined schema and persist the events in some storage. Then there is a batch processing system that wakes up every hour/day, depending upon the business requirements, reads the events from the event storage and processes the data using multiple processes and nodes. Finally, the batch processing system generates output data that is persisted in some other database such as MySQL and Cassandra.

## The MapReduce algorithm
Sometimes the data is so large that it cannot fit inside the memory of one machine. So we split the data and load it into multiple machines and then process them. There are three stages in mapreduce: 1. mapping 2. shuffling 3.reducing. We first map the data in a key value pair in each machine then we go on to the shuffling stage where we just compare the data across the machines and sort them out and then in the reducing stage, we aggregate the data based on the key and create the final result in the step. Here we have an example where we implement map reduce on an English sentence. We first split the sentence into multiple parts, we map the words in those parts that were processed in each machine, them we shuffle them to see which words were repeating in the parts processed on different machine and then we reduce with the final value representing the number of ways then words have been repeated.
![[mapReduce-sample.png]]
## How do we run batch processing?
We use tools like apache hadoop or apache spark where we have a job tracker and a task tracker which taskes care of this for us.

## Stream Processing
In the batch processing there is a delay which may not be desired in some applications like real time threat detection.   There we want to process the event as soon as it happens.
 The idea of stream processing is to process an event or an item from a stream of data as soon as the event appears in the stream. After processing, the stream processor will potentially publish the processed data into a new stream. Consumers interested in the processed data can now directly consume the new stream and act accordingly.
 Data items are continuously put in some storage queue which some stream processing framework is listening to. One example of such a queue is Apache Kafka, which is one of the most famous technologies in the industry. For the stream processing framework, an example could be Apache Flink.

As data is put on the queue, the framework continuously reads data from the queue and runs some actions. As soon as there is a result, the result is then put into a new stream for other systems to consume.
Note that an algorithm like MapReduce can also be used in stream processing. It’s just that in the case of stream processing, the framework will probably choose a very small time window (like half a minute or five minutes), and run the algorithm on top of it.
![[apache kafka.png]]