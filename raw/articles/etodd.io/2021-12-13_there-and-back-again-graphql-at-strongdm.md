---
title: 'There and Back Again: GraphQL at strongDM'
url: https://etodd.io/2021/12/13/there-and-back-again-graphql-at-strongdm/
published: '2021-12-13'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# There and Back Again: GraphQL at strongDM

*This post originally appeared on the strongDM engineering blog.*

Once upon a time, strongDM had no dedicated frontend engineers. We backend engineers dipped our toes in the React frontend as infrequently as possible. It relied on dusty, bespoke, private REST endpoints that returned schema-less JSON blobs. We let these languish while we built a shiny new public API with code-generated SDKs in five languages. Occasionally I was forced to write a new private endpoint for the frontend. I did so with shame, dreaming of a future when the whole frontend would only talk to the public API. Then one day, we hired a frontend engineer, and everything changed.

The new frontend team quickly grew to three engineers. Almost immediately, they ran into problems with our public API. The very first feature they attempted was related to the free 14-day trial strongDM offers to new customers. We didn't want to expose this feature in our Terraform provider or other SDKs. So we added some smarts to the code generator to exclude certain parts of the API from these SDKs, while the Typescript SDK included everything. The public API now had a private corner to it.

More problems followed. The public API was designed around a set of objects: users were objects, roles were objects, attachments between the two were objects. When the frontend needed to load a page of users and roles, it had to make one request to load the users, then another request per user to load their attachments, then even more requests to look up the roles on the other end of those attachments. This is known as the "N+1 requests" problem (where N is the number of users).

We refused to admit defeat and go back to custom REST endpoints for the frontend.
Instead we decided to try GraphQL, which was invented precisely to address the proliferation of frontend requests.
We threw together a GraphQL API in two days.
We quickly learned to test our work with [Insomnia](https://insomnia.rest/), which offers one-click GraphQL autocomplete and schema validation.

![Native GraphQL support in Insomnia](../../assets/6cf2d9e4da95c911.png)

On the backend team, we instantly fell in love with GraphQL and our library of choice, [gqlgen](https://gqlgen.com/).
It was easy to grok, and the assumptions it made fit our codebase well.
The schema definition language alone was a huge improvement over anything I had seen before. (OpenAPI, I'm looking at you.)
We got something running with only a thin layer of code on top of our existing public API functions.
Unfortunately, it was not a silver bullet.

The frontend team spiked prototypes with a few different GraphQL libraries and eventually chose [Relay](https://relay.dev/).
We quickly discovered that Relay imposes a lot of requirements on the GraphQL schema.
All objects must have a unique ID for caching purposes.
Relationships between objects must conform to a [somewhat verbose standard](https://relay.dev/graphql/connections.htm).
In our API and SDKs, relationships between objects are also objects themselves, complete with IDs.
But Relay views these relationships as second-class citizens known as "edges", which generally have no IDs and are not cached.

This mismatch caused some confusion between the teams, especially around the user-to-role relationships. The frontend team wanted them removed from the schema, while the backend team wanted to maintain some amount of parity with the concepts and nomenclature used in the API and all the other SDKs. After some discussion, the frontend team let us depart from Relay standards a bit by putting the relationship IDs in the edges. In practice, the ID only became important when deleting the relationship. The frontend team agreed to cache the IDs and make Delete requests on them.

Several months later, responsibility for the GraphQL backend shifted to a different team of engineers. The information handoff (done by me) was woefully inadequate, and user-to-role relationships returned as a hot topic for several weeks until the original solution was rediscovered. This issue has been a source of confusion from the beginning, and I suspect we haven't seen the end of it yet.

Despite the challenges, the frontend engineers have been generally thrilled with GraphQL.
Tooling on their side gives them type safety and other benefits.
They can write GraphQL [query fragments](https://graphql.org/learn/queries/#fragments) for each React component, which are compiled together into one big query for the whole page.
If someone edits a component to no longer rely on a piece of data, that data will no longer be sent down from the server, and could potentially not even be queried from the database.

On the backend team, we can't wait to decommission the "private corner" of our public API.
The GraphQL interface reuses 80% of the code from our many other interfaces, but it also offers a well-supported place to put the extra 20% of frontend-specific code.
And it's nice to have ready-made answers from the GraphQL ecosystem for things like [real-time updates](https://www.apollographql.com/docs/react/data/subscriptions/), which are critical for our business.

What have I learned? [Don't build a general purpose API to power your own front end](https://max.engineer/server-informed-ui).
There will always be some bespoke private endpoints.
That said, GraphQL gave our general-purpose API a massive boost toward becoming the perfect interface for our frontend.
It provided a solid foundation for the backend and frontend teams to iterate on and a ton of quality-of-life improvements for everyone.