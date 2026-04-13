---
title: Referrer and cache control APIs for fetch() – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/03/referrer-and-cache-control-apis-for-fetch/
author: Ehsan Akhgari
published: '2016-03-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Around a year ago, we [wrote](https://hacks.mozilla.org/2015/03/this-api-is-so-fetching/) about the new [fetch() API](https://developer.mozilla.org/en/docs/Web/API/Fetch_API). The WHATWG Fetch API provides a modern way to fetch network resources and gives you fine grained control over the details of the request and response. If you’re not familiar with the Fetch API, it would be a nice idea to read about it before proceeding.

We have recently implemented a few new additions to the Fetch API, and in this post I will give an overview of them and include examples of how they can help you develop your web applications.

## Referrer control APIs

Using fetch(), you can now control the HTTP request [referrer](https://en.wikipedia.org/wiki/HTTP_referer) and [referrer policy](https://w3c.github.io/webappsec-referrer-policy/). The HTTP Referer [sic] header is a (misspelled!) header that allows a target page to know what source page the user is coming from (for example, by clicking a link on that page). This is useful for example for gathering analytics data about where your web site users are coming from.

The referrer policy is a new W3C specification which we have been implementing in Firefox that allows the page to provide the browser with a policy that lets the page have more control over how the Referer header is set. There are a few different policy states, each with a specific goal in mind. Here is a summary.

prevents sending any Referer header. This can be useful when you want to hide the Referer header for privacy reasons. For example, some search engines add information about the user’s search phrase among other things to the URL, and they may not want to leak the user’s search phrase to the search result web sites that the user clicks on. The “no-referrer” referrer policy could be used for that purpose.`“no-referrer”`

is similar to “no-referrer” with the exception that the Referer header is only omitted when navigating from a`“no-referrer-when-downgrade”`

[secure context](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)to a non-secure one. For instance, with the search engine example above, if your privacy concern is limited to people monitoring the HTTP traffic instead of the target website, you can use the “no-referrer-when-downgrade” policy. In this case, if a search result links to a secure context, the browser would send the Referer header but if the target web site is an insecure HTTP site, the browser will refuse the send the Referer header in clear text. This is the default policy if an explicit policy has not been specified.will make the browser only include the referring origin and not the full URL in the Referer header. For example, if you want the target web sites to be able to tell that the user is coming from your search results page without revealing the full URL, you can use “origin”. In this case, the browser would strip away anything after the domain name in the URL sent in the Referer header.`“origin”`

is similar to “origin” except that it will only strip out the full URL when navigating across origins. For example, suppose you want to only include the origin for your search result pages (which we assume to be cross origin if your site is doing a normal web search), but send the full referrer to your own internal pages. This lets your own analytics software know how your users navigate across the pages of your site. In this case, “origin-when-cross-origin” is the right policy to choose.`“origin-when-cross-origin”`

causes the browser to send the full URL (sans any associated user name, password or fragment) to all pages that the user navigates to, no matter whether they’re cross origin and/or secure. The real reason why this is called`“unsafe-url”`

*unsafe*is that this will reveal the full URL to any target web page, which raises privacy concerns such as those the examples above try to address. You should consider using a different referrer policy if possible.

Right now, in Firefox you can use an [<meta name=referrer>](https://developer.mozilla.org/en/docs/Web/HTML/Element/meta) element on your page to set a global referrer policy for all network requests initiated from the page. We are also working on implementing the [per-element referrer policy attributes](https://w3c.github.io/webappsec-referrer-policy/#referrer-policy-delivery-referrer-attribute) that can be useful when you want to use a different referrer policy for a specific element (such as an <img>). With the new APIs introduced here, you can also control the referrer and the referrer policy for the resources downloaded using fetch().

The following code examples show a few examples of how you can use these new fetch() features.

```
// Let’s assume that the code below runs on https://example.site/page.html
// Download a json but don't reveal who is downloading it
fetch("sneaky.json", {referrerPolicy: "no-referrer"})
.then(function(response) { /* consume the response */ });
// Download a json but pretend another page is downloading it
fetch("sneaky.json", {referrer: "https://example.site/fake.html"})
.then(function(response) { /* consume the response */ });
// You can only set same-origin referrers.
fetch("sneaky.json", {referrer: "https://cross.origin/page.html"})
.catch(function(exc) {
// exc.name == "TypeError"
// exc.message == "Referrer URL https://cross.origin/page.html cannot be cross-origin to the entry settings object (https://example.site)."
});
// Download a potentially cross-origin json and don't reveal
// the full referrer URL across origins
fetch(jsonURL, {referrerPolicy: "origin-when-cross-origin"})
.then(function(response) { /* consume the response */ });
// Download a potentially cross-origin json and reveal a
// fake referrer URL on your own origin only.
fetch(jsonURL, {referrer: "https://example.site/fake.html",
referrerPolicy: "origin-when-cross-origin"})
.then(function(response) { /* consume the response */ });
// Override sending the document global referrer policy set using
// to send the full referrer URL.
// Be careful!
fetch(jsonURL, {referrerPolicy: "unsafe-url"})
.then(function(response) { /* consume the response */ });
```


If your site uses [service workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API), then you can examine the referrer and the referrer policy that accompanies a fetched resource. Look inside the [fetch event handler](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/onfetch) using the [referrer](https://developer.mozilla.org/en-US/docs/Web/API/Request/referrer) and [referrerPolicy](https://developer.mozilla.org/en-US/docs/Web/API/Request/referrerPolicy) attributes of [Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) objects.

This API will be available in Firefox 47, which is currently available in the [developer edition release channel](https://www.mozilla.org/en-US/firefox/developer/) for testing.

## Fetch cache control APIs

The resources downloaded through fetch(), similar to other resources that the browser downloads, are subject to the [HTTP cache](https://developer.mozilla.org/en/docs/Web/HTTP/Caching_FAQ). This is usually fine, since it means that if your browser has a cached copy of the response to the HTTP request. It can use the cached copy instead of wasting time and bandwidth re-downloading from a remote server.

However, there are cases where you would want some control over whether the browser’s HTTP cache is used. You can ensure that you’re getting a fresh response no matter what’s in the browser’s HTTP cache by [cache busting the URL](https://developers.google.com/web/showcase/case-study/service-workers-iowa?hl=en#cache-bust-your-precaching-requests) of the resources you want to to fetch into the [service worker controlled cache](https://developer.mozilla.org/en-US/docs/Web/API/Cache). This is typically done by appending a parameter such as `'cache-bust=' + Date.now()`

to the URL before downloading it, which is quite ugly. There is now a better way to do this, using the fetch cache control API.

The idea behind this API is specifying a caching policy for fetch to explicitly indicate how and when the browser HTTP cache should be consulted. It’s important to have a good understanding of the HTTP caching semantics in order to use these most effectively. There are many good articles on the web such as [this one](http://symfony.com/doc/current/book/http_cache.html#http-cache-introduction) that describe these semantics in detail. There are currently five different policies that you can choose from.

`“default”`

means use the default behavior of browsers when downloading resources. The browser first looks inside the HTTP cache to see if there is a matching request. If there is, and it is fresh, it will be returned from fetch(). If it exists but is stale, a conditional request is made to the remote server and if the server indicates that the response has not changed, it will be read from the HTTP cache. Otherwise it will be downloaded from the network, and the HTTP cache will be updated with the new response.`“no-store”`

means bypass the HTTP cache completely. This will make the browser not look into the HTTP cache on the way to the network, and never store the resulting response in the HTTP cache. Using this cache mode, fetch() will behave as if no HTTP cache exists.`“reload”`

means bypass the HTTP cache on the way to the network, but update it with the newly downloaded response. This will cause the browser to never look inside the HTTP cache on the way to the network, but update the HTTP cache with the downloaded response. Future requests can use that updated response if appropriate.`“no-cache”`

means always validate a response that is in the HTTP cache even if the browser thinks that it’s fresh. This will cause the browser to look for a matching request in the HTTP cache on the way to the network. If such a request is found, the browser always creates a conditional request to validate it even if it thinks that the response should be fresh. If a matching cached entry is not found, a normal request will be made. After a response has been downloaded, the HTTP cache will always be updated with that response.`“force-cache”`

means that the browser will always use a cached response if a matching entry is found in the cache, ignoring the validity of the response. Thus even if a really old version of the response is found in the cache, it will always be used without validation. If a matching entry is not found in the cache, the browser will make a normal request, and will update the HTTP cache with the downloaded response.

Let’s look at a few examples of how you can use these cache modes.

```
// Download a resource with cache busting, to bypass the cache
// completely.
fetch("some.json", {cache: "no-store"})
.then(function(response) { /* consume the response */ });
// Download a resource with cache busting, but update the HTTP
// cache with the downloaded resource.
fetch("some.json", {cache: "reload"})
.then(function(response) { /* consume the response */ });
// Download a resource with cache busting when dealing with a
// properly configured server that will send the correct ETag
// and Date headers and properly handle If-Modified-Since and
// If-None-Match request headers, therefore we can rely on the
// validation to guarantee a fresh response.
fetch("some.json", {cache: "no-cache"})
.then(function(response) { /* consume the response */ });
// Download a resource with economics in mind! Prefer a cached
// albeit stale response to conserve as much bandwidth as possible.
fetch("some.json", {cache: "force-cache"})
.then(function(response) { /* consume the response */ });
```


This API is planned for release in Firefox 48, and is currently available in [Firefox Nightly](https://nightly.mozilla.org/) for testing.

## About
[
Ehsan Akhgari ](https://ehsanakhgari.org/)

Ehsan has worked on various parts of Firefox since 2006. These days he spends most of his time working on Gecko and Web APIs.

## 14 comments

Chen ZhixiangMarch 23rd, 2016 at 03:09Ehsan AkhgariMarch 23rd, 2016 at 08:42Chen ZhixiangMarch 23rd, 2016 at 20:06Ehsan AkhgariMarch 24th, 2016 at 08:38Chen ZhixiangMarch 24th, 2016 at 19:01Ehsan AkhgariMarch 28th, 2016 at 07:44Eric LawrenceMarch 23rd, 2016 at 22:02Ehsan AkhgariMarch 24th, 2016 at 08:36Koemsie LyMarch 24th, 2016 at 07:06GerbenMarch 26th, 2016 at 12:47Ehsan AkhgariMarch 28th, 2016 at 07:48GerbenMarch 29th, 2016 at 08:04Ehsan AkhgariMarch 29th, 2016 at 08:39GerbenMarch 29th, 2016 at 08:51