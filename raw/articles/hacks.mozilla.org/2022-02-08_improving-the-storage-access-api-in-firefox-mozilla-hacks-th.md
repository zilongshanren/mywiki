---
title: Improving the Storage Access API in Firefox – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2022/02/improving-the-storage-access-api-in-firefox/
author: Benjamin VanderSloot
published: '2022-02-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Before we roll out [State Partitioning](https://hacks.mozilla.org/2021/02/introducing-state-partitioning/) for all Firefox users, we intend to make a few privacy and ergonomic improvements to the [Storage Access API](https://privacycg.github.io/storage-access/). In this blog post, we’ll detail a few of the new changes we made.

With State Partitioning, third parties can’t access the same cookie jar when they’re embedded in different sites. Instead, they get a fresh cookie jar for each site they’re embedded in. This isn’t just limited to cookies either—all storage is partitioned in this way.

In an ideal world, this would stop trackers from keeping tabs on you wherever they’re embedded because they can’t keep a unique identifier for you across all of these sites. Unfortunately, the world isn’t so simple—trackers aren’t the only third parties that use storage. If you’ve ever used an authentication provider that requires an embedded resource, you know how important third-party storage can be.

Enter the Storage Access API. This API lets third parties request storage access as if they were a first party. This is called “unpartitioning” and it gives browsers and users control over which third parties can maintain state across first-party origins as well as determine which origins they can access that state from. This is the preferred way for third parties to keep sharing storage across sites.

The Storage Access API leaves a lot of room for the browser to decide when to allow a third party unrestricted storage access. This is a feature that gives the browser freedom to make decisions it feels are best for the user and decide when to present choices about storage permissions to users directly.

On the other hand, this means the Storage Access API can vary from browser to browser and version to version. As a result, the developer experience will suffer unless we do two things: 1) Design with the developer experience in mind; and 2) communicate what we’re doing.

So let’s dive in! Here are four changes we’re making to the Storage Access API that will improve user privacy and maintain a strong developer experience…

## Requiring User Consent for Third-Parties the User Never Interacted With

With Storage API, the browser determines whether to involve the user in the decision to grant storage access to a third party. Previously, Firefox didn’t involve users until a third party already had access to its storage on five different sites. At that point, the third party’s storage access requests were presented to users to make a decision.

We’re allowing third parties some leeway to unpartition their storage on a few sites because we’re worried about overwhelming users with popup permission requests. We feel that allowing only a few permission grants per third party would keep the permission frequency down while still preventing any one party from tracking the user on many sites.

We also wanted to improve user privacy in our Storage Access API implementation by reducing the number of times third parties can automatically unpartition themselves without overwhelming the user with storage access requests. The improvement we settled on was requiring the user to have interacted with the third party recently to give them storage access without explicitly asking the user whether or not to allow it. We believe that removing automatic storage access grants for sites the user has never seen before captures the spirit of State Partitioning without having to bother the user too much more.

Careful readers may now be concerned that any embed-only pages, like some authentication services, will be heavily impacted by this. To tip the scales even further toward low user touch, we expanded the definition of “interacting with a site” to support embed-only contexts. Now, whenever a user grants storage access via permission popups or interacts with an iframe with storage access, these both count as user interactions. This change is the result of a lot of careful balancing between preserving legitimate use cases, protecting user privacy, and not annoying users with endless permission prompts. We think we found the sweet spot.

## Changing the Scope of First-Party Storage Access to Site

While rolling out State Partitioning, we’ve seen the emergence of a fair number of use cases for the Storage Access API. One common use is to enable authentication using a third party.

We found on occasion the login portal that gave first-party storage access to the authentication service was a subdomain, like **https://login.example.com**. This caused problems when the user navigated to **https://example.com** after logging in… they were no longer logged in! This is because the storage access permission was only granted to the login subdomain and not the rest of the site. The authentication provider had access to its cookies on **https://login.example.com**, but not on **https://example.com**.

We fixed this by moving the storage access permission to the Site-scope. This means that when a third party gets storage access on a page, it has access to unpartitioned storage on all pages on that same Site. So in the example above, the authenticating third party would have access to the user’s login cookie on **https://login.example.com**, **https://example.com**, and **https://any.different.subdomain.example.com**! Yet they still wouldn’t have access to that login cookie on **http://example.com** or **https://different-example.com**.

## Cleaning Up User Interaction Requirements

Requiring user interaction when requesting storage access was one rough edge of the Storage Access API definition. Let’s talk about that requirement.

If a third party calls requestStorageAccess as soon as a page loads, it should not get that storage access. It needs to wait until the user interacts with their iframe. Scrolling or clicking are good ways to get this user interaction and it will expire a few seconds after it’s granted. Unfortunately, there were some corner cases in this requirement that we needed to clean up.

One corner case concerns what to do with the user’s interaction state when they click Accept or Deny on a permission prompt. We decided that when a user clicks Deny on a storage access permission prompt, the third party should lose their user interaction. This prevents the third party from immediately requesting storage access again, bothering the user until they accept.

Conversely, we decided to reset the timer for user interaction if the user clicks Accept to reflect that the user did interact with the third party. This will allow the third party to use APIs that require both storage access and user interaction with only one user interaction in their iframe.

Another corner case concerned how strict to be when requiring user interaction for storage access requests. As we’ve iterated on the Storage Access API, minor changes have been introduced. One of the changes has to do with the case of giving a third party storage access on a page, but then the page is reloaded. Does the third party have to get a user interaction before requesting storage access again? Initially, the answer was no, but now it is yes. We updated our implementation to reflect that change and align with other browsers.

## Integrating User Cookie Preferences

In the settings for Firefox [Enhanced Tracking Protection](https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop), users can specify how they want the browser to handle cookies. By default, Firefox blocks cookies from known trackers. But we have a few other possible selections, such as allowing all cookies or blocking all third-party cookies. Users can alter this preference to their liking.

We have always respected this user choice when implementing the Storage Access API. However, this wasn’t clear to developers. For example, users that set Firefox to block all third-party cookies will be relieved to know the Storage Access API in no way weakens their protection; even a storage access permission doesn’t give a third party any access to storage. But this wasn’t clear to the third party’s developers.

The returned promise from requestStorageAccess would resolve, indicating that the third party had access to its unpartitioned storage. We endeavored to fix this. In Firefox 98, when the user has disabled third-party cookies via the preferences, the function requestStorageAccess will always return a rejecting promise and hasStorageAccess will always return false.



## One comment

AlexFebruary 8th, 2022 at 21:45