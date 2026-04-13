---
title: Month Archives for May 2019
url: https://blog.eyas.sh/2019/05/
author: Eyas Sharaiha
published: '2019-05-22'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Last time, we talked about
[modeling the Schema.org class hierarchy in TypeScript](https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/).
We ended up with an elegant, recursive solution that treats any type `Thing`

as
a `"@type"`

-discriminated union of `ThingLeaf`

and all the direct sub-classes of
the type. The next challenge in the journey of building TypeScript typings for
the Schema.org vocabulary is modeling
[Enumeration](https://schema.org/Enumeration)s.

Let’s look at a few examples from the Schema.org website to get a better sense of what Enumerations look like.

[Read more →](https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/)