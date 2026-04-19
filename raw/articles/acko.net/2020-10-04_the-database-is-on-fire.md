---
title: The Database is on Fire
url: https://acko.net/blog/the-database-is-on-fire/
author: Steven Wittens
published: '2020-10-04'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![The Database is on Fire](../../assets/ea18d7f68b2577d4.jpg)

# The Database is on Fire

Let me tell you a tech story.

Many years ago, I was working on an app with real-time collaboration built into it. It was a neat experimental stack, using early React and CouchDB to their full potential. It synced data live over JSON [OT](https://en.wikipedia.org/wiki/Operational_transformation). It was used to do actual work internally, but the general applicability and potential for re-use was evident.

Trying to sell potential customers on this technology, we ran into an unexpected wall. Our tech looked and worked great in the demo video, no problem there. It showed exactly how it worked, and nothing was faked. We had come up with and coded a credible field scenario.

![Two users interacting through a mobile app](../../assets/39e581057f00cc8b.png)

That was in fact the problem. Our demo worked exactly the way everyone else always pretended their apps worked. Namely that information would flow instantly from A to B, even large media files. That everyone would see new records as they came in. That by adopting an app, users could just work together without friction on the exact same things, even if they had a spotty internet connection in the middle of nowhere. This is the sort of thing every After Effects-product-video does implicitly.

Despite the fact that everyone knew what a Refresh button was for, it didn't register at all that the web apps they were asking us to build would normally be subject to its limitations. Or that it would be an entirely different experience if you stopped needing it altogether. What they mainly noticed was that you could "chat" by leaving notes between people, so they wondered how this was different from, say, Slack. Oof.

## The Design of Everyday Syncs

If you've been working in software for a while, it can be a bit jarring to remember that most people cannot look at a picture of an interface and infer what it will do when they interact with it. Let alone know what's going to happen behind the scenes. Knowing what *can* happen is largely a result of knowing what cannot happen, or should not happen. It requires a [mental model](https://uxdesign.cc/design-of-everyday-things-chapter-01-summary-and-keypoints-664d426a11e0) not just of what the software is doing, but how its different parts are arranged and can communicate.

A classic example is the user who is staring at a *spinner.gif* for 20 minutes, wondering when the work will finally be done. The developer would know the process is probably dead and that the gif will never go away. Its animation mimes that work is happening, but it's not connected to the state of the work. This is the sort of thing where some techies like to roll their eyes at just how misinformed a user can be. Notice though, which one of them is pointing at a spinning clock and saying it's actually standing still?

![An animated activity spinner](../../assets/1715f145d00abf0f.gif)


This is the value proposition of real-time in a nutshell. These days real-time databases are still mostly underused, and still regarded with suspicion. Most of them lean heavily into NoSQL style, which tend to bring up Mongo-fueled benders people would rather forget. For me though, it meant getting comfy on the CouchDB, as well as learning to design schemas that somebody other than a bureaucrat could correctly fill in. I think my time was better spent.

The real topic of this post is what I'm using these days. Not by choice, but through uncaring and blindly applied corporate policy. Hence a Totally Fair and Unbiased comparison of two closely related Real-Time Database Products By Google™.

![Firebase Suite Firebase](../../assets/67303cdef18da133.png)

*Anyone need more stickers?*

They both have fire in their name. One I regard with fondness. The other is a different kind of fire. If I'm hesitant to name them, it's because once I do, you will run into the first big problem, their names.

One is called the *Firebase Real-Time Database* and the other is the *Firebase Cloud Firestore*. They are both products in Google's *Firebase suite*. The APIs are respectively `firebase.database(…)`

and `firebase.firestore(…)`

.

This is because *Real-Time Database* is just the original *Firebase*, before Google bought it in 2014. They then decided to build a *copy* of Firebase on their big data whatsit, as a parallel offering, and named it Firestore with a cloud. Hope you're still following. If not, no worries, I have tried to rewrite this part a dozen times already.

Cos really you have a *Firebase* in your Firebase, and a *Firestore* in your Firebase, or at least you do if you want to be able to make sense of Stack Overflow from a few years ago.

If there is a Raspberry award for worst naming in software products, this surely qualifies. The mental hamming distance between these names is so small it will trip up even seasoned engineers, whose fingers will type one thing as their lips speak another. It will royally fuck up plans made with the best of intentions, fulfilling the prophecy of having your database be on fire. I'm not joking in the slightest. The person who came up with this naming scheme has blood, sweat and tears on their hands.

I will call them *Firebase*⚾️ and *Firestore*🧯. The baseball is for Fire*base*, and the fire extinguisher is for Fire*store*, because you need one.

![A man chasing bugs with a butterfly net in a forest that's on fire](../../assets/ae2f20d8e6419ac3.jpg)

## Pyrrhic Victory

You might think Firestore🧯 is the *replacement* for Firebase⚾️, a next-generation successor, but that would be false. Firestore🧯 is patently unsuitable as a Firebase⚾️ replacement. Somebody has seemingly engineered away almost everything that is interesting about it, and messed up most of the rest in various ways.

A cursory glance at the two offerings will confuse you though, because it seems they do the same thing, through mostly the same APIs and even the very same DB session. The differences are subtle and will only be discovered after careful comparative study of the sparse docs. Or when you're trying to port code that works perfectly fine on Firebase⚾️ over to work with Firestore🧯. When you discover that your database interface catches fire as soon as you try to do a mouse drag in real-time. Again, not kidding.

Firebase⚾️'s client is polite in that it buffers changes and auto-retries with last-write-wins best-effort consistency. Firestore🧯 however has a throttle of 1 write per document per user per second, enforced by the server. It's up to you to implement a rate limiter around it yourself when you use it, even though you're just trying to build your app. So Firestore🧯 is a real-time database without a real-time client, wearing the API of one as a skin suit.

This is also where you start to see the first hints of the reason for Firestore🧯's existence. Those words "best-effort consistency" tend to make Grumpy Database Admins' few remaining hairs stand up. I could be wrong about this, but I suspect that somebody high up enough at Google looked at Firebase⚾️ after they bought it and simply said: "No. Dear God, No. This is unacceptable. Not on my watch."

![A gray beard monk reading from a tome](../../assets/c11436301938c102.jpg)


They emerged from their chambers and declared:

*"One big JSON document? No. You will split your data into separate documents, each no more than 1MB in size."*

This seems like a limit that will not survive first encounter with any sufficiently motivated user base. You know it's true. Like, we have a few 1500+ slide presentations at my current job, which is Perfectly Normal.

Under this constraint, you will be forced to accept that one "document" in your database bears no resemblance to anything a user might refer to as a document. This is the kind of thing that will cause subtle misery from day 1 in attempting to match end-user requirements, and never cease.

*"Arrays of arrays that can contain other things recursively? No. Arrays will contain only objects, or numbers of a fixed size, as God intended."*

So if you were hoping to put GeoJSON in your OnFirestore🧯, you will discover that's not possible. With anything remotely not 1-dimensional. Hope you like Base64 and/or JSON inside JSON.

*"Import and Export JSON via HTTP, command line tools or the admin panel? No. You will only export and import data to and from Google Cloud Storage. At least I think that's what it's called these days. When I say 'you', I am only talking to those of you with Project Owner permissions. Everybody else go away and file a ticket."*

You see, FireBae🤵⚾️'s data model is straightforward to describe. It contains one big enormous JSON document, which maps JSON keys to URL paths. If you `HTTP PUT`

this to your ⚾️ at `/`

:

```
{
"hello": "world"
}
```


Then `GET /hello`

will return `"world"`

. For the most part this works as you'd expect. A ⚾️ collection of objects `/my-collection/:id`

is equivalent to a JSON dictionary `{"my-collection": {...}}`

at the root, whose contents are available at `/my-collection`

:

```
{
"id1": {...object},
"id2": {...object},
"id3": {...object},
// ...
}
```


This works fine as long as each insert has a non-colliding ID, which you are provided a standard solution for.

In other words, ⚾️ is 100% JSON compatible (*) and plays nice with HTTP, like CouchDB. But you mostly use it through its real-time API, which abstracts away the websockets, auth and subscriptions. The admin panel does both, allowing real-time edits and JSON import/export. If you embrace the same in your code, it's quite astonishing how much specialized code disappears once you realize JSON patch and diff can solve 90% of your persistent state handling chores.

🧯's data model is JSON-like, but diverges in a few critical ways. No arrays of arrays was already mentioned. The model for sub-collections is to have them be first class concepts, separate from the JSON document holding them. Because there is no readily available serialization for this, getting data in and out requires a specialized code path. You must build your own scripts and tools to handle your own collections. The admin panel only allows you to make small edits, one field at a time, and does not have any import/export.

They took a real-time NoSQL database and turned it into a slow, auto-joined not-SQL with a dedicated not-JSON column. *Something something GraftQL*.

![A developer sitting at a computer that's on fire](../../assets/63b3161d32ca352e.jpg)


## Hot Java

If 🧯 was supposed to be more reliable and scalable, then the irony is that the average developer will end up with a less reliable solution than if they had just used ⚾️ out of the box. The kind of software that Grumpy Database Admin has designed for requires a level of effort, and caliber of engineering, that just isn't realistic for the niche they are supposedly good at. It's similar to how HTML5 Canvas is not at all a Flash substitute, if the tools and player aren't there. What's more, it is steeped in an attitude towards data purity and sterile validation that simply doesn't match how the average business user actually *likes to get work done*, which is that everything is optional because everything is a draft until the very end.

The main flaw in ⚾️ is that the client was created a few years too soon, before you could reasonably expect most web developers to know what immutability was. As a result, ⚾️ assumes you are mutating your data, and will not benefit from any immutability you feed it. It will also not reuse data in the snapshots it gives you, making diffs much harder. For larger documents, its mutable-diff based transactional mechanism is just inadequate. C'mon guys, we have `WeakMap`

in JavaScript now. It's cool.

If you give your data the right shape, and keep your trees shallow, you can work around this. But I do wonder whether ⚾️ wouldn't get a whole lot more interesting to people if they just released a really good client API based on leveraging immutability, coupled with serious practical advice on schema design. Instead it's like they tried to fix what wasn't broken, and made it worse.

![A developer on fire](../../assets/2ad9f091190f16be.jpg)

I don't know the full intent behind building 🧯. Speculating about motives inside the Borg cube is part of the fun. The juxtaposition of these two extremely similar but discapable databases is a relative rarity in the scene. It's almost as if somebody thought *"*⚾️* is just a feature we can emulate on **<Google *☁️*>"* but hadn't yet discovered the concept of gathering real-world requirements, or coming up with useful solutions for all of them. *"Let the developers worry about that. Just make the UI pretty... Can we add more fire?"*

I do know a thing or two about data structures. I can certainly see that "everything is one big JSON tree" is attempting to abstract away any sense of large-scale structure from a database. Expecting the software to just cope with any kind of dubious schema fractal is madness. I really don't need to imagine how bad these things can get, for I have done hostile code audits, and *seen things you wouldn't believe*. But I also know what good schemas look like, [how you can leverage them](https://acko.net/blog/apis-are-about-policy), and [why you should](https://acko.net/blog/software-development-as-advanced-damage-control/). I can imagine a world where 🧯 seemed absolutely like the right thing to do and where the people who did it think they did a good job. But it's not the one I live in.

⚾️'s support for querying is poor by anyone's standards, borderline non-existent. It certainly could have used improvement, or even a rethink. But 🧯 isn't much better, as it is limited to the same 1 dimensional indices you get in basic SQL. If you want the kinds of queries humans like to do on messy data, that means full text search, multi-range filters, and arbitrary user-defined ordering. Anything that's basic SQL if you squint is itself too limited. Besides, the only SQL queries people can run in production are the fast ones. What you want is a dedicated indexing solution with grown up data structures. For everything else, there ought to at least be incremental map-reduce or something.

If you ask Google's docs about this, you will be helpfully pointed in the direction of things like BigTable and BigQuery. All these solutions however come with so much unadulterated enterprise sales speak, that you will quickly turn back and look elsewhere.

The last thing you need with a real-time database is something made by and for people who work on an executive schedule.

*(*) Just kidding, there is no such thing as 100% JSON compatible.*