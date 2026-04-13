---
title: Web Design Survey Findings and Next Steps – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2019/02/web-design-challenges-survey-finding/
author: Victoria Wang
published: '2019-02-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In November, I wrote about my team’s work on experimental new [web design tools](https://hacks.mozilla.org/2018/11/new-experimental-web-design-tools-feedback-requested/). We also ran a survey to rank the challenges of web design and development. A big thank you to everyone who participated in our open design process! We received over 900 responses in one month, and discovered major findings which continue to inform the Firefox DevTools’ 2019 roadmap.

## The Methods

With guidance from Mozilla’s data scientists, I chose the [MaxDiff](https://en.wikipedia.org/wiki/MaxDiff) method for the challenge-ranking portion of the survey. MaxDiff requires the survey taker to make trade-offs within subsets of the pool of options. This works well for ranking a large number of options, which would be too overwhelming for a regular card sort. It also produces a more accurate overall ranking by emphasizing relative differences in priority.

In practice, this produced 10 survey pages that each showed a set of 4 random options from a pool of 23 total web design challenges. Participants had to choose the “least“ and “most” impactful options in each set. The ranking was then determined by scores computed using the following formula:

—————————————————

# times item appeared

The second portion of the survey focused on specific frustrations with browser developer tools. For this section we only offered 7 options, so we used a simple drag-and-drop card sort.

## The Takeaways

The highest-ranked issues by far were related to *CSS layout debugging*—learning the root cause of mysteries like unwanted scrollbars and unexpected size and position. Accordingly, my highest priority right now is digging deeper into CSS debugging issues with further research and experiments. (You can help by taking my brief new [CSS Debugging follow-up survey](https://qsurvey.mozilla.com/s3/CSS-Debugging-65d9390435c7H)! More info below.)

Unsurprisingly, *cross-browser compatibility* was also a top choice. We’re investigating ways to ease the pain of debugging browser differences, including auditing, hints, and a more robust responsive design tool.

Mid-ranked issues included *Flexbox*, *Grid*, and *Accessibility*. We plan to continue improving our [Accessibility Panel](https://developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector); however, for now we’ll step back a bit from our successfully launched [Flexbox](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_Flexbox_layouts) and [Grid](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_grid_layouts) tools. Letting them breathe and collecting more real-world feedback will allow us to swing back with fresh new ideas later.

Lowest-ranked issues included *Lack of Visual/WYSIWYG Tools*, *Animations*, *WebGL*, and *SVG*. The visual tools part was surprising—we’ve seen a lot of love for click-and-drag visual tools like the beautifully designed [Visbug](https://chrome.google.com/webstore/detail/visbug/cdockenadnadldjbbgcallicgledbeoc) and [Webflow](https://webflow.com/). I suspect my old-school wording here—WYSIWYG (“what you see is what you get”)—brought to mind less-delightful experiences of the past. There are clearly ways to improve developers’ lives with modern tools in this space.

As for the browser issues card sort, we hear you loud and clear on the issue of “Moving CSS changes back to my editor.” We’re currently in the process of adding export options to our Changes panel, and would love your input on [our designs](https://twitter.com/firefoxdevtools/status/1095794448317898752?s=21)! DOM breakpoints are also in the plans for this year.

You can view the full MaxDiff and card sort rankings in [this report](https://data.surveygizmo.com/r/28049_5bfee46d691966.07620376).

## Follow-up Survey: CSS Layout Debugging

Now we need your help again! The main takeaway from the first survey was that developers and designers of every experience level want to better understand CSS issues like unexpected scrollbars and sizing. We’ve started researching and prototyping potential tool ideas for investigating specific types of CSS bugs, but we need your feedback to guide our work.

Please take a moment with our quick single-page [CSS Layout Debugging survey](https://qsurvey.mozilla.com/s3/CSS-Debugging-65d9390435c7H) and help us rank the most time-consuming bugs. Your feedback will be immensely helpful in clarifying our plans in 2019 and beyond.

Thank you!

Victoria & the Firefox DevTools team

## About
[
Victoria Wang ](https://violasong.com)

Victoria is a Portland-based UX designer at Mozilla who works on Firefox DevTools.

## 8 comments

OenononoFebruary 20th, 2019 at 19:47Victoria WangFebruary 21st, 2019 at 10:53RIPON MohammedFebruary 21st, 2019 at 09:28Jake PogorelecFebruary 21st, 2019 at 10:28Victoria WangFebruary 21st, 2019 at 10:54MattFebruary 23rd, 2019 at 01:25jopFebruary 21st, 2019 at 10:30Victoria WangFebruary 21st, 2019 at 10:55