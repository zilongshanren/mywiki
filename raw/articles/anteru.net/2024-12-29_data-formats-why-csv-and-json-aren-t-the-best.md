---
title: 'Data formats: Why CSV and JSON aren''t the best'
url: https://anteru.net/blog/2024/data-formats-why-csv-and-json-aren-t-the-best
published: '2024-12-29'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

First an admission - I’m guilty of doing this myself, many moons ago, I would store results from experiments in a MongoDB and thus by extension as JSON. I hope that the corresponding blog post didn’t fuel the dramatic expansion of JSON as a storage format for data, as I learned over the years that JSON for data - along with CSV - is causing harm in the field. In this blog post, I want to correct for past mistakes and hopefully encourage you to re-consider the way you’re storing what is commonly referred to as “tabular” data (no, this is not how to do backups, store VM images, large files, etc. - really just stuff you would open in a spreadsheet application one day.)

Before we discuss the solution, I like to cover the requirements and “how did we get here in the first place”. Requirements are fairly easy - you’re running some application doing measurements, each measurement has many dimensions; i.e. you know what you’re measuring ahead of time (that’s your dimension/column names), and each time you measure you measure the same things (each measurement is a row.) If your dimensions change widely between measurements, then I’m not sure what you’re measuring; this may be fine at the beginning while exploring, but eventually you’ll want to settle down on a set of dimensions you care about and only evolve it carefully. Evolution here means versioning: You want to know *what* you measured and also *how* you measured it. Versions allow you to capture both pieces of information, as long as you maintain a changelog.

I’m stressing the versioning information here, as it’s critical to know what measurements you can trust. Unless you have perfect knowledge of everything, there *will be bugs* in your collection or processing, which will results in some dimensions containing garbage data at times. Time alone is not sufficient to identify this, some measurement devices/applications can get updated at different times, so you really want to bake in some version with each data set. If you don’t have versioning ready, your tools will start breaking over time, and your analysis becomes less and less reliable as different errors in measurements get mixed in.

So far we have “tabular data” and “versioning” as requirements, one more requirement that’s more important than anyone would think at first and that trumps all other needs *in practice* is “easy to explore”. If you need to write a script to look at the data, this may be fine in some cases, but if all you get is a raw file, you better be able to look at it with minimal friction. Minimal friction somewhat implies plain text, but we’ll get to that later.

There are other requirements like performance or disk size, but they’re at best secondary until they completely dominate the decision. The majority of the time - at least in my experience - getting some data quickly is what matters most, and only once you accumulated a lot of data people will start to notice that all their disk drives are full and they should do something about it. I’m getting ahead of myself here though.

## The contenders

Let’s look at three popular solutions I’ve seen in the wild. A lot. Like, cannot be unseen times lot.

- Spreadsheet files for your favorite spreadsheet application
[JSON](https://www.json.org)(includes JSON stored in databases, be it NoSQL or thanks to recent improvements also real SQL databases)[CSV](https://en.wikipedia.org/wiki/Comma-separated_values)- comma separated values

## Spreedsheet files (application specific)

They’re not versioned, but we’ve obviously all seen people trying to put some extra info in a random cell, so let’s say they can be versioned with pain (an extra sheet with a version number, document properties, it’s not the end of the world.) Easy to look at - absolutely, as long as your favorite spreadsheet application is installed. Do they store tabular data well? Except for random re-interpretation of entries because you got the format wrong, they’re actually not terrible. The main issue I have with spreadsheet files as your main source of truth is - generating them is non-trivial, especially if you want to get all types done correctly, and they tend to be very large and slow to query (as in, batch processing of spreadsheet files is often not a good idea.) That said, out of the three popular solutions, if done right, they’re the least terrible. I really don’t like using them for performance reasons and because they tend to break in funny ways, but if you are hard pressed to make something work, and “convenience” is a premium, by all means, before going for the two solutions outlined below, get your [Pandas](https://pandas.pydata.org/) script ready and use [ to_excel](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html) (and keep in mind that can also create

[ODF](https://groups.oasis-open.org/communities/tc-community-home2?CommunityKey=4bf06d41-79ad-4c58-9e8e-018dc7d05da8)files so you’re not locked in.)

## CSV

Let’s get to CSV quickly: Trivial to generate, to the point that everyone generates their favorite flavor of CSV. I’ve written parsers for a dozen or so different variants of CSV in my life, mostly due to:

- No standard for string escaping. Every CSV file out there will have strings eventually, then strings with spaces, then strings with quotes, and all hell will break loose. I’ve seen escapes, triple quoting, double quotes, “last column is text”, and everything in-between.
- No standard types: Dates will be stored as strings (see above), and numbers won’t round-trip, because generally most CSV files out there are generated with
`printf`

and friends which are not optimized to produce the shortest string or most accurate representation. Also, booleans will be`On`

/`Off`

,`Yes`

/`No`

,`True`

/`False`

,`0`

/`1`

, just never consistent.

Is CSV trivial to open? In theory yes, in practice - there are spreadsheet applications which can import CSV, but some fail in funny ways because commas are decimal separators in Europe for example. As a result your comma separated file is a one large number and imports as a single column over here. Do they work in editors? Not really, unless someone starts formatting the CSV for better readability (comma separated but tab-aligned values, anyone?)

The final nail in the coffin in my book is that they simply can’t store versions. You’ll find a million different ways to put a version into a CSV file, all of which require domain knowledge by the reader to remove it (some extra row somewhere that needs to be ignored, a dummy column name, part of the filename, …) That makes them really bad for archival storage in my book. You find some random CSV somewhere, your guess is as good as mine as to what version it was, what application it belonged to, how it was captured, etc.

Why are they so popular? Other than “trivial to generate” and “feels trivial to look at because it’s text”, I’m not sure. They cause long-term harm due to complexity throughout the stack to process them, and the “trivial to look at because it’s text” argument falls short the moment you have a decent amount of data (ever tried opening a 20+ MiB CSV file in an editor?) It’s really a perception issue more than any hard technical argument that keeps them so popular.

## JSON

The other popular choice - especially due to NoSQL databases - is JSON. Versioning and metadata is easy with JSON, just add additional fields, so let’s get that sorted out immediately. Reading by humans? JSON is definitely not meant to be consumed by humans, especially once the files become big and consist of arrays mostly. With `jq`

you can get something resembling a query language for JSON, but good luck getting your JSON data into a spreadsheet application (or a tabular format, for that matter.) The biggest problem with JSON though is that it … can’t store numbers properly. It’s JSON, so everything is a `double`

, in theory, but doubles can only represent integers up to 53 bit precisely, and again you have the same issues with round-trips of numbers as CSV (and in practice much earlier than that, for example, 64-bit integers don’t work in general.) Not to mention, there’s no standard way to store a date in JSON.

Finally, I’ve seen JSON storing each row as an object, with the column names repeated: That’s a 10-100x expansion of the source data. Granted, any compression algorithm will get this removed again, but the amount of redundant parsing in those cases is staggering.

To wrap it up, JSON fails on all accounts as a *file format*, and the main reason to use it is really for convenience when using a document based database. But even then, if the database was extracting out the structure and store everything binary, you still get all the problems of JSON back when translating to/from JSON across the wire.

Before you start with binary JSON and alternative JSON encodings: There’s simply too many of them ([BSON](https://bsonspec.org/), [UBJSON](https://ubjson.org/), [CBOR](https://cbor.io/), [MessagePack](https://msgpack.org/), …) and there’s no standard, so good luck finding a library to write whatever flavour of binary JSON you have and find a matching reader in your scripting language or elsewhere.

## Protocol Buffers, HDF5, Parquet to the rescue?

There’s a bunch of structured message formats like protocol buffers out there, but they’re not really that well suited for processing large data sets as their goal is to facilitate RPC (and they come with a fair amount of overhead, i.e. protocol definitions, etc.) There’s also HDF5 which technically sounds like a good solution, but never really took off outside of its community. If I had to guess, it’s a bit too flexible for its own good - I’m sure there are good use cases to store arbitrary binary files inside a HDF5 file, but it also adds complexity on the consumer side. It also doesn’t give you much in terms of simplified access or “tabular” data benefits.

Interestingly, there is a format though which is pretty much a 1:1 replacement for CSV and spreadsheet files, with little “extra”, and it’s binary, and has bindings for most (all?) programming language you’d care about: [Parquet](https://parquet.apache.org/). It’s a column based format (that only matters if you filter out columns), it supports modern compression algorithms ([Zstd](https://facebook.github.io/zstd/)), and it provides a fairly clean mapping of the “spreadsheet” concept. The format itself is a bit too complex for my taste (being layered on top of Apache Thrift), but, it slots into the right place in the ecosystem. It’s trivially readable/writable by Pandas, and there are open-source viewers for it (like [Data Wrangler](https://github.com/microsoft/vscode-data-wrangler)), and also databases for it ([Iceberg](https://iceberg.apache.org/), [DuckDB](https://duckdb.org/).) Spreadsheet application support is non-existant, but, it’s fairly easy to convert Parquet into other formats, so my recommendation would be to treat the other formats as a derivative and generate them on-demand.

Parquet does solve the typing problem nicely, as each column is strongly typed, and being binary it means it will round-trip. The main strength is really that it’s super simple to process a Parquet file “down to” CSV or other formats as it’s not dramatically different. You can’t trivially convert HDF5 to CSV or any of the JSON formats, but here you can and that makes it easy to please the convenience crowd.

Does this solve all problems? It allows for versioning by adding meta-data to the file, so that’s covered. Tabular data - by construction. Easy to view - relatively good. It does win big time on the performance and size dimensions though, and it’s easy to use from various programming languages, so in the end it has become my current format of choice as the *primary* storage format. It seems also reasonable good for archival storage as the format is well-documented and everything built around it is open-source, so at the very least, at some day you’ll be able to convert from Parquet into whatever will be the best format at the time to store things. As long as it’s not JSON or CSV, you have my blessing! In the meantime, I think Parquet is about as good as it gets, so if you are struggling with the same problems as I do, please give it a shot.