---
title: 'Hack on MDN: Building useful tools with browser compatibility data – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/
author: Jean-Yves Perrier
published: '2018-03-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

From Friday, March 16 to Sunday, March 18, 2018, thirty-four people met in Mozilla’s Paris office to work on improving [MDN’s Browser Compat Data](https://hacks.mozilla.org/2018/02/mdn-browser-compatibility-data/). The amazing results included [221 pull requests](https://github.com/mdn/browser-compat-data/pulls) that improved the quality of our data and created, prototyped, and improved tools and dashboards.

![People clustered around 3 tables working on their computers in a gorgeous 19th century Parisian ballroom.](../../assets/838bc2e86d3ae93d.jpg)


![People clustered around 3 tables working on their computers in a gorgeous 19th century Parisian ballroom.](../../assets/838bc2e86d3ae93d.jpg)

*Hack on MDN* events

Hack on MDN evolved from the [documentation sprints](https://hacks.mozilla.org/2010/10/web-standards-doc-sprint-finis/) the MDN team organized between 2010 and 2013, which brought together a core team of volunteers to write and localize MDN content over a weekend. In 2014, we expanded the scope of the sprints by inviting people with different backgrounds; not just technical writers and wordsmiths, but also people who like to code or have UX design skill.

The first two Hack on MDN events happened in [Paris in 2014](https://blog.mozilla.org/community/2014/03/19/the-best-mdn-event-so-far-mdn-community-weekend-march-2014-paris/) and [Berlin in 2015](https://blog.mozilla.org/community/2015/04/17/a-highly-productive-hack-on-mdn-weekend-in-berlin/). We took a break for a few years but missed the events and the community spirit they embody. This Hack on MDN in Paris was the first of two planned for this year (the next will take place in the autumn). For March, we decided to bring together an emerging MDN community and maximize productivity by focusing on a single theme with a broad scope: browser compatibility data.

The Hack on MDN format is a combination of unconference and hackathon; participants pitch projects and commit to working on concrete tasks (rather than meetings or long discussions) that can be completed in three days or less. People choose projects in which a group can make significant progress over a weekend.

## Browser Compatibility Data

The web platform is unique in that it aims to create a consistent experience on top of different tools, browsers or servers. You create your website once, and it works in every browser, regardless of device, OS, or tool choice.

In an ever-evolving connected world, this is incredibly hard to achieve, and browsers implement the platform at different paces and with different priorities. Even if they aim for the same goals, it’s unlikely that a new feature is implemented by all major actors at the same time. Knowing the level of support in each browser helps developers make informed decisions about which technologies are mature enough to use, and which to avoid (e.g. unstable, non-standard, or obsolete ones).

MDN has collected this kind of browser compatibility information for the last decade and we use it to improve our reference pages. Integrating this info directly into MDN pages has had its own drawbacks: it’s been difficult to maintain, and next to impossible to reuse elsewhere. A few years ago, we decided to move this information into a machine-readable format so that it can be reused.

![A BCD table containing example browser information for an unspecified "browser status"](../../assets/882ece5a28aba367.png)


![A BCD table containing example browser information for an unspecified "browser status"](../../assets/882ece5a28aba367.png)

Under [Florian Scholz](https://twitter.com/floscholz?lang=en)‘s lead, we are now [migrating browser compatibility data](https://hacks.mozilla.org/2018/02/mdn-browser-compatibility-data/) into a JSON database, and we are about 60% done (including all of HTTP, HTML, JS, and even WebExtensions). We are working hard on getting all the Web APIs in it, as well as SVG, WebDriver, and MathML information.

At the same time, we are experimenting with reusing compatibility information in new tools, some developed internally and some externally. We publish our data weekly in the form of an [npm package](https://www.npmjs.com/package/mdn-browser-compat-data) that is guaranteed to stay up-to-date as MDN itself uses it. We are our own first customer!

Our goal this year is to have 100% of the MDN compatibility info in the JSON database, as well as to start reusing this data in tools beyond our inline compatibility tables.

## The 2018 Paris event

The level of interest around browser compatibility data (BCD) and the sheer amount of work left to do on it made it a natural candidate for the theme of the March event. The BCD community on Github is active and the event provided a great opportunity for contributors to meet in person.

![Some code displayed on a giant screen of the Paris office during the MDN Paris Event](../../assets/6dea7157eb0bb71c.jpg)


![Some code displayed on a giant screen of the Paris office during the MDN Paris Event](../../assets/6dea7157eb0bb71c.jpg)

Thirty-four people from different backgrounds and organisations gathered in the splendid Mozilla Paris office: Mozilla employees (developers, writers, and even managers) from several different teams (MDN, Open Innovation, Web Compat, and WebDriver/Marionette), volunteers, and representatives from Google, Samsung, Microsoft, and the W3C (both on-site and remote).

On the first morning, Florian Scholz presented BCD and everyone introduced themselves, so people were not afraid to talk to each other during the event and got an overview of the skills available in the room. After the project pitching, people clustered into groups and the work began. It was interesting to watch people interact with others who’d either pitched an idea or had specific skills. In a quarter of an hour, everybody was already deep into hacking.

At the end of each afternoon, we gathered to demo the work that had been done. Saturday and Sunday morning we also held a set of lightning talks, where anyone could present anything, with the goal of opening our minds to other ideas.

We finished on Sunday with a final set of demos, and the outcome was truly amazing…

## Outcomes

221 PRs were made to our repository by the participants of Hack on MDN. So many projects have been worked on that it is impossible to be exhaustive, but here are a few highlights.

### Visualisation tools

Mozilla Tech Speaker and JavaScript hacker [Istvan ‘Flaki’ Szmozsanszky](https://twitter.com/slsoftworks/) created a [tool](https://flaki.github.io/browser-compat-data/compat-editor/index.html) that displays a compatibility table without the help of the server: it reads the BCD file and constructs the table directly in the browser. This is a fundamental piece of code that will allow us to easily embed compatibility tables everywhere, starting with our own pull requests on Github. Flaki went further by coding a feature to [edit the JSON in the page](https://github.com/flaki/browser-compat-data/tree/compat-tables-editor) and generate a PR from it, as well as studying how to display the differences between the current data and the new one in a visual way.

![An example output of Flaki's tool, generating a local inline BCD table.](../../assets/d0e8f4324d0fc237.png)


![An example output of Flaki's tool, generating a local inline BCD table.](https://hacks.mozilla.org/wp-content/uploads/2018/03/Screen-Shot-2018-03-28-at-11.07.31-500x235.png)

[John Whitlock](https://github.com/jwhitlock) (from MDN’s Dev team) and [Anthony Maton](https://github.com/MatonAnthony) worked on creating a bot for GitHub requests: they focused on the back-end groundwork that will allow easy code maintenance. They created a new [repository](https://github.com/mdn/browser-compat-toolkit) and [moved](https://github.com/mdn/browser-compat-data/issues/1392) the rendering code into plain JS.

[Will Bamberg](https://github.com/wbamberg), [Eduardo Bouças](https://github.com/eduardoboucas), and [Daniel Beck](https://github.com/ddbeck) worked on a new [macro displaying aggregate data](https://github.com/mdn/kumascript/pull/650) in one table, like all animation-* CSS properties.

### Data migration

The more data we have in our JSON format, the more accurate the MDN pages and tools using it will be. We had just over 60% of our original data migrated before the event and made significant progress on the remaining 40% over the weekend.

Under the lead of [Jérémie Patonnier](https://github.com/JeremiePat) from Mozilla, [Maxime Lo Re](https://github.com/solfen) and [Sebastian Zartner](https://github.com/SebastianZ) migrated most of the SVG element data, and that of their attributes during the weekend. [Chris Mills](https://github.com/chrisdavidmills), [David Ross](https://mozillians.org/en-US/u/sw1ayfe/) and **Bruno Bruet** did the same with a lot of Web APIs. The amount of data migrated is more or less equivalent to a quarter’s worth of work and is a significant step in our migration work. Well done!

[Andreas Tolfsen](https://github.com/andreastt), one of Mozilla’s [WebDriver](https://www.seleniumhq.org/docs/03_webdriver.jsp) specialists, worked, with the help of Chris Mills, to bring [basic WebDriver browser compatibility info](https://github.com/mdn/browser-compat-data/pull/1417) to our repository, as well as to start documenting [WebDriver](https://developer.mozilla.org/en-US/docs/Web/WebDriver#Reference) on MDN.

### Data quality

Our data is not perfect: we have some data errors (usually this involves features marked as not supported when they have been supported), missing data (we have a way of marking unknown data differently), and of course some real code errors.

Several projects were conducted in order to improve the quality of our dataset.

[Mark Dittmer](https://github.com/mdittmer) from Google worked to bridge the Confluence tool with MDN. He created a tool, [mdn-confluence](https://github.com/mdittmer/mdn-confluence) that allows cross-checking of the information between both repositories.

[Ada Rose Cannon](https://github.com/AdaRoseCannon) and [Peter O’Shaughnessy](https://github.com/poshaughnessy) from Samsung created a [tool](https://github.com/SamsungInternet/mdn-bcd-map-browser-data) that produces an initial set of data for [Samsung Internet](http://www.samsung.com/global/galaxy/apps/samsung-internet/), which brings this important mobile browser to our repository. What makes this dataset even more interesting is that it has been designed to be repurposed for any Chromium-based browser, so we may be able to include QQ or UC browser info in our repository one day.

[Erika Doyle](https://twitter.com/erikanavara?lang=en), [Libby McCormick](https://github.com/libbymc), and [Matt Wojciakowski](https://github.com/mattwojo) from Microsoft participated remotely from the Seattle area and worked on some Edge-related data: updated [EdgeHTML release dates](https://github.com/mdn/browser-compat-data/pull/1482) and added [Edge compat data to WebExtensions](https://github.com/mdn/browser-compat-data/pull/1486).

### Scraping tools

Several people worked on taking existing data, on MDN or elsewhere, and using it to generate BCD JSON, totally or partially. These tools are valuable time-savers and will allow us to migrate data at a quicker pace.

[Dominique Hazaël-Massieux](https://www.w3.org/People/Dom/) from the W3C worked on a [tool](https://github.com/dontcallmedom/webidl2mdnbcd) that takes a WebIDL as input and generates the skeleton of our BCD. This is extremely useful for all new APIs that we will want to document, as we only have to modify the values afterwards. Several PRs that Dominique submitted have been generated using this tool.

[Kayce Basques](https://github.com/kaycebasques) from Google created a tool, [MDN Crawler](https://github.com/kaycebasques/mdncrawler), which takes an MDN page and reads the browser compatibility data from it. Even if not all the data can be read correctly (the manually crafted tables do not always follow the same structure), it is able to extract a lot of information that can be manually tweaked afterwards. This is a big time saver for the migration. Kayce also published this tool as a [glitch.me service](https://mdncrawler.glitch.me/) (with instructions).

### External tools reusing the data

Eduardo Bouças worked on improving his add-on, [compat-report](https://addons.mozilla.org/en-US/firefox/addon/compat-report/), that produces a visual compatibility report inside Firefox Dev Tools.

![Screenshot of compat-report fromEduardo Bouças.](https://hacks.mozilla.org/wp-content/uploads/2018/03/compat-report-500x409.png)


![Screenshot of compat-report fromEduardo Bouças.](../../assets/7dfdbaafbff44f23.png)

[Julien Gattelier](https://mozillians.org/en-US/u/Sphinx-Julien/) fixed several problems with his tool, [compat-tester](https://www.npmjs.com/package/compat-tester), adding support for global HTML attributes. He also added a *contribute mode* that lists features that are not in the browser compatibility dataset, allowing a user or potential contributor to detect missing features!

[Dennis Schubert](https://github.com/denschub) from Mozilla’s Web Compat team, along with Julien Gattelier and Kayce Basques, brainstormed about a new tool reusing Julien’s compat-tester tool to produce a report about the state of web compatibility, by crawling significant websites.

### Other projects

[Kadir Topal](https://github.com/atopal) created a dashboard enabling us to visualize the quality of our data and measure improvements we are making.

![Example of output of the data quality dashboard.](../../assets/6a9ebaa1ad518ef2.png)


![Example of output of the data quality dashboard.](../../assets/6a9ebaa1ad518ef2.png)

## What’s next?

There is a lot of follow-up work to do: we need to review all the PRs and do some work to integrate new prototypes and tools into our codebase or workflow. It is a good problem to have!

Overall, we will continue to migrate our browser compat data and improve its quality: the better the data is, the better the tools using it – and MDN Web docs itself – will be.

The most important outcome of this event is human: by working together we created new bonds and the relationships between participants will hopefully continue and grow, bringing extra awesomeness into the future of MDN Web Docs and the [Browser Compatibility Data project](https://github.com/mdn/browser-compat-data).

Want to get involved? Not sure where to begin? Visit the [MDN community on Discourse](https://discourse.mozilla.org/c/mdn) to learn about what we do and how you can make MDN more awesome with your contribution.

## About Jean-Yves Perrier

Jean-Yves is a program manager in the Developer Outreach team at Mozilla. Previous he was an MDN Technical Writer specialized in Web platform technologies (HTML, CSS, APIs), and for several years the MDN Content Lead.