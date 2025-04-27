# Transaction Isolation Levels and Anomalies in Distributed Systems

## Introduction to Transaction Isolation

In distributed database systems, multiple transactions often execute concurrently. This concurrency creates challenges: how do we ensure that transactions don't interfere with one another in harmful ways?

The fundamental problem is that when multiple transactions run simultaneously, their operations can become interleaved. Depending on this interleaving, we might get different—and sometimes unexpected—results. Without proper controls, this can lead to data inconsistencies that violate the integrity of our database.

To address these challenges, database systems implement different **isolation levels**. Each isolation level defines what kinds of interference are allowed or prevented between concurrent transactions, establishing formal boundaries for system behavior.

## Key Isolation Levels: From Weakest to Strongest

Isolation levels exist on a spectrum, with stronger levels preventing more anomalies but typically imposing greater performance costs. Here are the standard isolation levels, arranged from weakest to strongest:

### 1. Read Uncommitted

Read Uncommitted is the weakest isolation level. It allows transactions to see data that has been modified by other transactions but not yet committed. This level prioritizes performance over consistency.

**Key characteristic**: Transactions can see changes made by other transactions before those transactions commit.

### 2. Read Committed

Read Committed ensures that a transaction can only see data that has been committed by other transactions. This prevents one major anomaly (dirty reads) while still maintaining reasonable performance.

**Key characteristic**: A transaction will never see data from another transaction's uncommitted changes.

### 3. Repeatable Read

Repeatable Read guarantees that if a transaction reads a data item once, subsequent reads of that same item will yield the same value throughout the transaction's lifetime. This prevents non-repeatable (or fuzzy) reads.

**Key characteristic**: Once a transaction reads a piece of data, that data will not appear to change for the duration of the transaction.

### 4. Snapshot Isolation

Snapshot Isolation provides each transaction with a consistent view (or "snapshot") of the database as it existed at the start of the transaction. Changes made by other transactions that commit after the snapshot was taken remain invisible to the transaction.

**Key characteristic**: Each transaction works with a time-consistent view of the database, as if it had a private copy of the database at a specific point in time.

### 5. Serializability

Serializability is the strongest isolation level. It guarantees that the outcome of executing transactions concurrently is equivalent to executing them in some sequential order. This eliminates all anomalies but may significantly impact performance.

**Key characteristic**: The concurrent execution of transactions produces results identical to some sequential execution of those same transactions.

## Transaction Anomalies: Understanding the Problems

Anomalies are unexpected behaviors that can occur when transactions execute concurrently. Let's explore each type in detail:

### 1. Dirty Write

**Definition**: A dirty write occurs when a transaction overwrites a value that was previously written by another transaction that has not yet committed.

**Why it's problematic**:

- It can violate data integrity constraints
- It makes system rollbacks difficult or impossible
- It can lead to data inconsistencies if the first transaction aborts

**Real-world example**: Suppose we have two transactions modifying a customer's information:

- Transaction A: `UPDATE Customer SET email='new@example.com', phone='555-1234' WHERE id=101`
- Transaction B: `UPDATE Customer SET email='different@example.com', phone='555-5678' WHERE id=101`

If Transaction A sets the email but not yet the phone, and Transaction B overwrites the email before Transaction A completes, we could end up with a mix of data from both transactions. If Transaction A later aborts, we can't properly restore the original state.

### 2. Dirty Read

**Definition**: A dirty read happens when a transaction reads data written by another transaction that has not yet committed.

**Why it's problematic**:

- The read data might be rolled back and thus never actually exist in the committed database state
- Decisions might be made based on data that is ultimately discarded
- It can lead to logical inconsistencies in application behavior

**Real-world example**: Consider a banking system where Transaction A transfers $1000 from Account 1 (balance: $2000) to Account 2:

1. Transaction A deducts $1000 from Account 1 (new balance: $1000)
2. Transaction B reads Account 1 balance ($1000) and Account 2 balance (still $0)
3. Transaction B calculates total funds: $1000 (incorrectly shows $1000 "missing" from the system)
4. Transaction A completes by adding $1000 to Account 2

Transaction B observed the system in an inconsistent state where money appeared to have vanished.

### 3. Fuzzy (Non-Repeatable) Read

**Definition**: A fuzzy read occurs when a transaction reads the same data item multiple times but gets different values each time because another transaction has modified the data between reads.

**Why it's problematic**:

- It creates inconsistent views within the same transaction
- It can cause logical errors when transactions make decisions based on earlier reads but then use later, different values
- It violates a fundamental expectation of transaction stability

**Real-world example**: A transaction calculating average account balance might:

1. Read Account X balance: $1000
2. Another transaction deposits $500 to Account X and commits
3. Later in the first transaction, Account X is read again: $1500
4. The first transaction makes calculations using both values, creating inconsistent results

### 4. Phantom Read

**Definition**: A phantom read happens when a transaction executes a query that returns a set of rows, but a concurrent transaction inserts or deletes rows that would match that query, causing subsequent executions of the same query to return different sets of rows.

**Why it's problematic**:

- It violates the expectation that the set of records matching a particular condition remains stable
- It can lead to incorrect aggregates or decisions based on incomplete data sets
- It represents a fundamental inconsistency in how the transaction views the database

**Real-world example**: Consider a report that needs to analyze employee data:

1. Transaction A queries: `SELECT AVG(age) FROM employees WHERE department='Engineering'` (gets 35 years)
2. Transaction B adds five new young engineers to the department and commits
3. Transaction A later queries: `SELECT MAX(age) FROM employees WHERE department='Engineering'` (gets 62 years)
4. Transaction A reports that the maximum age (62) is much higher than the average (35), when in reality the average should be lower (30) with the new employees included

### 5. Lost Update

**Definition**: A lost update occurs when two transactions read the same item, and then both attempt to update it based on their reads. One transaction's update overwrites the other's without incorporating its changes.

**Why it's problematic**:

- It causes data loss as one transaction's changes are silently overwritten
- Neither transaction is aware that its view of the data may be outdated
- It frequently occurs in common "read-modify-write" patterns

**Real-world example**: In an inventory system:

1. Transaction A reads that Product X has 100 units in stock
2. Transaction B reads that Product X has 100 units in stock
3. Transaction A adds 5 units, updates stock to 105, and commits
4. Transaction B adds 10 units, updates stock to 110, and commits
5. Final stock shows 110 instead of the correct 115 units

Transaction A's update has been completely lost, potentially leading to inventory discrepancies.

### 6. Read Skew

**Definition**: Read skew occurs when a transaction reads multiple related data items, but another transaction modifies some of these items in between the reads, causing the first transaction to see an inconsistent view of the data.

**Why it's problematic**:

- It can violate integrity constraints between related data items
- It presents a view of the database that never actually existed as a consistent state
- It can cause application-level logical errors

**Real-world example**: Consider a social network with a mutual friendship constraint:

1. Transaction A reads Person 1's friends list (includes Person 2)
2. Transaction B unfriends Person 2 from Person 1 and Person 1 from Person 2, then commits
3. Transaction A reads Person 2's friends list (no longer includes Person 1)
4. Transaction A observes an inconsistent state where Person 1 considers Person 2 a friend, but not vice versa

### 7. Write Skew

**Definition**: Write skew happens when two transactions read the same data, make decisions based on that data, and then update different data items based on those decisions.

**Why it's problematic**:

- It can violate database constraints even when each transaction individually appears correct
- It represents a subtle concurrency issue that's difficult to detect
- It often leads to violation of application-level invariants

**Real-world example**: In a hospital scheduling system with a rule that at least one doctor must be on-call:

1. Transaction A (Doctor Alice) reads that there are two doctors on-call (Alice and Bob)
2. Transaction B (Doctor Bob) reads that there are two doctors on-call (Alice and Bob)
3. Transaction A updates Alice's record to "not on-call" (assuming Bob remains on-call)
4. Transaction B updates Bob's record to "not on-call" (assuming Alice remains on-call)
5. Result: No doctors are on-call, violating the system constraint

## Isolation Levels and Anomaly Prevention

The primary purpose of isolation levels is to prevent specific anomalies. Here's how each isolation level relates to the anomalies we've discussed:

|Isolation Level|Dirty Write|Dirty Read|Fuzzy Read|Phantom Read|Lost Update|Read Skew|Write Skew|
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|Read Uncommitted|Prevented|Allowed|Allowed|Allowed|Allowed|Allowed|Allowed|
|Read Committed|Prevented|Prevented|Allowed|Allowed|Allowed|Allowed|Allowed|
|Repeatable Read|Prevented|Prevented|Prevented|Allowed*|Allowed*|Allowed|Allowed|
|Snapshot Isolation|Prevented|Prevented|Prevented|Prevented|Prevented|Prevented|Allowed|
|Serializability|Prevented|Prevented|Prevented|Prevented|Prevented|Prevented|Prevented|

*Note: Some implementations of Repeatable Read (like in MySQL InnoDB) may prevent phantom reads and lost updates.

## Performance Considerations

Each increase in isolation level typically comes with a performance cost. Stronger isolation levels often require more locking, blocking, or complex mechanisms like multiversion concurrency control (MVCC).

When designing a system, you must carefully balance the need for consistency against performance requirements:

- Critical financial applications might require Serializability despite the performance impact
- High-throughput web applications might use Read Committed for better performance
- Reporting applications that can tolerate slight inconsistencies might use Read Uncommitted for maximum throughput

## Conclusion

Understanding transaction isolation levels and their relationship to anomalies is fundamental for designing robust distributed systems. By choosing the appropriate isolation level, you can ensure your application maintains the necessary data consistency while achieving acceptable performance.

The formalization of isolation levels has evolved over time, from the original ANSI SQL-92 standard to more refined academic research. This evolution reflects the growing understanding of distributed systems and the complex behaviors that can emerge from concurrent transactions.

For system designers, the key is to understand both what each isolation level guarantees and what anomalies it allows, enabling informed decisions based on the specific requirements of each application.