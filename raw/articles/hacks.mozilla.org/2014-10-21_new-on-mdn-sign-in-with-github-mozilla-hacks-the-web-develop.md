---
title: 'New on MDN: Sign in with Github! – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2014/10/new-on-mdn-sign-in-with-github/
author: Justin Crawford
published: '2014-10-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[MDN](http://developer.mozilla.org/) now gives users more options for signing in!

![Sign in with GitHub](../../assets/75cec114528ec785.png)


Signing in to MDN previously required a Mozilla Persona account. Getting a Persona account is[ free and easy](https://support.mozilla.org/en-US/kb/what-is-persona-and-how-does-it-work), but MDN analytics showed a steep drop-off at the “Sign in with Persona” interface. For example, almost 90% of signed-out users who clicked “Edit” never signed in, which means they never got to edit. That’s a lot of missed opportunities!

It should be easy to join and edit MDN. If you click “Edit,” we should make it easy for you to edit. Our analysis demonstrated that most potential editors stumbled at the Persona sign in. So, we looked for ways to improve sign in for potential contributors.

Common sense suggests that many developers have a GitHub account, and analysis confirms it. Of the MDN users who list external accounts in their profiles, approximately 30% include a GitHub account. GitHub is the 2nd-most common external account listed, after Twitter.

That got us thinking: If we integrated GitHub accounts with MDN profiles, we could one day share interesting GitHub activity with each other on MDN. We could one day use some of GitHub’s tools to create even more value for MDN users. Most immediately, we could offer “sign in with GitHub” to at least 30% (but probably more) of MDN’s existing users.

And if we did that, we could also offer “sign in with GitHub” to over 3 million GitHub users.

The entire engineering team and MDN community helped make it happen.

## Authentication Library

Adding the ability to authenticate using GitHub accounts required us to extend the way MDN handles authentication so that MDN users can start to add their GitHub accounts without effort. We reviewed the current code of [kuma](https://github.com/mozilla/kuma/) (the code base that runs MDN) and realized that it was deeply integrated with how Mozilla Persona works technically.

As we’re constantly trying to remove technical debt that meant revisiting some of the decisions we’ve made years ago when the code responsible for authentication was written. After a review process we decided to replace our home-grown system, [django-browserid](https://github.com/mozilla/django-browserid), with a 3rd party library called [django-allauth](https://github.com/pennersr/django-allauth/) as it is a well known system in the Django community that is able to use multiple authentication providers side-by-side – Mozilla Persona and GitHub in our case.

One challenge was making sure that our existing user database could be ported over to the new system to reduce the negative impact on our users. To our surprise this was not a big problem and could be automated with a database migration–a special piece of code that would convert the data into the new format. We implemented the new authentication library and migrated accounts to it several months ago. MDN has been using django-allauth for Mozilla Persona authentication since then.

## UX Challenges

We wanted our users to experience a fast and easy sign-up process with the goal of having them edit MDN content at the end. Some things we did in the interface to support this:

- Remember why the user is signing up and return them to that task when sign up is complete.
- Pre-fill the username and email address fields with data from GitHub (including pre-checking if they are available).
- Trust GitHub as a source of confirmed email address so we do not have to confirm the email address before the user can complete signing up.
- Standardise our language (this is harder than it sounds). Users on MDN “sign in” to their “MDN profile” by connecting “accounts” on other “services”.
[See the discussion](https://bugzilla.mozilla.org/show_bug.cgi?id=1051000).

One of our biggest UX challenges was allowing existing users to sign in with a new authentication provider. In this case, the user needs to “claim” an existing MDN profile after signing in with a new service, or needs to add a new sign-in service to their existing profile. We put a lot of work into making sure this was easy both from the user’s profile if they signed in with Persona first and from the sign-up flow if they signed in with GitHub first.

We started with an ideal plan for the UX but expected to make changes once we had a better understanding of what allauth and GitHub’s API are capable of. It was much easier to smooth the kinks out of the flow once we were able to click around and try it ourselves. This was facilitated by the way MDN uses feature toggles for testing.

## Phased Testing & Release

This project could potentially corrupt profile or sign-in data, and changes one of our most essential interfaces – sign up and sign in. So, we made a careful release plan with several waves of functional testing.

We love to alpha- and beta-test changes on MDN with [feature toggles](https://github.com/jsocol/django-waffle). To toggle features we use the excellent [django-waffle](https://github.com/jsocol/django-waffle) feature-flipper by [James Socol](http://jamessocol.com/) – MDN Manager Emeritus.

We deployed the new code to [our MDN development environment](https://developer-dev.allizom.org/) every day behind a feature toggle. During this time MDN engineers exercised the new features heavily, finding and filing bugs under [our master tracking bug](https://bugzilla.mozilla.org/showdependencytree.cgi?id=991351).

When the featureset was relatively complete, we created [our beta test page](https://wiki.mozilla.org/MDN/Development/GitHub_Beta), toggled the feature on [our MDN staging environment](https://developer.allizom.org) for even more review. We did the end-to-end UX testing, invited internal Mozilla staff to help us beta test, [filed a lot of UX bugs](https://bugzilla.mozilla.org/showdependencytree.cgi?id=1046775), and started to triage and prioritize launch blockers.

Next, we started an open beta by posting a site-wide banner on the live site, inviting anyone to test and file bugs. 365 beta testers participated in this round of QA. We also asked [Mozilla WebQA](https://quality.mozilla.org/teams/web-qa/) to help deep-dive into the feature on our stage server. We only received a handful of bugs, which gave us great confidence about a final release.

## Launch

It was a lot of work, but all the pieces finally came together and we launched. Because of our extensive testing & release plan, we’ve 0 incidents with the launch – no down-time, no stacktraces, no new bugs reported. We’re very excited to release this feature. We’re excited to give more options and features to our incredible MDN users and contributors, and we’re excited to invite each and every GitHub user to join the Mozilla Developer Network. Together we can make the web even more awesome. [Sign in now](http://developer.mozilla.org).

## Outlook

Now that we have worked out the infrastructure and UX challenges associated with multi-account authentication, we can look for other promising authentication services to integrate with. For example, [Firefox Accounts](https://blog.mozilla.org/blog/2014/02/07/introducing-mozilla-firefox-accounts/) (FxA) is the authentication service that powers [Firefox Sync](https://www.mozilla.org/en-US/firefox/sync/). FxA is integrated with Firefox and will soon be integrated with a variety of other Mozilla services. As more developers sign up for Firefox Accounts, we will look for opportunities to add it to our authentication options.

## 5 comments

Herbert Dupree, IIOctober 22nd, 2014 at 03:59Robert Nyman [Editor]October 22nd, 2014 at 04:27Herbert Dupree, IIOctober 22nd, 2014 at 18:55John KarahalisOctober 22nd, 2014 at 19:08Herbert Dupree, IIOctober 22nd, 2014 at 19:18