---
title: Multithreaded Gameplay
url: https://bitsquid.blogspot.com/2015/03/multithreaded-gameplay.html
author: Niklas
published: '2015-03-10'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I've written [before](http://bitsquid.blogspot.se/2009/10/multithreaded-gameplay.html) about multithreading gameplay, but since I didn't really come to any conclusion I think it is time to revisit the topic.

As the number of processors and cores in consumer hardware keeps increasing, [Amdahl's law](http://en.wikipedia.org/wiki/Amdahl's_law) tells us that any single-threaded part of the code will have a bigger and bigger effect on the performance. (As long as you are not memory bound, so keep those caches happy, ok?)

So even if single-threaded gameplay isn't a problem today it soon will be. At some point the elephant will outgrow the living room.

There are (at least) three problems with multithreading gameplay code as we know it:

Writing and reading multithreaded code is much harder than single threaded code, especially for "messy" stuff such as gameplay code.

Gameplay code tend to be more sprawling than engine code, touching all kinds of systems, which means that the standard optimisation technique of finding the hotspots and multithreading them is less likely to work.

Lua, which we use as our scripting language, does not have built-in multithreading support. This might not be a problem for you. On the other hand, if you expect your gameplay programmers to write multithreaded C++ code, you probably have other problems.


If we start with the first point, I don't think it is reasonable to expect gameplay programmers to write safe and efficient multithreaded code using the standard techniques of mutexes, locks, queues, semaphores, atomic operations, etc. Especially not when writing messy gameplay code where requirements often change and experimentation and quick iterations are important. If anyone has experience of this, I'd like to know.

So I think the primary goal is to find a multithreading model that is *easy* to work with.

To me, the best (easiest and safest) model seems to be the [Actor model](http://en.wikipedia.org/wiki/Actor_model) used for example by [Erlang](http://en.wikipedia.org/wiki/Erlang_(programming_language)) and [Scala](http://en.wikipedia.org/wiki/Scala_(programming_language)).

You can read up on the actor model if you are not familiar with it. The basic idea is that processing nodes only touch their own local memory and communicate with other nodes through asynchronous message passing. Since there is no shared memory, explicit synchronization primitives are not necessary.

Luckily for us, using this model also takes care of issue #3. If the nodes don't need to share memory, we can let them live in separate Lua VMs that communicate through message passing. Typically we would spawn a separate Lua VM for each processing core in our system.

As a completely contrived example, suppose we had a bunch of numbers that we needed to factor. We could then split them up by our number of VMs and send each VM a message [`'factor'`

, *n*]. Each VM would compute its factors in parallel and send the result back to the main thread.

All fine and dandy. This would work well and give us a good performance boost. But of course, this contrived example is *absolutely nothing like* real gameplay code.

In real gameplay code, we don't have pockets of completely isolated but computationally intensive code that lends itself to easy parallelization. (If we do, that code should probably be moved *out of* the gameplay code and *into* the engine.)

Instead, most gameplay code interacts with the world and does things like moving a unit a little bit, casting a physics ray, adjusting the position of another unit, etc. Unless we can paralelize that kind of *messy* code, we won't have gained very much.

The problem here is that your engine is probably a big ball of mutable state. If it isn't, congratulations to you I guess. You have figured out something we others haven't and I look forward to your next GDC talk. But for the sake of argument, let's assume that it is.

Any interaction with this mutable state (say a script calling `PhysicsWorld.raycast()`

) is a potential for threading issues.

We *could* try to make the entire script API thread-safe. For example, we could put a critical section in each API call. But that is unlikely to make anyone happy. With so many critical sections, we will probably loose whatever performance we hoped to gain from multithreading.

So we seem to be at an impasse. Gameplay code will need to interact frequently with a lot of engine APIs and making those APIs thread-safe will likely kill performance.

I've been stuck here for a while. To be honest, a couple of years. (Hey, it's not like I haven't had other stuff to do.) But in the general creative atmosphere of GDC and a discussion with some colleagues and the nice people at [Pixeldiet](http://pixeldiet.se), something shook loose.

Instead of synchronizing at each function call, what if we did it at the level of the API:

```
Unit = LuaThreads.lock_api("Unit", player, LockType.WRITE)
...
Unit.set_position(0, Vector3(0,0,0))
# Do other stuff with the player
...
LuaThreads.unlock_api(Unit)
```


In this model, the Lua VM for the threads start with a blank slate. There are no public APIs (except for safe, functional APIs that don't touch mutable state). To do anything with the engine, you must obtain a lock for a particular API.

You could argue that this is nothing than another shade of the complicated explicit multithreading model that we wanted to get rid of to begin with, but I do think there is something different here.

First, since the Lua part of the code will use the Actor model, we have eliminated all the problems with synchronizing the Lua state.

Second, since you can't use an API before locking in it there is a safety mechanism that prevents you from accidentally using multithreading the wrong way.

In this model, the main Lua thread (yes there would still be a *main* Lua thread) would spawn of a number of jobs for performing a computation intensive task, such as updating a number of units. The main Lua thread would be suspended while the task was performed. (We can only avoid suspension if the main thread also uses the locking mechanism to access the APIs, but that seems too cumbersome.)

The worker Lua threads lock the APIs they need to perform their tasks, and when they have completed the control returns back to the main Lua thread that can gather the results.

Since Lua supports [coroutines](http://en.wikipedia.org/wiki/Coroutine) (aka green threads) the `lock_api()`

function does not have to lock the thread if an API is locked by someone else, we can just switch to a different coroutine.

This model is certainly not perfect. It's a bit annoying that we still have to have a main Lua thread that is "special". It's also a pity that the main Lua thread can't continue to run while the jobs are being executed, since that could allow for greater parallelism.

And it is certainly possible for the gameplay programmer to mess up. For example, it is easy to create a deadlock by requiring the same APIs in different orders in different threads.

But still, to me this seems like the best solution, and something that would actually be worthwhile for the gameplay programmers (unlike some of my previous ideas). So I think I will start tinkering with it and see if it will fly.

I'm a bit confused about how the lock_api call works. Is it locking the entire Unit API, or just Unit API calls on that player entity?

ReplyDeleteIn this case just for this entity. The returned Unit table is locked to operate on just that unit.


ReplyDeleteYou could allow locking of an entire API as well, but for Units I think it make sense to lock on the entity level.

This comment has been removed by the author.

ReplyDeleteSorry! made a few typos so removed the comment :-/





ReplyDeleteDid you ever watch this (old) talk by Rich Hickey about living in a threaded world? http://www.infoq.com/presentations/Are-We-There-Yet-Rich-Hickey

Pretty salient to this discussion I think, I've toyed with the idea of implementing the sort of system he talks about in this presentation just for fun but I keep not getting around to it..

Another thing I've toyed with - which I know some people do already - is to avoid the mutability issue by double buffering some or all of the game state (e.g. post a read-only snapshot of the physics state each frame and use that for gameplay).

The double buffering might be a better idea to hide the nasty locking away from the game programmers. Sure, it requires some work and sacrifice some RAM, but depending on what game state you are mirroring, it shouldn't be such a big deal.

ReplyDeleteFrom there, the only part that needs to be thread safe is the called subsystem (eg. physics.raycast or whatever, in which case I would enqueue the raycast request and provide the results to some callback routine or next update frame, and not immediately/synced).

So, I would rather choose data cloning (if memory is not such a sensitive issue) instead of manually and tediously locking/unlocking parts of the game code systems, especially at a higher level such as Lua logic script.

Locking is also more prone to user errors, unless is reentrant or something.

In my humble personal experience with threading, I've come to the conclusion that double data buffering is the safest, most elegant (yet chubby) way of processing data in parallel, and every time I am designing a system to use many threads for data processing, double buffering is quite enjoyable to implement, and worry free :), with the price of more memory used, but at least on newer platforms and the data structures mirrored, this is not an issue.

Stay away from locking as much as possible, especially when the frequency is quite high in your example, what will happen when you run that over 10000+ game entities ?

Maybe a dumb question, but what if the update of the game is based in some event driven approuch? For exemple, in the game update tick, the objects are all updated in parallel (they consume events generated for them) and the output events generated this tick is used as input for the next frame(This can include the engine services as receiver of events too)?

ReplyDeleteAs long as the update is completely internal and uses the event system to communicate with other systems this would work (for a language with multi-threaded support).




DeleteBut this approach has two problems: latency and complexity.

Latency occurs when an action depends on a chain of events. For example, an AI may want to cast a ray, depending on what that hits cast another ray. Depending on that ask a friend for their health, and depending on that decide what to do. If there are 10 steps in that decision chain then it will take 20 frames until the AI can make its decision.

Complexity occurs because you now have multiple "execution threads" in various states of execution "in flight" at any one point. It can be really hard to get an overview of what is actually going on. Also, the target of events may disappear (get killed) so every system will need to be able to handle aborted events.

Thanks for the reply, I'm happy I found some blog with interesting content and a lot of thinking to make the algorithms run fast, this is what I love in programming (Sad that here the majority of enterprises want a more agile approuch to solution delivery - do the work in half a hour and if it's not crashing you're good to go)


DeleteYou're right, there'll be a lot of latency if the update is not in control of the engine and the complexity is a trade for efficiency (until the game crashes for some unknown reason xD)

I don't have so much experience with very big and complex games, so this event driven ideia come to mind based in a simple game maker that I saw a long long time ago: Click&Play

You have a matrix with intersections of objects that you can script triggers for them when they overlap, when there's some timeout, etc.

Again, this is not hard to paralellize, but maybe only works for simple games =)

Download, Install & Activate Microsoft office 365 for home , professional & Business purpose. Also get full technical support for office setup installation. Visit : office.com/setup for more details.


ReplyDeleteI also see these 3 errors. Thanks for method to solve it abcya

ReplyDeleteI am surfing internet on a daily basis and I always protect my connection with the different kinds of VPN/ Make sure you read this review https://vpnwelt.com/nordvpn-review/ to get some idea on what I am talking about

ReplyDeleteThis is the best guide thank you very much. Yellowstone Coat

ReplyDeletegoogle 1760

ReplyDeletegoogle 1761

google 1762

google 1763

google 1764

google 875

ReplyDeletegoogle 876

google 877

google 878

google 879

google 880

google 881

google 4321

ReplyDeletegoogle 4322

google 4323

google 4324

google 4325





ReplyDeleteslotxo auto

เล่นแล้วติดใจ

Informative guideline. It save in my memory. Squid Game Icons Red Hoodie with Free T-Shirt

ReplyDeleteWe understand that standing on the sidelines of the stock market can be frustrating. Our live, real stock market overview will help you stay up to date on Truff Stock . With our simple interface and real time quotes, staying on top of your stocks is now easier than ever!


ReplyDeleteYour Blog is very informative Plz Approve






ReplyDeleteGuppy Gold Logistics

Guppy Gold offers a number of air freight services with day-specific or day-definite scheduling, and door-to-door service. We have a wide variety of air freight services such as express, on-board courier, daily flights, and consolidated services.

Low-Cost Air Freight Forwarding Services.

Our Services

1. Best USA Freight Forwarders in Delhi NCR and India

2. Shipping to India from USA

3. Railway Logistics

4. Third Party Import Export

5. Trucking & Delivery

6. Best Custom Clearance Agents in Delhi

Email: info@guppygold.com

Phone: +91 859-585-1414

https://www.guppygold.com/

I found your blog via Google while searching for such kind of informative post and your post looks very interesting for me Astros Starter Black Varsity Jacket



ReplyDelete진안출장안마

ReplyDelete무주출장안마

장수출장안마

임실출장안마

순창출장안마

고창출장안마

부안출장안마

서울출장안마

고흥콜걸

ReplyDelete구례콜걸

곡성콜걸

광양콜걸

담양콜걸

나주콜걸

순천콜걸

여수콜걸

This comment has been removed by the author.

ReplyDeleteThis post is so informative. Thanks for sharing your knowledge!

ReplyDeleteSuch a great read! The Hand Painted Stoles mentioned here are perfect for both casual and festive wear.

ReplyDelete