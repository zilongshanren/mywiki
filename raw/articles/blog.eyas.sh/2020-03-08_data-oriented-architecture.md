---
title: Data-Oriented Architecture
url: https://blog.eyas.sh/2020/03/data-oriented-architecture/
author: Eyas Sharaiha
published: '2020-03-08'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

There’s a little-known pattern in software architecture that deserves more
attention. Data-Oriented Architecture was first described by Rajive Joshi in a
[2007 whitepaper at RTI](http://community.rti.com/sites/default/files/archive/Data-Oriented_Architecture.pdf),
and again in 2017 by Christian Vorhemus and Erich Schikuta at the University of
Vienna in [this iiWAS paper](https://dl.acm.org/doi/10.1145/3151759.3151770).
DOA is an inversion of the traditional dichotomy between a monolithic binary and
data store (monolithic architecture) on the one hand, and small, distributed,
independent binaries each with their own data stores (microservices, and
service-oriented architecture) on the other. In data-oriented architecture, a
monolithic data store is the sole source of state in the system, which is being
acted on by loosely-coupled, stateless microservices.

I was lucky that my [former employer](https://www.broadwaytechnology.com/) also
fell upon this unusual architectural choice. It was a reminder that things *can*
be done differently. Data-oriented architecture isn’t a silver bullet by any
means; it has its own unique set of costs and benefits. What I did find, though,
is that a lot of large companies and ecosystems are stuck at exactly the type of
bottleneck that data-oriented architecture is meant to resolve.

## A quick note on Monolithic Architecture

Since a lot of architectures are often defined *in contrast* to monolithic
architectures, it’s worth spending some time describing it. It is, after all,
the fabled [state of nature](https://en.wikipedia.org/wiki/State_of_nature) of
server-side software development.

In a **monolithic** service, the bulk of server-side code is in one program that
is talking to one or more databases, handling multiple aspects of a functional
computation. Imagine a trading system that receives requests from customers to
buy or sell some security, prices them, and fills their orders.

Within a monolithic server, code could still be componentized and separated into
individual modules, but there’s no *forced* API boundary between the different
components of the program. The only rigidly defined APIs in the program are
typically either **(a)** between the UI and the server (in whatever REST/HTTP
protocol they decide on), **(b)** between the server and the data stores (in
whatever query language they decide on), or **(c)** between the server and its
external dependencies.

## Service-Oriented Architecture and microservices

**Service-oriented architectures** (SOA), on the other hand, break up monolithic
programs into *services* for each independent, componentized function. In our
trading app, we might have a separate service as the external API receiving
requests and handling responses to the customer, a second system receiving
prices and other information about the market, a third system tracking orders,
risk, etc. The interface between each of these services is a formally-defined
API layer. Services typically communicate one-on-one through RPCs, although
other techniques like message-passing and pubsub are common.

Service oriented architectures allow different services to be developed and reasoned about independently (and in parallel), if needed. The services are loosely-coupled, which means that a totally new service can now reuse the other services.

As each service in an SOA defines its own API, each service can be independently accessed and interacted with. Developers debugging or mocking individual pieces can call individual components separately, and new flows can re-compose these individual services to enable new behaviors.

**Microservices** are a type of service-oriented architecture. Depending on who
you ask, they might differ from SOA because the services are meant to be
*especially* small and lightweight, or that they’re just a synonym of SOA
altogether.

### Problems of Scale

In SOA, individual components communicate directly with each other through a specific API defined by each of the components. To communicate, each component is individually addressable (i.e. using an IP address, service address, or some other internal identifier to send requests/messages back and forth). This means that each component in the architecture needs to know about its dependencies, and needs to integrate specifically with them.

Depending on the topology of the architecture, this can mean that an additional
component might need to know about all the previous components. Also, this can
mean that replacing an individual service that *N* other components already talk
to can be challenging: you’d need to take care in preserving whatever *ad hoc*
API you defined, and make sure you have a migration plan for moving each of the
components from addressing the old service to addressing the new one. Since
service-to-service APIs are *ad hoc* 1, it often means that RPCs between
components can be arbitrarily complicated, which potentially increases the
surface area of possible API changes in the future. Each API change in a service
depended on by many others is a significant undertaking.

What I’m getting at here is that as a microservices ecosystem grows, it starts being susceptible to the following problems at scale:

- N
2growth in complexity of*integration*as the number of components grow,[2](https://blog.eyas.sh#user-content-fn-2) - The shape of a network becomes hard to reason about
*a priori*; i.e. creating or maintaining a testing environment or sandbox will require a lot of reasoning to make sure*no*component within a graph has an external dependency

A few friends volunteered their own problems with Service-oriented architecture at scale:

Another problem with growth of SOA that I’ve seen is dependency cycles between services. Because you roll them out independently and rarely bring up the whole system from scratch, its easy to introduce cycles and break the DAG.


Another problem with SOAs at scale that may be worth calling out is that they require you to know all of your future customer workflows ahead of time. If you don’t—and you segregate data for a single workflow across multiple verticals—then you’re stuck with either performance problems trying to guarantee transactionality across multiple persistent stores or redefining which vertical masters duplicate (cached but really persisted in a db) data.


## Data-Oriented Architecture

In **Data-Oriented Architecture** (DOA), systems are still organized around
small, loosely-coupled components, as in SOA microservices. But DOA departs from
microservices in two key ways:

-
*Components are always stateless*Rather than componentizing and federating data stores for each relevant component, DOA mandates describing the

*data*or*state-layer*in terms of a centrally managed global schema. -
*Component-to-component interaction is minimized*, instead favoring interaction*through the data layer*In our trading system, a component receiving prices for different securities is just publishing prices in a canonical form in our data store. A system can consume these prices by querying the data layer for prices, rather than request prices from a specific service (or set of services) through a specific API.

Here, the integration cost is linearized. A DOA schema change means that up to

*N*components might need to be updated, rather up to*N*connections between them.2

Where this *really* shines is when individual high-level data types are
populated by different providers. If we replace *one* service with *one* table,
then we haven’t simplified things much. The benefit is if there are multiple
sources of the same general data type. If a trading system is connecting to
multiple marketplaces, who each publish requests from customers to an `RFQ`

table, then downstream systems can query this one table and not worry about
where a customer request is coming from.

### Types of Component Communication

Since *component-to-component interaction is minimized* in DOA, how would one
replace the inter-component communication in SOA today with interaction through
the data layer?

#### 1. Data Produces and Consumes

Organizing components into *producers* and *consumers* of data is the main way
to design a DOA system.

If you can, at a high level, write your business logic as a series of `map`

,
`filter`

, `reduce`

, `flatMap`

, and other monadic operations, you can write your
DOA system as a series of *components*, each which queries or subscribes to its
inputs and produces its outputs. The challenge in DOA is that these intermediate
steps are visible, queryable data—which means that it needs to be
well-encapsulated, well-represented, and corresponds to a particular
business-logic concept. The advantage, though, is that the behavior of the
system is externally observable, traceable, and auditable.

In a SOA trading system, a component taking orders from a marketplace might make
RPCs to figure out how to price, quote, or trade on an order. In DOA, a
microservice takes requests from marketplaces (usually in a SOA manner) and
*produces* RFQs, while other producers are producing pricing data, etc. Another
microservice queries for RFQs, joined with all their pricing and outputs quotes,
orders, or whatever custom response datums are needed.

#### 2. Triggering Actions and Behaviors

Sometimes, the simplest way to think about communication between components *is*
as an RPC. While a well-designed DOA system 3 should see a majority of its
inter-component communication replaced by producer/consumer paradigms, you might
still need direct ways for component X to tell Y to do Z.

First, it’s important to consider if RPCs can be reorganized as *events* and
their *effects*. I.e., asking if, rather than component X sending RPCs to
component Y where event *E* happens, can X instead *produce* events *E*, and
have component Y drive the responses by consuming these events?

This approach, which I’ll call **data-based events**, can be a powerful
inversion of how we typically have component communication. The reason it is so
powerful is because it allows us to take the term *loosely-coupled* to the next
level. Systems don’t need to know who is consuming their events (rather than an
RPC caller who absolutely needs to know who they’re calling), and producers
don’t need to worry about where the events are coming from, just the
business-logic semantic meaning of those events.

There is, of course, a naïve way to implement data-based events, where each
*event* is persisted to a database in its own table corresponding 1:1 with a
serialized version of a the RPC request. In that case, data-based events don’t
decouple a system at all. For data-based events to work, translating a
request/response into persisted *events* require them to be meaningful
business-logic constructs.

Data-based events might not be a good match. For example, if you actually want
to trigger a behavior in a *specific* component. In those cases, leaving a
*limited* number of actual **component-to-component RPCs** is probably still
desirable.

## Case Studies where Data-oriented architecture shines

### High Integration Problem Spaces

Part of why I keep mentioning trading/finance software as an example is because
finance often requires a large integration surface area. A typical *sell-side*
firm allowing smaller customers to trade often integrate with many marketplaces
to interact with customers, and many liquidity providers to get prices and place
orders. The business logic that needs to happen between when a request comes in
on a marketplace and a response comes out to the customer is a complex,
multi-stage process.

In a high-integration problem space, individual services might need to know
about *a lot* of other services. To avoid an *O(N 2)* integration
cost, and to avoid complex individual services with a high fan-out ratio,
rearchitecting a system around data producers and consumers allows integrations
to be simpler. If a new integration comes along, rather than having to edit

*N*new systems, or one system which has a complex fan-out to

*N*other systems, the integration process can involve writing one

*adaptor*that produces data in the common DOA schema, and consumes the final output and renders it in the right wire format.

Implicitly, there’s a new kind of complexity in integration: thinking about the
schema. Any new integration should feel *native* to your system, and your schema
should be extended without adding shims, hacks, and special cases. This, in and
of itself, is a hard exercise. When the number of integrations is sufficiently
high, however, the difficulty amortizes and is often worthwhile.

### Sandboxing Data, and Reasoning about Data Isolation

![Toys in a Sandbox](../../assets/f698cd050611f1a5.img)

If you’re prototyping or testing things manually, you’re hopefully doing it outside of production. Yet the way some SOA ecosystems are architected often means that it’s not easy to know what environment a service is in, or if a particular environment is self-contained at all.

An **environment** is an internally-consistent, consistently-connected
collection of services, usually/ideally structured in the same topology as
production. Since SOA services are typically independently addressable,
environment consistency predicates that every service must agree with every
other service in an environment on which address to call for what. The RPC,
pubsub, and data flow must not *leak* from one environment to another.

There are obviously ways around this in SOA, like shifting to service registries
that generate the right configuration for services 4, or, when services are
accessed through a URI, hiding direct service addresses in favor of different
paths under an environment prefix

.

[5](https://blog.eyas.sh#user-content-fn-5)In DOA, however, the concept of an *environment* is much simpler. Knowing which
data store layer a component connects to is sufficient to describe what
environment it is in. Since all components store no state internally, data is
isolated by definition. There’s no danger of leaking data from one environment
to another, as components only communicate via the data store.

## Data-oriented Architecture is closer than you think

There are a lot of common examples that approximate data-oriented architecture today. A data monolith where all (or most) data is persisted in one large data store, often signals that a system’s architecture is approaching DOA.

[Knowledge Graphs](https://en.wikipedia.org/wiki/Ontology_(information_science)),
for example, are a generalized data monolith. That said, they’re often not
generic enough; with a lot of *state* related to business logic potentially
missing.

[GraphQL](https://graphql.org/) is often used as a normalized datastore layer,
like a data monolith. The degree to which GraphQL can be a successful backend to
a DOA system is more about the system’s choices of schema design: choosing
generalizable schema and tables related to business logic concepts, rather than
schema and tables specific to the specific source of this data.

## It’s all about the trade-off

This architecture is not a magic bullet. Where data-oriented architecture erases
classes of problems, new ones arise: It requires the designer to think hard
about data ownership. Situations where multiple-writers are modifying the same
record can be tenuous, often encouraging systems to carefully partition record
*write* ownership. And because inter-component APIs are encoded in the data,
there is one shared, global schema that must be well-thought out.

I’m reminded of Google’s Protocol Buffers documentation, which, in a discussion
of marking fields in a schema as `required`

warns:
[Required Is Forever](https://developers.google.com/protocol-buffers/docs/proto#required_warning).
At Broadway Technology, CTO Joshua Walsky used to say something similar about
DOA schema: *Data Is Forever*. For reasons similar to the Protobuf warning, it
turns out, removing a column from a table in a loosely-coupled distributed
system is *really*, *really* hard.

My two cents: If you find yourself worrying about your architecture scaling
*horizontally*, you might think about designing it with a data monolith in its
center.

## Footnotes

-
Service-to-service APIs not

*necessarily**ad hoc*, but direct component-to-component communication often means that it’s easy to pass parameters between the two for a given purpose.[↩](https://blog.eyas.sh#user-content-fnref-1) -
Whether an architecture

*really*reaches N2growth in*integration complexity*is really dependent on it’s architecture topology. If you’re in a system where*integration*is one of your bottlenecks, you likely hit this problem.For example, a trading system integrating with various liquidity providers and OTC marketplaces should ideally not be in a situation where each component managing orders from a marketplace needs to know about each component providing liquidity.

[↩](https://blog.eyas.sh#user-content-fnref-2) -
One that is well-suited for DOA

*and*well-designed, that is.[↩](https://blog.eyas.sh#user-content-fnref-3) -
Assuming services call each other based on a direct address (e.g. an IP, or some internal address schema to a running process), and services know

*where to reach a particular service*based on command line parameters, one might need to wrap those with better-suited logic that constructs the right flags depending on the environment.[↩](https://blog.eyas.sh#user-content-fnref-4) -
e.g. rather than reaching a particular service by an IP address or some internal URI specific to that service, structuring each service to be served under a “path” routed by one server. E.g. rather than

`://process1.namespace.company.com/*`

, you talk to`://env.namespace.company.com/Employees/*`

.[↩](https://blog.eyas.sh#user-content-fnref-5)