---
title: Cache tables
url: https://fgiesen.wordpress.com/2019/02/11/cache-tables/
published: '2019-02-11'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Cache tables

Hash tables are the most popular probabilistic data structure, by quite a margin. You compute some hash code then compute an array index from that hash code. If you’re using open addressing-class schemes, you then have a rule to find other array indices that a value with the given hash code might be found at; with separate chaining, your array entries point to the head of a linked list, or the root of a binary tree, or whatever other data structure you prefer for the given use case.

No matter what exactly you do, this entire class of schemes always gives you a [Las Vegas algorithm](https://en.wikipedia.org/wiki/Las_Vegas_algorithm), meaning this type of hash table will always retain values for all the keys you inserted, but you’re gambling on how long a lookup takes.

An alternative is to enforce a strict limit P≥1 on the number of probes performed (for open addressing) or the size of any of the secondary data structures (for separate chaining). The result is a “forgetful dictionary”: keys are allowed to disappear, or at least become unretrievable. That’s quite a limitation. In return, the worst-case lookup cost becomes bounded. In short, we now have a [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_algorithm) algorithm: we’re now allowed to fail lookups (keys can disappear over time), but runtime variability is significantly reduced.

Let’s call this data structure a “cache table”, both because it’s useful for caching the results of queries and because it matches the most common organization of caches in hardware. We’ve been using that name at RAD for a while now, and I’ve also seen it used elsewhere, so it’s likely someone independently came up with the same name for the same thing, which I take to be a good sign.

In conventional hash tables, we have different probing schemes, or separate chaining with different data structures. For a cache table, we have our strict bound P on the number of entries we allow in the same bucket, and practical choices of P are relatively small, in the single or low double digits. That makes the most natural representation a simple 2D array: N rows of hash buckets with P columns, each with space for one entry, forming a N×P grid. Having storage for all entries in the same row right next to each other leads to favorable memory access patterns, better than most probe sequences used in open addressing or the pointer-heavy data structures typically used in separate chaining.

To look up a key, we calculate the row index from the hash code, using something like `row = hash % N`

. Then we check whether there is a matching entry in that row, by looping over all P columns. That’s also why you don’t want P to get too large. What I’ve just described matches the operation of a P-way [set associative cache](https://en.wikipedia.org/wiki/Cache_placement_policies#Set_Associative_Cache) in hardware exactly, and we will sometimes call P the number of “ways” in the cache table.

P=1 is the simplest case and corresponds to a direct-mapped cache in hardware. Each entry has exactly one location in the cache array where it can go; it’s either there or it’s not present at all. Inserting an entry means replacing the previous entry at that location.

For P≠1, there are multiple choices of which item to replace on insertion; which one is picked is determined by the *replacement policy*. There are many candidates to choose from, with different implementation trade-offs; a decent option that doesn’t require any extra metadata stored alongside each row is to use random replacement, i.e. just picking a (pseudo-)random column within the given row to evict on every insertion. “Hang on”, you might say, “aren’t hash codes pseudo-random already?”. Yes, they are, but you want to use a random number generator independent of your hash function here, or else you’re really just building a direct-mapped cache with N×P rows. One of the benefits of keeping P entries per row is that it allows us to have two different keys with identical hash values (i.e. a hash collision) in the same table; as per the [birthday problem](https://en.wikipedia.org/wiki/Birthday_problem), even with a well-distributed hash, you are likely to see collisions.

So what is this type of data structure useful for? I’ve come across two classes of use cases so far:

- Caching queries, as noted above. It’s used extensively to build (memory) caches in hardware, but it’s useful in software too. If you’re trying to cache results of operations in software, there is often a desire to keep the size of the cache bounded and have lookups take a predictable time; cache tables deliver both and are generally simpler than trying to manually limit the number of live entries in a regular hash table.
- Approximate searching tasks. For example, they’re quite useful in LZ77 match finding – and have been used that way since at least the late 80s (a 1986 patent covering the case P=1, now expired, was the subject of a rather
[famous lawsuit](https://en.wikipedia.org/wiki/Stac_Electronics#Microsoft_lawsuit)) and[early 90s](http://www.ross.net/compression/lzrw3a.html)(P≠1), respectively.

I’ve been using the name HacheTable for similar purposes. Basically it’s a hash table with function pointers to population and depopulate.

We used it for caching of blocks of data from a file format, queried as if in a hash table (with ref count incr/decr to avoid early removal), but backed up via a storage system. The advantage there is the caller never has to worry about keys not being present or disappearing, but the memory can still be limited.

The oldest variant I found was 2008. :) Latest incarnation (albeit still old) is https://sourceforge.net/p/staden/code/HEAD/tree/staden/trunk/src/gap5/hache_table.h and associated .c file. Gracefully aging code, hardly used any more alas.

Thanks for the article (and yes I know I’m rather slow in noticing it!)

I once coined the term HacheTable for a project (https://sourceforge.net/p/staden/code/HEAD/tree/staden/trunk/src/gap5/hache_table.h). The policy there was a fixed size hash table with load and delete function pointers to populate it, along with reference counting so uses could be pinned briefly.

The intention there was to pretend a large no-SQL style database file is entirely loaded and addressable, but the backend caches data appropriately. A somewhat similar idea, but completely different approach and implementation.

Therefore I’m pleased it also has a similar but different hash/cache name collision. :-)