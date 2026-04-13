---
title: 'Advent 2021: GraphQL'
url: https://anteru.net/blog/2021/advent-2021-graphql
published: '2021-12-12'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Yesterday I wrote about [gRPC](https://anteru.net/blog/2021/advent-2021-grpc), which is a high-performance remote procedure call library. This is super useful for services, but if you have a website and you want to provide a “classic”, JSON based API, gRPC is not for you. Instead, you can (realistically speaking) choose these days between two options: A REST API or [GraphQL](https://graphql.org/). In the last couple of years, I’ve been increasingly gravitating towards GraphQL, to the point that if I’m setting up a new web API these days I use GraphQL by default.

Why? There are two reasons. The first one is efficiency. With “classic” REST APIs (including [OpenAPI](https://www.openapis.org/)) you define the shape of each request and fix it. If you ask for a thing, you get a pre-defined chunk of JSON back, no matter what yo needed from it or not. A good example is if you want to enumerate a list of things and you just need the name/title of each item. There’s really no way in a REST API to describe what you’re asking for, so you end up getting a lot of data that you throw away. On the other hand, GraphQL requires you to pass in the shape of the data you’re expecting to the request. That gets boring real quick for reasonably complex applications. I [blogged about this previously](https://anteru.net/blog/2019/getting-started-with-graphql/) in case you’re curious how it looks in practice.

The second reason why I prefer GraphQL is because it’s less work overall. This starts with rather mundane tasks like coming up with an URL structure. GraphQL does away with this, as the structure of the data is the only thing that matters. Next, queries are less complex because there are only two types of queries – mutations and read-only queries. No more question if this is a `PUT`

, `POST`

, or other verb. A GraphQL can be fully explored and queried using the same endpoint, making it easy to discover everything. That’s used to great effect by [GraphiQL](https://graphql-dotnet.github.io/docs/getting-started/graphiql/) – you can try that out on [GitHub’s API](https://docs.github.com/en/graphql/overview/explorer). Finally, GraphQL has excellent tooling these days which makes it really simple to create a GraphQL API. For [Django](https://anteru.net/blog/2021/advent-2021-django) I use [graphene-django](https://docs.graphene-python.org/projects/django/en/latest/) and effectively my whole API ends up in a single schema file. On the client end, there’s [Angular Apollo](https://apollo-angular.com/docs) (which is what I as an [Angular](https://anteru.net/blog/2021/advent-2021-angular) user use), which makes it very simple to consume a GraphQL endpoint.

In a world of increasingly complex web APIs, I think GraphQL is a solid step forward. If you’re starting from scratch, and especially if you expose a lot of data, do yourself a favor and take a look at GraphQL!