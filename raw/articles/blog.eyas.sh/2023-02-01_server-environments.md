---
title: Server Environments
url: https://blog.eyas.sh/2023/02/server-environments/
author: Eyas Sharaiha
published: '2023-02-01'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

When maintaining large software systems, you will likely have multiple
*environments* with names like Prod, Staging, Dev, Eval, UAT, Daily, Nightly, or
some remix of these names. To distinguish *this* type of environment from the
dozen other things in software development that we give that same name, these
are often formally referred to as **Deployment Environments**.

One question I’ve *never* been asked directly is: *“What is an Environment?”*
This is surprising; because not understanding what Deployment Environments
*actually are* is one of the most common pitfalls I see in my day-to-day work.

## What is a Deployment Environment

A **Deployment Environment** is a *consistently connected* set of

- processes
- datastores, and
- any ecosystem around them (e.g., cron jobs, analytics, etc.)
[1](https://blog.eyas.sh#user-content-fn-1)

making up a fully functioning software system.

This definition is quite intuitive, but the devil is in the details. In this
case, that detail is the phrase *“consistently connected”*.

### What *consistently connected* entails

Ideally, environments should be *perfectly isolated*; no data or RPC should leak
between processes and data stores across environments during normal
operation 2.

#### A Case Study

*This concrete example convinces the uninitiated that you should never mix
dependencies across environments (e.g., Dev instances should only call other Dev
instances; never prod instances). If this is already intuitive for you, you can
skip this section and
go straight to the principles of consistent connectedness.*

An architecture representing a To-do system with some interdependencies.

Imagine the architecture above represents a system you maintain. Each box here
represents either a *service* or a *datastore*. Right now, you have one instance
of each of these endpoints, and they’re connected as you see above. Let’s say
these systems are connected by directly addressing each other (e.g., by calling
specific URIs for each service). Real people are about to use this service, but
you want to continue deploying more recent versions.

You might decide to create a set of *Dev* instances to help you out.

You might wonder: *How many instances do I need to set up and configure to have
a viable Dev environment?*

What is *viable* will certainly depend on which endpoints you care about
testing.

Let’s assume you want to test `TodoApi`

. This service:

- Calls
`PeopleApi`

- Reads and writes to
`TodoStore`

- Is
*called by*`PeopleApi`

- Is
*called by*`HttpBackend`


Generally, if you can exercise the service you’re interested in directly, you might not care about its callers.

Next, you have to decide:

- which
`PeopleApi`

should this instance call, and - which
`TodoStore`

should this instance read and write to?

Remember that `PeopleApi`

will call `TodoApi`

back. It’s very tough (and almost
*always* wrong) to try to get away with calling the *Production* instance of
`PeopleApi`

from your *Dev* instance of `TodoApi`

; the production instance you
call might mutate the production state, or it might call back the production
instance of `TodoApi`

instead of you. You might convince yourself it’s harmless,
but more often than not, you’ll be met with subtle glitchy behavior at best and
serious bugs or user data leaks at worst.

Instead, you’ll want an entirely separate *Dev* instance of `PeopleApi`

in its
own right. As you configure **this dev instance of PeopleApi**, you will have

**only one correct choice**for which

`TodoApi`

to call: the Dev instance we
just created.We will also likely want a separate `TodoStore`

database to be available to the
Dev instance of `TodoApi`

, with totally separate tasks, etc. This allows us to
make sure none of our *read/write* testing has the potential to affect
production users.

This line of reasoning applies recursively and can help you arrive at some general principles.

### Principles of consistent connectedness

An *instance* of a service or datastore can be described as being *in* an
environment. An instance can be *in exactly one environment*, and we can usually
identify a specific instance **by what environment it is in**. If an
architecture diagram includes a `TodoService`

, we can refer to instances of that
service as *“TodoService Prod”*, *“TodoService Dev”*, etc.

Given this, for any environment *Env*, an instance is in *Env* if and only if:

- it is only called by other instances in
*Env*, - it only calls instances in
*Env*, and - the instances it calls are equivalent in topology to the architecture diagram of Production (or a strict subset).

These principles of course have their limits if you stretch the definitions of
words like *process* and *call*. For example, as long as you have good
addressing separation, your distinct environments do not need to live on
non-overlapping servers or live in separate clouds. Other core infrastructure
might also be exempt if it has strong environment separation and does not need
to have separate testing instances brought up often.

## What you shouldn’t do with a Deployment Environment

To maintain a *valid* environment, there are a few things you shouldn’t do (that
plenty of people do):

-
**Decide that a given instance in some environment actually makes more sense to call another instance in another environment.**Trust me, 99.99% of the time, it isn’t.

You might tell yourself, for example:

*“Oh but the Dev instance doesn’t have interesting data”*;*“my Dev instance should call the Prod photo catalog service!”*.You’re almost always better off doing something else, like seeding fake photos in the

*Dev*photo catalog instance and continuing to call that, or setting up a cron job that copies over photos from the prod catalog to the dev catalog, after making sure they’re stripped of any sensitive data, etc.You might convince yourself none of the pitfalls apply today (“the

*Prod*service I’m calling is stateless”; “the*Prod*service I’m calling is a sink”), but it’s often hard to guarantee this will always be the case. Exercise plenty of caution when you are forced to do this. -
**Treat an instance of a service you own that exists in some environment as “internal to your team”.**If you have a

*Dev*environment, in your company, and your team maintains the`TodoService`

, you might consider saying “TodoService Dev is for our team only, no one else should call it”. This will often break consistent connectedness, however.Other teams’ Dev instances

**should**call*your*Dev instance. Your Dev instance should do the same.If you want an internal service only you can call, it should be totally sandboxed. You will of course run into trouble if your instance has dependencies that can’t be stubbed out since your sandboxed instance might violate consistent connectedness if it writes to other teams’ Dev datastores.


## The challenge with maintaining valid environments

The challenge, for many, in maintaining a valid, consistently connected
environment is **addressing**.

Addressing, in this context, describes how a given instance describes
*which other instance* it is going to interact with (i.e., services to call,
pubsub channels to broadcast to or listen from, databases to read from or write
to).

Services, databases, and pubsub channels might identify themselves with nothing but an IP and port, a full URI, a process ID, or some other naming and addressing scheme.

Each service must have a way to address all of its dependencies, either written in its configuration, passed into it through command-line flags, encoded in the binary, etc.

If the addressing and configuration scheme in a given setup is brittle, then so
will the topology and health of the deployment environments. For example,
service that identifies its dependencies by an arbitrary host and port (say,
`[::1]:8001`

for `PeopleApi`

and `[::1]:8002`

for its `TodoStore`

) in
command-line flags is very easy to contain mistakes. That service will also have
trouble programmatically verifying that it is correctly connected.

A smaller organization might get away with a slightly more brittle addressing scheme than a larger organization. When stretching the brittleness to the extreme (e.g., hosts and ports passed by hand to command-line flags), however, even the smallest organizations will have trouble keeping healthy environment separation.

While some enjoy the flexibility of configuration setups where we can
individually *pick and choose* what each dependency address should be,
internalizing the importance of *consistent connectedness* will help us notice
that this approach is often *more brittle than powerful*.

## Approaches to Consistent Connectedness

### Endpoint Registries

Can we restructure and centralize our configuration into a *registry*? Rather
than a client specifying the address of the instance it wants, it provides an
`(Environment, Service)`

pair (e.g., `("dev", "TodoService")`

) to a registry
that is responsible for returning the correct address.

Such registries can be built into binaries, libraries that themselves consume registry data that is pushed regularly, or simply middleware layers that abstract away brittle configuration.

### Relative URI Addressing Schemes

If instances can address each other via a URI, we can *invert* the concept of an
Endpoint Registry to our benefit.

Rather than services that accept traffic on a host and port, we can set our
services up to accept traffic at **a specific path**. We can then set up a
server that accepts traffic to a hostname for an environment and routes the
traffic to the individual services in that environment.

We can have services like `/_/api/TodoService`

and `/_/api/PeopleService`

. In
Dev, we have a hostname like `dev-todoapp.acme.com`

that serves these paths
through the Dev instances.

In this case, we can have

`todoapp.acme.com`

(Production)`todoapp.acme.com/_/api/TodoService`

`todoapp.acme.com/_/api/PeopleService`


`dev-todoapp.acme.com`

(Development)`dev-todoapp.acme.com/_/api/TodoService`

`dev-todoapp.acme.com/_/api/PeopleService`



In this case, services can address each other through hostname-relative URIs.
`TodoService`

can address `PeopleService`

in its code by `/_/api/PeopleService`

.

### Smash the Topology with Data-Oriented Architecture

Other architectures, like
[Data-Oriented Architecture](https://blog.eyas.sh/2020/03/data-oriented-architecture/), allow us to
ditch complicated topologies in favor of routing all interactions through a
*Data Access Layer* monolith.

Because all process-to-process interaction in Data-Oriented Architecture goes
through a Data Access Layer (DAL), an environment is effectively **defined by
which** data layer it talks to.

A `TodoService`

writing `Todo`

objects into a DAL and querying `People`

objects
will always be dealing with consistent data.

A `TodoService`

that addresses the Prod DAL is writing & reading Prod `Todo`

s
and is querying Prod `People`

. A `PeopleService`

talking to that DAL is
necessarily the Prod instance! Without loss of generality, we can say the same
about services talking to the Dev DAL, and so on.

## A Better Definition of Environment

So far, I’ve described *deployment environments* that are 1:1 with the
datastores that make up the system. However, if your system architecture allows
you to have multiple replicated services talking to the same data store, you
might wonder to what extent is the data store isolation important.

One way to add nuance to our definition of a deployment environment is to also
define **Storage Environment** as a distinct concept.

A Storage Environment is a consistently connected set of datastores that represent the state of the world according to that environment.

For a consumer product, there will typically be a single **production** storage
environment, and more internal (fake, test, dev) storage environments for
testing. For business-facing products, each customer’s “production” environment
can be its own storage environment.

Armed with the definition of a storage environment, a Deployment Environment can
be defined as a consistently connected set of processes & an ecosystem that
*agree on a storage environment*.

Typically, a consistently connected set of processes would share *some property*
in common. For instance, mature builds can make up a production environment,
while cutting-edge builds might make up a development environment.

For example, imagine a company that has two *Storage Environments*:

**public****testing**

and uses those to create a few environments:

- Production (
`public`

storage environment with`release`

binaries & schemas) - Staging or RC (
`public`

storage environment with`rc`

binaries & schemas) - Nightly (
`public`

storage environment with fresh binaries & schemas) - QA (
`testing`

storage environment with`rc`

binaries & schemas) - Development (
`testing`

storage environment with fresh binaries & schemas)

While each instance in a deployment environment must agree on the storage
environment it is in, you’d be forgiven to wonder whether *consistent
connectedness* within a deployment environment is as important as it was under
the old definition.

Consistent connectedness is certainly not *as* crucial in this definition. For
example, you might decide that *Nightly* in the definition above is more useful
if each instance (in the `public`

storage environment) with fresh binaries is
calling the production binaries. A common motivation for this is to isolate bugs
to a specific service, i.e. you don’t want a bug in `PeopleService`

to make it
look like `TodoService`

is also broken.

In practice, though, especially because many dependency and call graphs can be
quite circular, it’s actually hard to isolate the effects of a broken service
that way. For example, if `Nightly`

services called `Production`

services, it is
unclear if a break in the nightly `TodoService`

would manifest in a failure
**in** `TodoService`

, rather than one in the *Production* `PeopleService`

, as a
result of a malformed payload/call from the *Nightly* `TodoService`

.

If you have no such cycles in your architecture diagram, such schemes might work for you, but my general recommendation is to continue value consistent connectedness for its simplicity.

## What about Sandboxes?

Sandboxes are typically isolated sub-sets of an architecture of a given system. If a Sandbox is truly isolated, it can be an excellent way to test a given service, with the immediate dependencies that concern it.

Some architectures lend themselves well to sandboxing (e.g., Data-Oriented Architecture) where missing components simply stub out parts of some functionality but never break an active call chain. Other architectures might rely on stub implementations to achieve the desired result.

Often still, however, many sandboxes will *leak out in the edges* to a real
long-running environment. In that case, it is important to think carefully about
what is and isn’t a valid sandbox construction.

A few pointers can help:

- Just like an
*instance*of a service or datastore, a Sandbox itself can be said to be**in**a particular environment - If an architecture diagram includes a cycle, that entire cycle should be either inside or outside of the Sandbox, in other words, an instance in a Sandbox should not try to call an instance that won’t call (transitively?) call it back
- A sandbox should leak to
*at most one*environment; in other words: the edges of the sandbox that are communicating with real instances must all communicate to instances in the same environment - Production is almost always the wrong environment to leak a sandbox into, but will often be the most tempting.

## Closing Thoughts

I don’t think anyone *ever* asked me *“What is an environment?”* Yet I’ve
certainly found myself arguing against configurations of large systems that
effectively cross and break environments. Terms as ubiquitous as “environment”
often feel obvious at first glance, but not too much more.

Here, I tried to give a strongly-worded view of how an environment can be defined. Rules are meant to be broken, and I’ve broken all of these rules (to mixed results). So my goal isn’t to tell you, dear reader, the One True Way, but rather, to communicate an ideal that, if we veer away from, we do so consciously.

## Footnotes

-
I include the rest of the ecosystem around this for completeness, but often it’s sufficient to think of a Deployment Environment simply as a consistently connected set of processes & datastores.

[↩](https://blog.eyas.sh#user-content-fnref-1) -
Explicit processes that exist

*beyond*the bounds of any environment may purposely interact with multiple environments. For example, it might be desirable to sync or seed some test data between environments, etc.[↩](https://blog.eyas.sh#user-content-fnref-2)