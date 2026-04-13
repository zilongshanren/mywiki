---
title: Optimizing Open Addressing
url: https://thenumb.at/Hashtables/
published: '2023-01-08'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Optimizing Open Addressing

Your default hash table should be open-addressed, using Robin Hood linear probing with backward-shift deletion. When prioritizing deterministic performance over memory efficiency, two-way chaining is also a good choice.

*Code for this article may be found on GitHub.*

[Open Addressing vs. Separate Chaining](https://thenumb.at#open-addressing-vs-separate-chaining)[Benchmark Setup](https://thenumb.at#benchmark-setup)[Discussion](https://thenumb.at#discussion)[Unrolling, Prefetching, and SIMD](https://thenumb.at#unrolling-prefetching-and-simd)[Benchmark Data](https://thenumb.at#benchmark-data)

# Open Addressing vs. Separate Chaining

Most people first encounter hash tables implemented using *separate chaining*, a model simple to understand and analyze mathematically.
In separate chaining, a hash function is used to map each key to one of $$K$$ *buckets*.
Each bucket holds a linked list, so to retrieve a key, one simply traverses its corresponding bucket.

Given a hash function drawn from a [universal family](https://en.wikipedia.org/wiki/Universal_hashing), inserting $$N$$ keys into a table with $$K$$ buckets results in an expected bucket size of $$\frac{N}{K}$$, a quantity also known as the table’s *load factor*.
Assuming (reasonably) that $$\frac{N}{K}$$ is bounded by a constant, all operations on such a table can be performed in expected constant time.

Unfortunately, this basic analysis doesn’t consider the myriad factors that go into implementing an efficient hash table on a real computer.
In practice, hash tables based on *open addressing* can provide superior performance, and their limitations can be worked around in nearly all cases.

## Open Addressing

In an open-addressed table, each bucket only contains a single key. Collisions are handled by placing additional keys elsewhere in the table. For example, in linear probing, a key is placed in the first open bucket starting from the index it hashes to.

Unlike in separate chaining, open-addressed tables may be represented in memory as a single flat array.
*A priori*, we should expect operations on flat arrays to offer higher performance than those on linked structures due to more coherent memory accesses.[1](https://thenumb.at#fn:1)

However, if the user wants to insert more than $$K$$ keys into an open-addressed table with $$K$$ buckets, the entire table must be resized.
Typically, a larger array is allocated and all current keys are moved to the new table.
The size is grown by a constant factor (e.g. 2x), so insertions occur in *amortized* constant time.

## Why Not Separate Chaining?

In practice, the standard libraries of many languages provide separately chained hash tables, such as C++’s `std::unordered_map`

.
At least in C++, this choice is now considered to have been a mistake—it violates C++’s principle of not paying for features you didn’t ask for.

Separate chaining still has some purported benefits, but they seem unconvincing:

*Separately chained tables don’t require any linear-time operations.*First, this isn’t true. To maintain a constant load factor, separate chaining hash tables

*also*have to resize once a sufficient number of keys are inserted, though the limit can be greater than $$K$$. Most separately chained tables, including`std::unordered_map`

, only provide amortized constant time insertion.Second, open-addressed tables can be incrementally resized. When the table grows, there’s no reason we have to move all existing keys

*right away*. Instead, every subsequent operation can move a fixed number of old keys into the new table. Eventually, all keys will have been moved and the old table may be deallocated. This technique incurs overhead on every operation during a resize, but none will require linear time.*When each (key + value) entry is allocated separately, entries can have stable addresses. External code can safely store pointers to them, and large entries never have to be copied.*This property is easy to support by adding a single level of indirection. That is, allocate each entry separately, but use an open-addressed table to map keys to pointers-to-entries. In this case, resizing the table only requires copying pointers, rather than entire entries.

*Lower memory overhead.*It’s possible for a separately chained table to store the same data in less space than an open-addressed equivalent, since flat tables necessarily waste space storing empty buckets. However, matching

[high-quality](https://thenumb.at#robin-hood-linear-probing)open addressing schemes (especially when storing entries indirectly) requires a load factor greater than one, degrading query performance. Further, individually allocating nodes wastes memory due to heap allocator overhead and fragmentation.

In fact, the only situation where open addressing truly doesn’t work is when the table cannot allocate *and* entries cannot be moved.
These requirements can arise when using [intrusive linked lists](https://www.data-structures-in-practice.com/intrusive-linked-lists/), a common pattern in kernel data structures and embedded systems with no heap.

# Benchmark Setup

For simplicity, let us only consider tables mapping 64-bit integer keys to 64-bit integer values. Results will not take into account the effects of larger values or non-trivial key comparison, but should still be representative, as keys can often be represented in 64 bits and values are often pointers.

We will evaluate tables using the following metrics:

- Time to insert $$N$$ keys into an empty table.
- Time to erase $$N$$ existing keys.
- Time to look up $$N$$ existing keys.
- Time to look up $$N$$ missing keys.
[2](https://thenumb.at#fn:2) - Average probe length for existing & missing keys.
- Maximum probe length for existing & missing keys.
- Memory amplification in a full table (total size / size of data).

Each open-addressed table was benchmarked at 50%, 75%, and 90% load factors.
Every test targeted a table capacity of 8M entries, setting $$N = \lfloor 8388608 * \text{Load Factor} \rfloor - 1$$.
Fixing the table capacity allows us to benchmark behavior at exactly the specified load factor, avoiding misleading results from tables that have recently grown.
The large number of keys causes each test to unpredictably traverse a data set much larger than L3 cache (128MB+), so the CPU 3 cannot effectively cache or prefetch memory accesses.

## Table Sizes

All benchmarked tables use exclusively power-of-two sizes. This invariant allows us to translate hashes to array indices with a fast bitwise AND operation, since:

```
h % 2**n == h & (2**n - 1)
```


Power-of-two sizes also admit a neat virtual memory trick, 4 but that optimization is not included here.

However, power-of-two sizes can cause pathological behavior when paired with some hash functions, since indexing simply throws away the hash’s high bits.
An alternative strategy is to use *prime* sized tables, which are significantly more robust to the choice of hash function.
For the purposes of this post, we have a fixed hash function and non-adversarial inputs, so prime sizes were not used.[5](https://thenumb.at#fn:5)

## Hash Function

All benchmarked tables use the `squirrel3`

hash function, a fast integer hash that (as far as I can tell) only exists in [this GDC talk on noise-based RNG](https://www.youtube.com/watch?v=LWFzPP8ZbdU).

Here, it is adapted to 64-bit integers by choosing three large 64-bit primes:

```
uint64_t squirrel3(uint64_t at) {
constexpr uint64_t BIT_NOISE1 = 0x9E3779B185EBCA87ULL;
constexpr uint64_t BIT_NOISE2 = 0xC2B2AE3D27D4EB4FULL;
constexpr uint64_t BIT_NOISE3 = 0x27D4EB2F165667C5ULL;
at *= BIT_NOISE1;
at ^= (at >> 8);
at += BIT_NOISE2;
at ^= (at << 8);
at *= BIT_NOISE3;
at ^= (at >> 8);
return at;
}
```


I make no claims regarding the quality or robustness of this hash function, but observe that it’s cheap, it produces the expected number of collisions in power-of-two tables, and it passes [smhasher](https://github.com/rurban/smhasher) when applied bytewise.

## Other Benchmarks

Several less interesting benchmarks were also run, all of which exhibited identical performance across equal-memory open-addressed tables and **much** worse performance for separate chaining.

- Time to look up each element by following a
[Sattolo cycle](https://danluu.com/sattolo/)(2-4x).[6](https://thenumb.at#fn:6) - Time to clear the table (100-200x).
- Time to iterate all values (3-10x).

# Discussion

## Separate Chaining

To get our bearings, let’s first [implement](https://github.com/TheNumbat/hashtables/blob/main/code/chaining.h) a simple separate chaining table and benchmark it at various load factors.

Separate Chaining | 50% Load | 100% Load | 200% Load | 500% Load | ||||
| Existing | Missing | Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 115 | 113 | 120 | 152 | ||||
| Erase (ns/key) | 110 | 128 | 171 | 306 | ||||
| Lookup (ns/key) | 28 | 28 | 35 | 40 | 50 | 68 | 102 | 185 |
| Average Probe | 1.25 | 0.50 | 1.50 | 1.00 | 2.00 | 2.00 | 3.50 | 5.00 |
| Max Probe | 7 | 7 | 10 | 9 | 12 | 13 | 21 | 21 |
| Memory Amplification | 2.50 | 2.00 | 1.75 | 1.60 |

These are respectable results, especially lookups at 100%: the CPU is able to hide much of the memory latency. Insertions and erasures, on the other hand, are pretty slow—they involve allocation.

Technically, the reported memory amplification in an *underestimate*, as it does not include heap allocator overhead.
However, we should not *directly* compare memory amplification against the coming open-addressed tables, as storing larger values would improve separate chaining’s ratio.

`std::unordered_map`


Running these benchmarks on `std::unordered_map<uint64_t,uint64_t>`

produces results roughly equivalent to the 100% column, just with marginally slower insertions and faster clears.
Using `squirrel3`

with `std::unordered_map`

additionally makes insertions slightly slower and lookups slightly faster.
Further comparisons will be relative to these results, since exact performance numbers for `std::unordered_map`

depend on one’s standard library distribution (here, Microsoft’s).

## Linear Probing

Next, let’s [implement](https://github.com/TheNumbat/hashtables/blob/main/code/linear.h) the simplest type of open addressing—linear probing.

In the following diagrams, assume that each letter hashes to its alphabetical index. The skull denotes a *tombstone*.

Insert: starting from the key’s index, place the key in the first empty or tombstone bucket.

Lookup: starting from the key’s index, probe buckets in order until finding the key, reaching an empty non-tombstone bucket, or exhausting the table.

Erase: lookup the key and replace it with a tombstone.


The results are surprisingly good, considering the simplicity:

Linear Probing(Naive) | 50% Load | 75% Load | 90% Load | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 46 | 59 | 73 | |||
| Erase (ns/key) | 21 | 36 | 47 | |||
| Lookup (ns/key) | 20 | 86 | 35 | 124 | 47 | 285 |
| Average Probe | 0.50 | 6.04 | 1.49 | 29.5 | 4.46 | 222 |
| Max Probe | 43 | 85 | 181 | 438 | 1604 | 2816 |
| Memory Amplification | 2.00 | 1.33 | 1.11 |

For existing keys, we’re already beating the separately chained tables, and with lower memory overhead! Of course, there are also some obvious problems—looking for missing keys takes much longer, and the worst-case probe lengths are quite scary, even at 50% load factor. But, we can do much better.

### Erase: Rehashing

One simple optimization is automatically recreating the table once it accumulates too many tombstones.
Erase now occurs in *amortized* constant time, but we already tolerate that for insertion, so it shouldn’t be a big deal.
Let’s [implement](https://github.com/TheNumbat/hashtables/blob/main/code/linear_with_rehashing.h) a table that re-creates itself after erase has been called $$\frac{N}{2}$$ times.

Compared to **naive linear probing**:

Linear Probing+ Rehashing | 50% Load | 75% Load | 90% Load | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 46 | 58 | 70 | |||
| Erase (ns/key) | 23 (+10.4%) | 27 (-23.9%) | 29 (-39.3%) | |||
| Lookup (ns/key) | 20 | 85 | 35 | 93 (-25.4%) | 46 | 144 (-49.4%) |
| Average Probe | 0.50 | 6.04 | 1.49 | 9.34 (-68.3%) | 4.46 | 57.84 (-74.0%) |
| Max Probe | 43 | 85 | 181 | 245 (-44.1%) | 1604 | 1405 (-50.1%) |
| Memory Amplification | 2.00 | 1.33 | 1.11 |

Clearing the tombstones dramatically improves missing key queries, but they are still pretty slow. It also makes erase slower at 50% load—there aren’t enough tombstones to make up for having to recreate the table. Rehashing also does nothing to mitigate long probe sequences for existing keys.

### Erase: Backward Shift

Actually, who says we need tombstones? There’s a little-taught, but very simple algorithm for erasing keys that doesn’t degrade performance *or* have to recreate the table.

When we erase a key, we don’t know whether the lookup algorithm is relying on our bucket being filled to find keys later in the table.
Tombstones are one way to avoid this problem.
Instead, however, we can guarantee that traversal is never disrupted by simply *removing and reinserting all following keys*, up to the next empty bucket.

Note that despite the name, we are not simply shifting the following keys backward. Any keys that are already at their optimal index will not be moved. For example:

After [implementing](https://github.com/TheNumbat/hashtables/blob/main/code/linear_with_deletion.h) backward-shift deletion, we can compare it to **linear probing with rehashing**:

Linear Probing+ Backshift | 50% Load | 75% Load | 90% Load | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 46 | 58 | 70 | |||
| Erase (ns/key) | 47 (+105%) | 82 (+201%) | 147 (+415%) | |||
| Lookup (ns/key) | 20 | 37 (-56.2%) | 36 | 88 | 46 | 135 |
| Average Probe | 0.50 | 1.50 (-75.2%) | 1.49 | 7.46 (-20.1%) | 4.46 | 49.7 (-14.1%) |
| Max Probe | 43 | 50 (-41.2%) | 181 | 243 | 1604 | 1403 |
| Memory Amplification | 2.00 | 1.33 | 1.11 |

Naturally, erasures become significantly slower, but queries on missing keys now have reasonable behavior, especially at 50% load. In fact, at 50% load, this table already beats the performance of equal-memory separate chaining in all four metrics. But, we can still do better: a 50% load factor is unimpressive, and max probe lengths are still very high compared to separate chaining.

*You might have noticed that neither of these upgrades improved average probe length for existing keys.
That’s because it’s not possible for linear probing to have any other average!
Think about why that is—it’ll be interesting later.*

## Quadratic Probing

Quadratic probing is a common upgrade to linear probing intended to decrease average and maximum probe lengths.

In the linear case, a probe of length $$n$$ simply queries the bucket at index $$h(k) + n$$. Quadratic probing instead queries the bucket at index $$h(k) + \frac{n(n+1)}{2}$$. Other quadratic sequences are possible, but this one can be efficiently computed by adding $$n$$ to the index at each step.

Each operation must be updated to use our new probe sequence, but the logic is otherwise almost identical:

There are a couple subtle caveats to quadratic probing:

- Although this specific sequence will touch every bucket in a power-of-two table, other sequences (e.g. $$n^2$$) may not. If an insertion fails despite there being an empty bucket, the table must grow and the insertion is retried.
- There actually
*is*a[true deletion algorithm for quadratic probing](https://epubs.siam.org/doi/pdf/10.1137/1.9781611975062.3), but it’s a bit more involved than the linear case and hence not reproduced here. We will again use tombstones and rehashing.

After [implementing](https://github.com/TheNumbat/hashtables/blob/main/code/quadratic.h) our quadratic table, we can compare it to **linear probing with rehashing**:

Quadratic Probing+ Rehashing | 50% Load | 75% Load | 90% Load | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 47 | 54 (-7.2%) | 65 (-6.4%) | |||
| Erase (ns/key) | 23 | 28 | 29 | |||
| Lookup (ns/key) | 20 | 82 | 31 (-13.2%) | 93 | 42(-7.3%) | 163 (+12.8%) |
| Average Probe | 0.43 (-12.9%) | 4.81 (-20.3%) | 0.99 (-33.4%) | 5.31 (-43.1%) | 1.87 (-58.1%) | 18.22 (-68.5%) |
| Max Probe | 21 (-51.2%) | 49 (-42.4%) | 46 (-74.6%) | 76 (-69.0%) | 108 (-93.3%) | 263 (-81.3%) |
| Memory Amplification | 2.00 | 1.33 | 1.11 |

As expected, quadratic probing dramatically reduces both the average and worst case probe lengths, especially at high load factors.
These gains are not *quite* as impressive when compared to the linear table with backshift deletion, but are still very significant.

Reducing the average probe length improves the average performance of all queries. Erasures are the fastest yet, since quadratic probing quickly finds the element and marks it as a tombstone. However, beyond 50% load, maximum probe lengths are still pretty concerning.

## Double Hashing

Double hashing purports to provide even better behavior than quadratic probing. Instead of using the same probe sequence for every key, double hashing determines the probe stride by hashing the key a second time. That is, a probe of length $$n$$ queries the bucket at index $$h_1(k) + n*h_2(k)$$

- If $$h_2$$ is always co-prime to the table size, insertions always succeed, since the probe sequence will touch every bucket. That might sound difficult to assure, but since our table sizes are always a power of two, we can simply make $$h_2$$ always return an odd number.
- Unfortunately, there is no true deletion algorithm for double hashing. We will again use tombstones and rehashing.

So far, we’ve been throwing away the high bits our of 64-bit hash when computing table indices. Instead of evaluating a second hash function, let’s just re-use the top 32 bits: $$h_2(k) = h_1(k) >> 32$$.

After [implementing](https://github.com/TheNumbat/hashtables/blob/main/code/double.h) double hashing, we may compare the results to **quadratic probing with rehashing**:

Double Hashing+ Rehashing | 50% Load | 75% Load | 90% Load | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 70 (+49.6%) | 80 (+48.6%) | 88 (+35.1%) | |||
| Erase (ns/key) | 31 (+33.0%) | 43 (+53.1%) | 47 (+61.5%) | |||
| Lookup (ns/key) | 29 (+46.0%) | 84 | 38 (+25.5%) | 93 | 49 (+14.9%) | 174 |
| Average Probe | 0.39 (-11.0%) | 4.39 (-8.8%) | 0.85 (-14.7%) | 4.72 (-11.1%) | 1.56 (-16.8%) | 16.23 (-10.9%) |
| Max Probe | 17 (-19.0%) | 61 (+24.5%) | 44(-4.3%) | 83(+9.2%) | 114 (+5.6%) | 250(-4.9%) |
| Memory Amplification | 2.00 | 1.33 | 1.11 |

Double hashing succeeds in further reducing average probe lengths, but max lengths are more of a mixed bag. Unfortunately, most queries now traverse larger spans of memory, causing performance to lag quadratic hashing.

## Robin Hood Linear Probing

So far, quadratic probing and double hashing have provided lower probe lengths, but their raw performance isn’t much better than linear probing—especially on missing keys.
Enter * Robin Hood linear probing*.
This strategy drastically reins in maximum probe lengths while maintaining high query performance.

The key difference is that when inserting a key, we are allowed to steal the position of an existing key if it is closer to its ideal index (“richer”) than the new key is. When this occurs, we simply swap the old and new keys and carry on inserting the old key in the same manner. This results in a more equitable distribution of probe lengths.

This insertion method turns out to be so effective that we can entirely ignore rehashing as long as we keep track of the maximum probe length. Lookups will simply probe until either finding the key or exhausting the maximum probe length.

[Implementing](https://github.com/TheNumbat/hashtables/blob/main/code/robin_hood.h) this table, compared to **linear probing with backshift deletion**:

Robin Hood(Naive) | 50% Load | 75% Load | 90% Load | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 53 (+16.1%) | 80 (+38.3%) | 124 (+76.3%) | |||
| Erase (ns/key) | 19 (-58.8%) | 31 (-63.0%) | 77 (-47.9%) | |||
| Lookup (ns/key) | 19 | 58 (+56.7%) | 31 (-11.3%) | 109 (+23.7%) | 79 (+72.2%) | 147 (+8.9%) |
| Average Probe | 0.50 | 13 (+769%) | 1.49 | 28(+275%) | 4.46 | 67 (+34.9%) |
| Max Probe | 12 (-72.1%) | 13 (-74.0%) | 24 (-86.7%) | 28(-88.5%) | 58 (-96.4%) | 67 (-95.2%) |
| Memory Amplification | 2.00 | 1.33 | 1.11 |

Maximum probe lengths improve *dramatically*, undercutting even quadratic probing and double hashing.
This solves the main problem with open addressing.

However, performance gains are less clear-cut:

- Insertion performance suffers across the board.
- Existing lookups are slightly faster at low load, but much slower at 90%.
- Missing lookups are maximally pessimistic.

Fortunately, we’ve got one more trick up our sleeves.

### Erase: Backward Shift

When erasing a key, we can run a very similar backshift deletion algorithm. There are just two differences:

- We can stop upon finding a key that is already in its optimal location. No further keys could have been pushed past it—they would have stolen this spot during insertion.
- We don’t have to re-hash—since we stop at the first optimal key, all keys before it can simply be shifted backward.

With backshift deletion, we no longer need to keep track of the maximum probe length.

[Implementing](https://github.com/TheNumbat/hashtables/blob/main/code/robin_hood_with_deletion.h) this table, compared to **naive robin hood probing**:

Robin Hood+ Backshift | 50% Load | 75% Load | 90% Load | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 52 | 78 | 118 | |||
| Erase (ns/key) | 31 (+63.0%) | 47 (+52.7%) | 59 (-23.3%) | |||
| Lookup (ns/key) | 19 | 33 (-43.3%) | 31 | 74 (-32.2%) | 80 | 108 (-26.1%) |
| Average Probe | 0.50 | 0.75 (-94.2%) | 1.49 | 1.87 (-93.3%) | 4.46 | 4.95 (-92.6%) |
| Max Probe | 12 | 12 (-7.7%) | 24 | 25 (-10.7%) | 58 | 67 |
| Memory Amplification | 2.00 | 1.33 | 1.11 |

We again regress the performance of erase, but we finally achieve reasonable missing-key behavior. Given the excellent maximum probe lengths and overall query performance, Robin Hood probing with backshift deletion should be your default choice of hash table.

*You might notice that at 90% load, lookups are significantly slower than basic linear probing.
This gap actually isn’t concerning, and explaining why is an interesting exercise.*[7](https://thenumb.at#fn:7)

## Two-Way Chaining

Our Robin Hood table has excellent query performance, and exhibited a maximum probe length of only 12—it’s a good default choice.
However, another class of hash tables based on *Cuckoo Hashing* can *provably* never probe more than a constant number of buckets.
Here, we will examine a particularly practical formulation known as *Two-Way Chaining*.

Our table will still consist of a flat array of buckets, but each bucket will be able to hold a small handful of keys.
When inserting an element, we will hash the key with *two different* functions, then place it into whichever corresponding bucket has more space.
If both buckets happen to be filled, the entire table will grow and the insertion is retried.

You might think this is crazy—in separate chaining, the expected maximum probe length scales with $$O(\frac{\lg N}{\lg \lg N})$$, so wouldn’t this waste copious amounts of memory growing the table?
It turns out adding a second hash function reduces the expected maximum to $$O(\lg\lg N)$$, for reasons [explored elsewhere](https://www.cs.cmu.edu/afs/cs/project/pscico-guyb/realworld/www/slidesS14/load-balancing.pdf).
That makes it practical to cap the maximum bucket size at a relatively small number.

Let’s [implement](https://github.com/TheNumbat/hashtables/blob/main/code/two_way.h) a flat two-way chained table.
As with double hashing, we can use the high bits of our hash to represent the second hash function.

Two-WayChaining | Capacity 2 | Capacity 4 | Capacity 8 | |||
| Existing | Missing | Existing | Missing | Existing | Missing | |
| Insert (ns/key) | 265 | 108 | 111 | |||
| Erase (ns/key) | 24 | 34 | 45 | |||
| Lookup (ns/key) | 23 | 23 | 30 | 30 | 39 | 42 |
| Average Probe | 0.03 | 0.24 | 0.74 | 2.73 | 3.61 | 8.96 |
| Max Probe | 3 | 4 | 6 | 8 | 13 | 14 |
| Memory Amplification | 32.00 | 4.00 | 2.00 |

Since every key can be found in one of two possible buckets, query times become essentially deterministic. Lookup times are especially impressive, only slightly lagging the Robin Hood table and having no penalty on missing keys. The average probe lengths are very low, and max probe lengths are strictly bounded by two times the bucket size.

The table size balloons when each bucket can only hold two keys, and insertion is very slow due to growing the table. However, capacities of 4-8 are reasonable choices for memory unconstrained use cases.

Overall, two-way chaining is another good choice of hash table, at least when memory efficiency is not the highest priority. In the next section, we’ll also see how lookups can even further accelerated with prefetching and SIMD operations.

*Remember that deterministic queries might not matter if you haven’t already implemented incremental table growth.*

### Cuckoo Hashing

[Cuckoo hashing](https://www.brics.dk/RS/01/32/BRICS-RS-01-32.pdf) involves storing keys in two separate tables, each of which holds one key per bucket.
This scheme will guarantee that every key is stored in its ideal bucket in one of the two tables.

Each key is hashed with two different functions and inserted using the following procedure:

- If at least one table’s bucket is empty, the key is inserted there.
- Otherwise, the key is inserted anyway, evicting one of the existing keys.
- The evicted key is transferred to the opposite table at its other possible position.
- If doing so evicts another existing key, go to 3.

If the loop ends up evicting the key we’re trying to insert, we know it has found a cycle and hence must grow the table.

Because Cuckoo hashing does not strictly bound the insertion sequence length, I didn’t benchmark it here, but it’s still an interesting option.

# Unrolling, Prefetching, and SIMD

So far, the lookup benchmark has been implemented roughly like this:

```
for(uint64_t i = 0; i < N; i++) {
assert(table.find(keys[i]) == values[i]);
}
```


Naively, this loop runs one lookup at a time.
However, you might have noticed that we’ve been able to find keys *faster than the CPU can load data from main memory*—so something more complex must be going on.

In reality, modern out-of-order CPUs can execute several iterations in parallel. Expressing the loop as a dataflow graph lets us build a simplified mental model of how it actually runs: the CPU is able to execute a computation whenever its dependencies are available.

Here, green nodes are resolved, in-flight nodes are yellow, and white nodes have not begun:

In this example, we can see that each iteration’s root node (`i++`

) only requires the value of `i`

from the previous step—**not** the result of `find`

.
Therefore, the CPU can run several `find`

nodes in parallel, hiding the fact that each one takes ~100ns to fetch data from main memory.

## Unrolling

There’s a common optimization strategy known as *loop unrolling*.
Unrolling involves explicitly writing out the code for several *semantic* iterations inside each *actual* iteration of a loop.
When each inner pseudo-iteration is independent, unrolling explicitly severs them from the loop iterator dependency chain.

Most modern x86 CPUs can keep track of ~10 simultaneous pending loads, so let’s try manually unrolling our benchmark 10 times.
The new code looks like the following, where `index_of`

hashes the key but doesn’t do the actual lookup.

```
uint64_t indices[10];
for(uint64_t i = 0; i < N; i += 10) {
for(uint64_t j = 0; j < 10; j++) {
indices[j] = table.index_of(keys[i + j]);
}
for(uint64_t j = 0; j < 10; j++) {
assert(table.find_index(indices[j]) == values[i + j]);
}
}
```


This isn’t true unrolling, since the inner loops introduce dependencies on `j`

.
However, it doesn’t matter in practice, as computing `j`

is never a bottleneck.
In fact, our compiler can automatically unroll the inner loop for us (`clang`

in particular does this).

Lookups (ns/find) | Naive | Unrolled |
| Separate Chaining (100%) | 35 | 34 |
| Linear (75%) | 36 | 35 |
| Quadratic (75%) | 31 | 31 |
| Double (75%) | 38 | 37 |
| Robin Hood (75%) | 31 | 31 |
| Two-Way Chaining (x4) | 30 | 32 |

Explicit unrolling has basically no effect, since the CPU was already able to saturate its pending load buffer.
However, manual unrolling now lets us introduce *software prefetching*.

## Software Prefetching

When traversing memory in a predictable pattern, the CPU is able to preemptively load data for future accesses.
This capability, known as *hardware prefetching*, is the reason our flat tables are so fast to iterate.
However, hash table *lookups* are inherently unpredictable: the address to load is determined by a hash function.
That means hardware prefetching cannot help us.

Instead, we can explicitly ask the CPU to prefetch address(es) we will load from in the near future.
Doing so can’t speed up an individual lookup—we’d immediately wait for the result—but software prefetching can accelerate batches of queries.
Given several keys, we can compute where each query *will* access the table, tell the CPU to prefetch those locations, and **then** start actually accessing the table.

To do so, let’s make `table.index_of`

prefetch the location(s) examined by `table.find_indexed`

:

- In open-addressed tables, we prefetch the slot the key hashes to.
- In two-way chaining, we prefetch
*both*buckets the key hashes to.

Importantly, prefetching requests the entire cache line for the given address, i.e. the aligned 64-byte chunk of memory containing that address. That means surrounding data (e.g. the following keys) may also be loaded into cache.

Lookups (ns/find) | Naive | Unrolled | Prefetched |
| Separate Chaining (100%) | 35 | 34 | 26 (-22.6%) |
| Linear (75%) | 36 | 35 | 23 (-36.3%) |
| Quadratic (75%) | 31 | 31 | 22 (-27.8%) |
| Double (75%) | 38 | 37 | 33 (-12.7%) |
| Robin Hood (75%) | 31 | 31 | 22 (-29.4%) |
| Two-Way Chaining (x4) | 30 | 32 | 19 (-40.2%) |

Prefetching makes a big difference!

- Separate chaining benefits from prefetching the unpredictable initial load.
[8](https://thenumb.at#fn:8) - Linear and quadratic tables with a low average probe length greatly benefit from prefetching.
- Double-hashed probe sequences quickly leave the cache line, making prefetching a bit less effective.
- Prefetching is ideal for two-way chaining: keys can
*always*be found in a prefetched cache line—but each lookup requires fetching two locations, consuming extra load buffer slots.

## SIMD

Modern CPUs provide SIMD (single instruction, multiple data) instructions that process multiple values at once. These operations are useful for probing: for example, we can load a batch of $$N$$ keys and compare them with our query in parallel. In the best case, a SIMD probe sequence could run $$N$$ times faster than checking each key individually.

Let’s [implement](https://github.com/TheNumbat/hashtables/blob/main/code/two_way_simd.h) SIMD-accelerated lookups for linear probing and two-way chaining, with $$N=4$$:

Lookups (ns/find) | Naive | Unrolled | Prefetched | Missing |
| Linear (75%) | 36 | 35 | 23 | 88 |
| SIMD Linear (75%) | 39 (+10.9%) | 42 (+18.0%) | 27 (+19.1%) | 98 (-21.2%) |
| Two-Way Chaining (x4) | 30 | 32 | 19 | 30 |
| SIMD Two-Way Chaining (x4) | 28 (-6.6%) | 30 (-4.6%) | 17 (-9.9%) | 19 (-35.5%) |

Unfortunately, SIMD probes are *slower* for the linearly probed table—an average probe length of $$1.5$$ meant the overhead of setting up an (unaligned) SIMD comparison wasn’t worth it.
However, missing keys are found faster, since their average probe length is much higher ($$29.5$$).

On the other hand, two-way chaining consistently benefits from SIMD probing, as we can find any key using at most two (aligned) comparisons. However, given a bucket capacity of four, lookups only need to query 1.7 keys on average, so we only see a slight improvement—SIMD would be a much more impactful optimization at higher capacities. Still, missing key lookups get significantly faster, as they previously had to iterate through all keys in the bucket.

# Benchmark Data

*Updated 2023/04/05: additional optimizations for quadratic, double hashed, and two-way tables.*

- The linear and Robin Hood tables use backshift deletion.
- The two-way SIMD table has capacity-4 buckets and uses AVX2 256-bit SIMD operations.
- Insert, erase, find, find unrolled, find prefetched, and find missing report nanoseconds per operation.
- Average probe, max probe, average missing probe, and max missing probe report number of iterations.
- Clear and iterate report milliseconds for the entire operation.
- Memory reports the ratio of allocated memory to size of stored data.

Table | Insert | Erase | Find | Unrolled | Prefetched | Avg Probe | Max Probe | Find DNE | DNE Avg | DNE Max | Clear (ms) | Iterate (ms) | Memory |
| Chaining 50 | 115 | 110 | 28 | 26 | 21 | 1.2 | 7 | 28 | 0.5 | 7 | 113.1 | 16.2 | 2.5 |
| Chaining 100 | 113 | 128 | 35 | 34 | 26 | 1.5 | 10 | 40 | 1.0 | 9 | 118.1 | 13.9 | 2.0 |
| Chaining 200 | 120 | 171 | 50 | 50 | 37 | 2.0 | 12 | 68 | 2.0 | 13 | 122.6 | 14.3 | 1.8 |
| Chaining 500 | 152 | 306 | 102 | 109 | 77 | 3.5 | 21 | 185 | 5.0 | 21 | 153.7 | 23.0 | 1.6 |
| Linear 50 | 46 | 47 | 20 | 20 | 15 | 0.5 | 43 | 37 | 1.5 | 50 | 1.1 | 4.8 | 2.0 |
| Linear 75 | 58 | 82 | 36 | 35 | 23 | 1.5 | 181 | 88 | 7.5 | 243 | 0.7 | 2.1 | 1.3 |
| Linear 90 | 70 | 147 | 46 | 45 | 29 | 4.5 | 1604 | 135 | 49.7 | 1403 | 0.6 | 1.2 | 1.1 |
| Quadratic 50 | 47 | 23 | 20 | 20 | 16 | 0.4 | 21 | 82 | 4.8 | 49 | 1.1 | 5.1 | 2.0 |
| Quadratic 75 | 54 | 28 | 31 | 31 | 22 | 1.0 | 46 | 93 | 5.3 | 76 | 0.7 | 2.1 | 1.3 |
| Quadratic 90 | 65 | 29 | 42 | 42 | 30 | 1.9 | 108 | 163 | 18.2 | 263 | 0.6 | 1.0 | 1.1 |
| Double 50 | 70 | 31 | 29 | 28 | 23 | 0.4 | 17 | 84 | 4.4 | 61 | 1.1 | 5.6 | 2.0 |
| Double 75 | 80 | 43 | 38 | 37 | 33 | 0.8 | 44 | 93 | 4.7 | 83 | 0.8 | 2.2 | 1.3 |
| Double 90 | 88 | 47 | 49 | 49 | 42 | 1.6 | 114 | 174 | 16.2 | 250 | 0.6 | 1.0 | 1.1 |
| Robin Hood 50 | 52 | 31 | 19 | 19 | 15 | 0.5 | 12 | 33 | 0.7 | 12 | 1.1 | 4.8 | 2.0 |
| Robin Hood 75 | 78 | 47 | 31 | 31 | 22 | 1.5 | 24 | 74 | 1.9 | 25 | 0.7 | 2.1 | 1.3 |
| Robin Hood 90 | 118 | 59 | 80 | 79 | 41 | 4.5 | 58 | 108 | 5.0 | 67 | 0.6 | 1.2 | 1.1 |
| Two-way x2 | 265 | 24 | 23 | 25 | 17 | 0.0 | 3 | 23 | 0.2 | 4 | 17.9 | 19.6 | 32.0 |
| Two-way x4 | 108 | 34 | 30 | 32 | 19 | 0.7 | 6 | 30 | 2.7 | 8 | 2.2 | 3.7 | 4.0 |
| Two-way x8 | 111 | 45 | 39 | 39 | 28 | 3.6 | 13 | 42 | 9.0 | 14 | 1.1 | 1.5 | 2.0 |
| Two-way SIMD | 124 | 46 | 28 | 30 | 17 | 0.3 | 1 | 19 | 1.0 | 1 | 2.2 | 3.7 | 4.0 |

## Footnotes

Actually, this prior shouldn’t necessarily apply to hash tables, which by definition have unpredictable access patterns. However, we will see that flat storage still provides performance benefits, especially for linear probing, whole-table iteration, and serial accesses.

[↩︎](https://thenumb.at#fnref:1)To account for various deletion strategies, the

`find-missing`

benchmark was run after the insertion & erasure tests, and after inserting a second set of elements. This sequence allows separate chaining’s reported maximum probe length to be larger for missing keys than existing keys. Looking up the latter set of elements was also benchmarked, but results are omitted here, as the tombstone-based tables were simply marginally slower across the board.[↩︎](https://thenumb.at#fnref:2)AMD 5950X @ 4.4 GHz + DDR4 3600/CL16, Windows 11 Pro 22H2, MSVC 19.34.31937.


No particular effort was made to isolate the benchmarks, but they were repeatable on an otherwise idle system. Each was run 10 times and average results are reported.[↩︎](https://thenumb.at#fnref:3)Virtual memory allows separate regions of our address space to refer to the

*same*underlying pages. If we map our table*twice*, one after the other, probe traversal never has to check whether it needs to wrap around to the start of the table. Instead, it can simply proceed into the second mapping—since writes to one range are automatically reflected in the other, this just works.[↩︎](https://thenumb.at#fnref:4)You might expect indexing a prime-sized table to require an expensive integer mod/div, but it actually doesn’t. Given a fixed set of possible primes, a prime-specific indexing operation can be selected at runtime based on the current size. Since each such operation is a modulo by a

*constant*,[the compiler can translate it to a fast integer multiplication](https://lemire.me/blog/2021/04/28/ideal-divisors-when-a-division-compiles-down-to-just-a-multiplication/).[↩︎](https://thenumb.at#fnref:5)A Sattolo traversal causes each lookup to directly depend on the result of the previous one, serializing execution and preventing the CPU from hiding memory latency. Hence, finding each element took ~

[100ns](https://gist.github.com/jboner/2841832)in*every*type of open table: roughly equal to the latency of fetching data from RAM. Similarly, each lookup in the low-load separately chained table took ~200ns, i.e. $$(1 + \text{Chain Length}) * \text{Memory Latency}$$[↩︎](https://thenumb.at#fnref:6)First,

*any*linearly probed table requires the same*total*number of probes to look up each element once—that’s why the average probe length never improved. Every hash collision requires moving some key one slot further from its index, i.e. adds one to the total probe count.Second, the cost of a lookup, per probe, can

*decrease*with the number of probes required. When traversing a long chain, the CPU can avoid cache misses by prefetching future accesses. Therefore, allocating a larger portion of the same*total*probe count to long chains can increase performance.Hence, linear probing tops this particular benchmark—but it’s not the most useful metric in practice. Robin Hood probing greatly decreases maximum probe length, making query performance far more consistent even if technically slower on average. Anyway, you really don’t need a 90% load factor—just use 75% for consistently high performance.

[↩︎](https://thenumb.at#fnref:7)Is the CPU smart enough to automatically prefetch addresses contained within the explicitly prefetched cache line? I’m pretty sure it’s not, but that would be cool.

[↩︎](https://thenumb.at#fnref:8)