---
title: jsDelivr and its open-source load balancing algorithm – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2014/11/jsdelivr-and-its-open-source-load-balancing-algorithm/
author: Dmitriy Akulov
published: '2014-11-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post by Dmitriy Akulov of jsDelivr.*

Recently I wrote about [jsDelivr and what makes it unique](https://hacks.mozilla.org/2014/03/jsdelivr-the-advanced-open-source-public-cdn/) where I described in detail about the features that we offer and how our system works. Since then we improved a lot of stuff and released even more features. But the biggest one is was the [open source of our load balancing algorithm](http://blog.jsdelivr.com/2014/11/load-balancing-algorithm-open-sourced.html).

As you know from the previous blog post we are using Cedexis to do our load balancing. In short we collect millions of RUM (Real User Metrics) data points from all over the world. When a user visits a website partner of Cedexis or ours a JavaScript is executed in the background that does performance checks to our core CDNs, MaxCDN and CloudFlare, and sends this data back to Cedexis. We can then use it to do load balancing based on real time performance information from real life users and ISPs. This is important as it allows us to mitigate outages that CDNs can experience in very localized areas such as a single country or even a single ISP and not worldwide.

## Open-sourcing the load balancing code

Now our [load balancing code is open to everybody](https://github.com/jsdelivr/dns-openmix) to review, test and even send their own Pull Requests with improvements and modifications.

Until recently the code was actually written in PHP, but due to performance issues and other problems that arrised from that it was decided to switch to JavaScript. Now the DNS application is completely written in js and I will try to explain how exactly it works.

This is an application that runs on a DNS level and integrates with Cedexis’ API. Every DNS request made to cdn.jsdelivr.net is processed by the following code and then based on all the variables it returns a CNAME that the client can use to get the requested asset.

## Declaring providers

The first step is to declare our providers:

```
providers: {
'cloudflare': 'cdn.jsdelivr.net.cdn.cloudflare.net',
'maxcdn': 'jsdelivr3.dak.netdna-cdn.com',
...
},
```

This array contains all the aliases of our providers and the hostnames that we can return if the provider is then chosen. We actually use a couple of custom servers to improve the performance in locations that the CDNs lack but we are currently in the process of removing all of them in favor of more enterprise CDNs that wish to sponsor us.

Before I explain the next array I want to skip to line 40:

```
defaultProviders: [ 'maxcdn', 'cloudflare' ],
```

Because our CDN providers get so much more RUM tests than our custom servers their data and in turn the load balancing results are much more reliable and better. This is why by default only MaxCDN and CloudFlare are considered for any user request. And its actually the main reason we want to sunset our custom servers.

## Country mapping

Now that you know that comes our next array:

```
countryMapping: {
'CN': [ 'exvm-sg', 'cloudflare' ],
'HK': [ 'exvm-sg', 'cloudflare' ],
'ID': [ 'exvm-sg', 'cloudflare' ],
'IT': [ 'prome-it', 'maxcdn', 'cloudflare' ],
'IN': [ 'exvm-sg', 'cloudflare' ],
'KR': [ 'exvm-sg', 'cloudflare' ],
'MY': [ 'exvm-sg', 'cloudflare' ],
'SG': [ 'exvm-sg', 'cloudflare' ],
'TH': [ 'exvm-sg', 'cloudflare' ],
'JP': [ 'exvm-sg', 'cloudflare', 'maxcdn' ],
'UA': [ 'leap-ua', 'maxcdn', 'cloudflare' ],
'RU': [ 'leap-ua', 'maxcdn' ],
'VN': [ 'exvm-sg', 'cloudflare' ],
'PT': [ 'leap-pt', 'maxcdn', 'cloudflare' ],
'MA': [ 'leap-pt', 'prome-it', 'maxcdn', 'cloudflare' ]
},
```

This array contains country mappings that override the “defaultProviders” parameter. This is where the custom servers currently come to use. For some countries we know 100% that our custom servers can be much faster than our CDN providers so we manually specify them. Since these locations are few we only need to create handful of rules.

## ASN mappings

```
asnMapping: {
'36114': [ 'maxcdn' ], // Las Vegas 2
'36351': [ 'maxcdn' ], // San Jose + Washington
'42473': [ 'prome-it' ], // Milan
'32489': [ 'cloudflare' ], // Canada
...
},
```

ASN mappings contains overrides per ASN. Currently we are using them to improve the results of Pingdom tests. The reason for this is because we rely on RUM results to do load balancing we never get any performance tests for ASNs used by hosting providers such as companies where Pingdom rents their servers. So the code is forced to failover to country level performance data to chose the best provider for Pingdom and any other synthetic test and server. This data is not always reliable because not all ISPs have the same performance with a CDN provider as the fastest CDN provider country-wide. So we tweak some ASNs to work better with jsDelivr.

## More settings

`lastResortProvider`

sets the CDN provider we want to use in case the application fails to chose one itself. This should be very rare.`defaultTtl: 20`

is the TTL for our DNS record. We made some tests and decided that this was the most optimal value. In worst case scenario in case of downtime the maximum downtime jsDelivr can have is 20 seconds. Plus our DNS and our CDN are fast enough to compensate for the extra DNS latency every 20 seconds without having any impact on performance.`availabilityThresholds`

is a value in percentage and sets the uptime below which a provider should be considered down. This is based on RUM data. Again because of some small issues with synthetic tests we had to lower the Pingdom threshold. The Pingdom value does not impact anyone else.`sonarThreshold`

Sonar is a secondary uptime monitor we use to ensure the uptime of our providers. It runs every 60 seconds and checks all of our providers including their SSL certificates. If something is wrong our application will pick up the change in uptime and if it drops below this threshold it will be considered as down.- And finally
`minValidRtt`

is there to filter out all invalid RUM tests.

## The initialization process

Next our app starts the initialization process. Wrong config and uptime not meeting our criteria is checked and all providers not matching our criteria are then removed from the potential candidates for this request.

Next we create a `reasons`

array for debugging purposes and apply our override settings. Here we use Cedexis API to get the latest live data for sonar uptime, rum update and HTTP performance.

```
sonar = request.getData('sonar');
candidates = filterObject(request.getProbe('avail'), filterCandidates);
//console.log('candidates: ' + JSON.stringify(candidates));
candidates = joinObjects(candidates, request.getProbe('http_rtt'), 'http_rtt');
//console.log('candidates (with rtt): ' + JSON.stringify(candidates));
candidateAliases = Object.keys(candidates);
```

In case of uptime we also filter our bad providers that dont meet our criteria of uptime by calling the `filterCandidates`

function.

```
function filterCandidates(candidate, alias) {
return (-1 < subpopulation.indexOf(alias))
&& (candidate.avail !== undefined)
&& (candidate.avail >= availabilityThreshold)
&& (sonar[alias] !== undefined)
&& (parseFloat(sonar[alias]) >= settings.sonarThreshold);
}
```

The actual decision making is performed by a rather small code:

```
if (1 === candidateAliases.length) {
decisionAlias = candidateAliases[0];
decisionReasons.push(reasons.singleAvailableCandidate);
decisionTtl = decisionTtl || settings.defaultTtl;
} else if (0 === candidateAliases.length) {
decisionAlias = settings.lastResortProvider;
decisionReasons.push(reasons.noneAvailableOrNoRtt);
decisionTtl = decisionTtl || settings.defaultTtl;
} else {
candidates = filterObject(candidates, filterInvalidRtt);
//console.log('candidates (rtt filtered): ' + JSON.stringify(candidates));
candidateAliases = Object.keys(candidates);
if (!candidateAliases.length) {
decisionAlias = settings.lastResortProvider;
decisionReasons.push(reasons.missingRttForAvailableCandidates);
decisionTtl = decisionTtl || settings.defaultTtl;
} else {
decisionAlias = getLowest(candidates, 'http_rtt');
decisionReasons.push(reasons.rtt);
decisionTtl = decisionTtl || settings.defaultTtl;
}
}
response.respond(decisionAlias, settings.providers[decisionAlias]);
response.setReasonCode(decisionReasons.join(''));
response.setTTL(decisionTtl);
};
```

In case we only have 1 provider left after our checks we simply select that provider and output the CNAME, if we have 0 providers left then the `lastResortProvider`

is used. Otherwise if everything is ok and we have more than 1 provider left we do more checks.

Once we have left with providers that are currently online and don’t have any issues with their performance data we sort them based on RUM HTTP performance and push the CNAME out for the user’s browser to use.

And thats it. Most of the other stuff like fallback to country level data is automatically done in backend and we only get the actual data we can use in our application.

## Conclusion

I hope you found it interesting and learned more about what you should be considering when doing load balancing especially based on RUM data.

Check out [jsDelivr](http://www.jsdelivr.com/) and feel free to use it in your projects. If you are interested to help we are also looking for node.js developers and designers to help us out.

We are also looking for companies sponsors to help us grow even faster.

## About
[
Dmitriy Akulov ](http://www.jsdelivr.com)

System administrator. In love with technology, high performance and fast web. Some times pretending to be a dev. Working for MaxCDN.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

trogNovember 12th, 2014 at 15:38Dmitriy AkulovNovember 13th, 2014 at 03:11