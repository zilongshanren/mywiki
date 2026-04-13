---
title: 'Hack on MDN: Better accessibility for MDN Web Docs – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2018/10/hack-on-mdn-better-accessibility-for-mdn-web-docs/
author: Janet Swisher
published: '2018-10-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

From Saturday, September 22 to Monday, September 24, more than twenty people met in London to work on improving accessibility on [MDN Web Docs](https://developer.mozilla.org/en-US/) — both the content about accessibility and the accessibility of the site itself. While much remains to be done, the result was a considerable refresh in both respects.

## Hack on MDN events

*Hack on MDN* events evolved from the [documentation sprints](https://hacks.mozilla.org/?s=%22doc+sprint%22) for MDN that were held from 2010 to 2013, which brought together staff members and volunteers to write and localize content on MDN over a weekend. As implied by the name, “Hack on MDN” events expand the range of participants to include those with programming and design skills. In its current incarnation, each Hack on MDN event has a thematic focus. One in March of this year focused on [browser compatibility data](https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/).

The Hack on MDN format is a combination of hackathon and unconference; participants pitch projects and commit to working on concrete tasks (rather than meetings or long discussions) that can be completed in three days or less. People self-organize to work on projects in which a group can make significant progress over a long weekend. Lightning talks provide an unconference break from projects.

## Accessibility on MDN Web Docs

Making websites accessible to a wide range of users, including those with physical or cognitive limitations, is a vital topic for creators on the web. Yet information about accessibility on MDN Web Docs was sparse and often outdated. Similarly, the accessibility of the site had eroded over time. Therefore, accessibility was chosen as the theme for the September 2018 Hack on MDN.

## Hack on MDN Accessibility in London

The people who gathered at [Campus London](https://www.campus.co/london/en/) (thanks to Google for the space), included writers, developers, and accessibility experts, from within and outside of Mozilla. After a round of introductions, there was a “pitch” session presenting ideas of projects to work on. Participants rearranged themselves into project groups, and the hacking began. [Adrian Roselli](https://twitter.com/aardrian) gave a brief crash course on accessibility for non-experts in the room, which he fortunately had up his sleeve and was able to present while jet-lagged.

At the end of each morning and afternoon, we did a status check-in to see how work was progressing. On Sunday and Monday, there were also lightning talks, where anyone could present anything that they wanted to share. Late Sunday afternoon, some of us took some time out to explore some of the offerings of the [Shoreditch Design Triangle](https://www.shoreditchdesigntriangle.com/), including playing with a “font” comprised of (more or less sit-able) chairs.

![Glenda Sims, Estelle Weyl, Janet Swisher and Adrian Roselli pose with metal letter-shaped chairs spelling "HACK" and "MdN"](../../assets/f4592a6e9550aad3.jpg)


![Glenda Sims, Estelle Weyl, Janet Swisher and Adrian Roselli pose with metal letter-shaped chairs spelling "HACK" and "MdN"](../../assets/f4592a6e9550aad3.jpg)

Glenda Sims, Estelle Weyl, Janet Swisher and Adrian Roselli pose with metal letter-shaped chairs spelling “HACK” and “MdN”. Photo by Dan Rubin.

## Outcomes

One project focused on updating the [WAI-ARIA documentation](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles) on MDN Web Docs, using a new [ARIA reference page template](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Structures/Page_types/ARIA_Page_Template) created by [Estelle Weyl](https://twitter.com/estellevw). [Eric Bailey](https://twitter.com/ericwbailey), [Eric Eggert](https://twitter.com/yatil), and several others completed documentation on 27 ARIA roles, including recommending appropriate semantic HTML elements to use in preference to an ARIA role. The team even had remote contributors, with [Shane Hudson](https://twitter.com/shanehudson) writing about the [ARIA alert role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/Alert_Role).

A number of participants worked on adding sections on “Accessibility concerns” to relevant HTML, CSS, and JavaScript pages, such as the [ <canvas>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas#Accessibility_concerns) element,

[property, and the](https://developer.mozilla.org/en-US/docs/Web/CSS/display#Accessibility_concerns)

`display`

[Animation API](https://developer.mozilla.org/en-US/docs/Web/CSS/display#Accessibility_concerns).

Other efforts included:

[Glenda Sims](https://twitter.com/goodwitch)updated the articles about the[Web Content Accessibility Guidelines](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Understanding_WCAG)(WCAG) for version 2.1 of that standard, and updated the tutorial on[What is accessibility?](https://developer.mozilla.org/en-US/docs/Learn/Accessibility/What_is_accessibility).[Eva Ferreira](https://twitter.com/evaferreira92)wrote an article on[using media queries for accessibility](https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries/Using_Media_Queries_for_Accessibility), and translated a number of accessibility-related articles into Spanish.- Adrian Roselli
[prototyped alternatives](https://codepen.io/aardrian/pen/WgWMvv)to MDN’s use of the[title attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/title), which is[well-known to be problematic](https://developer.paciellogroup.com/blog/2012/01/html5-accessibility-chops-title-attribute-use-and-abuse/)for accessibility. [Hidde de Vries](https://twitter.com/hdv)completely rewrote and updated the article on[accessibility information for UI designers and developers](https://developer.mozilla.org/en-US/docs/Mozilla/Accessibility/Accessibility_information_for_UI_designers), and opened a[pull request to add accessible text to social icons](https://github.com/mozilla/kuma/pull/5000)on MDN.[Bruce Lawson](https://twitter.com/brucel)reviewed, updated, and consolidated several general articles about accessibility, including the[ARIA landing page](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA),[keyboard-navigable JavaScript widgets](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Keyboard-navigable_JavaScript_widgets), and an[overview of accessible web applications and widgets](https://developer.mozilla.org/en-US/docs/Web/Accessibility/An_overview_of_accessible_web_applications_and_widgets).[Marco Zehe](https://twitter.com/MarcoInEnglish)blogged about[reasons not to use ARIA menus](https://www.marcozehe.de/2018/09/22/wai-aria-menus-and-why-you-should-generally-avoid-using-them/).[Stephanie Hobson](https://twitter.com/stephaniehobson)submitted[several pull requests](https://github.com/mozilla/kuma/commits?author=stephaniehobson&since=2018-09-01T05:00:00Z&until=2018-10-01T05:00:00Z)to improve the usability of the MDN Web Docs site for users of screen readers, such as moving the link to each section heading after the heading text, and moving the close button for menus to the top of the menu.[Josh Mize](https://twitter.com/jgmize)opened a[pull request to increase contrast](https://github.com/mozilla/kuma/pull/4983)for blue and link-color to meet WCAG AA guidelines.[Jean-Yves Perrier](https://twitter.com/Teoli2003)prototyped a schema for compatibility data regarding browser and screen reader combinations.

Also, a fun time was had and the group enjoyed working together. Check the [#HackOnMDN](https://twitter.com/search?q=%23HackOnMDN&src=typd) tag on Twitter for photos, “overheard” quotes, nail art by [@ninjanails](https://twitter.com/ninjanails) and more. Also see blog posts by [Adrian Roselli](http://adrianroselli.com/2018/09/hack-on-mdn.html) and [Hidde de Vries](https://hiddedevries.nl/en/blog/2018-09-25-hackonmdn) for their perspectives and more details.

## What’s next?

There is plenty of work left to make MDN’s accessibility content up-to-date and useful. The list of [ARIA roles, states, and properties](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Techniques) is far from complete. More reference pages need “accessibility concerns” information added. The accessibility of the MDN Web Docs site still can be improved. As a result of the enthusiasm from this event, discussions are starting about doing a mini-hack in connection with an upcoming accessibility conference.

If you find issues that need to be addressed, please file a bug against the [site](https://bugzilla.mozilla.org/enter_bug.cgi?product=developer.mozilla.org) or the [content](https://bugzilla.mozilla.org/enter_bug.cgi?product=Developer%20Documentation). Better yet, [get involved](https://developer.mozilla.org/en-US/docs/MDN/Getting_started) in improving MDN Web Docs. If you’re not sure where to begin, visit the [MDN community forum](https://discourse.mozilla.org/c/mdn) to ask any questions you might have about how to make MDN more awesome (and accessible). We’d love to have your help!

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.

## 3 comments

NageswararaoOctober 7th, 2018 at 04:48Vitaly ZdanevichOctober 19th, 2018 at 15:23Janet SwisherOctober 19th, 2018 at 16:06