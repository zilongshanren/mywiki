---
title: GraphQL in the GPU database
url: https://anteru.net/blog/2017/graphql-in-the-gpudb
published: '2017-12-28'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

One thing I’ve been asked about is providing some kind of API access to the GPU database I’m running. I’ve been putting this off for most of the year, but over the last couple of days, I gave it yet another try. Previously, my goal was to provide a “classic” REST API, which would provide various endpoints like /card, /asic etc. where you could query a single object and get back some JSON describing it.

This is certainly no monumental task, but it never felt like the right thing to do. Mostly because I don’t really know what people actually want to query, but also because it means I need to somehow version the API, provide tons of new routes, and then translate rather complex objects into JSON. Surely there must be some better way in 2017 to query structured data, no?

GraphQL

Turns out, there is, and it’s called GraphQL. GraphQL is a query language where the user specifies the shape of the data needed, and the system then builds up tailor-made JSON. On top of that, introspection is also well defined so you can discover what fields are exposed by the endpoint. Finally, it provides a single end-point for everything, making it really easy to extend.

I’ve implemented a basic GraphQL endpoint which you can use to query the database. It does not expose all information, but provides access to hopefully the most frequently used data. I’m not exposing everything mostly due to the lack of pagination. If you use the allCards query, you can practically join large parts of the database together, and I don’t want enable undue load on the server. As a small appetizer, here’s a sample query executed locally through GraphiQL.

Using GraphiQL to query the GPU database programmatically.

If you want to see more data exported, please drop me a line, either by sending me an email or by getting in tough through Twitter.

Background

What did I have to implement? Not that much, but at the same time, more than expected. The GPU database is built using Django, and fortunately there’s a plugin for Django to expose GraphQL called graphene-django which in turn uses Graphene as the actual backend.

Unfortunately, Graphene and in particular, Graphene-Django is not as well documented as I was hoping for. There’s quite a bit of magic happening where you just specify a model and it tries to map all fields, but those won’t be documented. I ended up exposing things manually by restricting the fields I want using only_fields, and then writing at least a definition for each field, occasionally with a custom resolve function. For instance, here’s a small excerpt from the Card class:

classCardType(DjangoObjectType):classMeta:model=Cardname="Card"description='A single card'interfaces=(graphene.Node,)only_fields=['name','releaseDate']# More fields omittedaluCount=graphene.Int(description="Number of active ALU on this card.")computeUnitCount=graphene.Int(description="Number of active compute units on this card.")powerConnectors=graphene.List(PowerConnectorType,description="Power connectors")defresolve_powerConnectors(self,info,**kwargs):return[PowerConnectorType(c.count,c.connector.name,c.connector.power)forcinself.cardpowerconnector_set.all()]# more fields and accessors omitted

Here’s also an interesting bit. The connection between a card and its power or display connector is a ManyToManyField, complete with custom data on it. Here’s the underlying code for the link:

classCardDisplayConnector(models.Model):"""Map from card to display connector. """connector=models.ForeignKey(DisplayConnector,on_delete=models.CASCADE)card=models.ForeignKey(Card,on_delete=models.CASCADE,db_index=True)count=models.IntegerField(default=1)def__str__(self):return'{}x {}'.format(self.count,self.connector)

Now the problem is how to pre-fetch the whole thing, as otherwise iterating through the cards will issue a query to fetch the display connectors, and then one more query per connector to get the data related to this connector… which led to a rather lengthy quest to figure out how to optimize this.

Optimizing many-to-many prefetching with Django

The end goal we want is that we perform a single Card.objects.all() query which somehow pre-fetches the display connectors (equivalently, the power connectors, but I’ll keep using the display connectors for the explanation.) We can’t use select_related though as this is only designed for foreign keys. The documentation hints at prefetch_related but it’s trickier than it seems. If we just use prefetch_related ('displayConnectors'), this will not prefetch what we want. What we want to prefetch is the actual relationship, and from there on select_related the connector. Turns out, we can use the Prefetch to achieve this. What we’re going to do is to prefetch the set storing the relationship (which is called carddisplayconnector_set), and provide the explicit query set to use which can then specify the select_related data. Sounds complicated? Here’s the actual query:

What this does is to force an extra query on the display connector table (with joins, as we asked for a foreign key relation there), and then caches that data in Python. Now if we ask for display connector, we can look it up directly without an extra roundtrip to the database. How much does this help? It reduces the allCard query time from anywhere between 4-6 seconds, with 500-800 queries, down to 100 ms and 3 queries!

Wrapping it up

With GraphQL in place, and some Django query optimizations, I think I can tick off the “programmatic access to the GPU database” item from my todo list. Just in time for 2017 :) Thanks for reading and don’t hesitate to get in touch with me if you got any questions.