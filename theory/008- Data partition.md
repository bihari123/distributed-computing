## What is partitioning?
Partitioning is a mechanism in which data is divided into smaller chunks based on some specific attributes. Those chunks are called partitions. One partition is independent of another partition. Two partitions can be stored in two different machines in a distributed system. A partition can also be treated as a standalone database table.
### Diff between partition and sharding?
- Sharding denotes physically storing data in multiple server instances.
- Partitioning refers to both the physical and the logical division of data. For example, if you break down a database table into multiple smaller tables but still store the tables on the same machine, this is partitioning
## Partitioning vs. Sharding: A Detailed Explanation with Practical Examples

Both partitioning and sharding are techniques used to manage large databases by breaking them into smaller, more manageable pieces. Let me walk you through each concept with practical examples to highlight their differences.

### Database Partitioning

Partitioning involves dividing a single database instance into multiple separate parts, called partitions, but still managed by a single database server.

#### Types of Partitioning

1. **Horizontal Partitioning**: Splitting a table by rows
2. **Vertical Partitioning**: Splitting a table by columns
3. **Range Partitioning**: Based on ranges of values
4. **List Partitioning**: Based on discrete values
5. **Hash Partitioning**: Based on a hash function

#### Practical Example of Partitioning

Let's consider an e-commerce database with an `orders` table containing millions of records:

##### Horizontal (Range) Partitioning Example

Imagine our `orders` table has grown to contain 5 years of data with over 10 million rows. Performance is degrading because queries often only need recent data but have to scan the entire table.

**Solution**: We implement range partitioning by date:

```sql
-- Creating a partitioned table in PostgreSQL
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (order_date);

-- Creating individual partitions
CREATE TABLE orders_2023 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

When a query like `SELECT * FROM orders WHERE order_date > '2025-01-01'` is executed, the database automatically knows to only scan the `orders_2025` partition, significantly improving performance.

##### Vertical Partitioning Example

Our `products` table contains basic information and large text descriptions and image URLs that are rarely accessed together:

**Solution**: Split into two tables:

```sql
-- Original table before vertical partitioning
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    category VARCHAR(50),
    description TEXT, -- Large text field
    specifications TEXT, -- Large text field
    image_urls TEXT[] -- Array of image URLs
);

-- After vertical partitioning
CREATE TABLE product_basic (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    category VARCHAR(50)
);

CREATE TABLE product_details (
    product_id INT PRIMARY KEY REFERENCES product_basic(product_id),
    description TEXT,
    specifications TEXT,
    image_urls TEXT[]
);
```

Now, when the application needs just the basic product information (which happens in 80% of cases), it can query the smaller `product_basic` table, improving performance.

#### Benefits of Partitioning

- **Improved query performance**: Only scans relevant partitions
- **Easier maintenance**: Can perform operations on individual partitions
- **Better storage optimization**: Can place frequently accessed partitions on faster storage

### Database Sharding

Sharding goes beyond partitioning by distributing data across multiple separate database servers or instances. Each shard contains a subset of the data and operates as an independent database.

#### Practical Example of Sharding

Let's consider a social media application with 50 million users. The `users` and `posts` tables have grown too large for a single database server to handle efficiently.

##### Sharding by User ID

We decide to implement a sharding strategy based on user IDs, using a modulo function:

```
Shard number = user_id % number_of_shards
```

With 4 shards, our architecture looks like:

- **Shard 0**: Contains data for users where `user_id % 4 = 0`
- **Shard 1**: Contains data for users where `user_id % 4 = 1`
- **Shard 2**: Contains data for users where `user_id % 4 = 2`
- **Shard 3**: Contains data for users where `user_id % 4 = 3`

Each shard is a completely separate database server with its own resources:

```
Shard 0 Server: database01.example.com
Shard 1 Server: database02.example.com
Shard 2 Server: database03.example.com
Shard 3 Server: database04.example.com
```

Our application code needs to know which shard to query for a given user:

```python
def get_user_data(user_id):
    shard_number = user_id % 4
    shard_server = f"database0{shard_number + 1}.example.com"
    
    # Connect to the appropriate shard
    connection = connect_to_database(shard_server)
    
    # Query data for this user
    result = connection.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    return result
```

When retrieving posts for a given user, we know exactly which shard to query, avoiding the need to search across all shards.

#### Implementing Sharding in a Real System

In production, we might use a sharding middleware like:

1. **In MongoDB**: Using native sharding
    
    ```javascript
    // Enable sharding for a database
    sh.enableSharding("social_network")
    
    // Set the shard key for the users collection
    sh.shardCollection("social_network.users", { "user_id": 1 })
    ```
    
2. **In MySQL**: Using technologies like Vitess
    
    ```sql
    -- Define sharding schema in Vitess
    CREATE VSCHEMA KEYSPACE social_network;
    
    -- Define the sharding key
    ALTER VSCHEMA ON users ADD VINDEX hash(user_id) USING hash;
    ```
    

#### Benefits of Sharding

- **Horizontal scalability**: Can add more shards as data grows
- **Improved performance**: Each shard handles a fraction of the total load
- **Higher availability**: A problem with one shard doesn't affect others
- **Geographic distribution**: Can place shards closer to their users

### Key Differences Illustrated by the Examples

1. **Scope and Infrastructure**:
    
    - In the partitioning example, we're still using a single database server managing multiple partitions
    - In the sharding example, we're using multiple separate database servers, each with its own infrastructure
2. **Application Awareness**:
    
    - For partitioning, our application simply connects to the database as usual; the database system handles partition selection
    - For sharding, our application needs specific logic to determine which shard to query
3. **Query Complexity**:
    
    - With partitioning, we can still easily query across multiple partitions (though it may be slower)
    - With sharding, queries across multiple shards require special handling and often application-level joins
4. **Scaling Approach**:
    
    - Partitioning scales by optimizing resource usage within a server
    - Sharding scales by adding more servers to handle additional data

### When to Use Each Approach

**Use Partitioning When**:

- Your data volume is large but still manageable on a single server
- You need to improve query performance but don't need distributed scaling
- You want to simplify data lifecycle management (e.g., archiving old data)

**Use Sharding When**:

- Your data volume exceeds what a single server can handle
- You need to distribute load across multiple machines
- You need higher availability through redundancy
- You want to distribute data geographically closer to users

In practice, many large systems use both techniques simultaneously: sharding to distribute data across multiple servers, and then partitioning within each shard for additional performance benefits.

## Why use partitioning?
In modern systems, the data keeps coming. You may not have enough storage on one machine to keep all of it . So, you make a logical arrangement to divide the data between nodes. Ex, you have data related to users having userid <1000 on server 1 and for userid>=1000, you have the data on server 2. This way, it becomes to easy to query the users having userid <1000 as the load balancer knows where to look at. Also,  it becomes easy to scale horizontally. Partitioning should be implemented with replication. 

## Partitioning Techniques
##### Range based partitioning 
In range-based partitioning, data is partitioned based on the ranges of the key. For example, say we have keys of type strings. Now the data with keys starting with ‘a’ to ‘j’ is stored in node 1, ‘k’ to ‘p’ in node 2, and ‘q’ to ‘z’ in node 3.
This techniques can sometimes lead to **data skewness**. Data skewness is a condition where one or few partitions have significantly more data than other partitions.
Skewed partitions can create **hotspots** where some nodes receive a huge amount of read and write requests compared to others.

### Hash Partitioning
One way of avoiding skewedness in the partitions is hash partitioning. In this technique, the key is hashed using some hash function. A good function ensures the keyspace gets evenly distributed in a predefined range. For example, a 32 but hash function will take the key as an input and return a random number from the range 0 to 2^32 -1. Then we calculate the selected node as 
```
selected_node= node_list[hash(k)%n]
```
However, this approach can be harmful if we want to add a new node. because then the number of nodes increase and the whole formula is affected 
```
selected_node= node_list[hash(k)%(n+1)]
```
now the data of all the nodes have to be re-balanced and it is too costly.
A better approach is to use **virtual nodes**, also know as vnodes. The procedure goes as follows:
- Predefine a large number of partitions based on the hash of the key. For example, predefine 10001000 partitions. These 10001000 partitions are the vnodes.
- Keys will be mapped to the vnodes.
- Map the vnodes to the physical servers. This means each server will contain a set of vnodes, approximately 250250 vnodes per physical node.
- When a new node is added, a number of vnodes will get mapped to it. As a result, the new node will now copy a few vnodes from the existing physical nodes.

### Pros[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5852494755528704#Pros)

- Compared to range-based partitioning, hotspots are less likely to occur since keys are evenly distributed in a range.

### Cons[](https://www.educative.io/module/page/P1vxGOto4z83LN78X/10370001/6275949640548352/5852494755528704#Cons)

- If the rebalancing strategy is poor, rebalancing might also be costly in this technique.
- We lose efficient range queries on the key since continuous ranges of keys are not stored anymore in the system. But for many systems, this may not be a problem due to the data query patterns.
#### Consistent Hashing
In general hashing, the keys are mapped to a one-dimension space. In consistent hashing, the idea is to have a hash ring instead of a one dimensional array and map each server on its ring.
![[conistent-hashing.png]]
We map the keys is the same way as we did in regular hashing. 
![[mapping-in-consistent-hashing.png]]
To choose the nodes for the keys to store the data, we go clockwise and assign the keys to the first nodes we encounter. So basically, all the keys that fall between S0 and S1 are assigned to S1. Similarly, keys between S2 and S3 are assigned to S3.
Node addition and removal are handled the same way. If a node is added, the keys between the new node and the node next to it in the anti-clockwise direction are assigned to the new node. So, a small fraction of the total keys are remapped.

Similarly, if a node is deleted, all the keys that were assigned to it now get remapped to the node next to the removed node in the clockwise direction. Again, only a small fraction of keys are remapped.
Since nodes can be added or removed, and having a good hash function plays a major role in the even distribution of keys, the basic version of consistent hashing can still have hotspots in the cluster. To avoid this, the same idea of virtual nodes can be greatly helpful.

So basically, using multiple hash functions, we can map one server multiple times on the ring. And then, similarly, we have to map the keys and assign them to the virtual nodes. These virtual nodes are inherently mapped to the physical nodes which actually store the data.

# Partitioning in Distributed Systems: Making Systems Scalable

Partitioning is a fundamental strategy that enables distributed systems to achieve scalability by dividing large datasets into smaller, manageable pieces that can be stored and processed across multiple nodes.

## Core Concepts

Scalability is one of the major benefits of distributed systems, allowing us to handle datasets much larger than what a single machine could process. Partitioning serves as the primary mechanism to achieve this scalability.

When we partition data, we split a large dataset into multiple smaller datasets and assign each portion to different nodes in a distributed system. This approach allows us to expand our system's capacity by simply adding more nodes.

## Two Types of Partitioning

There are two main approaches to partitioning data:

### Vertical Partitioning

Vertical partitioning divides a table by columns, creating multiple tables with fewer columns each. These different tables can then be stored on separate nodes. This approach:

- Splits data based on columns (attributes)
- Often requires join operations to recombine related data
- Can leverage normalization techniques, though vertical partitioning extends beyond normalization

### Horizontal Partitioning (Sharding)

Horizontal partitioning, also known as sharding, divides a table by rows. Each resulting subtable contains a percentage of the original rows and can be stored on different nodes. This approach:

- Splits data based on rows (entries)
- Can use various strategies for splitting, such as alphabetical divisions
- Keeps all attributes of each entry together on the same node

## Limitations and Trade-offs

Both partitioning approaches come with specific limitations:

**Vertical Partitioning Challenges:**

- Requests requiring joined data from different tables become less efficient
- May require accessing multiple nodes to fulfill a single request

**Horizontal Partitioning Challenges:**

- Queries spanning multiple partitions may still require accessing multiple nodes
- Loss of transactional semantics - atomic operations across different nodes become difficult
- Harder to ensure that either all operations succeed or none do when data spans multiple nodes

## Practical Considerations

Vertical partitioning is primarily a data modeling practice that engineers can implement somewhat independently of the storage systems. In contrast, horizontal partitioning is a common feature built into distributed databases, requiring engineers to understand the underlying mechanics to use these systems effectively.

This illustrates a recurring theme in distributed systems: there's no perfect solution. Every design decision involves trade-offs to achieve desired properties like scalability, consistency, or performance.