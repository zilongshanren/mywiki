---
title: Account Manager coming to Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/04/account-manager-coming-to-firefox/
author: Dan Mills
published: '2010-04-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Update:** The Account Manager is no longer maintained. Building on this experiment, we have conceived [BrowserID](https://www.browserid.org/). Please consider using it instead.

Last month Mozilla Labs announced a new concept series on [online identity](http://mozillalabs.com/conceptseries/identity/). As part of this exploration, we developed the [Account Manager](https://mozillalabs.com/blog/2010/03/account-manager/).

The Account Manager makes it incredibly easy for users to create new accounts with optional randomly generated passwords, and log into and out of them with just a click. As a web developer, adding support for this feature could take as little as fifteen minutes of hacking (in fact, we’ll mention the first 5 people to add support – read below to learn more.).

We want to make signing into websites easier for all Firefox users, and are looking to [ship this feature](https://bugzilla.mozilla.org/show_bug.cgi?id=562161) as soon as possible in Firefox. As part of that process we’re looking for feedback to refine the specification. Now is a really good time to [get involved](http://www.mozilla.com/en-US/firefox/accountmanager/) in defining the spec.

There are three things that you can do right now:

- Read the
[draft specification](https://wiki.mozilla.org/Labs/Weave/Identity/Account_Manager/Spec/Latest). - Join our
[discussion group](https://groups.google.com/group/mozilla-labs-online-identity?pli=1). - Come to our
[in-person meet-up](http://www.mozilla.com/en-US/firefox/accountmanager/form)on May 20th.

This feature is currently available as an experimental add-on, available on the [Account Manager homepage](http://www.mozilla.com/en-US/firefox/accountmanager/).

Here’s a video where you can get a basic idea of how Account Manager works today:

**How Does It Work?**

The Account Manager specification proposes two small changes to Web sites:

-
The browser needs to know how to register, sign in, and sign out of your site. You will need a static JSON document, automatically discovered by the browser, which describes what methods the site supports and how they should be executed. For example, a web site might describe their support of “connect” (sign in) like this:

"methods": { "username-password-form": { "connect": { "method": "POST", "path": "/accounts/LoginAuth", "params": { "username": "Email", "password": "Passwd" } }

This example tells the browser that the site supports signing in with a form POST to /accounts/LoginAuth, and what parameter names to use for the username and password (Email and Passwd respectively).

-
The browser needs a way to check which user (if any) is currently signed in. To do this, you need to set an HTTP header in the same code where you would set a cookie with a session ID. If you can’t set an HTTP header, you can also supply a URL the browser will ping.

The header would look like this:

X-Account-Management-Status: active; name="Joe User"

That would tell the browser that “Joe User” is now signed in, so it can provide the appropriate UI (to switch users or sign out).

**How do I try it?**[Install the demo add-on](http://www.mozilla.com/en-US/firefox/accountmanager/).- Place a host-meta document to your website at /.well-known/host-meta (it must be at this location). This tells the browser where to find the JSON file we described above. For examples, check
[the spec](https://wiki.mozilla.org/Labs/Weave/Identity/Account_Manager/Spec/Latest#Appendix_B:_Host-meta_example)or[Yahoo!’s host-meta](http://www.yahoo.com/.well-known/host-meta). - Add the JSON file itself to your site. We call this the Account Manager Control Document, or AMCD for short. The AMCD should contain your form end-points for sign-in and sign-out. Note that you don’t need to change the end-points, just describe them. Check
[the spec](https://wiki.mozilla.org/Labs/Weave/Identity/Account_Manager/Spec/Latest#Appendix_A:_Account_Management_Control_Document_Example)for a complete example. - Change your site to set the correct headers when users sign in or out.
- Make sure you have a password saved in the password manager; you may need to sign in manually once to do that if you haven’t already (this requirement will go away in the future).
- When we add sign-up support in Account Manager, you will likely need to make minor changes to your registration code.

Update, 5:45PM PST: Just realized while debugging an intrepid first adopter’s site that there is one more requirement:

- You can send the status header with every request, or if you don’t want to do that, then you need to provide a sessionstatus method (see the spec) that the browser can ping to find out the user’s signed-in status.

That’s it, folks! Be one of the first to try implementing the specification on your website, and

[let us know](https://groups.google.com/group/mozilla-labs-online-identity?pli=1), and let us know how long it took you to add support for it. We’ll put the first five people to implement this on the[@mozhacks](http://twitter.com/mozhacks)twitter account with a link to your site!Next time we will go into more depth on how discovery works, our plans to support other auth schemes (like HTTP Auth, OpenID, etc), as well as other neat features we plan to add. Stay tuned! And don’t forget to

[tell us what you think](http://www.mozilla.com/en-US/firefox/accountmanager/).

**Web Developer FAQ**-
**Do I need to redo all of my authentication code?**No. Account Manager is designed to require minimal server-side changes. You do have a couple of options, but the minimal setup is just a flat file and a couple of extra headers you need to send out.

-
**Do I need to redo all of my account creation code?**Registration will require some small changes to your registration flow, but we have put extra thought into making it as simple as possible for both Web sites and users alike. Check out our discussion group and specification for the details, and let us know what you think!

-
**How is this going to help my users?**Account Manager is great for users. Here are a few highlights:

-
**Simple, convenient, user control**The browser has a couple of advantages when it comes to making this kind of UI. First, it can dedicate a spot in the browser chrome that will look and behave the same for every site, making it a convenient and automatic go-to place for users to check or change their sign-in status.

The browser also has deep knowledge about the user. For example, the browser could implement fast user switching with just a click. Or think about picking a username: the browser can look at usernames for other accounts and make some pretty good guesses about what usernames are preferred.

-
**Secure**Many security researchers will tell you: one of the biggest security problems on the Web today is that usernames and passwords are often short and easily guessed. Account Manager makes it so that users don’t need to remember their passwords, and in fact can automatically generate strong passwords when signing up.

Moreover, Account Manager begins the process of abstracting the plumbing of account management from the UI, making it possible in the future to support cryptographically strong protocols without any major UI changes.

-
**Works on top of current and emerging solutions**Lastly, Account Manager is not a new ID for the Web. Rather, it is designed to work on top of current and emerging solutions like OpenID or others, to bring them all under the same user experience. Users shouldn’t have to care what the underlying technology is.


-
-
**How is this going to help me get more users?**The easier it is to sign up and sign into your site, the more users you will get. It’s pretty much that simple.

Note that Account Manager doesn’t force your users to make a choice: you can keep all of your current content-based flows intact, so there is really no downside to adding Account Manager support to your site.

-
**Do I need to have special content for Firefox only?**No! First of all, you don’t need to do *any* changes to your current content at all. Account Manager works behind the scenes using a sitemap and headers to communicate with your site and present the right UI to the user.

On the other hand, we hope that Account Manager will not be a Firefox-only technology. We’re working towards defining the protocol as a formal specification that other Web browsers can implement.


## About

[Dan Mills](http://blog.sandmill.org/)

## 74 comments

DanApril 27th, 2010 at 15:02Dan MillsApril 27th, 2010 at 15:07Fernando AgüeroApril 27th, 2010 at 15:20WayApril 27th, 2010 at 15:22WayApril 27th, 2010 at 15:23UlrichApril 27th, 2010 at 15:29RobertApril 27th, 2010 at 15:34Toby AdamsApril 27th, 2010 at 15:54HansApril 27th, 2010 at 16:20Nino D’AversaApril 27th, 2010 at 16:36Kroc CamenApril 27th, 2010 at 16:43John DrinkwaterApril 28th, 2010 at 03:59l.m.orchardApril 28th, 2010 at 18:12Dan MillsApril 27th, 2010 at 16:45Edward LeeApril 27th, 2010 at 16:48Paul-JosephApril 27th, 2010 at 16:54Dan MillsApril 27th, 2010 at 16:56Kroc CamenApril 27th, 2010 at 16:57Dan MillsApril 27th, 2010 at 17:08HansApril 27th, 2010 at 17:31Jesse RudermanApril 27th, 2010 at 17:52Dan MillsApril 27th, 2010 at 18:27Mike JonesApril 27th, 2010 at 19:03Dan MillsApril 27th, 2010 at 19:26Justin L.April 27th, 2010 at 20:25Dan MillsApril 27th, 2010 at 21:27KumarApril 27th, 2010 at 21:59Tharaka DevindaApril 27th, 2010 at 22:16Martin KliehmApril 27th, 2010 at 23:34Robert AccetturaApril 28th, 2010 at 06:38Terence JohnsonApril 28th, 2010 at 07:14Shirley V.April 28th, 2010 at 08:21fpiatApril 28th, 2010 at 08:28AZApril 28th, 2010 at 09:15Dan MillsApril 28th, 2010 at 10:44AZApril 28th, 2010 at 11:25Dan MillsApril 28th, 2010 at 11:50Dan MillsApril 28th, 2010 at 11:52Dave MackeyApril 29th, 2010 at 06:40NikitaApril 29th, 2010 at 08:11riveyApril 29th, 2010 at 08:32JasonApril 29th, 2010 at 14:39Carlos J.MillsApril 29th, 2010 at 15:43MarkusMay 1st, 2010 at 04:06Kim A. BettiMay 2nd, 2010 at 10:45ArmenMay 3rd, 2010 at 11:25DanMay 3rd, 2010 at 11:32RonMay 25th, 2010 at 23:59KOKMay 4th, 2010 at 08:29Simon B.May 21st, 2010 at 03:46RonMay 26th, 2010 at 00:02PatrickMay 27th, 2010 at 06:49PigpromoterMay 27th, 2010 at 23:44FrankMay 28th, 2010 at 11:54Anthony DeRobertisJune 8th, 2010 at 20:40Simon B.June 15th, 2010 at 00:05Anthony DeRobertisJune 21st, 2010 at 10:01Preturi asigurari RCAJuly 15th, 2011 at 01:46louisremiJuly 20th, 2011 at 07:05MacarthurJuly 13th, 2010 at 07:40RCA ieftinOctober 29th, 2010 at 07:10EivindFebruary 3rd, 2011 at 01:22Asigurari LocuinteOctober 3rd, 2011 at 22:00dambovitaOctober 19th, 2011 at 04:03