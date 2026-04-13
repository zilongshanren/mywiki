---
title: Changes to SameSite Cookie Behavior – A Call to Action for Web Developers –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/08/changes-to-samesite-cookie-behavior/
author: Mike Conca
published: '2020-08-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We are changing the default value of the ** SameSite** attribute for cookies from

**to**

`None`

**. This will greatly improve security for users. However, some web sites may depend (even unknowingly) on the old default, potentially resulting in breakage for those sites. At Mozilla, we are slowly introducing this change. And we are strongly encouraging all web developers to test their sites with the new default.**

`Lax`

## Background

[ SameSite](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#SameSite_cookies) is an attribute on cookies that allows web developers to declare that a cookie should be restricted to a first-party, or same-site, context. The attribute can have any of the following values:

– The browser will send cookies with both cross-site and same-site requests.`None`

– The browser will only send cookies for same-site requests (i.e., requests originating from the site that set the cookie).`Strict`

– Cookies will be withheld on cross-site requests (such as calls to load images or frames). However, cookies will be sent when a user navigates to the URL from an external site; for example, by following a link.`Lax`


Currently, the absence of the ** SameSite** attribute implies that cookies will be attached to any request for a given origin, no matter who initiated that request. This behavior is equivalent to setting

**. However, this “open by default” behavior leaves users vulnerable to Cross-Site Request Forgery (**

`SameSite=None`

[CSRF](https://developer.mozilla.org/en-US/docs/Glossary/CSRF)) attacks. In a CSRF attack, a malicious site attempts to use valid cookies from legitimate sites to carry out attacks.

## Making the Web Safer

To protect users from CSRF attacks, browsers need to change the way cookies are handled. The two primary changes are:

- When not specified, cookies will be treated as
by default`SameSite=Lax`

- Cookies that explicitly set
in order to enable cross-site delivery must also set the`SameSite=None`

attribute. (In other words, they must require HTTPS.)`Secure`


Web sites that depend on the old default behavior must now explicitly set the ** SameSite** attribute to

**. In addition, they are required to include the**

`None`

**attribute. Once this change is made inside of Firefox, if web sites fail to set**

`Secure`

**correctly, it is possible those sites could break for users.**

`SameSite`

## Introducing the Change

The new ** SameSite** behavior has been the default in Firefox Nightly since Nightly 75 (February 2020). At Mozilla, we’ve been able to explore the implications of this change. Starting with Firefox 79 (June 2020), we rolled it out to 50% of the

[Firefox Beta](https://www.mozilla.org/en-US/firefox/80.0beta/releasenotes/)user base. We want to monitor the scope of any potential breakage.

There is currently no timeline to ship this feature to the release channel of Firefox. We want to see that the Beta population is not seeing an unacceptable amount of site breakage—indicating most sites have adapted to the new default behavior. Since there is no exact definition of “breakage” and it can be difficult to determine via telemetry, we are watching for reports of site breakage in several channels (e.g. Bugzilla, social media, blogs).

Additionally, we’d like to see the proposal advance further in the IETF. As proponents of the open web, it is important that changes to the web ecosystem are properly standardized.

## Industry Coordination

This is an industry-wide change for browsers and is not something Mozilla is undertaking alone. Google has been [rolling this change out](https://www.chromium.org/updates/same-site) to Chrome users since February 2020, with ** SameSite=Lax** being the default for a certain (unpublished) percentage of all their channels (release, beta, canary).

Mozilla is cooperating with Google to track and share reports of website breakage in our respective bug tracking databases. Together, we are encouraging all web developers to start explicitly setting the ** SameSite** attribute as a best practice.

## Call to Action for Web Developers

Testing in the Firefox Nightly and Beta channels has shown that website breakage does occur. While we have reached out to those sites we’ve encountered and encouraged them to set the ** SameSite** attribute on their web properties, the web is clearly too big to do this on a case-by-case basis.

It is important that all web developers test their sites against this new default. This will prepare you for when both Firefox and Chrome browsers make the switch in their respective release channels.

### Test your site in Firefox

To test in Firefox:

- Enable the new default behavior (works in any version past 75):
- In the URL bar, navigate to
**about:config**. (accept the warning prompt, if shown). - Type
**SameSite**into the “Search Preference Name” bar. - Set
to`network.cookie.sameSite.laxByDefault`

**true**using the toggle icon. - Set
to`network.cookie.sameSite.noneRequiresSecure`

**true**using the toggle icon. - Restart Firefox.

- In the URL bar, navigate to
- Verify the browser is using the new SameSite default behavior:
- Navigate to
[https://samesite-sandbox.glitch.me/](https://samesite-sandbox.glitch.me/). - Verify that all rows are green.

- Navigate to

At this point, test your site thoroughly. In particular, pay attention to anything involving login flows, multiple domains, or cross-site embedded content (images, videos, etc.). For any flows involving requests, you should test with and without a long delay. This is because both Firefox and Chrome implement a two-minute threshold that permits newly created cookies without the

`POST`

**attribute to be sent on top-level, cross-site**

`SameSite`

**requests (a common login flow).**

`POST`

### Check your site for breakage

To see if your site is impacted by the new cookie behavior, examine the [Firefox Web Console](https://developer.mozilla.org/docs/Tools/Web_Console) and look for either of these messages:

- Cookie rejected because it has the “
`sameSite=none`

” attribute but is missing the “`secure`

” attribute. - Cookie has “
`sameSite`

” policy set to “`lax`

” because it is missing a “`sameSite`

” attribute, and “`sameSite=lax`

” is the default value for this attribute.

Seeing either of these messages does not necessarily mean your site will no longer work, as the new cookie behavior may not be important to your site’s functionality. It is critical, therefore, that each site test under the new conditions. Then, verify that the new ** SameSite** behavior does not break anything. As a general rule, explicitly setting the

**attribute for cookies is the best way to guarantee that your site continues to function predictably.**

`SameSite`

## Additional Resources


## About Mike Conca

Mike Conca is the Group Product Manager for the Firefox Web Platform, leading the product team responsible for the core web technologies in Firefox including JavaScript, DOM Web API, WebAssembly, storage, layout, media, and graphics.

## 3 comments

Sachin MourAugust 5th, 2020 at 01:58Jan VAugust 7th, 2020 at 02:14NuxAugust 13th, 2020 at 04:40