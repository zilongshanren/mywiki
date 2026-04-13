---
title: Month Archives for December 2018
url: https://blog.eyas.sh/2018/12/
author: Eyas Sharaiha
published: '2018-12-21'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

My previous articles on [using AsyncPipe](https://blog.eyas.sh/2018/12/use-asyncpipe-when-possible/)
and
[data refresh patterns in Angular](https://blog.eyas.sh/2018/12/data-and-page-content-refresh-patterns-in-angular/)
hint at some common anti-patterns dealing with Observables. If there’s any
common thread in my advice, it is: **delay unpacking an Observable into its
scalar types** when performing logic you can rewrite as side-effect-free,
leaving code with side-effects for subscription callbacks and other downstream
logic.

My two earlier articles focused on cases users can benefit from handling more of
the object’s lifecycle in its Observable form. In other words, cases where the
Observable was being subscribed to and unpacked *too soon*. Instead, I suggested
transforming the Observable using operators like `map`

, `switchMap`

, `filter`

,
etc. and taking advantage of the power offered by this form. In the case of
Angular, it provides `AsyncPipe`

, which takes the care of the step with
side-effects (actually rendering the page) in template code.

[Read more →](https://blog.eyas.sh/2018/12/observables-side-effects-and-subscriptions/)