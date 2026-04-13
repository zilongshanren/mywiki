---
title: 'Do not let your CDN betray you: Use Subresource Integrity – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2015/09/subresource-integrity-in-firefox-43/
author: Frederik Braun
published: '2015-09-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Mozilla Firefox [Developer Edition 43](https://www.mozilla.org/en-US/firefox/developer/) and other modern browsers help websites to control third-party JavaScript loads and prevent unexpected or malicious modifications. Using a new specification called [Subresource Integrity](http://www.w3.org/TR/SRI/), a website can include JavaScript that will stop working if it has been modified. With this technology, developers can benefit from the performance gains of using Content Delivery Networks (CDNs) without having to fear that a third-party compromise can harm their website.

Using Subresource Integrity is rather simple:

```
<script src="https://code.jquery.com/jquery-2.1.4.min.js"
integrity="sha384-R4/ztc4ZlRqWjqIuvf6RX5yb/v90qNGx6fS48N0tRxiGkqveZETq72KgDVJCp2TC"
crossorigin="anonymous"></script>
```


The idea is to include the script along with its cryptographic hash (e.g. SHA-384) when creating the web page. The browser can then download the script and compute the hash over the downloaded file. The script will only be executed if both hashes match. The security properties of a [collision resistant hash function](https://en.wikipedia.org/wiki/Collision_resistance), ensure that a modification results in a very different hash. This helps the site owner detect and prevent any changes, whether they come from a compromised CDN or an evil administrator.

An important side note is that for Subresource Integrity to work, the CDN must support [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS). The `crossorigin`

attribute in the above code snippet enforces a CORS-enabled load. The anonymous value means that the browser should omit any cookies or authentication that the user may have associated with the domain. This prevents [cross-origin data leaks](http://www.w3.org/TR/SRI/#cross-origin-data-leakage), and also makes the request smaller.

### Integrity syntax

As you may have noticed, the integrity attribute does not just include the hash value. It also contains the digest name. The syntax for the integrity attribute allows multiple tokens of this name-value format. This allows site owners to specify hashes of different strengths as well as the values of multiple scripts that may be behind a URL. This is useful for browser sniffing or content negotiation.

```
<script src="https://code.jquery.com/jquery-2.1.4.min.js"
integrity="sha384-R4/ztc4ZlRqWjqIuvf6RX5yb/v90qNGx6fS48N0tRxiGkqveZETq72KgDVJCp2TC
sha256-8WqyJLuWKRBVhxXIL1jBDD7SDxU936oZkCnxQbWwJVw="
crossorigin="anonymous"></script>
```


### Failover

For the best performance, users would load all resources from the CDN, but if integrity cannot be verified, you don’t want your users to be trapped on a non-working web page. To make failover work, we recommend hosting a copy of the script on your own origin. To recover from failure one could then extend the previous snippet with the following code:

`<script>window.jQuery || /* reload from own domain here */;</script>`


This code will check if jQuery has been defined and could otherwise insert a script tag that loads the same origin version of the script.

Please note that many scripts update regularly, especially if they do not come with a version number. If you want to secure your CDN-loaded scripts, it is best to stick to a specific version and not use filenames with the word ‘latest’ in them.

### HTTP or HTTPS?

Subresource Integrity works on both HTTP and HTTPS. If you are serving your page over plain HTTP, the browser can still figure out if the script was modified on the CDN, but it is not protected against active network attackers, as they would be able to just remove the integrity attribute from your HTML. It is, however, in the interest of your users to provide confidentiality, integrity, and authenticity of your web applications by using HTTPS for the entirety of your website.

**Stylesheet support**

While we are working on adding support for subresources other than scripts, you can also use Subresource Integrity for CSS. Just use the integrity attribute that you now know so well on your <link> tag!

### Try Subresource Integrity Now!

If you want to test browser support or toy with examples, take a look at [https://srihash.org/](https://srihash.org/), which can do all the grunt work of computing hashes as well as checking if your CDN already supports HTTPS. A few early adopters like [BootstrapCDN](https://www.bootstrapcdn.com/), [CloudFlare](https://blog.cloudflare.com/an-introduction-to-javascript-based-ddos/) and [GitHub](http://githubengineering.com/subresource-integrity/) are already experimenting with it.

There is some additional documentation of [Subresource Integrity on MDN](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity). But if you want to read all the fine details of Subresource Integrity, take a look at the [specification](http://www.w3.org/TR/SRI/).

To conclude, Subresource Integrity can make your website safer when using a CDN that you do not fully control. It’s as simple as adding just a few extra attributes to your script tags.

## About
[
Frederik Braun ](https://frederikbraun.de)

Frederik Braun builds security for the web and for Mozilla Firefox from Berlin. As a contributor to standards, Frederik is also improving the web platform by bringing security into the defaults with specifications like the Sanitizer API and Subresource Integrity. When not at work, Frederik likes reading a good novel or going on long bike treks across Europe.

## About
[
Francois Marier ](https://mozillians.org/u/francois/)

Security and Privacy Engineer

## 38 comments

Jerry QuSeptember 27th, 2015 at 01:28Frederik BraunSeptember 27th, 2015 at 11:50Francis KimSeptember 27th, 2015 at 05:40Jerry QuSeptember 27th, 2015 at 05:50Frederik BraunSeptember 27th, 2015 at 11:31Francis KimSeptember 29th, 2015 at 01:58Steve SoudersSeptember 28th, 2015 at 08:21Francois MarierSeptember 28th, 2015 at 15:58Frederik BraunSeptember 29th, 2015 at 01:21Steve SoudersSeptember 29th, 2015 at 09:08Frederik BraunSeptember 30th, 2015 at 03:49GerbenSeptember 28th, 2015 at 09:06JWSeptember 28th, 2015 at 12:24Francois MarierSeptember 28th, 2015 at 16:04Paul IrwinOctober 1st, 2015 at 10:00starbuckOctober 1st, 2015 at 08:53NatimSeptember 29th, 2015 at 07:16NatimOctober 1st, 2015 at 07:50Paul MasurelOctober 1st, 2015 at 07:28Frederik BraunOctober 1st, 2015 at 07:38Paul MasurelOctober 1st, 2015 at 08:10Frederik BraunOctober 2nd, 2015 at 00:39Sébastien PierreOctober 1st, 2015 at 08:34Francois MarierOctober 1st, 2015 at 15:50Joe DevonOctober 1st, 2015 at 10:59Justin DorfmanOctober 1st, 2015 at 11:23Martin UeckerOctober 1st, 2015 at 13:35Josh GrahamOctober 2nd, 2015 at 00:17Frederik BraunOctober 2nd, 2015 at 00:43Josh GrahamOctober 2nd, 2015 at 01:18AlexOctober 2nd, 2015 at 06:26Francois MarierOctober 5th, 2015 at 13:51AlexOctober 2nd, 2015 at 16:26Francois MarierOctober 6th, 2015 at 14:39AlexOctober 3rd, 2015 at 05:45Francois MarierOctober 6th, 2015 at 14:41plutoOctober 3rd, 2015 at 13:59Francois MarierOctober 6th, 2015 at 14:43