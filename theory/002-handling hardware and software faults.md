## Handling hardware faults[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#Handling-hardware-faults)

For disk failures, it’s a very common practice to add redundancy by having more than one disk drive store the same data. These disks are generally cheap ones. Storing the same data in more than one disk helps to make sure that if there is an unrecoverable disk failure, then another disk can be used to recover the data.

> **Note**: Arranging multiple disks to store the same copy of data is called **RAID** (**R**edundant **A**rray of **I**ndependent **D**isks). Say your initial system of the My Cool App was like this:

- A single node.
- The server and database process are both running on the same node.

Now, if there is a failure in the disk of the single node, it’s unusable. In this situation, if you had redundant disks, you could just use one of the redundant disks available to quickly bring your backend back to life.

For many applications, this RAID scheme works when downtime is tolerable. If things go wrong, the system will be down and won’t be available for the time being. But the redundancies will ensure correctness as the data is not lost—and the system will not serve users with any corrupted data.

On the other hand, in a distributed environment, we don’t want to let our whole system stop working every time there is a random node crash. We want it to be _available_ all the time. And at the same time, we want to ensure that the system is _reliable_, functioning _correctly_.

As a result, the standard practice is to use multi-machine redundancy in this case. Data is replicated _correctly_ across machines. We achieve two things here:

- When a node crashes, other nodes can serve. This means your system is _available_ (more on availability later in this chapter).
- There is no data loss. Other nodes can serve the users with correct data. This achieves _reliability_ in the system.

The above might sound easy, but in reality it’s difficult. Having multiple copies of data and making sure all the copies are consistent is by default a very complex problem. We will explore more about this in this course when we discuss data replication.

In summary, the standard practice is to create redundancy—at both the hardware component level and on the machine level—to handle hardware faults.

## Handling software faults[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#Handling-software-faults)

There are a couple of ways you can consider handling software faults in your system. Let’s discuss briefly.

### Write tests[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#Write-tests)

Write tests for your code. There are different types of tests that are pretty common in developing distributed systems.

#### Unit tests[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#Unit-tests)

Unit tests are targeted at individual functions or modules of your codebase. For example, for a specific function, you create a set of test cases, pass the cases as parameters to the functions, and check the output against the expected input. Tests like these are written by the programmer to ensure the correctness of the logical flow of code.

#### Integration tests[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#Integration-tests)

Integration tests are targeted at different pieces of the system or modules in more of a combined way—they test how pieces interact with each other. For example, a server program sends queries to a database. You might want to run integration tests to check whether the flow between server and database is working correctly.

#### End-to-end tests[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#End-to-end-tests)

End-to-end tests are run to simulate user behavior. Their purpose is to touch the whole flow in the system starting from the user interaction on the app or website to database operations and system response. Tests like this require much more effort and collaboration between multiple teams in large systems. But they are definitely worth the effort.

### Handle errors[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#Handle-errors)

Handle errors in all parts of your codebase, wherever they are likely. Sometimes while writing code, you may think that a function call or some file input or output won’t throw an error, but it eventually does. (Well, it might be rare—but as a developer, do not take things by chance.)

### Monitor critical parts[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5489312656523264#Monitor-critical-parts)

You should monitor the critical parts of the system, and add logs wherever required. This will help you to get notified of any abnormality in the system immediately so that you can react fast and ensure fault tolerance. There are third-party services you can use for this purpose. The services will give you graphical interfaces on which you can see all kinds of statuses of your system. We will discuss more on this later.