---
title: Magic Link Pitfalls
url: https://etodd.io/2026/03/22/magic-link-pitfalls/
published: '2026-03-22'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Magic Link Pitfalls

Recently I was surprised to discover that there are several bad ways to do magic links.

The basic idea is: a user hits “login”, enters their email address, and receives an email that allows them to login without a password. What could possibly go wrong?

I work in security, so I already knew a few best practices I would need to implement:

- The link should have a short expiration
- The link should only work once
- The link should include a secret code with a sufficient amount of entropy (I went with 64 bits; your paranoia may vary)
- The database should store a hash of the secret code, not the code itself

Here’s two more that were not immediately obvious to me.

## Require a click

My first attempt at a magic link logged the user in immediately as soon as they clicked it. That is, as soon as their browser issued a GET request. Somewhat alarmingly, some of these links were already claimed before I could click on them. Then I realized, some programs issue GET requests to render link previews. Browsers might even prefetch the page when you hover over the link with your mouse. So the code might be unintentionally “claimed” without me ever seeing it.

To avoid this pitfall, the link should lead to a page which only claims the code once the user clicks a big button.

## Login the original tab, not the magic link tab

The first time I clicked a magic link on my phone, the in-app browser inside my email app got logged in. The default browser on my phone remained painfully unaware.

To avoid this pitfall, the link should do nothing but mark the code as “verified” and instruct the user to return to their original browser tab, which should auto-refresh every few seconds to check whether the code is verified, and if so, log the user in.

This also allows users to login on devices that don’t have access to email, by clicking a link on a different device. You can also achieve the same effect by sending a short (6-ish digit) code in the email and asking the user to type the code in the original browser tab. But in my opinion, 6 digits only offers enough entropy for low-stakes use cases like logging into your TV, or for a second factor on top of some other verification method.

So that’s where I’m at now. What do you think? Any other pitfalls I’m missing?