---
title: APIs are About Policy
url: https://acko.net/blog/apis-are-about-policy/
author: Steven Wittens
published: '2019-07-26'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![APIs are About Policy](../../assets/235106285be95b47.jpg)

# APIs are About Policy

## A pox on both houses

“The Web is a system, Neo. That system is our enemy. But when you're inside, you look around, what do you see? Full-stack engineers, web developers, JavaScript ninjas. The very minds of the people we are trying to save.

But until we do, these people are still a part of that system and that makes them our enemy. You have to understand, most of these people are not ready to be unplugged. And many of them are so inured, so hopelessly dependent on the system, that they will fight to protect it.

Were you listening to me, Neo? Or were you looking at the widget library in the red dress?"

...

"What are you trying to tell me, that I can dodge unnecessary re-renders?"

"No Neo. I'm trying to tell you that when you're ready, you won't have to."


The web is always moving and shaking, or more precisely, shaking *off* whatever latest fad has turned out to be a mixed blessing after all. Specifically, the latest hotness for many is GraphQL, slowly but surely dethroning King REST. This means changing the way we shove certain data into certain packets. This then requires changing the code responsible for packing and unpacking that data, as well as replacing the entire digital last mile of routing it at both source and destination, despite the fact that all the actual infrastructure in between is unchanged. This is called full stack engineering. Available for hire now.

The expected custom and indeed, regular passtime, is of course to argue for or against, the old or the new. But instead I'd like to tell you why both are completely wrong, for small values of complete. You see, APIs are about policy.

## RESTless API

Take your typical RESTful API. I say typical, because an *actual* Representationally State Transferred API is as common as a unicorn. A client talks to a server by invoking certain methods on URLs over HTTP, let's go with that.

Optimists will take a constructive view. The API is a tool of empowerment. It enables you to do certain things in your program you couldn't do before, and that's why you are importing it as a dependency to maintain. The more methods in the swagger file, the better, that's why it's called swagger.

But instead I propose a subtractive view. The API is a tool of imprisonment. Its purpose is to take tasks that you are perfectly capable of doing yourself, and to separate them from you with bulletproof glass and a shitty telephone handset. One that is usually either too noisy or too quiet, but never just right. Granted, sometimes this is self-inflicted or benign, but rarely both.

This is also why there are almost no real REST APIs. If we consult the [book of difficult-to-spot lies](https://en.wikipedia.org/wiki/Representational_state_transfer), we learn that the primary features of a REST API are Statelessness, Cacheability, Layeredness, Client-Side Injection and a Uniform Interface. Let's check them.

*Statelessness* means a simple generality. URLs point to blobs, which are GET and PUT atomically. All the necessary information is supplied with the request, and no state is retained other than the contents saved and loaded. Multiple identical GETs and PUTs are idempotent. The DELETE verb is perhaps a PUT of a null value. So far mostly good. The PATCH verb is arguably a stateless partial PUT, and might be idempotent in some implementations, but only if you don't think too much about it. Which means a huge part of what remains are POST requests, the bread and butter of REST APIs, and those aren't stateless or idempotent at all.

*Cacheability* and *layeredness* (i.e. HTTP proxies) in turn have both been made mostly irrelevant. The move to HTTPS everywhere means the layering of proxies is more accurately termed a man-in-the-middle attack. That leaves mainly reverse proxying on the server or CDN side. The HTTP Cache-Control headers are also completely backwards in practice. For anything that isn't immutable, the official mechanism for cache invalidation is for a server to make an educated guess when its own data is going to become stale, which it can almost never know. If they guess too late, the client will see stale data. If they guess too soon, the client has to make a remote request before using their local cache, defeating the point. This was designed for a time when transfer time dominated over latency, whereas now we have the opposite problem. Common practice now is actually for the server to tag cacheable URLs with a revision ID, turning a *mutable resource at an immutable URL* into an *immutable resource at a mutable URL*.

*Client-Side Injection* on the other hand, i.e. giving a browser JavaScript to run, is obviously here to stay, but still, no sane REST API makes you interpret JavaScript code to interact with it. That was mostly a thing Rubyists did in their astronautical pursuits to minimize the client/server gap from their point of view. In fact, we have entirely the opposite problem: we all want to pass bits of code *to* a server, but that's unsafe, so we find various ways of encoding lobotomized chunks of not-code and pretend that's sufficient.

Which leaves us with the need for a *uniform interface*, a point best addressed with a big belly laugh and more swagger definition file.

Take the most common REST API of them all, and the one nearly everyone gets wrong, `/user`

. User accounts are some of the most locked up objects around, and as a result, this is a prime candidate for breaking all the rules.

The source of truth is usually something like:

| ID | Handle | Real Name | Password Hash | Picture | Karma | Admin | |
|---|---|---|---|---|---|---|---|
| 1 | admin@example.com | admin | John Doe | sd8ByTq86ED... | s3://bucket/1.jpg | 5 | true |
| 2 | jane@example.com | jane | Jane Doe | j7gREnf63pO... | s3://bucket/2.jpg | -3 | false |

But if you `GET /user/2`

, you likely see:

```
{
"id": 2,
"handle": "jane",
"picture": "s3://bucket/2.jpg"
}
```


Unless *you* are Jane Doe, receiving:

```
{
"id": 2,
"email": "jane@example.com",
"handle": "jane",
"name": "Jane Doe",
"picture": "s3://bucket/2.jpg"
}
```


Unless you are *John* Doe, the admin, who'll get:

```
{
"id": 2,
"email": "jane@example.com",
"handle": "jane",
"name": "Jane Doe",
"picture": "s3://bucket/2.jpg",
"karma": -3,
"admin": false
}
```


What is supposedly a stateless, idempotent, cacheable, proxiable and uniform operation turns out to be a sparse GET of a database row, differentiated by both the subject and the specific objects being queried, which opaquely determines the specific variant we get back. People say horizontal scaling means treating a million users as if they were one, but did they ever check how true that actually was?

I'm not done yet. These GETs won't even have matching PUTs, because likely the only thing Jane was allowed to do initially was:

**POST /user/create**


```
{
"name": "Jane Doe",
"email": "jane@example.com",
"password": "hunter2"
}
```


Note the subtle differences with the above.

- She couldn't supply her own picture URL directly, she will have to upload the actual file to S3 through another method. This involves asking the API for one-time permission and details to do so, after which her user record will be updated behind the scenes. Really, the type of
`picture`

is not`string`

, it is a bespoke read-only`boolean`

wearing a foreign key outfit. - She didn't get to pick her own
`id`

either. Its appearance in the GET body is actually entirely redundant, because it's merely humoring you by echoing back the number you gave it in the URL. Which it assigned to you in the first place. It's not part of the data, it's metadata... or rather the URL is. See, unless you put the string`/user/`

before the`id`

you can't actually do anything with it.`id`

is not even metadata, it's truncated metadata; unless you're crazy enough to have a REST API where IDs are mutable, in which case, stop that. - One piece of truth "data," the password hash, actually never appears in either GETs or POSTs. Only the unencoded password, which is shredded as soon as it's received, and never given out. Is the hash also metadata? Or is it the result of policy?

`PATCH /user/:id/edit`

is left as an exercise for the reader, but consider what happens when Jane tries to change her own email address? What about when John tries to change Jane's? Luckily nobody has ever accidentally mass emailed all their customers by running some shell scripts against their own API.

Neither from the perspective of the client, nor that of the server, do we have a `/user`

API that saves and loads user objects. There is no consistent JSON schema for the client—not even among a given single type during a single "stateless" session—nor idempotent whole row updates in the database.

Rather, there is an endpoint which allows you to read/write one or more columns in a row in the user table, according to certain very specific rules per column. This is dependent not just on the field types and values (i.e. data integrity), but on the *authentication state* (i.e. identity and permission), which comes via an HTTP header and requires extra data and lookups to validate.

If there was no client/server gap, you'd just have data you owned fully and which you could manipulate freely. The effect and purpose of the API is to prevent that from happening, which is why REST is a lie in the real world. The only true REST API is a freeform key/value store. So I guess S3 and CouchDB qualify, but neither's access control or query models are going to win any awards for elegance. [When "correctly" locked down](https://docs.couchdb.org/en/stable/intro/security.html#users-public-information), CouchDB too will be a document store that doesn't return the same kind of document contents for different subjects and objects, but it will at least give you a single ID for the true underlying data and its revision. It will even tell you in real-time when it changes, a superb feature, but one that probably should have been built into the application-session-transport-whatever-this-is layer as the `SUBSCRIBE`

HTTP verb.

Couch is the exception though. In the usual case, if you try to cache any of your responses, you usually have too much or too little data, no way of knowing when and how it changed without frequent polling, and no way of reliably identifying let alone ordering particular snapshots. If you try to PUT it back, you may erase missing fields or get an error. Plus, I know your Express server spits out some kind of ETag for you with every response, but, without looking it up, can you tell me specifically what that's derived from and how? Yeah I didn't think so. If that field meant anything to you, you'd be the one supplying it.

If you're still not convinced, you can go through this exercise again but with a fully normalized SQL database. In that case, the `/user`

API implementation reads/writes several tables, and what you have is a facade that allows you to access and modify one or more columns in specific rows in these particular tables, cross referenced by meaningless internal IDs you probably don't see. The rules that govern these changes are fickle and unknowable, because you trigger a specific set of rules through a combination of URL, HTTP headers, POST body, and internal database state. If you're lucky your failed attempts will come back with some notes about how you might try to fix them individually, if not, too bad, computer says no.

For real world apps, it is generally impossible by construction for a client to create and maintain an accurate replica of the data they are supposed to be able to query and share ownership of.

## Regressive Web Apps

I can already hear someone say: *my* REST API is clean! My data models are well-designed! All my endpoints follow the same consistent pattern, all the verbs are used correctly, there is a single source of truth for every piece of data, and all the schemas are always consistent!

So what you're saying is that you wrote or scaffolded the exact same code to handle the exact same handful of verbs for all your different data types, each likely with their own Model(s) and Controller(s), and their own URL namespace, without any substantial behavioral differences between them? And you think this is good?

As an aside, consider how long ago people figured out that password hashes should go in the `/etc/shadow`

file instead of the now misnamed `/etc/passwd`

. This is a one-to-one mapping, the kind of thing database normalization explicitly doesn't want you to split up, with the same repeated "primary keys" in both "tables". This duplication is actually good though, because the OS' user API implements Policy™, and the rules and access patterns for shell information are entirely different from the ones for password hashes.

You see, if APIs are about policy and not empowerment, then it absolutely makes sense to store and access that data in a way that is streamlined to enforce those policies. Because you know exactly what people are and aren't going to be doing with it—if you don't, that's undefined behavior and/or a security hole. This is something most NoSQLers also got wrong, organizing their data not by policy but rather by how it would be indexed or queried, which is not the same thing.

This is also why people *continue* to write REST APIs, as flawed as they are. The busywork of creating unique, bespoke endpoints incidentally creates a time and place for defining and implementing some kind of rules. It also means you never have to tackle them all at once, consistently, which would be more difficult to pull off (but easier to maintain). The stunted vocabulary of ad-hoc schemas and their ill-defined nouns forces you to harmonize it all by hand before you can shove it into your meticulously typed and normalized database. The superfluous exercise of individually shaving down the square pegs you ordered, to fit the round holes you carved yourself, has incidentally allowed you to systematically check for woodworms.

It has nothing to do with REST or even HTTP verbs. There is no semantic difference between:

**PATCH /user/1/edit**


`{"name": "Jonathan Doe"}`


and

**UPDATE TABLE users SET name = "Jonathan Doe" WHERE id = 1**


The main reason you don't pass SQL to your Rails app is because deciding on a policy for which SQL statements are allowed and which are not is practically impossible. At most you could pattern match on a fixed set of query templates. Which, if you do, would mean effectively using the contents of arbitrary SQL statements as `enum`

values, using the power of SQL to express the absense of SQL. The Aristocrats.

But there is an entirely more practical encoding of sparse updates in `{whatever}`

`<flavor />`

`(of (tree you) prefer)`

.

**POST /api/update**


```
{
"user": {
"1": {
"name": {"$set": "Jonathan Doe"}
}
}
}
```


It even comes with free bulk operations.

Validating an operation encoded like this is actually entirely feasible. First you validate the access policy of the individual objects and properties being modified, according to a defined policy schema. Then you check if any new values are references to other protected objects or forbidden values. Finally you opportunistically merge the update, and check the result for any data integrity violations, before committing it.

You've been doing this all along in your REST API endpoints, you just did it with bespoke code instead of declarative functional schemas and lambdas, like a chump.

If the acronyms CRDT and OT don't mean anything to you, this is also your cue to google them so you can start to imagine a very different world. One where your sparse updates can be undone or rebased like git commits in realtime, letting users resolve any conflicts among themselves as they occur, despite latency. It's one where the idea of remote web apps being comparable to native local apps is actually true instead of a lie an entire industry has shamelessly agreed to tell itself.

You might also want to think about how easy it would be to make a universal reducer for said updates on the client side too, obviating all those Redux actions you typed out. How you could use the composition of closures during the UI rendering process to make memoized update handlers, which produce sparse updates automatically to match your arbitrary descent into your data structures. That is, `react-cursor`

and its ancestors except maybe reduced to two and a half hooks and some change, with all the same time travel. Have you ever built a non-trivial web app that had undo/redo functionality that actually worked? Have you ever used a native app that didn't have this basic affordance?

It's entirely within your reach.

## GraftQL

If you haven't been paying attention, you might think GraphQL answers a lot of these troubles. Isn't GraphQL just like passing an arbitrary `SELECT`

query to the server? Except in a query language that is recursive, typed, composable, and all that? And doesn't GraphQL have typed mutations too, allowing for better write operations?

Well, no.

Let's start with the elephant in the room. GraphQL was made by Facebook. *That* Facebook. They're the same people who made the wildly successful React, but here's the key difference: you probably have the same front-end concerns as Facebook, but you do not have the same back-end concerns.

The value proposition here is of using a query language designed for a platform that boxes its 2+ billion users in, feeds them extremely precise selections from an astronomical trove of continuously harvested data, and only allows them to interact by throwing small pebbles into the relentless stream in the hope they make some ripples.

That is, it's a query language that is very good at letting you traverse an enormous graph while verifying all traversals, but it was mainly a tool of necessity. It lets them pick and choose what to query, because letting Facebook's servers tell you everything they know about the people you're looking at would saturate your line. Not to mention they don't want you to keep any of this data, you're not allowed to take it home. All that redundant querying over time has to be minimized and overseen *somehow*.

One problem Facebook didn't have though was to avoid busywork, that's what junior hires are for, and hence GraphQL mutations are just `POST`

requests with a superficial layer of typed paint. The Graph part of the QL is only for reading, which few people actually had real issues with, seeing as `GET`

was the one verb of REST that worked the most as advertised.

Retaining a local copy of all visible data is impractical and undesirable for Facebook's purposes, but should it be impractical for your app? Or could it actually be extremely convenient, provided you got there via technical choices and a data model adapted to your situation? In order to do that, you cannot be fetching arbitrary sparse views of unlabelled data, you need to sync subgraphs reliably both ways. If the policy boundaries don't match the data's own, that becomes a herculean task.

What's particularly poignant is that the actual realization of a GraphQL back-end in the wild is typically done by... hooking it up to an SQL database and grafting all the records together. You recursively query this decidedly non-graph relational database, which has now grown JSON columns and other mutations. Different peg, same hole, but the peg shaving machine is now a Boston Dynamics robot with a cute little dog called Apollo and they do some neat tricks together. It's just an act though, you're not supposed to participate.

Don't get me wrong, I know there are real benefits around GraphQL typing and tooling, but you do have to realize that most of this serves to scaffold out busywork, not eliminate it fully, while leaving the `INSERT/UPDATE/DELETE`

side of things mostly unaddressed. You're expected to keep treating your users like robots that should only bleep the words GET and POST, instead of just looking at the thing and touching the thing directly, preferably in group, tolerant to both error and lag.


This is IMO the real development and innovation bottleneck in practical client/server application architecture, the thing that makes so many web apps still feel like web apps instead of native apps, even if it's Electron. It makes any requirement of an offline mode a non-trivial investment rather than a sane default for any developer. The effect is also felt by the user, as an inability to freely engage with the data. You are only allowed to siphon it out at low volume, applying changes only after submitting a permission slip in triplicate and getting a stamped receipt. Bureaucracy is a necessary evil, but it should only ever be applied at minimum viable levels, not turned into an industry tradition.

The exceptions are rare, always significant feats of smart engineering, and unmistakeable on sight. It's whenever someone has successfully managed to separate the logistics of the API from its policies, without falling into the trap of making a one-size-fits-all tool that doesn't fit by design.

Can we start trying to democratize *that*? It would be a good policy.

*Next: The Incremental Machine*