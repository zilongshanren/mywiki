---
title: 'A Web for Everyone: Interviews with Web Practitioners — Fyrd – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2016/09/a-web-for-everyone-interviews-with-web-practitioners-fyrd/
author: Justin Crawford
published: '2016-09-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In recent posts, we’ve explained why it’s important to [make the web work for everyone](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/). We’ve spoken with several top web developers about [how they do that](https://hacks.mozilla.org/category/a-web-for-everyone-interviews/). And in between, we’ve shown [how browser makers can advance compatibility](https://hacks.mozilla.org/2016/09/firefox-49-fixes-sites-designed-with-webkit-in-mind-and-more/) by adopting [living standards](https://compat.spec.whatwg.org/). Today we’ll show how a single individual can dramatically improve the tooling space, helping to make the web work for everyone.

In 2015, we asked MDN visitors which tools they use most when working on cross-browser compatibility issues. Three quarters of respondents mentioned **good reference materials**. 65% of respondents said they use [MDN](https://developer.mozilla.org/en-US/docs/Web) as a cross-browser compatibility reference, and 64% said they use [ caniuse.com](http://caniuse.com). No other reference sites came close.

Like MDN, caniuse.com is an open-source project with hundreds of contributors. Anyone can [fork and PR the caniuse data](https://github.com/Fyrd/caniuse) or adapt it for use in a brand new tool ([examples](https://github.com/Fyrd/caniuse/wiki/Third-party-tools)). Building new tools in this space is important and valuable: More than 25% of developers said they want to make their sites more compatible, but they don’t because they need better tools — for example, automation and linting.

Helping web developers is what motivates [Alexis Deveria](http://a.deveria.com/) (a.k.a. [@Fyrd](https://twitter.com/Fyrd)), the developer behind caniuse.com. Alexis is a web developer at Adobe by day and a champion of cross-browser compatibility by night. He took a break from reading up on the latest browser esoterica to talk with us about compatibility.

![Fyrd](../../assets/5be955494adf741e.jpg)


**What inspired you to build a website devoted to browser compatibility? Was there a specific experience that got it started? What motivates you to keep it going?**

I started the site in 2008 because around that time various web browsers started implementing a number of interesting new technologies, especially around HTML5 and CSS3. However, support was sporadic across browsers and there didn’t seem to be a central location to find cross-browser support. So I created a page that listed about 10-15 of such features. As the page slowly became more popular I started adding to it and making it more interactive until little by little it became the full-fledged browser compatibility site you see today.

My motivation to keep it going revolves around a few things, firstly its popularity: so many people visit and rely on it today that it would feel irresponsible to give up on it. It’s also my most successful and longest-running project, something I’m very proud of. Then there’s the fact that it forces me to stay up to date with web tech developments which helps with my day job and finally there’s some ad revenue which always helps.

**Caniuse includes Statcounter or Google Analytics stats to help users determine how much of their potential market can use a particular feature. Do you think most developers are basing technical decisions on a market formula like this? What percentage of feature adoption in the market do you think developers are looking for when they decide?**

Yeah, I imagine a number of developers take the usage % rate to determine whether or not they can use a feature, though I suspect it’s very much relative to the different factors involved, like what type of feature it is, how important the feature is to have, whether or not it can be polyfilled, etc. My guess would be that most developers don’t just have a specific cut-off percentage for all features, but I haven’t heard one way or the other.

**Have you heard from developers that they use Caniuse to help convince their bosses or stakeholders to take a particular technical direction?**

I’ve heard of a few of such cases, yes. Which is great of course, especially when they can start using features they’d otherwise be uncertain about using.

**What other factors do you think developers should consider — aside from the size of a feature’s potential market — when deciding whether to use a particular feature?**

Being on the lookout for partial support and buggy support is important… While in general bugs aren’t blockers, it’s always good to be aware of potential pitfalls. There are also cases where a feature may be deprecated and eventually removed from a browser, particularly for proprietary technologies and features that haven’t received much cross-browser adoption. Thankfully it’s pretty rare for that to happen, but it’s still worth looking out for.

**If you could magically make one feature of the web platform 100% compatible across browsers and devices, which would it be?**

Wow, just one? If we’re talking just in modern browsers I would go for [CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout). Layout’s been one of the biggest paint points in web development and I believe having 100% cross-browser support there would be brilliant. If I could also perform magic on older browsers it would be [Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout) for the same reasons. Thankfully in modern browsers it’s looking quite good already.

**Caniuse is an important part of a developer’s toolkit when building cross-browser compatible sites. What other tools or techniques do you think every web dev should consider incorporating to help them build compatible sites?**

Using services like [BrowserStack](https://www.browserstack.com) or [Sauce Labs](https://saucelabs.com/) is incredibly helpful in easily testing on older & mobile browsers, though they require a paid subscription. I’d also recommend becoming familiar with each browser’s own development tools. They’re all good, but it takes some time to understand how to do the same kind of debugging for each browser. Also when using a new technology make sure you do your research beyond Caniuse. Cross-browser support can still come with gotchas, so read MDN, search for blog posts on the subject, etc.

**Browser compatibility continues to be one of the biggest challenges in web development — it’s hard! Do you think it’s something a new tool could solve? What would the tool do?**

It would be cool if there was a all-rendering-engines-in-one browser where developers could easily switch between them to test their site. In particular this would be useful if it included mobile browsers and older versions… but I can’t see that being anything more than a fantasy, so tools like BrowserStack are likely the closest we’ll get to that.

More ideally, and perhaps more realistically, it would be nice if browser makers would spend more time cooperating on writing tests and ensuring reliable support for technologies so certain types of cross-browser issues wouldn’t occur in the first place.

**What would you tell a brand new developer graduating from a coding bootcamp about cross-browser compatibility?**

It can get ugly, messy and complicated. Don’t make any assumptions about what will work cross-browser until you’re familiar with it. The good news is that for many basic things cross-browser compatibility is so much better than it used to be. Together with the state of developer tools these days, there’s a lot to be thankful for.

**Tips from Alexis’s interview**

- If you see a gap in tooling, you’re probably not the only one. Consider building or contributing to tools that help advance the practice of web development and make the web better for everyone.
- Don’t assume new features work cross browser. Read about them and experiment with them before committing to use one on a public site.
- When trying to understand a new web feature, cast a wide net: Look things up on caniuse.com and MDN, and pay attention to other sources (e.g. blogs) too.

## About
[
Justin Crawford ](http://hoosteeno.com)

Justin Crawford is a product engineer at Mozilla, working on developer marketing and growth. He likes thinking about the future, building things and riding bikes.