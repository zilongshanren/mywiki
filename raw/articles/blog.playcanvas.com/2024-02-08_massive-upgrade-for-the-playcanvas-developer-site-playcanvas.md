---
title: Massive Upgrade for the PlayCanvas Developer Site | PlayCanvas Blog
url: https://blog.playcanvas.com/massive-upgrade-for-the-playcanvas-developer-site
author: Will Eastcott
published: '2024-02-08'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Today, we are excited to announce the brand new [PlayCanvas Developer Site](https://developer.playcanvas.com/) and [API Reference Manual](https://api.playcanvas.com/)!

## Developer Site[](https://blog.playcanvas.com#developer-site)

Let's start by taking a look at the new Developer Site, home of the PlayCanvas User Manual and Tutorials.

![Developer Site Landing Page](../../assets/f6033c09b012a3e6.png)


### Migrating from Metalsmith to Docusaurus[](https://blog.playcanvas.com#migrating-from-metalsmith-to-docusaurus)

Since PlayCanvas was born in 2011, the basic look of the Developer Site has changed little. The content was written in Markdown and converted to a static HTML site using a tool called [Metalsmith](https://metalsmith.io/). Customizing the site to our needs meant we had to write many Metalsmith plugins (for localization, navigation and more) and a lot of HTML and CSS to style the pages as we wanted.

13 years later, the world of static site generators has moved on with lots of exciting new options! We evaluated [Docusaurus](https://docusaurus.io/) and decided to migrate over to it.

### What's New[](https://blog.playcanvas.com#whats-new)

So what made Docusaurus so compelling? First up, the migration was going to be straightforward because, like Metalsmith, Docusaurus consumes Markdown and outputs a static site. And much of the customization we did for Metalsmith is supplied 'out-of-the-box' with Docusaurus. So that's all great. But the new site comes with lots of cool new features we known you're going to love:

#### 🔍 Powerful Search[](https://blog.playcanvas.com#-powerful-search)

The site now integrates [Algolia](https://www.algolia.com/) for advanced searching of the documentation.

![Developer Site Search](../../assets/5f9048b762fb236e.png)


This is a quantum leap over what came before. Try it (by pressing `CTRL + K`

) - you'll be amazed. 🤯

#### 🌒 Light and Dark Modes[](https://blog.playcanvas.com#-light-and-dark-modes)

Easily switch between light and dark themes (by clicking on the sun/moon icon top-right).

![Developer Site Light and Dark Modes](../../assets/7a0d92d3448783f6.png)


#### 🌏 Language Selection[](https://blog.playcanvas.com#-language-selection)

Switch language from the nav-bar. At the moment, we're shipping with Japanese translations.

![Developer Site Localization](../../assets/e30a43b419b987fa.png)


#### 👩💻 Edit on GitHub[](https://blog.playcanvas.com#-edit-on-github)

As you might expect, [the Developer Site is Open Source (MIT)](https://github.com/playcanvas/developer.playcanvas.com). Every page now has a handy link to the content on GitHub. Spot a mistake? Now can you fix it yourself and improve the docs for the community!

#### 🧭 Easier Navigation[](https://blog.playcanvas.com#-easier-navigation)

At the top of each page, you'll find 'Sidebar Breadcrumbs' which allow you to click back up the page hierarchy.

To the right of each page, you'll find a table of contents which can be a big help, especially for long pages.

And at the bottom of each page, you'll find 'Previous' and 'Next' links that allow you to read through the User Manual sequentially.

## API Reference[](https://blog.playcanvas.com#api-reference)

We are not just launching a new Developer Site today. We are also launching our brand new, upgraded [API Reference Manual](https://api.playcanvas.com/)!

![API Reference Site](../../assets/3d214fbdea1d6d8e.png)


### Migrating from JSDoc to TypeDoc[](https://blog.playcanvas.com#migrating-from-jsdoc-to-typedoc)

Since the start, we have relied on [JSDoc](https://jsdoc.app/) to generate our API reference manual. But since then, we have seen the introduction of [TypeDoc](https://typedoc.org/) which offers some major advantages over JSDoc.

#### 🎨 High Quality Default Theme[](https://blog.playcanvas.com#-high-quality-default-theme)

While it's not perfect, the default TypeDoc theme is gorgeous and a big improvement over our custom JSDoc theme. It provides:

- Light and dark modes (like the main developer site)
- Links to the source code on GitHub
- Grouping of API into related categories
- Powerful search (press
`/`

to activate it) - ...and much more!

It's a great foundation for us to begin with and we can customize the default theme to our requirements as needed.

#### 🔗 Easy Combining of APIs[](https://blog.playcanvas.com#-easy-combining-of-apis)

Did you know that PlayCanvas develops frameworks and libraries other than the PlayCanvas Engine? There's [PCUI](https://github.com/playcanvas/pcui), a front-end framework for web-based tools. There's the [PlayCanvas Editor API](https://github.com/playcanvas/editor-api) for automating the interface. And more! The new API reference collects all of the PlayCanvas APIs into a single manual.

![API Reference Site APIs](../../assets/f44a21e458d10f96.png)


## Open Source FTW[](https://blog.playcanvas.com#open-source-ftw)

Everything we are announcing today is 100% open source.

We want to empower to community to get involved and make PlayCanvas better for everybody. It's never been easier to submit your first pull request on GitHub. So why wait - get started today! ❤️