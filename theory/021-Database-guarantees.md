# Consistency Models and Isolation Levels: Understanding Database Guarantees

## Introduction

When working with databases, especially distributed systems, we need to understand what guarantees the system provides. Two important concepts help us understand these guarantees: **consistency models** and **isolation levels**. Let's explore how they work, how they're similar, and how they differ.

## Similarities Between Consistency Models and Isolation Levels

At their core, both consistency models and isolation levels serve the same fundamental purpose. They help us understand:

1. **Which executions are possible** in the system
2. **Which executions are not possible** (and therefore which problematic situations we're protected from)

Both concepts establish a spectrum from weaker to stronger guarantees:

- **Stronger guarantees** (like linearizability or serializability) offer increased safety but typically reduce performance and availability
- **Weaker guarantees** (like causal consistency or snapshot isolation) offer better performance but allow more potential anomalies

We can express these relationships as implications:

- If a system provides linearizability, it automatically provides causal consistency as well
- If a system provides serializability, it automatically provides snapshot isolation as well

Think of this as a "strictness hierarchy" where stronger models allow fewer possible execution patterns than weaker ones.

> Note: Some models aren't directly comparable—neither is strictly stronger than the other.

## Key Differences Between Consistency Models and Isolation Levels

Despite their similarities, these concepts differ in important ways:

### 1. Scope of Operations

- **Consistency models** apply to single-object operations (like reading or writing to a single register)
- **Isolation levels** apply to multi-object operations (like reading and writing multiple rows within a transaction)

### 2. Real-Time Guarantees

A crucial difference exists between even the strictest models in each category:

- **Linearizability** (strongest consistency model) provides real-time guarantees
- **Serializability** (strongest isolation level) does not provide real-time guarantees

### What Are Real-Time Guarantees?

**Linearizability** guarantees that the effects of an operation occurred at some point between when the client started the operation and when the result was returned.

**Serializability** only guarantees that transactions appear to execute in some sequential order. This order might not match the actual real-time order in which clients performed the operations.

## Why Real-Time Guarantees Matter: The ATM Example

Consider an ATM that supports two operations:

- `GET_BALANCE()` - Reads the account balance
- `WITHDRAW(amount)` - Reduces the balance and dispenses cash

Imagine this scenario with a customer whose initial balance is $100:

1. The customer checks their balance: `GET_BALANCE()` → $100
2. They withdraw $20: `WITHDRAW(20)` → ATM dispenses $20
3. They check their balance again: `GET_BALANCE()` → Still shows $100 (not $80)

Surprisingly, this sequence is technically **serializable**! The database could have executed these operations in the order: first operation 1, then operation 3, then operation 2. This meets the serializability guarantee (there exists some serial order) but violates our intuitive expectation that operations should respect real-time order.

This example shows why serializability alone isn't always sufficient for applications.

## Strict Serializability: The Best of Both Worlds

**Strict serializability** combines the strengths of both linearizability and serializability:

- It guarantees transactions appear to execute in a serial order (like serializability)
- It also guarantees this order respects the real-time sequence of operations (like linearizability)

With strict serializability, each transaction takes effect at some point between when it starts and when it completes—and the results reflect this real-time ordering.

### In Practice

- In **centralized databases**, providing strict serializability is often no more costly than providing regular serializability, so many systems labeled as "serializable" actually provide strict serializability.
- In **distributed databases**, strict serializability requires additional coordination between nodes, which can impact performance and availability.

Understanding the distinction between these guarantees helps you choose the right one for your application's needs.