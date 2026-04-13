---
title: Overscripted! Digging into JavaScript execution at scale – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2018/06/overscripted-digging-into-javascript-execution-at-scale/
author: Martin Lopatka
published: '2018-06-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This research was conducted in partnership with the UCOSP (Undergraduate Capstone Open Source Projects) initiative. UCOSP facilitates open source software development by connecting Canadian undergraduate students with industry mentors to practice distributed development and data projects.*

*The team consisted of the following Mozilla staff: Martin Lopatka, David Zeber, Sarah Bird, Luke Crouch, Jason Thomas*

*2017 student interns — crawler implementation and data collection: Ruizhi You, Louis Belleville, Calvin Luo, Zejun (Thomas) Yu*

*2018 student interns — exploratory data analysis projects: Vivian Jin, Tyler Rubenuik, Kyle Kung, Alex McCallum*

As champions of a [healthy Internet](https://www.mozilla.org/en-US/internet-health/), we at Mozilla have been increasingly concerned about the current advertisement-centric web content ecosystem. Web-based ad technologies continue to evolve increasingly sophisticated [programmatic models](https://arxiv.org/abs/1701.07058) for targeting individuals based on their demographic characteristics and interests. The financial underpinnings of the current system incentivise optimizing on *engagement* above all else. This, in turn, has evolved an insatiable appetite for data among advertisers aggressively iterating on models to drive human clicks.


Most of the content, products, and services we use online, whether provided by media organisations or by technology companies, are funded in whole or in part by advertising and various forms of marketing.–Timothy Libert and Rasmus Kleis Nielsen [

[link]]

We’ve talked about the potentially adverse effects on the [Web’s morphology](https://medium.com/firefox-context-graph/are-trackers-the-new-backbone-of-the-web-fb800435da15) and how content silos can [impede a diversity of viewpoints](https://medium.com/firefox-context-graph/context-graph-its-time-to-bring-context-back-to-the-web-a7542fe45cf3). Now, the Mozilla Systems Research Group is raising a call to action. [Help us](https://github.com/mozilla/overscripted) search for patterns that describe, expose, and illuminate the complex interactions between people and pages!

Inspired by the [Web Census](https://webtransparency.cs.princeton.edu/webcensus/) recently published by [Steven Englehardt](https://senglehardt.com) and [Arvind Narayanan](http://randomwalker.info) of Princeton University, we adapted the [OpenWPM](https://github.com/citp/OpenWPM) crawler framework to perform a comparable crawl gathering a rich set of information about the JavaScript execution on various websites. This enables us to delve into further analysis of web tracking, as well as a general exploration of client-page interactions and a survey of different APIs employed on the modern Web.

In short, we set out to explore the unseen or otherwise not obvious series of JavaScript execution events that are triggered once a user visits a webpage, and all the first- and third-party events that are set in motion when people retrieve content. To help enable more exploration and analysis, we are providing our [full set of data about JavaScript executions](https://github.com/mozilla/overscripted) open source.

The following sections will introduce the data set, how it was collected and the decisions made along the way. We’ll share examples of insights we’ve discovered and we’ll provide information on how to participate in the associated [“Overscripted Web: A Mozilla Data Analysis Challenge”](https://challenges.mozilla.community/overscripted/), which we’ve [launched today](https://medium.com/mozilla-open-innovation/overscripted-91881d8662c3) with Mozilla’s Open Innovation Team.

## The Dataset

In October 2017, several Mozilla staff and a group of Canadian undergraduate students [forked](https://help.github.com/articles/fork-a-repo/) the [OpenWPM](https://github.com/citp/OpenWPM) crawler repository to begin tinkering, in order to collect a plethora of information about the unseen interactions between modern websites and the Firefox web browser.

### Preparing the seed list

The [master list of pages](https://github.com/RuizhiYou/URLCrawler/blob/master/intersect_url.csv) we crawled in preparing the dataset was itself generated from a preliminary shallow crawl we performed in November 2017. We ran a [depth-1 crawl](https://en.wikipedia.org/wiki/Web_crawler#Selection_policy), seeded by [Alexa’s top 10,000 site list](https://www.alexa.com/topsites), using 4 different machines at 4 different IP addresses (all in residential non-Amazon IP addresses served by Canadian internet service providers). The crawl was implemented using the [Requests](http://docs.python-requests.org/en/master/) Python library and collected no information except for an indication of successful page loads.

Of the 2,150,251 pages represented in the union of the 4 parallel shallow crawls, we opted to use the intersection of the four lists in order to prune out dynamically generated (e.g. personalized) outbound links that varied between them. This meant a reduction to 981,545 URLs, which formed the seed list for our main OpenWPM crawl.

### The Main Collection

The following workflow describes (at a high level) the collection of page information contained in this dataset.

- Alexa top 10k (10,000 high traffic pages as of November 1st, 2017)
- Precrawl using the python
*Requests*library, visits each one of those pages- Request library requests that page
- That page sends a response
- All href tags in the response are captured to a depth of 1 (away from Alexa page)
- For each of those href tags all valid pages (starts with “http”) are added to the link set.
- The link set union (2,150,251) was examined using the request library in parallel, which gives us the intersection list of 981,545.
- The set of urls in the list 981,545 is passed to the deeper crawl for JavaScript analysis in a parallelized form.


- Each of these pages was sent to our adapted version of OpenWPM to have the execution of JavaScript recorded for 10 seconds.
- The
`window.location`

was hashed as the unique identifier of the location where the JavaScript was executed (to ensure unique source attribution).- When OpenWPM hits content that is inside an iFrame, the location of the content is reported.
- Since we use the
`window.location`

to determine the location element of the content, each time an iFrame is encountered, that location can be split into the parent location of the page and the iFrame location. - Data collection and aggregation performed through a websocket associates all the activity linked to a location hash for compilation of the crawl dataset.


Interestingly, for the Alexa top 10,000 sites, our depth-1 crawl yielded properties hosted on 41,166 TLDs across the union of our 4 replicates, whereas only 34,809 unique TLDs remain among the 981,545 pages belonging to their intersection.

A [modified version of OpenWPM](https://github.com/RuizhiYou/OpenWPM/tree/RunThis) was used to record JavaScript calls potentially used for browsers tracking data from these pages. The collected JavaScript execution trace was written into an s3 bucket for later aggregation and analysis. Several additional parameters were defined based on cursory ad hoc analyses.

For example, the minimum dwell time per page required to capture the majority of JavaScript activity was set as 10 seconds per page. This was based on a random sampling of the seed list URLs and showed a large variation in time until no new JavaScript was being executed (from no JavaScript, to what appeared to be an infinite loop of self-referential JavaScript calls). This dwell time was chosen to balance between capturing the majority of JavaScript activity on a majority of the pages and minimizing the time required to complete the full crawl.

Several of the probes instrumented in the [Data Leak](https://github.com/groovecoder/data-leak) repo were ported over to our hybrid crawler, including instrumentation to monitor JavaScript execution occuring inside an iFrame element (potentially hosted on a third-party domain). This would prove to provide much insight into the relationships between pages in the crawl data.

## Exploratory work

In January 2018, we got to work analyzing the dataset we had created. After substantial data cleaning to work through the messiness of real world variation, we were left with a gigantic [Parquet](https://parquet.apache.org/) dataset (around 70GB) containing an immense diversity of potential insights. Three example analyses are summarized below. The most important finding is that we have only just scratched the surface of the insights this data may hold.

### Examining session replay activity

[Session replay](https://en.wikipedia.org/wiki/Session_replay) is a service that lets websites track users’ interactions with the page—from how they navigate the site, to their searches, to the input they provide. Think of it as a “video replay” of a user’s entire session on a webpage. Since some session replay providers may record personal information such as personal addresses, credit card information and passwords, this can present a significant risk to both privacy and security.

We explored the incidence of session replay usage, and a few associated features, across the pages in our crawl dataset. To identify potential session replay, we obtained the [Princeton WebTAP project](https://webtransparency.cs.princeton.edu/no_boundaries/session_replay_sites.html) list, containing 14 Alexa top-10,000 session replay providers, and checked for requests to script URLs belonging to the list.

Out of 6,064,923 distinct script references among page loads in our dataset, we found 95,570 (1.6%) were to session replay providers. This translated to 4,857 distinct domain names (netloc) making such requests, out of a total of 87,325, or 5.6%. Note that even if scripts belonging to session replay providers are being accessed, this does not necessarily mean that session replay functionality is being used on the site.

Given the set of pages making requests to session replay providers, we also looked into the consistency of SSL usage across these requests. Interestingly, the majority of such requests were made over HTTPS (75.7%), and 49.9% of the pages making these requests were accessed over HTTPS. Additionally, we found no pages accessed over HTTPS making requests to session replay scripts over HTTP, which was surprising but encouraging.

Finally, we examined the distribution of TLDs across sites making requests to session replay providers, and compared this to TLDs over the full dataset. We found that, along with .com, .ru accounted for a surprising proportion of sites accessing such scripts (around 33%), whereas .ru domain names made up only 3% of all pages crawled. This implies that 65.6% of .ru sites in our dataset were making requests to potential session replay provider scripts. However, this may be explained by the fact that Yandex is one of the primary session replay providers, and it offers a range of other analytics services of interest to Russian-language websites.

### Eval and dynamically created function calls

JavaScript allows a function call to be dynamically created from a string with the `eval()`

function or by creating a new `Function()`

object. For example, this code will print hello twice:

```
eval("console.log('hello')")
var my_func = new Function("console.log('hello')")
my_func()
```


While dynamic function creation has its uses, it also opens up users to injection attacks, such as [cross-site scripting](https://en.wikipedia.org/wiki/Cross-site_scripting), and can potentially be used to hide malicious code.

In order to understand how dynamic function creation is being used on the Web, we analyzed its prevalence, location, and distribution in our dataset. The analysis was initially performed on 10,000 randomly selected pages and validated against the entire dataset. In terms of prevalence, we found that 3.72% of overall function calls were created dynamically, and these originated from across 8.76% of the websites crawled in our dataset.

These results suggest that, while dynamic function creation is not used heavily, it is still common enough on the Web to be a potential concern. Looking at call frequency per page showed that, while some Web pages create all their function calls dynamically, the majority tend to have only 1 or 2 dynamically generated calls (which is generally 1-5% of all calls made by a page).

We also examined the extent of this practice among the scripts that are being called. We discovered that they belong to a relatively small subset of script hosts (at an average ratio of about 33 calls per URL), indicating that the same JavaScript files are being used by multiple webpages. Furthermore, around 40% of these are known trackers (identified using the [disconnectme entity list](https://github.com/disconnectme/disconnect-tracking-protection)), although only 33% are hosted on a different domain from the webpage that uses them. This suggests that web developers may not even know that they are using dynamically generated functions.

### Cryptojacking

Cryptojacking refers to the unauthorized use of a user’s computer or mobile device to mine cryptocurrency. More and more websites are using browser-based cryptojacking scripts as cryptocurrencies rise in popularity. It is an easy way to generate revenue and a viable alternative to bloating a website with ads. An excellent contextualization of crypto-mining via client-side JavaScript execution can be found in the [unabridged cryptojacking analysis](https://github.com/mozilla/UCOSP-winter-2018_TrackingTechnologies/blob/master/analyses/cryptojacking/cryptojacking_analysis.md) prepared by Vivian Jin.

We investigated the prevalence of cryptojacking among the websites represented in our dataset. A list of potential cryptojacking hosts (212 sites total) was obtained from the [adblock-nocoin-list GitHub repo](https://github.com/hoshsadiq/adblock-nocoin-list/blob/master/hosts.txt). For each script call initiated on a page visit event, we checked whether the script host belonged to the list. Among 6,069,243 distinct script references on page loads in our dataset, only 945 (0.015%) were identified as cryptojacking hosts. Over half of these belonged to CoinHive, the original script developer. Only one use of AuthedMine was found. Viewed in terms of domains reached in the crawl, we found calls to cryptojacking scripts being made from 49 out of 29,483 distinct domains (0.16%).

However, it is important to note that cryptojacking code can be executed in other ways than by including the host script in a script tag. It can be disguised, stealthily executed in an iframe, or directly used in a function of a first-party script. Users may also face redirect loops that eventually lead to a page with a mining script. The low detection rate could also be due to the popularity of the sites covered by the crawl, which might dissuade site owners from implementing obvious cryptojacking scripts. It is likely that the actual rate of cryptojacking is higher.

The majority of the domains we found using cryptojacking are streaming sites. This is unsurprising, as users have streaming sites open for longer while they watch video content, and mining scripts can be executed longer. A Chinese variety site called 52pk.com accounted for 207 out of the overall 945 cryptojacking script calls we found in our analysis, by far the largest domain we observed for cryptojacking calls.

Another interesting fact: although our cryptojacking host list contained 212 candidates, we found only 11 of them to be active in our dataset, or about 5%.

### Limitations and future directions

While this is a rich dataset allowing for a number of interesting analyses, it is limited in visibility mainly to behaviours that occur via JS API calls.

Another feature we investigated using our dataset is the presence of [ Evercookies](https://samy.pl/evercookie/).

*Evercookies*is a tracking tool used by websites to ensure that user data, such as a user ID, remains permanently stored on a computer. Evercookies persist in the browser by leveraging a series of tricks including Web API calls to a variety of available storage mechanisms. An initial attempt was made to search for evercookies in this data by searching for consistent values being passed to suspect Web API calls.

Acar et al., “The Web Never Forgets: Persistent Tracking Mechanisms in the Wild”, (2014) [developed techniques](https://securehomes.esat.kuleuven.be/~gacar/persistent/the_web_never_forgets.pdf) for looking at evercookies at scale. First, they proposed a mechanism to detect identifiers. They applied this mechanism to HTTP cookies but noted that it could also be applied to other storage mechanisms, although some modification would be required. For example, they look at cookie expiration, which would not be applicable in the case of localStorage. For this dataset we could try replicating their methodology for set calls to `window.document.cookie`

and `window.localStorage`

.

They also looked at Flash cookies respawning HTTP cookies and HTTP respawning Flash cookies. Our dataset contains no information on the presence of Flash cookies, so additional crawls would be required to obtain this information. In addition, they used multiple crawls to study Flash respawning, so we would have to replicate that procedure.

In addition to our lack of information on Flash cookies, we have no information about HTTP cookies, the first mechanism by which cookies are set. Knowing which HTTP cookies are initially set can serve as an important complement and validation for investigating other storage techniques then used for respawning and evercookies.

Beyond HTTP and Flash, Samy Kamkar’s [evercookie library](https://samy.pl/evercookie/) documents over a dozen mechanisms for storing an id to be used as an evercookie. Many of these are not detectable by our current dataset, e.g. HTTP Cookies, HSTS Pinning, Flask Cookies, Silverlight Storage, ETags, Web cache, Internet Explorer userData storage, etc. An evaluation of the prevalence of each technique would be a useful contribution to the literature. We also see the value of an ongoing repeated crawl to identify changes in prevalence and accounting for new techniques as they are discovered.

However, it is possible to continue analyzing the current dataset for some of the techniques described by Samy. For example, `window.name caching`

is listed as a technique. We can look at this property in our dataset, perhaps by applying the same ID technique outlined by Acar et al., or perhaps by looking at sequences of calls.

## Conclusions

Throughout our preliminary exploration of this data it became quickly apparent that the amount of superficial JavaScript execution on a Web page only tells part of the story. We have observed several examples of scripts running parallel to the content-serving functionality of webpages, these appear to fulfill a diversity of other functions. The analyses performed so far have led to some exciting discoveries, but so much more information remains hidden in the immense dataset available.

We are calling on any interested individuals to be part of the exploration. You’re invited to participate in the [Overscripted Web: A Mozilla Data Analysis Challenge](https://github.com/mozilla/overscripted) and help us better understand some of the hidden workings of the modern Web!

**Note:** In the interest of being responsive to all interested contest participants and curious readers in one centralized location, we’ve closed comments on this post. We encourage you to bring relevant questions and discussion to the contest repo at: [https://github.com/mozilla/overscripted](https://github.com/mozilla/overscripted)

## Acknowledgements

Extra special thanks to Steven Englehardt for his contributions to the OpenWPM tool and advice throughout this project. We also thank Havi Hoffman for valuable editorial contributions to earlier versions of this post. Finally, thanks to Karen Reid of University of Toronto for coordinating the UCOSP program.