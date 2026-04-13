---
title: Getting started with GraphQL
url: https://anteru.net/blog/2019/getting-started-with-graphql
published: '2019-04-29'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

It’s been more than a year that I’ve added support for GraphQL to the GPU database. Back then, I had the choice between a more “classic” REST API or GraphQL, and I chose GraphQL as it was starting to become more popular with big adopters like GitHub and I expected a lot of industry adaption. Turns out, I was probably a bit overly optimistic. Those who need to consume it don’t seem to write much about it, so today I want to provide you with a quick tutorial on how to consume a GraphQL endpoint – including how to figure out what it’s doing, and writing a simple client application. I’ll be using Python3 with the excellent requests library.

What we’re up to

We’re going to write a simple client for the GPU database, which, given a search entry, will produce a list of all cards matching that query and provide us with some information about the ASIC used on it. But before we start hacking in code, let’s understand what GraphQL is and how it works.

Let’s do this

GraphQL is a way to consume a web API. It’s still JSON everywhere, but with a few important differences:

There is only one end-point, which provides all the data and introspection of all queries and types.

It delivers data in the shape requested by the client API.

The first feature is nice for development, as it makes it easy to find out what the endpoint provides and how to access it. More so, as the built-in schema in GraphQL is rather expressive and can contain documentation. The second bit is the tricky one, as it means that if you don’t know what you’re looking for, you’re in for a lot of errors. For instance, if we just look at the endpoint:

$curlhttps://db.thegpu.guru/graphql
{"errors":[{"message":"Must provide query string."}]}

That’s not very helpful – we got an error because we didn’t provide a query, and without a query, nothing can happen. The easiest way to start is to use a tool which queries the schema. There are a bunch of tools out there – the most popular one probably being GraphiQL; for this blog post, I’ll use a packaged version as this happens to be a simple to run stand-alone application (while setting up GraphiQL requires you to run a web-server locally).

GraphiQL supports GraphQL schema discovery out-of-the-box, so all we need to do is to point it at our endpoint, https://db.thegpu.guru/graphql. This will look something like this:

GraphQL schema browsing in GraphiQL -- ignore the error message, we have not sent a valid query yet. The right hand side contains the documentation and that's what we're looking for at the moment.

What happened here? Well, the tool got the schema, and is showing us what requests we can make. If you wonder, whether we could do it ourselves, the answer is yes, but exploring the schema manually is … cumbersome. We’ll do this once to get the basic idea, and we’ll query for what queries are available:

You’ll be likely wondering how the structure at the end forms a query. One of the core ideas behind GraphQL is that you provide a structured query, and the result will be in the same shape, so you get exactly what you want. For the query above, we provided:

{__schema{queryType{fields{name}}}}

The server will thus only fetch the fields and connections we asked for. This allows the schema to evolve without disturbing clients and reduces bandwidth requirements by only sending the bits we can actually consume. Armed with this knowledge, let’s try to make some sense of the search. For this example, our search string will be “70”, and we want to find out the ASIC name and transistor count.

Search

A search differs from what we did so far as it’s a query, i.e. it passes some parameters around. In our case, we want to use the search query, which has a bunch of fields:

query: The query string

type: The type of object we’re querying (strongly typed!)

A bunch of fields related to pagination – first, last, before and after.

Let’s ignore the pagination for now and focus on the data at hand. The search returns a SearchConnection, which is the GraphQL way of returning “a list of things”. I’ve quoted it because GraphQL is an API designed to process a graph, and there are no lists in a graph. Instead, you model collections via a set of (directed) edges from one node to other nodes, and iterate over those edges. That’s what the connection consists of – a list of edges, and some pagination info. Let’s give it a try. One thing we’ll learn here is that GraphiQL will guide us through autocompletion up to the point where our query looks like this:

{search(query:"70",type:CARD){edges{node{}}}}

We’ll get an error inside node { ... }, but what can we do about it? node is a SearchResultItem, which is a union and can be either Card or ASIC. Selecting the right types requires the ... on syntax, as explained in the GraphQL documentation:

Done? No, we’re going to get an error that first or last must be set. Those are pagination related, and in order to not overload the server, it requires you to set some pagination count. We’ll try first:3 and hope for the best. With that, our query looks like this:

That’s looking good. For pagination, we’ll turn to our Python script, as it’s easier to see how you’d do this from code than running a dozen queries in the UI. I’ll assume for now that you have some Python environment with requests working (if not, you’ll likely want to create a virtual environment using virtualenv or pipenv), so import requests works for you.

Following the links

To follow the links, we’ll make use of the pageInfo field on the search. This contains two fields of our interest:

hasNextPage: Is there another page?

endCursor: A cursor we can pass to search to offset the first entry.

What we’ll do is: While hasNextPage returns true, issue another request, and pass the endCursor via an after paramter to the search query. Let’s look at the full sample code, which should make this clear:

importrequestsimportsysendpoint='https://db.thegpu.guru/graphql'if__name__=='__main__':query_string=sys.argv[1]print('Querying database for',query_string)pagination=''whileTrue:query='''{ search(query:"%QUERY",type:CARD,first:3%PAGE) { edges { node { ... on Card { name asic { name transistorCount } } } } pageInfo { endCursor hasNextPage } } }'''query=query.replace("%PAGE",pagination)query=query.replace("%QUERY",query_string)r=requests.get(endpoint,params={'query':query})d=r.json()forcardind['data']['search']['edges']:card=card['node']print('Name',card['name'],'uses ASIC',card['asic']['name'],'with',card['asic']['transistorCount'],'transistors')pageInfo=d['data']['search']['pageInfo']ifpageInfo['hasNextPage']:# We have another page, pass the endCursor into the# search querypagination=f',after:"{pageInfo["endCursor"]}"'else:break

And that’s it – there’s more to GraphQL than what I covered here, in particular, I completely ignored mutations, but this should help you to get starting consuming GraphQL endpoints like the one available in the GPU database.