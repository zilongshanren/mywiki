---
title: Getting involved with Account Manager – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/05/getting-involved-with-account-manager/
author: Dan Mills
published: '2010-05-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It’s been a couple of weeks since we [originally posted about Account Manager](http://hacks.mozilla.org/2010/04/account-manager-coming-to-firefox/) and we’ve gotten a lot of feedback. We’ve got a few opportunities for people to get more involved with the project, listed below.

**Join us at the Account Manager Meet-up or at IIW**

We are hosting an [Account Manager Meet-up on Friday, May 21st at Mozilla’s Mountain View Headquarters](https://wiki.mozilla.org/Firefox/Projects/AccountManager/Meetup). This meetup will be an excellent opportunity to give your feedback on the [draft specification](https://wiki.mozilla.org/Labs/Weave/Identity/Account_Manager/Spec/Latest) as we prepare to finalize it. So, if you are a web developer, sysadmin, protocol or security expert, RSVP [here](http://www.mozilla.com/en-US/firefox/accountmanager/form).

The summit will be from 1PM to 4PM followed by a “cantina” during which you’ll get a chance to meet with other Mozilla developers over informal drinks and snacks.

We’ll also be presenting at the [Internet Identity Workshop](http://iiw.idcommons.net/Main_Page) next week; if you are planning on attending IIW look for the Account Manager talk and come and say hello!

**Browser-assisted registration**

Another way to help out is to add reigistration support to your site. The latest version of the Account Manager add-on adds support for a basic registration flow, and we’re very interested in finding out what the Web development community thinks about it. Here’s what you need to do:

Add a snippet to the username-password-form profile in your AMCD:

```
"register": {
"method": "POST",
"path": "/register-endpoint",
"id-type": "email"
}
```

Then you need to add a method at /register-endpoint which will receive the user id and secret as POST parameters. Your method should return 200 if the id and secret are OK, otherwise return 400 with a snippet of JSON (see the spec for details and examples).

You might need to change your content to accomodate this new model: after you return 200 the expectation is that there is a username+password pair which is valid, even though it might map to a disabled account. For example, if you need to ask for additional information, have the user solve a captcha, or require email verification, simply keep the account disabled until those additional requirements have been met.

**Addressing cross-site request forgeries**

Based on feedback from the community, we’ve been investigating several possibilities for preventing CSRF attacks with Account Manager. In addition to supporting CSRF tokens, the latest proposal leverages headers to achieve the same goal with fewer requests and without a session cookie. Interested? Join the discussion on our [forum](https://groups.google.com/group/mozilla-labs-online-identity?pli=1).

**Join us online**

Join our online community, visit the Account Manager [feature page](http://www.mozilla.com/en-US/firefox/accountmanager/) to learn more about Account Manager, and to subscribe to our mailing list/forum.

If you add support for Account Manager to your site, please add yourself to the the [wiki page for early Account Manager sites](https://wiki.mozilla.org/Firefox/Projects/AccountManager/SupportedSites).

## 6 comments

Robert KaiserMay 16th, 2010 at 08:55lgMay 17th, 2010 at 11:00jpvincentMay 18th, 2010 at 02:01Lg from beforeMay 18th, 2010 at 07:37AnonymousMay 19th, 2010 at 16:46zafar iqbalSeptember 14th, 2010 at 22:42