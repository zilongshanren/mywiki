---
title: fxosstub – a minimalist's working example of the design guide rules for Firefox
  OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/12/fxosstub-a-minimalists-working-example-of-the-design-guide-rules-for-firefox-os/
author: Pierre Richard
published: '2012-12-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This post is written by Pierre Richard, Principal, Jaxo, Inc.*

I know, by experience and practice, the importance of the first hours—or even the first minutes—spent discovering and learning new concepts. During this period, developers take their go/no-go decision, mostly based on the apparent complexity of what they see.

Once you gain expertise in a given domain, you have tendencies to forget the obvious, the basics, which is where the new developers (“newbies”) need the most help. Experts are focusing on topics largely irrelevant to newbies wanting to get the essentials.

A Getting Started guide should never be written by an expert—it’s too late because they forgot what it’s was like to be a newbie.

This document and [fxosstub](https://github.com/Jaxo/fxosstub) were written by a Firefox OS newbie.

git clone https://github.com/Jaxo/fxosstub

![image](../../assets/4021a948b07b1f55.png)


## My 2-week Firefox OS Trip

I started from scratch studying Firefox OS about 2 weeks ago. The first minutes were frustrating, but my Jaxo, Inc., co-founder, Joe Latone, had me motivated. Having faced and understood many innovations in the past, I was confident. I knew that, in a few days or more, I would be able to overcome these difficulties, i.e., “developer ego.”

I enjoy and respect the Mozilla community. I thought that I could give my 2 pence to the Firefox OS community, while learning about their new work. So, I decided to gain profit of my inexperience in playing the Janus figure, keeping one of my faces as the newbie as long as I could, and then switching to the veteran face when needed. This is where the Firefox OS “Hello, World” sample, fxosstub, derives.

It is intended for people with minimum knowledge. You only need to know the following:

- Basic EcmaScript, HTML, and CSS versus HTML5, CSS3, JS Objects, JQuery, requireJS, Node, Volo, etc.
[fxosstub](https://github.com/Jaxo/fxosstub)*versus*[mortar_app_stub](https://github.com/mozilla/mortar-app-stub)

### My First Hour with Firefox OS

Here are some remarks I conscientiously jotted from the very first minutes I discovered Firefox OS:

#### Newbie notes:

- A fxos application is a big blue Install button.
*I was wrong, of course*. - What’s the role of this Install button?
*I was afraid to press it*. - Use the force and read the code!
*Do I need to learn requireJS? Why the strange syntax/look of these functions?*- Whats is B2G?
*Alas,*.[R2D2B2G](https://github.com/mozilla/r2d2b2g)doesn’t work, but that was mid-November, and now it does – it has now evolved into the[Firefox OS Simulator](https://hacks.mozilla.org/2012/11/announcing-the-prototype-firefox-os-simulator/) - This seemingly random directory structure is frustrating.
*What’s www? tool?*

→*3 out of 4 newbies may give up at this point*. - Ask Google! Search for GaiaChrono, MozillaBall.
*Ah, that’s better*.

#### Veteran notes:

- I have to simplify all of this, and reduce a “Hello, World” to the minimum.
- Examples are buried in ~/.mozilla/firefox/lkz6bqgi.default/extensions/r2d2b2g@mozilla.org/profile and in there is a r2d2-installed application, zipped.
*Ah ha! So, that’s the way they do install, but there was a mistake in the launch-path*. - Should I install BootToGecko? OK, let’s do it. It smells like Android. Lucid, Precise, 32, 64?
`adb-get install`

? Use[Nightly](http://nightly.mozilla.org/)?*I wasted 1 day on this and so will finish later this +6-hours long build, if it is really necessary*.

### The Next Day

I had written several apps on Google App Engine (GAE) and these should be good candidates to use to build an application for Firefox OS because they’re HTML5, they’re RESTful (through XMLHttpRequest, not JQuery), and they interface with Google APIs.

One of my GAE applications, Genetick, I decided to “install” on Firefox OS. How?

- Create a
`manifest.webapp`

in the war directory, but it needs fixes:- If I forget the icons, I get a cryptic message.
- I have to remove the launch-path, and get rid of the cache line as well.

- Seize this opportunity to make the “install” code self-contained:
- A standard Install JS Object, private.
- A
`setInstallButton`

JS method, exported.


#### It works quite well!

Now, a newbie can start with the following test:

- Navigate your Firefox OS Simulator (former r2d2b2g) to
[http://8.jaxo-genetick.appspot.com](http://8.jaxo-genetick.appspot.com)and press the install button. - Do the same on a Firefox OS device.

In my opinion, this makes it much more obvious to the newbie how Firefox OS deals with mobiles, and raises their enthusiasm!

- “Wow, my pre-existing application looks a true mobile one!”
- “Yes, the veteran says, that is what FxOS-Mobile is about—later you might be able to make it stand-alone, with no need for an Internet connection.”
*Note that I couldn’t show it on FxOS-Desktop, problems on Ubuntu 12.04, no dashboard*.- “But it doesn’t have the proper look and feel, the newbie argues, can I fix it?”
*Newbies love new-look designs, that makes them feel they gain the knowledge and ownership of the application*.

Googling again, this newbie finds the [Warsaw 2012 Mozilla Camp](https://blog.mozilla.org/ux/2012/09/mozcamp-warsaw-design-principles-behind-firefox-os-ux/), as well as some other gems, [patterns](https://marketplace.firefox.com/developers/docs/patterns) and [custom elements](https://marketplace.firefox.com/developers/docs/custom_elements), and gets frustrated again:

Where are all those icons the Camp advertised about? No place to go. The icons I dug up from the samples are of different sizes (30, 32, 40), different naming schemes, etc. Sigh!


The CSS3’s scripts are obscure. It seems that the styler added rules over a set of defined rules, some of them new just for nullifying previous ones—using role, type, id, classes—increasing the preferences or, worse, exploiting the order of rules as it happens to be implemented.

On the HTML side, there is no clear pattern giving life to the design concept, i.e., between nav, section, and menu. What HTML5 tag should I use?!

### The Next Days…

The veteran decided to provide the newbie with a working example of the design guide rules. No much to say, except that it was a tedious work to:

- Select the best icons from the samples;
- Use GIMP to resize them properly;
- Simplify the CSS rules (remove the useless ones, check several combinations of buttons);
- Make sure the fonts and color pan-tones obey the
[Firefox Identity](http://www.mozilla.org/en-US/styleguide/identity/firefox/color/)rules.

It began with the twittershare application, because it wasn’t the worst application regarding its look’ n feel (and structure, although it could have been better at terminology). It also was the one closer to a vanilla application, from a newbie point of view.

It ended 2 days later with ffoxstub, consisting of:

- A simple
**index.html** - A
**style**directory with its CSS and standard iconic images - A
**js**directory containing**install.js.**

Then, as a newbie, I was able to adapt my GAE application—mentioned earlier—in the context of a Firefox OS mobile device. This step took 3 hours, starting from the stub. Now, a newbie can start to get more involved with Firefox OS and the community, trust the approaches, feel the power. Soon, the newbie will be an expert.

## So, what is fxosstub?

The most simplistic, minimalist pattern to get the most newbies started building an application for Firefox OS on mobile, and it must stay as such: no rings, no bells. The Ariadne’s string through the Labyrinth, just enough to wake up the enthusiasm of legions of developers. Those, one day or another, will evolve to the wonderful world of requireJS, Volo, and the rest, but not at the start. Target the widest audience first.

[fxosstub](https://github.com/Jaxo/fxosstub) does absolutely nothing, except to show a screen suitable for obtaining the familiar layout of a mobile application aujus Firefox: a top header—with an install button, a body section, a bottom toolbar—with normalized icons. In the body section, there is a text area—launching the virtual keyboard—and a progress bar. All of this is supposed to self-adapt to an adequate size, keeping the text readable, the buttons finger-reachable.

fxosstub fills the gap between:

- What you are used to for building a regular web-page on a laptop/desktop display
- What is required on mobile with touch screens of reduced size.

## About Pierre Richard

As principal and co-founder of Jaxo, Inc., Pierre G. Richard has over 25 years of software engineering and product development experience, having shipped products for IBM and start-ups, generating $10M's in software sales. Pierre is one of the world's leading experts in algorithms and imaging techniques for information processing in barcodes (QR Codes, Data Matrix) and markup languages (XML, XSL), having authored the industry's best software in these areas. He has extensive experience on today's mobile platforms such as Android and iOS. His most recent interests are in descriptive techniques (HTML5, CSS3) and interpreters (JavaScript) in order to unify the programming of applications on all systems and devices, for example, Firefox OS. Pierre is a graduate of the French "Grande Ecole" Ecole Supérieure d'Electricité, spent several years as Research Staff Member at the IBM Watson Research Center. He has held executive positions as Chief Scientist and VP technology at several high-tech start-ups.

## 12 comments

ADecember 10th, 2012 at 07:32Pierre RichardDecember 10th, 2012 at 23:43uokesitaDecember 10th, 2012 at 19:02Pierre RichardDecember 11th, 2012 at 00:01julienDecember 11th, 2012 at 06:32Variya Soft SolutionsDecember 13th, 2012 at 09:29Robert NymanDecember 13th, 2012 at 12:48Variya Soft SolutionsDecember 15th, 2012 at 01:19NoitidartDecember 13th, 2012 at 13:21Robert NymanDecember 14th, 2012 at 00:39Variya Soft SolutionsDecember 17th, 2012 at 09:39Robert NymanDecember 18th, 2012 at 01:45