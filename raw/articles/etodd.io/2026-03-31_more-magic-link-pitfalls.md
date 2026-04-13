---
title: More Magic Link Pitfalls
url: https://etodd.io/2026/03/31/more-magic-link-pitfalls/
published: '2026-03-31'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# More Magic Link Pitfalls

Folks kindly responded with [some criticism](https://lobste.rs/s/lzxb0m/magic_link_pitfalls) of my [list of magic link pitfalls](https://etodd.io/2026/03/22/magic-link-pitfalls/).
So let’s talk about some more pitfalls!

## Magic links are annoying

This was by far the most common sentiment: “just give me a username and password”. I’m 99% sure this criticism comes from tech-savvy developers, so I’ll rephrase this as: “just give me a way to login with my password manager”. That’s fair!

The most common proposed solution was to implement passkeys. They can’t replace magic links entirely, since most users will not understand where their passkeys are stored or how to transport them between devices and browsers made by competing companies. But they are a good idea! Better than passwords. I will be implementing them.

## Magic links are vulnerable to phishing

This is in response to my advice to “login the original tab, not the magic link tab”.
The idea is, the user enters their email into an adversarial server masquerading as the real server, probably with a [similar domain name](https://en.wikipedia.org/wiki/Typosquatting).
The adversarial server initiates the login on behalf of the user and starts polling the real server, waiting to be logged in.
The user clicks the magic link, and the adversarial server’s login is now verified, so it receives an auth cookie.
The user is none the wiser.

At first I thought this was a flaw specific to magic links; perhaps switching to a slightly more annoying 6-digit code could fix it. But this is not much better; the user would simply return to the phishing website and enter the 6-digit code.

So, magic links are just as vulnerable to phishing as password logins. Can we do better?

One idea is to record the browser’s IP and user agent string when it initiates a login. Then your magic link email can look like something like this:

Someone is trying to login to

[your@email.com]from Smalltown, KS via Chrome on macOS. Is this you?

- That’s me, log me in
- This looks fishy

Combined with passkeys which are not vulnerable to phishing, I think this is an acceptable mitigation.

## Handle flaky email delivery

My previous article said “the database should store a hash of the secret code, not the code itself”. If you only store a hash, that means you can only send the code once. You can’t resend if something goes wrong with the email delivery, you have to generate a new code.

The problem with that is, if your email is being flaky and you generate several codes and only one of them eventually makes it to your email inbox, how do you know which code it was? Maybe the second code is the one that makes it through, but it’s useless now because you already started the login process over with a new code.

So, you need a way to resend the code without restarting the login process and generating a new code. And to do that, you need to store the code itself, not a hash of it.

I will admit, this hashing idea was a bit of cargo-culting on my part. At $WORK, I’ve found that it’s simpler and less error-prone to have a blanket rule like “no plaintext credentials in the database”. The more complex the rule is, the more likely it is that someone will make a mistake.

So, that said, I think I will encrypt these codes instead of hashing them, and add a “resend code” button to the login screen.

## Rate limit login attempts

I didn’t mention this originally because it’s not really specific to magic links; all types of login attempts should be rate limited. The approach that makes sense to me is to limit the number of pending authentications per IP address and per account, to, say, 5.

Limiting by IP can cause problems if there are lots of users [NAT’d behind a shared IP address](https://en.wikipedia.org/wiki/Network_address_translation), but unless [everything in your country is routed through a single IP](https://superuser.com/questions/1013630/why-does-qatar-use-a-single-ip-address-when-800-000-ip-addresses-are-allocated-t), it works fine in practice.
It won’t stop an attacker using a residential proxy, but we have to start somewhere.

Limiting by account does mean that an attacker can pretty easily lock someone out of their account, although I’ve never seen this happen. Maybe someone else that has experience with this can chime in.

I think that’s everything. Thanks everyone for your feedback. What do you think? What other pitfalls did I miss?