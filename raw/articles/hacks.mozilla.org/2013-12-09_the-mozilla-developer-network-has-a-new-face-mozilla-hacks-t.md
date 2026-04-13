---
title: The Mozilla Developer Network has a New Face – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/12/the-mozilla-developer-network-has-a-new-face/
author: David Walsh
published: '2013-12-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last summer the [Mozilla Developer Network (MDN)](https://developer.mozilla.org/en-US/) underwent a massive platform change, moving from a hosted third-party solution to our own custom Django application code-named [Kuma](http://github.com/mozilla/kuma). That move laid the ground work for our latest major MDN upgrade: a complete front-end redesign, included many new features as well as usability and accessibility enhancements. Let me provide you with a quick overview of what you can expect to see on the new MDN and what features we’re cooking up for the future!

## New MDN Features

### Increased Commitment to Search

The majority of MDN users are looking to find documentation the moment they land on the MDN homepage, so we’ve placed search front and center:

We’ve also added search filters to the mix, allowing users to narrow down search results to their specific needs:

From a technical perspective, we’ve moved to Elasticsearch for search, allowing us to continue making indexing and filtering improvements, as well as add new search features at will. We anticipate fine-tuning search as we receive feedback so we’ll continue the push to get you to better documentation faster.

### Ease in Navigation

Getting from document to document was a pain point in the previous design, so we’ve fixed that in two ways. The first was creating Content Zones, a method for creating navigation for a given topic. We’ve started with the most prominent parts of MDN, including [App Center](https://developer.mozilla.org/en-US/Apps), [Firefox](https://developer.mozilla.org/en-US/Firefox), [Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS), [Firefox Marketplace](https://developer.mozilla.org/en-US/docs/Mozilla/Marketplace), [Add-ons](https://developer.mozilla.org/en-US/Add-ons), and [Persona](https://developer.mozilla.org/en-US/Persona):

#### Content Zones

MDN’s new Content Zones provide a complete collection of documentation about a given topic, encompassing the very basics of a topic to API details and advanced techniques. We’ll be kicking off with the following zones:

Highlights of the Firefox OS zone include:

- A detailed Platform Guide
- Build and Install details
- Hacking Firefox OS
- App Design & Development

Highlights of this zone include:

- App submission and review
- App publishing and monetization
- Marketplace API information

Highlights of the App Center zone include:

- Quickstart Guide
- Design and Build tips
- App publishing guidelines
- API references

Highlights of the Persona zone include:

- Guide to using Persona on your site
- Becoming an identify provider
- Details on the Persona project

Highlights of the Firefox zone include:

- A complete Firefox Add-on overview
- Information on Firefox internals
- Detailed instructions for building Firefox and contributing

Highlights of the Add-ons zone include:

- XUL extension information
- Best practice tips
- Theming
- Add-on publishing guidelines

#### “See Also” Links

We’ve also implemented “See Also” links which may appear in any wiki page, linking to documents which may be relevant based on the document you’re currently viewing.

Both the zone subnavigation and “See Also” link sidebar widgets are built from basic link lists in the wiki document, so adding links and shuffling navigation is easy for anyone looking to contribute to MDN. These link lists can also be built using MDN’s macro language, Kumascript, and our writing team has done a great job automating “See Also” links so that contributors can save on the manual labor of hunting down other relevant documents.

#### Top level navigation

In the top level navigation, you will have access to five distinct areas:

- The above-mentioned Content Zones
[Web Platform](https://developer.mozilla.org/en-US/docs/Web), including direct links to more information on technologies, references and guides[Developer Program](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_Program)– To be able to help developers and establish long-term relationships and channels, we have created the Mozilla Developer Program. We have a lot of plans and ideas for iteratively expanding the Program, and we want you involved as we do so! So, sign up! You will get a membership, be able to subscribe to our newsletter and get access to features over time as we roll them out.[Tools](https://developer.mozilla.org/en-US/docs/Tools)– more information on the Firefox Developer Tools and their features[Demos](https://developer.mozilla.org/en-US/demos/), being a direct link to the Demo Studio

### Enhanced Kumascript Macro Features

[Kumascript](https://github.com/mozilla/kumascript), MDN’s dynamic macro language, was also outfitted with the ability to read external RSS feeds. At present MDN is using the feed reader capability to pull forum posts from StackOverflow and blog posts from the Mozilla Hacks blog. Check out the [MDN:Common macro](https://developer.mozilla.org/en-US/docs/Template:mdn:common) to view the `fetchJSONResource`

and `fetchHTTPResource`

methods which aid in displaying feed content in wiki documents.

## Future Features

This visual redesign is just the beginning of our push to make MDN more dynamic and usable. The MDN development and UX teams have plenty more coming in 2014. Here are a few peeks into what you can expect to see!

### Dynamic Search Filtering

To improve the efficiency in user search, we plan to implement hashtag-prefixed text filtering which may be added in the initial search — doing so will prevent the need for additional filtering when the user lands on the search results page.

![](http://static.squarespace.com/static/5015397584aea6ed68d41dca/t/52790476e4b0c331152075b7/1383662714993/hhabstritt_commandquery2.png?format=500w)


Holly Habstritt Gaal has [detailed this query system](http://hollyhabstritt.com/blog/2013/11/5/command-query-a-better-filter-and-search-for-developers-on-mdn) in detail on her [blog](http://hollyhabstritt.com/blog/). Check out her blog post to see implementation details.

### Docs Navigator

So you’ve completed a search and you click the first link you thought would be applicable, but you want to move onward and view other results. Instead of backing out to the search results page again, the wiki page (if the user came from search) will display a doc navigator to move to the next or previous result, or you can view the entire list of results from your original search:

Just another handy way of finding what you need faster!

### Demo Studio and Dev Derby Redesign

A redesign to the MDN [Demo Studio](https://developer.mozilla.org/en-US/demos) and Dev Derby will be coming shortly. We have an [excellent design in review](https://bugzilla.mozilla.org/show_bug.cgi?id=925893) and we hope to roll that out in early 2014.

If you have a suggestion or find any bugs within the new MDN, [please let us know](http://mzl.la/mdn-post-redesign-feedback).

Look forward to more from MDN in 2014 and beyond. The MDN platform promises to expand and improve the way we view, write, and experience documentation and web technologies!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 57 comments

ChrisArchitectDecember 9th, 2013 at 13:42groovecoderDecember 9th, 2013 at 14:08LanceDecember 9th, 2013 at 14:10Robert Nyman [Editor]December 10th, 2013 at 03:07gabriele vidaliDecember 9th, 2013 at 14:26Robert Nyman [Editor]December 9th, 2013 at 14:27Chris MoreDecember 9th, 2013 at 14:45Robert Nyman [Editor]December 10th, 2013 at 03:08Ivan DejanovicDecember 9th, 2013 at 16:02Robert Nyman [Editor]December 10th, 2013 at 02:20MaurizioDecember 9th, 2013 at 16:29Robert Nyman [Editor]December 10th, 2013 at 02:20Randy ApuzzoDecember 9th, 2013 at 17:04Robert Nyman [Editor]December 10th, 2013 at 02:21Yaroslaff FedinDecember 9th, 2013 at 18:39Robert Nyman [Editor]December 10th, 2013 at 03:02Andrea GiammarchiDecember 9th, 2013 at 19:10Robert Nyman [Editor]December 10th, 2013 at 03:03Rudolf OlahDecember 9th, 2013 at 22:41Robert Nyman [Editor]December 10th, 2013 at 03:03RolfenDecember 9th, 2013 at 23:04Robert Nyman [Editor]December 10th, 2013 at 03:06VikashDecember 10th, 2013 at 00:11Robert Nyman [Editor]December 10th, 2013 at 03:03FranciscDecember 10th, 2013 at 05:37Robert Nyman [Editor]December 10th, 2013 at 05:53adyDecember 10th, 2013 at 06:06Robert Nyman [Editor]December 10th, 2013 at 06:37adyDecember 10th, 2013 at 09:44thelolcatDecember 10th, 2013 at 08:04Robert Nyman [Editor]December 10th, 2013 at 08:21John SoutarDecember 10th, 2013 at 09:59Robert Nyman [Editor]December 10th, 2013 at 12:52Tin Aung LinDecember 10th, 2013 at 11:34Robert Nyman [Editor]December 10th, 2013 at 12:52Andre JaenischDecember 10th, 2013 at 14:40Robert Nyman [Editor]December 11th, 2013 at 04:00lem torovDecember 10th, 2013 at 23:12Robert Nyman [Editor]December 11th, 2013 at 04:01RummyDecember 11th, 2013 at 04:31Robert Nyman [Editor]December 11th, 2013 at 04:36Felipe Nascimento de MouraDecember 11th, 2013 at 14:17Robert Nyman [Editor]December 11th, 2013 at 15:07Abin AbrahamDecember 11th, 2013 at 21:20Robert Nyman [Editor]December 12th, 2013 at 02:41DerekDecember 12th, 2013 at 02:09Robert Nyman [Editor]December 12th, 2013 at 02:42DwayneDecember 12th, 2013 at 06:28Robert Nyman [Editor]December 12th, 2013 at 12:21Robert IvanDecember 12th, 2013 at 16:24groovecoderDecember 16th, 2013 at 09:02Roma MatusevichDecember 14th, 2013 at 06:44Robert Nyman [Editor]December 16th, 2013 at 04:12TysonDecember 14th, 2013 at 21:29Robert Nyman [Editor]December 16th, 2013 at 04:13SteveDecember 15th, 2013 at 04:22Robert Nyman [Editor]December 16th, 2013 at 04:13