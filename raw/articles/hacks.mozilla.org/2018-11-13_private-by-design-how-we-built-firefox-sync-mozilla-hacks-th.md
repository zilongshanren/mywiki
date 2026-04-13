---
title: 'Private by Design: How we built Firefox Sync – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2018/11/firefox-sync-privacy/
author: Tom Ritter
published: '2018-11-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## What is Firefox Sync and why would you use it

*That shopping rabbit hole you started on your laptop this morning? Pick up where you left off on your phone tonight. That dinner recipe you discovered at lunchtime? Open it on your kitchen tablet, instantly. Connect your personal devices, securely. – **Firefox Sync*

Firefox Sync lets you share your bookmarks, browsing history, passwords and other browser data between different devices, and [send tabs](https://www.mozilla.org/en-US/firefox/features/send-tabs/) from one device to another. It’s a feature that millions of our users take advantage of to streamline their lives and how they interact with the web.

But on an Internet where sharing your data with a provider is the norm, we think it’s important to highlight the privacy aspects of Firefox Sync.

Firefox Sync **by default** protects all your synced data so Mozilla can’t read it. We built Sync this way because we put user privacy first. In this post, we take a closer look at some of the technical design choices we made and why.

When building a browser and implementing a sync service, we think it’s important to look at what one might call ‘Total Cost of Ownership’. Not just what users *get* from a feature, but what they *give up* in exchange for ease of use.

We believe that by making the right choices to protect your privacy, we’ve also lowered the barrier to trying out Sync. When you sign up and choose a strong passphrase, your data is protected from both attackers and from Mozilla, so you can try out Sync without worry. Give it a shot, it’s right up there in the menu bar!

## Why Firefox Sync is safe

Encryption allows one to protect data so that it is entirely unreadable without the key used to encrypt it. The math behind encryption is strong, has been tested for decades, and every government in the world uses it to protect its most valuable secrets.

The hard part of encryption is that key. What key do you encrypt with, where does it come from, where is it stored, and how does it move between places? Lots of cloud providers claim they encrypt your data, and they do. But they also have the key! While the encryption is not meaningless, it is a small measure, and does not protect the data against the most concerning threats.

The encryption key is the essential element. The service provider must *never* receive it – even temporarily – and must *never* know it. When you sign into your Firefox Account, you enter a username and passphrase, which are sent to the server. How is it that we can claim to never know your encryption key if that’s all you ever provide us? *The difference is in how we handle your passphrase.*

A typical login flow for an internet service is to send your username and passphrase up to the server, where they hash it, compare it to a stored hash, and if correct, the server sends you your data. ([Hashing](https://www.wired.com/2016/06/hacker-lexicon-password-hashing/) refers to the activity of converting passwords into unreadable strings of characters impossible to revert.)

The crux of the difference in how we designed Firefox Accounts, and Firefox Sync (our underlying syncing service), is that you never send us your passphrase. We transform your passphrase *on your computer* into two different, unrelated values. With one value, you cannot derive the other 0. We send an authentication token, derived from your passphrase, to the server as the password-equivalent. And the encryption key derived from your passphrase never leaves your computer.

Interested in the technical details? We use 1000 rounds of PBKDF2 to derive your passphrase into the authentication token 1. On the server, we additionally hash this token with

[scrypt](https://en.wikipedia.org/wiki/Scrypt)(parameters N=65536, r=8, p=1)

to make sure our database of authentication tokens is even more difficult to crack.

[2](https://hacks.mozilla.org#foot-2)We derive your passphrase into an encryption key using the same 1000 rounds of PBKDF2. It is domain-separated from your authentication token by using [HKDF](https://tools.ietf.org/html/rfc5869) with separate info values. We use this key to unwrap an encryption key (which you generated during setup and which we never see unwrapped), and *that* encryption key is used to protect your data. We use the key to encrypt your data using AES-256 in CBC mode, protected with an HMAC 3.

This cryptographic design is solid – but the constants need to be updated. One thousand rounds of PBKDF can be improved, and we intend to do so in the future ([Bug 1320222](https://bugzilla.mozilla.org/show_bug.cgi?id=1320222)). This token is only ever sent over a HTTPS connection (with preloaded HPKP pins) and is not stored, so when we initially developed this and needed to support low-power, low-resources devices, a trade-off was made. AES-CBC + HMAC is acceptable – it would be nice to upgrade this to an authenticated mode sometime in the future.

## Other approaches

This isn’t the only approach to building a browser sync feature. There are at least three other options:

### Option 1: Share your data with the browser maker

In this approach, the browser maker is able to read your data, and use it to provide services to you. For example, when you sync your browser history in Chrome it will automatically go into your [Web & App Activity](https://myactivity.google.com/) unless you’ve changed the default settings. As Google Chrome Help explains, “Your activity may be used to personalize your experience on other Google products, like Search or ads. For example, you may see a news story recommended in your feed based on your Chrome history.”[4](https://hacks.mozilla.org#foot-4)

### Option 2: Use a separate password for sign-in and encryption

We developed Firefox Sync to be as easy to use as possible, so we designed it from the ground up to derive an authentication token and an encryption key – and we never see the passphrase *or* the encryption key. One cannot safely derive an encryption key from a passphrase if the passphrase is sent to the server.

One could, however, add a second passphrase that is never sent to the server, and encrypt the data using that. Chrome provides this as a non-default option 5. You can sign in to sync with your Google Account credentials; but you choose a separate passphrase to encrypt your data. It’s imperative you choose a separate passphrase though.

All-in-all, we don’t care for the design that requires a second passphrase. This approach is confusing to users. It’s very easy to choose the same (or similar) passphrase and negate the security of the design. It’s hard to determine which is more confusing: to require a second passphrase or to make it optional! Making it optional means it will be used very rarely. We don’t believe users should have to opt-in to privacy.

### Option 3: Manual key synchronization

The key (pun intended) to auditing a cryptographic design is to ask about the key: *“Where does it come from? Where does it go?”* With the Firefox Sync design, you enter a passphrase of your choosing and it is used to derive an encryption key that never leaves your computer.

Another option for Sync is to remove user choice, and provide a passphrase *for* you (that never leaves your computer). This passphrase would be secure and unguessable – which is an advantage, but it would be near-impossible to remember – which is a disadvantage.

When you want to add a new device to sync to, you’d need your existing device nearby in order to manually read and type the passphrase into the new device. (You could also scan a QR code if your new device has a camera).

### Other Browsers

Overall, Sync works the way it does because we feel it’s the best design choice. Options 1 and 2 don’t provide thorough user privacy protections by default. Option 3 results in lower user adoption and thus reduces the number of people we can help (more on this below).

As noted above, Chrome implements Option 1 by default, which means *unless you change the settings before you enable sync*, Google will see all of your browsing history and other data, and use it to market services to you. Chrome also implements Option 2 as an opt-in feature.

Opera ~~and Vivaldi~~ follow Chrome’s lead, implementing Option 1 by default and Option 2 as an opt-in feature. **Update:** Vivaldi actually prompts you for a separate password by default (Option 2), and allows you to opt-out and use your login password (Option 1).

Brave, also a privacy-focused browser, has implemented Option 3. And, in fact, Firefox *also* implemented a form of Option 3 in its original Sync Protocol, but we changed our design in April 2014 (Firefox 29) in response to user feedback 6. For example, our original design (and Brave’s current design) makes it much harder to regain access to your data if you lose your device or it gets stolen. Passwords or passphrases make that experience substantially easier for the average user, and significantly increased Sync adoption by users.

Brave’s sync protocol has some interesting wrinkles 7. One distinct minus is that you can’t change your passphrase, if it were to be stolen by malware. Another interesting wrinkle is that Brave does not keep track of how many or what types of devices you have. This is a nuanced security trade-off: having less information about the user is always desirable… The downside is that Brave can’t allow you to detect when a new device begins receiving your sync data or allow you to deauthorize it. We respect Brave’s decision. In Firefox, however, we have chosen to provide this additional security feature for users (at the cost of knowing more about their devices).

## Conclusion

We designed Firefox Sync to protect your data – by default – so Mozilla can’t read it. We built it this way – despite trade-offs that make development and offering features more difficult – because we put user privacy first. At Mozilla, this priority is a core part of [our mission](https://www.mozilla.org/en-US/mission/) to “ensure the Internet is a global public resource… where individuals can shape their own experience and are empowered, safe and independent.”

0 It is possible to use one to *guess* the other, but only if you choose a weak password. [⬑](https://hacks.mozilla.org#back-foot-0)

1 You can find more details in the [full protocol specification](https://github.com/mozilla/fxa-auth-server/wiki/onepw-protocol) or by following the code [starting at this point](https://github.com/mozilla/fxa-js-client/blob/1d92f0ec458aceb56ef1619b5365ad8621183a1d/client/lib/credentials.js#L53). There are a few details we have omitted to simplify this blog post, including the difference between kA and kB keys, and application-specific subkeys. [⬑](https://hacks.mozilla.org#back-foot-1)

2 Server hashing code is [located here](https://github.com/mozilla/fxa-auth-server/blob/c28f227dc089eaf949494e8c3f810e31d9789dfa/lib/crypto/password.js#L20). [⬑](https://hacks.mozilla.org#back-foot-2)

3 The encryption code can be seen [here](https://searchfox.org/mozilla-central/rev/65f9687eb192f8317b4e02b0b791932eff6237cc/services/sync/modules/record.js#145). [⬑](https://hacks.mozilla.org#back-foot-3)

4 [https://support.google.com/chrome/answer/165139](https://support.google.com/chrome/answer/165139) Section “Use your Chrome history to personalize Google” [⬑](https://hacks.mozilla.org#back-foot-4)

5 Chrome 71 says “For added security, Google Chrome will encrypt your data” and describes these two options as “Encrypt synced passwords with your Google username and password” and “Encrypt synced data with your own [sync passphrase](https://support.google.com/chrome/?p=settings_encryption)”. Despite this wording, only the sync passphrase option protects your data from Google. [⬑](https://hacks.mozilla.org#back-foot-5)

6 One of the original engineers of Sync has written [two](https://blog.mozilla.org/warner/2014/04/02/pairing-problems/) [blog posts](https://blog.mozilla.org/warner/2014/05/23/the-new-sync-protocol/) about the transition to the new sync protocol, and why we did it. If you’re interested in the usability aspects of cryptography, we highly recommend you read them to see what we learned. [⬑](https://hacks.mozilla.org#back-foot-6)

7 You can read more about Brave sync [on Brave’s Design page](https://github.com/brave/sync/wiki/Design). [⬑](https://hacks.mozilla.org#back-foot-7)

## 36 comments

TedNovember 13th, 2018 at 11:06Tom RitterNovember 13th, 2018 at 11:55RaphaelNovember 13th, 2018 at 13:17Tom RitterNovember 14th, 2018 at 10:49johnyNovember 27th, 2018 at 00:57TGNovember 13th, 2018 at 20:38Qio XuanNovember 13th, 2018 at 20:42Luis AshureiNovember 13th, 2018 at 22:29Tom RitterNovember 14th, 2018 at 10:47BrunoNovember 14th, 2018 at 00:42Krishna MohanNovember 14th, 2018 at 00:53Tom RitterNovember 14th, 2018 at 10:46Yuri NamekovskiNovember 14th, 2018 at 01:16alloNovember 14th, 2018 at 04:23Tom RitterNovember 14th, 2018 at 11:04alloNovember 14th, 2018 at 14:24DanielNovember 14th, 2018 at 06:17void@klankschap.nlNovember 14th, 2018 at 07:15Brian DoyleNovember 14th, 2018 at 07:32Tom RitterNovember 14th, 2018 at 10:45Brian DoyleNovember 14th, 2018 at 12:29Tom RitterNovember 14th, 2018 at 12:39Mark TNovember 14th, 2018 at 09:36Tom RitterNovember 14th, 2018 at 10:42kzNovember 14th, 2018 at 13:57enthusiastNovember 14th, 2018 at 15:06AmdNovember 14th, 2018 at 19:52MikeNovember 15th, 2018 at 12:29ChrisNovember 15th, 2018 at 12:38ShujNovember 15th, 2018 at 18:52ClemensNovember 16th, 2018 at 16:52wolfiedkNovember 17th, 2018 at 12:33Igor BukanovNovember 19th, 2018 at 06:56ｔｃNovember 29th, 2018 at 06:38fredDecember 2nd, 2018 at 03:02Stephan PorzDecember 4th, 2018 at 01:43