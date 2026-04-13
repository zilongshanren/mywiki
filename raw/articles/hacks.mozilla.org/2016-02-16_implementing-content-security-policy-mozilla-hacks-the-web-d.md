---
title: Implementing Content Security Policy – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/02/implementing-content-security-policy/
author: April King
published: '2016-02-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The add-ons team recently completed work to enable [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/Security/CSP) (CSP) on [addons.mozilla.org](https://addons.mozilla.org/) (AMO). This article is intended to cover the basics of implementing CSP, as well as highlighting some of the issues that we ran into implementing CSP on AMO.

**What is Content Security Policy?**

Content Security Policy (CSP) is a security standard introduced to help prevent [cross-site scripting (XSS)](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting) and other content injection attacks. It achieves this by restricting the sources of content loaded by the user agent to those only allowed by the site operator.

The policy is implemented via headers that are sent with the server response. From there, it’s up to supporting user agents to take that policy and actively block policy violations as they are detected.

**Why is it needed?**

CSP is another layer of defense to help protect users from a variety of attack vectors such as XSS and other forms of content injection attacks. While it’s not a silver bullet, it does help make it considerably more difficult for an attacker to inject content and exfiltrate data.

Building websites securely is difficult. Even if you know general web security best practices it’s still incredibly easy to overlook something or unwittingly introduce a security hole in an otherwise secure site.

CSP works by restricting the origins that active and passive content can be loaded from. It can additionally restrict certain aspects of active content such as the execution of inline JavaScript, and the use of `eval()`.

**Implementing CSP**

To implement CSP, you must define lists of allowed origins for the all of the types of resources that your site utilizes. For example, if you have a simple site that needs to load scripts, stylesheets, and images hosted locally, as well as from the [jQuery](https://jquery.com/) library from their [CDN](https://en.wikipedia.org/wiki/Content_delivery_network), you could go with:

`Content-Security-Policy:<br> <b>default-src</b> 'self';<br> <b>script-src</b> 'self' https://code.jquery.com;`


In the example above, `Content-Security-Policy` is the HTTP header. You can also specify `Content-Security-Policy-Report-Only`, which means that the user agent will report errors but not actively block anything. While you’re testing a new policy, this is a useful feature to enable.

`script-src`, we have to also explicitly list

`'self'`because if you define a directive then it no longer inherits from

`default-src`.

It’s very important to always define `default-src`. Otherwise, the directives will default to allowing all resources. Because we have `default-src 'self'`, this means that images served from the site’s domain will also be allowed.

`default-src` is a special directive that source directives will fall back to if they aren’t configured. However, the following directives don’t inherit from `default-src`, so be aware of this and remember that not setting them to anything means they will either be unset or use the browser’s default settings:

- base-uri
- form-action
- frame-ancestors
- plugin-types
- report-uri
- sandbox

Setting `'self'` as `default-src` is generally safe, because you control your own domain. However if you really want to default to locking things down more tightly you could use `default-src 'none'` and explicitly list all known resource types. Given the example above, this would result in a policy that looks like:

`Content-Security-Policy:<br> <b>default-src</b> 'none';<br> <b>img-src</b> 'self';<br> <b>script-src</b> 'self' https://code.jquery.com;<br> <b>style-src</b> 'self';`


`default-src 'none'`. On AMO, we discovered that browser prefetching in Firefox will not be identified as a specific content type, therefore falling back to

`default-src`. If

`default-src`doesn’t cover the origin involved, the prefetched resource will be blocked. There’s a

[bug open with additional information on this issue](https://bugzilla.mozilla.org/show_bug.cgi?id=1242902).

**Dealing with inline script**

CSP by default doesn’t allow inline JavaScript unless you explicitly allow it. This means that you need to remove the following:

`<script>`blocks in the page- DOM event handlers in HTML e.g:
`onclick` `javascript:`pseudo protocol.

If you do need to allow it then CSP provides a way to do it safely through the use of the `nonce-source` or `hash-source` directives, which allow specific blocks of content to be executed. You can opt out of this protection through the use of `‘unsafe-inline’` in the `script-src` directive, but this is strongly discouraged as it opens up your site to XSS attacks.

For additional information on `nonce-source` and `hash-source`, see [CSP for the web we have](https://blog.mozilla.org/security/2014/10/04/csp-for-the-web-we-have/).

**Dealing with eval()**

CSP also blocks dynamic script execution such as:

`eval()`- A string used as the first argument to
`setTimeout`/`setInterval` `new Function()`constructor

If you need this enabled you can use `'unsafe-eval'` but again this is not recommended as it is easy for untrusted code to sneak into `eval` blocks.

On AMO, we found a lot of library code that used eval and new Function, and this was the part of CSP implementation that took the most time to fix. For example, we had underscore templates that used `new Function`. Fixing these required us to move to pre-compiled templates.

**Dealing with cascading stylesheets (CSS)**

CSP defaults to not allowing:

`<style>`blocks`style`attributes in HTML

This was a bit more of a problem for us. Lots of libraries use style attributes in HTML snippets added to the page with JavaScript and we had a sprinkling of style attributes directly in HTML templates.

It’s worth mentioning that if style properties are updated via JavaScript directly, then you won’t have a problem. For example, jQuery’s `css()` method is fine because it updates style properties directly under the covers. However, you can’t use `style="background: red"` in a block of HTML added by JS.

As before, you can use the `nonce-source` and `hash-source` directives if you need a controlled approach to allow select pieces of inline CSS.

You’re probably thinking, *“This is CSS, what’s the risk?”* There are various clever ways that CSS can be used to exfiltrate data from a site. For example, with attribute selectors and background images, you can brute force and exfiltrate attribute sensitive data such as CSRF tokens. For more information on this and other more advanced attack vectors through CSS see [XSS (No, the _other ‘S’)](https://mikewest.org/2013/09/xss-no-the-other-s-cssconfeu-2013).

Using `'unsafe-inline'` for `style-src` is not recommended, but it’s a case of balancing the risks against the number of changes that would be necessary to eliminate inline styles.

**Reporting**

It’s a good idea to set the `report-uri` directive and point it somewhere to collect JSON reports of CSP violations. As CSP doesn’t currently coalesce error reports, a single page with multiple errors will result in multiple reports to your reporting endpoint. If you run a site with a large audience, that endpoint can receive a significant amount of traffic.

In addition to reports triggered by actual violations, you’ll also find that many add-ons and browser extensions can cause CSP violations. The net result is a lot of noise: Having something that allows for filtering on the incoming data is highly recommended.

**Testing**

Once you have created your initial policy, the next step is to test it and fix any missing origins. If you run a large site, you may be surprised by the number of sources that you are pulling resources from. Running the site with CSP in report-only mode allows you to catch problems via the console and CSP reports before they actively block things.

Once everyone has confirmed that there’s nothing being blocked erroneously, it’s time to enforce the policy. From there on, it’s just a case of watching out for anything that was missed and keeping the policy up to date with browser support for some of the newer features in CSP.

**Implementing**

After you have settled upon a policy that works properly, your next step is to configure your system to deliver the CSP directives. Implementing this varies widely depending on your choice of web server software, but it should generally look like this:

```
# Enable CSP in Apache
Header set Content-Security-Policy "default-src 'none'; img-src 'self';
script-src 'self' https://code.jquery.com; style-src 'self'"
```


```
# Enable CSP in nginx
add_header Content-Security-Policy "default-src 'none'; img-src 'self';
script-src 'self' https://code.jquery.com; style-src 'self'";
```


If your service provider doesn’t offer control over your web server’s configuration, don’t panic! You can still enable CSP through the use of `meta` tags. Simply have your `meta` tag be the first tag inside `<head>`:

```
<!-- Enable CSP inside the page's HTML -->
<head>
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self';
script-src 'self' https://code.jquery.com; style-src 'self'">
</head>
```


**Our final implementation**

Given that AMO is an older and extremely complex site, you’re probably curious as to what our final policy ended up looking like:

`Content-Security-Policy:<br> <b>default-src</b> 'self';<br> <b>connect-src</b> 'self' https://sentry.prod.mozaws.net;<br> <b>font-src</b> 'self' https://addons.cdn.mozilla.net;<br> <b>frame-src</b> 'self' https://ic.paypal.com https://paypal.com<br> https://www.google.com/recaptcha/ https://www.paypal.com;<br> <b>img-src</b> 'self' data: blob: https://www.paypal.com https://ssl.google-analytics.com<br> https://addons.cdn.mozilla.net https://static.addons.mozilla.net<br> https://ssl.gstatic.com/ https://sentry.prod.mozaws.net;<br> <b>media-src</b> https://videos.cdn.mozilla.net;<br> <b>object-src</b> 'none';<br> <b>script-src</b> 'self' https://addons.mozilla.org<br> https://www.paypalobjects.com https://apis.google.com<br> https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/<br> https://ssl.google-analytics.com https://addons.cdn.mozilla.net;<br> <b>style-src</b> 'self' 'unsafe-inline' https://addons.cdn.mozilla.net;<br> <b>report-uri</b> /__cspreport__`


Wow! As you can imagine, [quite a lot of testing](https://github.com/mozilla/olympia/issues/995) went into discovering the myriad resources that AMO utilizes.

**In Summary**

The older your site is, the more work it will take to set and adhere to a reasonable Content Security Policy. However, the time is worth spending as it’s an additional layer of security that supports the idea of [defense in depth](https://en.wikipedia.org/wiki/Defense_in_depth_%28computing%29).

**Further Reading**

[An Introduction to Content Security Policy](http://www.html5rocks.com/en/tutorials/security/content-security-policy/), by Mike West[Browser Support for CSP](http://caniuse.com/#search=Content%20Security%20Policy)[Content Security Policy Level 2 Specification](http://www.w3.org/TR/CSP2/)[MDN docs on CSP](https://developer.mozilla.org/en-US/docs/Web/Security/CSP/CSP_policy_directives)

## About
[
April King ](https://pokeinthe.io/)

IRC: April

## About
[
Stuart Colville ](https://muffinresearch.co.uk/)

Stuart is the Engineering Manager for Firefox Add-ons.

## 11 comments

Scott HelmeFebruary 16th, 2016 at 12:17barretleeFebruary 16th, 2016 at 16:32Lucas RinaldiFebruary 18th, 2016 at 05:16EarlFebruary 18th, 2016 at 07:56April KingFebruary 18th, 2016 at 08:32Koemsie LyFebruary 23rd, 2016 at 20:57Seth BergerFebruary 26th, 2016 at 08:19Dan VeditzFebruary 26th, 2016 at 09:37Seth BergerFebruary 26th, 2016 at 10:52Thor Brendan BunnysonMarch 14th, 2016 at 22:14April KingMarch 15th, 2016 at 07:00