---
title: Content Security Policy 1.0 lands in Firefox Aurora – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2013/05/content-security-policy-1-0-lands-in-firefox-aurora/
author: Frederik Braun
published: '2013-05-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*The information in this article is based on work together with Ian Melven, Kailas Patil and Tanvi Vyas*.

We have just landed support for the [Content Security Policy (CSP) 1.0
specification](http://www.w3.org/TR/CSP/) in

[Firefox Aurora](http://www.mozilla.org/en-US/firefox/aurora/)(Firefox 23), available as of tomorrow (May 30th). CSP is a security mechanism that aims to protect a website against content injection attacks by providing a whitelist of known-good domain names to accept JavaScript (and other content) from. CSP does this by sending a Content-Security-Policy header with the document it protects (yes, we lost the X prefix with the 1.0 version of the spec).

To effectively protect against XSS, a few JavaScript features have to be

disabled:

- All inline JavaScript is disallowed. This means, that all the JavaScript code must be placed in a separate file that is linked via
`<script src=... >`

- All calls to functions which allow JavaScript code being executed from strings (e.g.,
*eval*) are disabled

## CSP now more intuitive and consistent

While Firefox has had support for CSP since its invention here at Mozilla, things have been changing a lot. The streamlined development of a specification within the W3C has made the concept more intuitive and consistent. Most directives in a CSP header are now of a unified form which explicitly specifies the type of content you want to restrict:

- img-src
- object-src
- script-src
- style-src and so on.

Oh and if you feel like you must allow less secure JavaScript coding styles, you can add the values *unsafe-inline* or *unsafe-eval* to your list of script sources. (This used to be inline-script and eval-script before).

Start protecting your website by implementing CSP now!

But wait – isn’t that a bit tedious… Writing a complex policy and making sure that you remembered all the resources that your website requires? Don’t fret! Here comes [UserCSP](https://addons.mozilla.org/en-US/firefox/addon/newusercspdesign/) again!

## Generate your Content Security Policies with UserCSP!

During the last few months, Kailas Patil, a student in our [Security Mentorship Program](https://wiki.mozilla.org/Security/Mentorship) has continued his GSoC [work from last year](https://blog.mozilla.org/tanvi/2012/09/18/user-specified-content-security-policy/) to update [UserCSP](https://addons.mozilla.org/en-US/firefox/addon/newusercspdesign/).

UserCSP is a Firefox add-on that helps web developers and security-minded users use CSP. Web developers can create a Content Security Policy (CSP) for their site by using UserCSP’s infer CSP feature. This feature can list required resource URLs and turn them into a policy ready to plug into a CSP header.

In addition, UserCSP is the first step to expose a policy enforcement mechanism directly to web users. Furthermore, users can enforce a stricter policy than a page supplies through the add-on or apply a policy to certain websites that don’t currently support CSP.

While earlier versions of UserCSP were more aligned to content security policies as originally invented at Mozilla, this version is updated to be in compliance with the CSP 1.0 specification. This means that policies derived with this add-on may work in all browsers as soon as they [support](http://caniuse.com/#search=CSP) the specification. Hooray!

As this evolves and ships, our [MDN documentation on Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Security/CSP) will keep on evolving, and we also plan to write more about this in the [Mozilla Security Blog](https://blog.mozilla.org/security/) in the next few weeks, so stay tuned!

## About
[
Frederik Braun ](https://frederikbraun.de)

Frederik Braun builds security for the web and for Mozilla Firefox from Berlin. As a contributor to standards, Frederik is also improving the web platform by bringing security into the defaults with specifications like the Sanitizer API and Subresource Integrity. When not at work, Frederik likes reading a good novel or going on long bike treks across Europe.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 8 comments

DmitryMay 29th, 2013 at 18:32Robert Nyman [Editor]May 29th, 2013 at 23:42Robert Nyman [Editor]May 30th, 2013 at 04:38DmitryMay 30th, 2013 at 05:14Robert Nyman [Editor]May 30th, 2013 at 13:10DmitryMay 30th, 2013 at 14:34DmitryMay 30th, 2013 at 15:21Mathew PorterJune 5th, 2013 at 11:58