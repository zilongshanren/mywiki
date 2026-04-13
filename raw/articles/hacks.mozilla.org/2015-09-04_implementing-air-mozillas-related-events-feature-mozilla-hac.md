---
title: Implementing Air Mozilla’s Related Events Feature – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2015/09/implementing-air-mozillas-related-events-feature/
author: Gloria Dwomoh
published: '2015-09-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Editor’s note:**It’s not often that we hear from web developers and software engineers at the start their careers here on the Hacks blog. This post is a great reminder of what it’s like.*

Mozilla participates in [Outreachy](https://wiki.gnome.org/OutreachProgramForWomen), and offers internship opportunities to bring women and other under-represented groups into the world of [free and open source software](https://en.wikipedia.org/wiki/Free_and_open-source_software). The [application process for the upcoming round](https://wiki.gnome.org/Outreachy/2015/DecemberMarch) will open on September 22, 2015. The application deadline is October 26. Internship dates will be December 7, 2015 to March 7, 2016. If you’ve been thinking of applying, read this, be like Gloria – and go for it!

### How I became a Mozilla intern

It was a spring night in Greece when I got the news I’d been selected by Mozilla to be an [Outreachy](https://outreachy.gnome.org/) intern. Outreachy is a project of the [Software Freedom Conservancy](https://sfconservancy.org/) that helps people from groups underrepresented in FOSS (free and open source software) to get involved by offering focused internship opportunities with a number of open source software organizations. That night, I was the happiest person in my town, I believe. I remember rushing to say a big thank you to my mentor [Peter Bengtsson](https://mozillians.org/u/peterbe), before I got too overwhelmed with happiness to the point that I forgot to be grateful. It was a two-way street. I chose Mozilla and Mozilla chose me.

I started contributing to [Air Mozilla](https://air.mozilla.org/) in March 2015, by solving beginner-friendly bugs. Initially I didn’t want to apply at all, because there were too many wonderful contributors, and in some way I felt overwhelmed by how rigorous the process was. I told several people I won’t apply because I am afraid I won’t be getting it, and sometimes it is okay to be afraid, but it is not okay to be afraid of something you are capable of achieving to the point of sabotaging yourself.

After several pep talks, I went to view the list of the companies and decided to apply only for Mozilla. It will be a hit or miss, I told myself. I noticed it listed “Python” and I was aware that I didn’t know Python that well as it was something I self-studied briefly in the past, but I told myself to go ahead and try. Sometimes you need to do hard things to get the experience you want. Every expert was once a newbie. I went to check Bugzilla to see what I could fix. One bug looked very easy, so I thought I should work on that. That’s how it all started. Feedback after feedback, perseverance, pull, merge, merge conflicts, and getting a deeper understanding of how the code base functions made me able to contribute a lot more. One thing I loved about interning with open source is the fact that everything is open. I was asked to blog about what I worked on, and I didn’t need to hide anything that concerned it. Well… that doesn’t mean I shared my passwords too though! Passwords need to be protected and secret for a reason.

### Getting to work on Air Mozilla

The internship day officially started on May 25th. I was told that after discussions I am being assigned to add a new feature. That new feature will act as a recommendation system suggesting similar events to Air Mozilla viewers while they view a specific event. [Air Mozilla](https://air.mozilla.org/) is a platform for Mozilla’s online multimedia presence that provides live and pre-recorded shows, interviews, news snippets, tutorial videos, and features about the Mozilla community.

That sounded fascinating. I wasn’t nervous at all, it seemed pretty interesting and I always wondered how those things worked, that’s until I started getting really stuck down the road. Then I realized the complexity of it. I had to either build my own algorithms and computations to do the job, or find an open source tool we could use instead of reinventing the wheel. After several days of research we decided [Elastic Search](https://www.elastic.co/) seemed like a good fit. Elastic Search, is a search server. It has a function called “More Like This” and that helps you search for similar events based on your set parameters. I went and read the documentation of Elastic Search but to be honest, I had a very hard time navigating it. Mostly because I couldn’t find enough examples on how to use it with Python. At some point we decided [pyelasticsearch](https://github.com/pyelasticsearch/pyelasticsearch) might make things easier; it’s a Python library version of Elastic Search that has the functionalities we were looking for.

For a short recap, Elastic Search creates a mapping and indexes all the events on Air Mozilla. When you visit an event page, with the “More Like This” feature, we ask it to search the indexed events that are similar to the event you are currently viewing and return back the title, id, tags and its similarity scores on the back-end. For events to be considered related, their tags, channel and titles must be very much alike, but that’s not where we stop.

We also need to be able to set someone’s level of access: a person who is logged in as a Mozilla employee will have more access than an anonymous guest would. A logged in volunteer contributor will have more access than an anonymous guest, but less than a Mozilla employee. You get the idea. Each event has its own access level setting. Some events are private and limited to employees, while the majority of Air Mozilla events are accessible to the public or to members of the entire Mozilla community. Regardless, the Related Events feature lets people see a list of similar events, filtered for their level of access, with the most similar “related events” appearing on top.

### Implementing Elastic Search

In the code below we are using the *more_like_this (mlt)* query. We break the tags and the titles into different queries because we want to boost the relevance score of each one to a different degree. In this case we want a similar title to have a higher relevance score than the similar tags. The field parameter is used to determine which field we are trying to run *mlt* against, the docs parameter is the documents we are trying to find similar events for. You can read more about this at the [More Like This Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-mlt-query.html) page.

mlt_query1 = { 'more_like_this': { 'fields': ['title'], 'docs': [ { '_index': index, '_type': doc_type, '_id': event.id }], 'min_term_freq': 1, 'max_query_terms': 20, 'min_doc_freq': 1, 'boost': 1.0, } } mlt_query2 = { 'more_like_this': { 'fields': ['tags'], 'docs': [ { '_index': index, '_type': doc_type, '_id': event.id }], 'min_term_freq': 1, 'max_query_terms': 20, 'min_doc_freq': 1, 'boost': -0.5, } }



Below we are asking that one or more of the given *mlt* queries should match the documents, i.e., list of events:

query_ = { 'bool': { 'should': [mlt_query1, mlt_query2], } }



Below, with `request.user.is_active`

we are checking if the user is logged in and what their access level is. If the user is logged in as a volunteer the events that appear *must not* contain events that are restricted to Mozilla employees only.

If the user is logged in and is not a volunteer, that means they are Mozilla paid staff members. Their “related events” results should contain all events that are similar to the event we are currently viewing.

In the case of an anonymous user, the “related events” results *must* contain only events that are accessible to everyone.

if request.user.is_active: query = { 'fields': fields, 'query': query_ } else: query = { 'fields': fields, 'query': query_, "filter": { "bool": { "must": { "term": {"privacy": Event.PRIVACY_PUBLIC} } } } }

In the code above you see we used the *more_like_this* query along with a filter. *More_like_this* does return similar events based on title, tags and channels but it doesn’t ensure that the events returned are filtered by access level. So this is where `“filter”`

comes in. It makes sure to filter the relevant events and allow only the ones the user can view based on their level of access.

With the use of cron jobs I completely delete and re-index the index for the week, and every 10 minutes we re-index (without first deleting) all events that have changed in the last 10 minutes.

AJAX queries were used to get the thumbnails and links of the related events. AJAX loads asynchronously, so running those queries doesn’t slow the pageload. When I view an event, I want it to load the page fully without waiting for Elastic Search to finish running the queries. Elastic Search queries run pretty fast but it still takes some time. Sometimes, it can be slow. The relevant events section appears under the events’ details. Ideally, someone watching an event won’t mind if there is a slight delay in the loading of the related events while they view the event, however a page that loads slowly as a whole can be frustrating. Through AJAX our Elastic Search queries can run in the background after the page has loaded.

In the screenshots below, you can see how it works. I have added red arrows to the title of event we are on and the title of the first recommended event. If you compare both pictures you can see how the events we are viewing, and/or recommending, relate to each other.


### 4 key things that make you realize how much you enjoyed your internship:

- Your mentor made sure you took the right steps to learn a lot.
- You feel that every portion of it, even the frustrating moments, made you grow not only in skills but as a person.
- You were extremely happy you got it.
- You are extremely sad it is ending.

That’s exactly how it’s been for me. I want to take a moment to thank Outreachy, my mentor Peter, and the other Mozillians I met on IRC and in email during my internship. Thank you for being helpful, welcoming, and for contributing to my learning experience.

What made the pensive ending of my internship bright and merry is a motto Mozilla takes pride in: Once a Mozillian, Always a Mozillian.

## About
[
Gloria Dwomoh ](http://www.gloriadwomoh.me/)

Gloria Dwomoh studied Informatics and Computer Engineering at Piraeus University of Applied Sciences in Greece. She enjoys problem solving, learning new things, and coding. She is always on the look out to find ways to improve her technical skills through open source contributions, self-study, and other methods. She is a generalist with many talents. You can read more about her at her personal blog: gloriadwomoh,me/blog