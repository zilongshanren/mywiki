---
title: Search Engine Optimization research for localized game website
url: https://gametorrahod.com/seo-game-website/
author: Sirawat Pitaksarit
published: '2019-10-13'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

You may not be building a web-based game, but you probably want your personal **public face** for your game other than App Store/Google Play Store page.

And you can add as much cool artworks from your game as you like instead of a generic corporatey template. It can contains links to respective available stores, and probably you want to have a press kit for those generous reviewers to write an article of your game easier. A lot of possibilities on this little page.

Now, the lowest requirement for this is to go build a folder of `index.html`

, `characters.html`

, `goodies.html`

, `main.css`

, `images/`

and `misc.js`

then dump the folder to Firebase Hosting. But wait, let's think what a minimal but ideal game website should consist of, and how that leads to either SEO problems or development problem.

## Considering requirements

- More than a birthday and blood type of your game's protagonist which you could display on the site YOU WANT THE GAME TO BE FAMOUS. You hope it helps land those Google search better than store page especially with custom domain name. Therefore we need it to show up on Google's first page.
- You want to develop the site fast so you could make the game. That could be achieved with either templating engine or reusable components. It would be maintenance nightmare if you have to copy paste that navigation bar to each pages with a slight variation (e.g. highlighting the current page you are on..)
- You want a little bit of interactivity that doesn't refresh the page. For example a simple foldouts which CSS framework could, or more complex which may need web framework to efficiently update a piece of your page dynamically. (For example, a live scoreboard the same as viewable from inside the game, it could make your game interesting enough to tempt wild visitor to download the game!)
- Nowadays web frameworks like React, Vue, Angular, Svelte, and so on helps you build a website from components AND also let you build dynamic pages. So we are using one of these to address both concerns.
- Then you are faced with temptation of single page application (SPA) which these tools could build very efficiently. SPA gives an impression of "app" where everything your visitor do happen instantly. The URL even changes as they do so, but the change is not real. The page didn't refresh and still "single". The content pieces changed and the framework edit the URL. This is commonly called "routing" of the SPA. SPA also has potential to be minified or packed with Webpack or Rollup. Because we want the visitor to see our glorious game as soon as possible.
- You want the web to be content-optimized and cost optimized. You want all the images your user receive to not be larger than they need to be. You don't want to upload unused image to the server. Again, bundler like Webpack or Rollup along with web frameworks help with this greatly in its build process.
- If the site is static enough, you can serve them with more simpler service such as Netlify, Github Pages, Firebase Hosting. When you don't need your own server "running" the web and just hand the client everything as they request, you get cheaper host and faster serving potential. (easy to be duplicated across CDNs, etc.)
- I concluded that we will be doing SPA with web frameworks and bundlers (even though the web is not complex and not at all app-like) to get both developement speed of reusable components, and page good page experience, and optimized content.
- SPA usually achieve its dynamic nature with the magic of JavaScript. This turns out to be a problem with Google crawler.
[This article](https://vuejsdevelopers.com/2018/04/09/single-page-app-seo/)explain everything better that I could. - You want your game website to be localized which very likely translated to wider reach. Country like Japan where there are many gamers is not so comfortable with English language. Obviously this is a pain to do by-hand if you have to duplicate everything to all languages. A maintenance nightmare. Let's use web frameworks to help us.
- In your SPA you can make a button that dynamically change page's text, with URL router that when you came into your SPA with
`/ja/`

in the middle it automatically switch language, but will that work with SEO? Ideally you want the page content, along with`<title>`

to show up in that language in Google! Can we localize`<head>`

in our SPA app fast enough at startup for search engine to understand? See relevant articles from Google how it wants your website to be localized to efficiently index :[https://support.google.com/webmasters/answer/182192?hl=en](https://support.google.com/webmasters/answer/182192?hl=en) - You want the web to be shared on social network gloriously (correct header, description, and image with cropping at the right point) on all localizations. (If Thai people shares your game, he would want Thai content to live on his timeline more than English for example.)
[Open Graph Protocol](https://ogp.me/)that Facebook tries to push helps but this maybe an issue with SPA where Facebook may understand as only a single page. (Where you may want to share a routed URL on Facebook and have them appear differently.) Note that Facebook tries to push the standard for social sharing but Twitter is only following some of them (lol corporates), in the end we need to include`<meta>`

with`og`

for Facebook and`twitter`

for Twitter... - Note that there are some meta tags that is created specifically for apps, so a direct link to download the app appears somewhere on the net like in Google search!
- Server side rendering (SSR) maybe a solution to end it all, but still statically servable site is sooo tempting.
- Prerendering is the next solution. So almost SSR but you do it at home then upload everything. This means in your dev machine you maybe making an SPA but it ended up with individual pages, all pages with individual languages, in a correct folder structure like you tediously made everything by hand. Each with their own correct
`<head>`

section. Clicking change language now really go to a new page instead of SPA. Interactivity inside the page may remains. This sounds like**the best approach**, but could be difficult to setup. - Final conclusion : let's test the extent of SPA with localization if it works with a search engine or not before falling to prerendered solution. I hope the crawler is smart enough! Remember the first goal, WE WANT THE GAME TO BE FAMOUS.

## Requirement summary

We want to use :

- Web frameworks for component reuse.
- SPA for responsiveness, but if possible Google should index each "page" magically.
- Bundler for optimized file serving.
- No server side rendering, no pre-rendering if possible.

## Concerns

The change language button in the page is SPA-based. Normally Google could know all the language variants by `<link rel="alternate" hreflang="`

where it wire up all other same page but different languages therefore requiring them to be a completely separated file. Can the crawler even click on these SPA-localization button and index them? (Clicking on the button would also update the *lang_code*"`<link rel="alternate" hreflang="`

section, along with other *lang_code*"`<meta>`

sections.)

## The SPA router test

I have written a minimal SPA game homepage (use your imagination and imagine a complete website) using [Svelte](https://svelte.dev/). The web could go to different page, switching language preserve the current language. And when going to English (en) the router logic remove `/en/`

from the URL automatically.

![](../../assets/ac88d01edf6e3b25.gif)

As you can see the URL dynamically changes on clicking the button thanks to

, tricking you to think that you go to a different page. Also, Svelte came with [svelte-routing](https://github.com/EmilTholin/svelte-routing)`<svelte:head>`

to reactively change the `<head>`

section when the content is injected, so I tried using it to change `<meta>`

tag as well as `<link>`

and `<title>`

. This is done immediately after routing so I believe it is as fast as possible. If you use other frameworks, there should be an equivalent way of doing this.

### Google crawler

Test it with Google Search Console. (Formerly "fetch as Google")

![](../../assets/5a69042033183f1c.png)

I tried `/ja/characters`

where it would jump straight to the character page in Japanese language.

![](../../assets/3c35686180195147.png)

Looks promising! Both the content and localized `<head>`

came in the crawler without prerendering.

Do note the bug in my design on the page switching anchor at the bottom most (the `<a href`

element) they has no `ja/`

prefixed on any of them. This is because I have written the logic to remember `"ja"`

as a variable that is to be pasted in front just before linking, but not actually have them on the anchor HTML. The crawler will not able to follow to other page in the same language like this.

Using the Sharing Debugger we can confirm whether our router could be understood by Facebook or not.

![](../../assets/b2e04847a9d76b08.png)

Turns out Facebook is not as smart as Google, seeing the title is NO LANGUAGE even though Google crawler clearly shows the `<meta property="og:title"`

tag existing. **Facebook cannot run JavaScript.**

![](../../assets/a1bbb988974f043a.png)

This time we will use Cards Validator.

![](../../assets/349800a2df20d16f.png)

Same goes for Twitter, it cannot follow JavaScript deep enough for the tag for cards to be populated.

## What should I do with my SPA!?

The next "perfect" solution without going to server side rendering is prerendering... but ugh, I do like my router and SPA magic that came with it which make me finish the website really fast.

If you **really **want each separated page to share differently, richly to Facebook and Twitter then it can't be helped. But since this is **just a game website**.. it wouldn't hurt much if all the pages show up the same on Facebook and Twitter. (You may only have a few pages and users may only share the main page anyways.) At least Google could crawl stuff well. The solution in this case, is to just bake a set of `<meta>`

to the `index.html`

of our SPA that it is generic enough for all pages.

![](../../assets/44784f13e1e53c82.png)

![](../../assets/edef862fadac7372.png)

![](../../assets/52862d7079a2da8c.png)

Note that there are various types of cards on Twitter to choose from, including App Card that sounds like the appropriate type for game website.

Do note that this way ALL paths of your website will show the app on sharing with Twitter since actually you have just a single `index.html`

with a magic router. Here's what we have now, 3 buttons for routing to a different tab, 3 buttons for changing language and stay in the same tab (But the `/en/`

URL will change automatically)

![](../../assets/e6e31449090c5c44.png)

But if your game website design is literally a single front page with some interactivity on it, that it doesn't feel like a new page at all. (URL don't even change by interacting with it), then your web is by definition exactly SPA and the soution is perfect.

### SPA still falters on anchor tag

![](../../assets/9aaee8abaa301761.png)

Despite all my effort to make the language switch and page switch looked "normal" like traveling to a new page, Google still really see my page as **single **page.

Maybe the way Google look through those `<a>`

tag is **not the tag and not just how the URL changes after doing so**, but Google clicked it for real and see if a new** **page **file** is coming from a real.

Hence, our fake SPA routing did not register as pages for Google as an anchor to a new address ended up coming to the only one `index.html`

anyways, even though the visitor sees new URL.

## Server side authoring, static serving : prerendering

Whether you are React, Vue, or Svelte fan there should be some solution already waiting for you : [Next.js static exporting](https://nextjs.org/features/static-exporting), [Nuxt.js static site generation](https://nuxtjs.org/), [Sapper export](https://sapper.svelte.dev/docs#sapper_export), etc.

This way you can use the power of modern component-based web making and let them bake out your big tree of website for you. For example with Next.js and Sapper you can use folder structure as a route (which can be parameterized). This alone save so much time.

The idea is that you write a web that looks to be server side rendered, but bake them out to an individual folders and files by following all possible links. This way all the `<head>`

tag could be tailored per page or localization as well. After this your generated site could be uploaded easily to Firebase Hosting, Github Pages, etc.

![](../../assets/c4e11519ce4744b4.png)

![](../../assets/14b6c9ac15c6a426.png)

### Example

In Sapper here's how to do it so you can go `/en/`

, `/th/presskit`

, `ja/v20`

and so on. I put the regex on the folder name so you can put at most 2 letters there. The outer ones are for redirecting to `/en/`

equivalent. `_layout`

is a Sapper-thing to apply this to everything on the same level and below recursively.

![](../../assets/9c973abbdb228a69.png)

Static site export result :

![](../../assets/1be931f53d0d023d.png)

Even though I specified that I can use any 2 letters, because the static site generator is a crawler that starts from the front page, it then see my change language button that is limited to 3 languages, and from there crawl out to everything in that language. I got my 3 slightly different `presskit/index.html`

baked out effortlessly. It would be a big pain doing this by hand. Now they have statically baked `<meta>`

tags as well. Japanese user sharing the site will see more friendly Japanese texts.

### Beware of server things such as redirecting

When you generate static prerendering from what would have been server side, you may get something like this. This is an example of `/index.html`

that goes to `/en/index.html`

automatically by Sapper's routing capability.

![](../../assets/93c2a8ced4da5918.png)

Ok, so Sapper did nothing wrong as it is really translating server side real routing (returning 301 redirection code) to a fully client side compatible code.. which works when you use the browser though it looks kinda too simple.

But crawler like Facebook cannot understand it. If someone share your game website using pure url without `/en`

? See that response code is 206 and not a redirection, because the redirection is now faked. Facebook stuck here and cannot continue to the page that has the `og:image`

.

![](../../assets/9f08b5f78b33b0ee.png)

This now depends on your static site host if they have some customization options to **bring back "a little bit of server-side"** or not. Firebase hosting for example [could do it](https://firebase.google.com/docs/hosting/full-config#redirects). I heard we could put some meta HTML tags for redirects too but I trust server-based redirect more. Don't even have to download the page!

After telling Firebase to 301 properly, now anyone sharing non localized URL could go to the correct file with meta tags ready.

![](../../assets/6b8a0885e979821b.png)

In summary, if your game site is really single page then go SPA. If multiple pages then I think using web app frameworks with static baking is the best way to finish this fast.