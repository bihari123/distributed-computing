If some request is accessed again and again, then the server stores the response in  memory so that we don't need to run the query again and again until there is a change in the data. This helps up deliver result fast. 
For a server with cache layer, there can be two scenarios when recieving a request from a client:
- ***Cache-hit***: The response is found in the cache. The server fetches the data and responds immediately.
- ***Cache miss***: The response is not there in the cache. This results in
	- Server sends the query to the database system.
	- Query is executed and the data is sent back to the server node.
	- Server responds to the client request.
	- Cache is updated accordingly. So if the next time the same request is again encountered, the cache can be useful.

The cache layer, being an in-memory store is small and expensive. The idea is to store a portion of a data that is frequently accessed by the clients. This helps to server the most queries faster and reduce the load on the database. 
## Distribured Caching
Large scale systems will require a large cluster of cache layers. The cache layer can be distributed just like the database layer. There can be multiple nodes holding the same data. This is just replication that helps to achieve availability.
#### Time to leave (TTL)
TTL is the amount of time after which a piece of data will be evicted from the cache. Time begins being counted after the last update for the particular piece of data.
TTL is generally pre-configured on the cache server. It is automatically handled on the server-side.

#### Eviction policies
- Least recently used (LRU)
	- Most commonly used eviction policy. If the cache is fill, the remove the least recently used data first.
	- Instagram photos - newer photos will get more vies while older one fade out.
- Least frequently userd (LFU)
	- When you type on your phone and get the suggestions for the possible words, there can be an LFU cache that stores words and their counts. This cache will prefer storing the most frequently used words and evicting the least used ones.
- Most recently used (MRU)
	- If you remove someone from the friends list, then you would  not want the to appear again. In that case an MRU will be prefered.
## Writing policies for caching
- **Write-through cache**: In this caching technique, when a request is received, the data is written on the cache and also on the database. This can happen either in parallel or one after another.  In this strategy, the cache will hold the most recently written data. And it will be consistent with the database. This write-through cache is not very suitable for systems that are write-heavy due to increased write latency. On the flip side, systems that require immediate access to data after persisting can benefit from this type of cache.
- **Write-back cache**: Data is written to the cache and then asynchronously updated to the database. Neither read or write latency is hurt but the database which is the source of truth lags and this might cause problems. Systems that don't require the latest data to be available in the source of truth can potentially benefit from this caching strategy.
- **Write around cache**: The data is directly written to the database, bypassing the cache layer. The cache is only updated when the **cache miss** occurs. But there is a problem, if the data is already in the cache and that data is not updated in the database, the cache layer still have the outdated data. This is resolved by one of the following ways: 
	- Cache invalidation: When data is written to the main storage, the corresponding cache entry (if exists) is marked as invalid.
	- Time based expiration: Time to leave is used to refresh the cache periodically,
	- Write through with write around: Critical updates are write-through while less critical writes use write-around.