---
title: privacy-related changes coming to CSS :visited – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2010/03/privacy-related-changes-coming-to-css-vistited/
author: Christopher Blizzard
published: '2010-03-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*For more information about this, have a look at David Baron’s post, the bug and the post on the security blog.*

For many years the [CSS :visited](http://www.w3.org/TR/css3-selectors/#the-link-pseudo-classes-link-and-visited) selector has been a vector for querying a user’s history. It’s not particularly dangerous by itself, but when it’s combined with `<a href="https://developer.mozilla.org/en/DOM/window.getComputedStyle">getComputedStyle()</a>`

in JavaScript it means that someone can walk through your history and figure out where you’ve been. And quickly – some tests show the [ability to test 210,000 URLs per minute](http://saizai.livejournal.com/960791.html). At that rate, it’s possible to brute force a lot of your history or at least establish your [identity through fingerprinting](http://panopticlick.eff.org). Given that browsers often keep history for a long time it can reveal quite a bit about where you’ve been on the web.

At Mozilla we’re serious about protecting people’s privacy, so we’re going to fix this problem for our users. To do so we’re making changes to how :visited works in Firefox. We’re not sure what release this will be part of yet and the fixes are still making their way through code review, but we wanted to give a heads up to people as soon as we understood how we wanted to approach fixing this.

These changes will have some impact on web sites and developers, so you should be aware of them. At a high level here’s what’s changing:

`getComputedStyle`

(and similar functions like`querySelector`

) will lie. They will always return values as if a user has never visited a site.- You will still be able to visually style visited links, but you’re severely limited in what you can use. We’re limiting the CSS properties that can be used to style visited links to
`<a href="https://developer.mozilla.org/en/CSS/color">color</a>`

,`<a href="https://developer.mozilla.org/en/CSS/background-color">background-color</a>`

,`<a href="https://developer.mozilla.org/en/CSS/border-top-color">border-*-color</a>`

, and`<a href="https://developer.mozilla.org/en/CSS/outline-color">outline-color</a>`

and the color parts of the`<a href="https://developer.mozilla.org/en/SVG/Tutorial/Fill_Stroke_and_Gradients">fill</a>`

and`<a href="https://developer.mozilla.org/en/SVG/Tutorial/Fill_Stroke_and_Gradients">stroke</a>`

properties. For any other parts of the style for visited links, the style for unvisited links is used instead. In addition, for the list of properties you can change above, you won’t be able to set[rgba()](http://www.w3.org/TR/css3-color/#rgba-color)or[hsla()](http://www.w3.org/TR/css3-color/#hsla-color)colors or`<a href="http://www.w3.org/TR/css3-color/#transparent">transparent</a>`

on them.

These are pretty obvious cases that are used widely. There are a couple of subtle changes to how selectors work as well:

- If you use a sibling selector (
[combinator](http://www.w3.org/TR/css3-selectors/#combinators)) like`:visited + span`

then the`span`

will be styled as if the link were unvisited. - If you’re using nested link elements (rare) and the element being matched is different than the link whose presence in history is being tested, then the element will be drawn as if the link were unvisited as well.

These last two are somewhat confusing, and we’ll have examples of them up in a separate post.

The impact on web developers here should be minimal, and that’s part of our intent. But there are a couple of areas that will likely require changes to sites:

- If you’re using
[background images](https://developer.mozilla.org/en/CSS/background-image)to style links and indicate if they are visited, that will no longer work. - We won’t support
[CSS Transitions](https://developer.mozilla.org/en/CSS/CSS_transitions)that related to visitedness. There isn’t that much CSS Transition content on the web, so this is unlikely to affect very many people, but it’s still worth noting as another vector we won’t support.

We’d like to hear more about how you’re using CSS :visited and what the impact will be on your site. If you see something that’s going to cause something to break, we’d like to at least get it documented. Please leave a comment here with more information so others can see it as well.

## 176 comments

DanielApril 17th, 2010 at 08:21AlexApril 21st, 2010 at 12:03NikkeApril 21st, 2010 at 21:23Shivanand SharmaApril 23rd, 2010 at 16:37Christopher BlizzardApril 23rd, 2010 at 17:20Matti Schneider-GhibaudoMay 17th, 2010 at 02:18Shaun SpillerMay 21st, 2010 at 16:57Matti Schneider-GhibaudoMay 25th, 2010 at 11:49MathieuMay 24th, 2010 at 17:21Christopher BlizzardApril 23rd, 2010 at 17:21Cyrus OmarApril 26th, 2010 at 19:28mauroMay 23rd, 2010 at 21:37LucaMay 27th, 2010 at 03:19ShadokJune 16th, 2010 at 13:31MaxJune 13th, 2010 at 20:36J.S.June 14th, 2010 at 18:53EuroJuly 7th, 2010 at 09:16Michael KozakewichJuly 7th, 2010 at 10:54Matt AmackerJuly 7th, 2010 at 13:36BastianJuly 8th, 2010 at 21:54Daniel DinnyesNovember 9th, 2010 at 08:44Jacob RaskJuly 8th, 2010 at 03:33ZhouQiJuly 8th, 2010 at 20:33JasonAugust 3rd, 2010 at 09:44ZhouQiJanuary 4th, 2011 at 18:59StephenJuly 9th, 2010 at 05:38JohnJuly 9th, 2010 at 14:04Matt AmackerJuly 9th, 2010 at 17:06Giso StallenbergAugust 8th, 2010 at 07:07Peter da SilvaDecember 2nd, 2010 at 04:23DamonDecember 13th, 2010 at 15:01Ant GrayJuly 10th, 2010 at 23:39ab lafontainJuly 16th, 2010 at 12:41Buddhism For VampiresJuly 20th, 2010 at 14:31Sebastian FerreyaJuly 21st, 2010 at 12:33White-TigerJuly 30th, 2010 at 19:15Matti Schneider-GhibaudoJuly 31st, 2010 at 15:27White-TigerAugust 1st, 2010 at 03:35Will EntrikenAugust 2nd, 2010 at 09:17Peter da SilvaDecember 2nd, 2010 at 04:33Giso StallenbergAugust 8th, 2010 at 07:04DennisDecember 11th, 2010 at 12:28FrozenKnightAugust 20th, 2010 at 12:13HenrikAugust 25th, 2010 at 16:42HenrikAugust 26th, 2010 at 07:13Sebastian FerreyaAugust 26th, 2010 at 00:56HughSeptember 4th, 2010 at 12:50John FarrenSeptember 7th, 2010 at 08:36louisSeptember 25th, 2010 at 20:19YuriKolovskySeptember 30th, 2010 at 08:32James B.October 2nd, 2010 at 12:38Will EntrikenOctober 3rd, 2010 at 08:21James B.October 3rd, 2010 at 22:21SpiderOctober 13th, 2010 at 04:14thinsoldierOctober 15th, 2010 at 08:29thinsoldierOctober 15th, 2010 at 08:32LayOctober 15th, 2010 at 05:03thinsoldierOctober 15th, 2010 at 08:25Matti Schneider-GhibaudoOctober 15th, 2010 at 08:49Daniel DinnyesNovember 9th, 2010 at 09:05YuriKolovskyNovember 10th, 2010 at 01:06Sebastian FerreyraNovember 10th, 2010 at 09:21PaulNovember 11th, 2010 at 07:11YuriKolovskyNovember 11th, 2010 at 07:57cw3theophilusNovember 12th, 2010 at 07:10AndréDecember 15th, 2010 at 01:48e.r.June 7th, 2011 at 13:50Gary HvizdakNovember 15th, 2010 at 23:07ARCNDecember 10th, 2010 at 20:59PaulDecember 12th, 2010 at 01:06rayDecember 25th, 2010 at 05:17awsdertDecember 12th, 2010 at 04:06Joe HontonDecember 13th, 2010 at 20:32awsdertDecember 22nd, 2010 at 13:32AndrewDecember 28th, 2010 at 21:56YuriKolovskyJanuary 4th, 2011 at 13:39Crystobal LionsJanuary 9th, 2011 at 13:23KafpauzoApril 20th, 2011 at 02:09Paul RougetApril 20th, 2011 at 14:55nomailMay 5th, 2011 at 02:01FLskydiverMay 8th, 2011 at 19:37sdfpokdfsjJanuary 15th, 2011 at 06:02stfuandrtfmJanuary 21st, 2011 at 14:25PeterJanuary 23rd, 2011 at 18:36Matti Schneider-GhibaudoJanuary 24th, 2011 at 05:03MJ.February 3rd, 2011 at 20:39trlklyFebruary 9th, 2011 at 04:38CycronFebruary 26th, 2011 at 15:43Frank WillwrightMarch 1st, 2011 at 14:34SteveMarch 2nd, 2011 at 02:09KafpauzoMarch 3rd, 2011 at 22:54KafpauzoMarch 4th, 2011 at 02:12JoeMarch 5th, 2011 at 15:39thMarch 5th, 2011 at 19:06HawkMarch 8th, 2011 at 14:46T.March 9th, 2011 at 16:06TarMarch 11th, 2011 at 07:35CarlMarch 11th, 2011 at 17:38GlennMarch 12th, 2011 at 10:05The Neighbourhood NerdMarch 13th, 2011 at 14:04YuriKolovskyMarch 15th, 2011 at 02:44PeterMarch 16th, 2011 at 17:47PeterMarch 16th, 2011 at 18:01MattGMarch 17th, 2011 at 11:09DuncanMarch 24th, 2011 at 01:00HemiltonApril 22nd, 2011 at 16:01OneMarch 25th, 2011 at 07:12TomMarch 31st, 2011 at 15:55marcApril 9th, 2011 at 17:05ranimiApril 12th, 2011 at 01:42GlitchMrApril 14th, 2011 at 10:34ehsanApril 29th, 2011 at 22:59Alan GresleyApril 19th, 2011 at 09:36Alan GresleyApril 19th, 2011 at 09:38Tomcat76April 23rd, 2011 at 08:18HenrikApril 30th, 2011 at 07:08HenrikApril 30th, 2011 at 07:12EricMay 8th, 2011 at 15:23benMay 14th, 2011 at 04:47marcJune 1st, 2011 at 10:01GlennJune 2nd, 2011 at 13:26evrixJune 27th, 2011 at 12:20Jason FeatheringhamJuly 2nd, 2011 at 15:47evrixJuly 3rd, 2011 at 11:45JulianJuly 3rd, 2011 at 09:33evrixJuly 5th, 2011 at 01:05evrixJuly 5th, 2011 at 01:07louisremiJuly 7th, 2011 at 05:39JulianJuly 7th, 2011 at 07:47MoonJuly 11th, 2011 at 21:40benJuly 13th, 2011 at 01:30LuisJuly 24th, 2011 at 12:35louisremiJuly 25th, 2011 at 00:47NailgunAugust 4th, 2011 at 05:42DannyAugust 7th, 2011 at 12:25cheeOctober 26th, 2012 at 09:37AxelAugust 8th, 2011 at 01:06ilPestiferoSeptember 26th, 2011 at 03:39Reason A BubbleOctober 5th, 2011 at 15:27Christopher BlizzardOctober 7th, 2011 at 07:06Christopher BlizzardOctober 7th, 2011 at 07:09MoonOctober 6th, 2011 at 20:37LilaOctober 7th, 2011 at 07:20cheeOctober 26th, 2012 at 09:30LeftEarofCornOctober 7th, 2011 at 14:33MoonOctober 7th, 2011 at 16:35Peter da SilvaOctober 8th, 2011 at 04:39MoonOctober 9th, 2011 at 04:38MoonOctober 9th, 2011 at 08:15David POctober 12th, 2011 at 16:33Bernd SchneiderNovember 8th, 2011 at 11:41roger21November 15th, 2011 at 04:54Christos GeorgiouNovember 17th, 2011 at 00:13arminNovember 24th, 2011 at 06:33Bernd SchneiderNovember 24th, 2011 at 07:24heikeDecember 19th, 2011 at 08:39popittoJanuary 23rd, 2012 at 09:02brendaMarch 25th, 2012 at 21:52EricMarch 26th, 2012 at 10:54estrellaOctober 8th, 2012 at 18:29SergueiNovember 24th, 2012 at 18:37MoonNovember 30th, 2012 at 16:03