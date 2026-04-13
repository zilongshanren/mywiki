---
title: Bringing interactive examples to MDN – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/03/bringing-interactive-examples-to-mdn/
author: Will Bamberg
published: '2018-03-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*“This is scoped to be a pretty small change.”* – [me, January 2017](https://groups.google.com/d/msg/mozilla.dev.mdc/dhxwpNnlkSA/Vt7nnUFaEgAJ).

Over the last year and a bit, the [MDN Web Docs](https://developer.mozilla.org) team has been designing, building, and implementing interactive examples for our reference pages. The motivation for this was the idea that MDN should do more to help “action-oriented” users: people who like to learn by seeing and playing around with example code, rather than by reading about it.

We’ve just finished adding interactive examples for the JavaScript and CSS reference pages. This post looks back at the project to see how we got here and what we learned on the way.

## First prototypes

The project was first outlined in the [MDN product strategy](https://docs.google.com/presentation/d/1PIj-ZZ07SP-VmBQA-MsJaAPSKsN3VDC5-5HMdtVdnb0/edit#slide=id.p), published at the end of 2016. We discussed some ideas on the MDN mailing list, and developed some prototypes.

The JS editor looked like this:

The CSS editor looked like this:

We wanted the examples – especially the CSS examples – to show users the different kinds of syntax that an item could accept. In the early prototypes, we did this using autocomplete. When the user deleted the value assigned to a CSS property, we showed an autocomplete popup listing different syntax variations:

![](../../assets/63e9b4693c237b31.gif)


## First round of user testing

In March 2017 [Kadir Topal](https://twitter.com/atopal) and I attended the first round of user testing, which was run by [Mark Hurst](https://twitter.com/markhurst). We learned a great deal about user testing, about our prototypes, and about what users wanted to see. We learned that users wanted examples and appreciated them being quick to find. Users liked interactive examples, too.

But autocomplete was not successful as a way to show different syntax forms. It just wasn’t discoverable, and even people who did accidentally trigger it didn’t seem to understand what it was for.

Especially for CSS, though, we still wanted a way to show readers the different kinds of syntax that an item could accept. For the CSS pages, we already had a code block in the pages that lists syntax options, like this:

```
transform: matrix(1.0, 2.0, 3.0, 4.0, 5.0, 6.0);
transform: translate(12px, 50%);
transform: translateX(2em);
transform: translateY(3in);
transform: scale(2, 0.5);
transform: scaleX(2);
transform: scaleY(0.5);
transform: rotate(0.5turn);
transform: skew(30deg, 20deg);
```


One user interaction we saw, that we really liked, was when readers would copy lines from this code block into the editor, to see the effect. So we thought of combining this block with the editor.

In this next version, you can select a line from the block underneath, and the style is applied to the element above:

![](../../assets/2d67d9417ec8f9b8.gif)


Looking back at this prototype now, two things stand out: first, the basic interaction model that we would eventually ship was already in place. Second, although the changes we would make after this point were essentially about styling, they had a dramatic effect on the editor’s usability.

## Building a foundation

After that not much happened for a while, because our front-end developers were busy on other projects. [Stephanie Hobson](https://github.com/stephaniehobson) helped improve the editor design, but she was also engaged in a full-scale redesign of MDN’s article pages. In June [Schalk Neethling](https://github.com/schalkneethling) joined the team, dedicated to this project. He built a solid foundation for the editors and a whole new contribution workflow. This would be the basis of the final implementation.

In this implementation, interactive examples are maintained in the [interactive-examples](https://github.com/mdn/interactive-examples) GitHub repository. Once an interactive example is merged to the repo, it is built automatically as a standalone web page which is then served from the “mdn.mozilla.net” domain. To include the example in an MDN page, we then embed the interactive example’s document using an `iframe`

.

## UX work and more user testing

At the end of June, we showed the editors to [Jen Simmons](https://twitter.com/jensimmons) and [Dan Callahan](https://twitter.com/callahad), who provided us some very useful feedback. The JavaScript editor seemed pretty good, but we were still having problems with the CSS editor. At this point it looked like this:

People didn’t understand that they could edit the CSS, or even that the left-hand side consisted of a list of separate choices rather than a single block.

Stephanie and Schalk did a full UX review of both editors. We also had an independent UX review from [Julia Lopez-Mobilia](https://twitter.com/juliachirps) from [The Brigade](https://thisisthebrigade.com/). After all this work, the editors looked like this in static screenshots:

Then we had another round of user testing. This time we ran remote user tests over video, with participants recruited through MDN itself. This gave us a tight feedback loop for the editors: we could quickly make and test adjustments based on user feedback.

This time user testing was very positive, and we decided we were ready for beta.

## Beta testing

The beta test started at the end of August and lasted for two weeks. We embedded editors on three JavaScript and three CSS pages, added a survey, and asked for feedback. [Danielle Vincent](https://twitter.com/HowdyDanielle) mentioned it in the [Mozilla Developer Newsletter](https://www.mozilla.org/en-US/newsletter/developer/), which drove thousands of people to [our Discourse announcement post](https://discourse.mozilla.org/t/interactive-editors-in-beta/18548).

Feedback was overwhelmingly positive: 156/159 people who took the survey voted to see the editor on more pages, and the free-form text feedback was very encouraging. We were confident that we had a good UX.

## JavaScript examples and page load optimization

Now we had an editor but very few actual examples. We asked [Mark Boas](https://github.com/maboa) to write examples for the JavaScript reference pages, and in a couple of months he had written about 400 beautiful concise examples.

We had another problem, though: the editors regressed page load time too much. Schalk and Stephanie worked to wring every last millisecond of performance optimization out of the architecture, and finally, in December 2017, we decided to ship.

We have some extra tricks we plan to implement this year to continue improving page load performance, the fact is we’re still not happy with current performance on interactive pages.

## CSS examples

In the first three weeks of 2018, Schalk and I updated 400 JavaScript pages to [include Mark’s examples](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all), and then we turned to getting examples written for the CSS pages.

[We asked for help](https://discourse.mozilla.org/t/css-interactive-examples-help-wanted/24956), [Jen Simmons tweeted about it](https://twitter.com/jensimmons/status/960616256465403904), and three weeks later [our community had contributed more than 150 examples](https://discourse.mozilla.org/t/css-interactive-examples-help-wanted/24956/2), with over a hundred coming from a single volunteer, [mfluehr](http://github.com/mfluehr).

After that [Rachel Andrew](https://github.com/rachelandrew) and [Daniel Beck](https://github.com/ddbeck) started working with us, and they took care of the rest.

## What’s next?

Right now we’re working on implementing interactive examples for the [HTML reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference). We have just finished a round of user testing, with [encouraging results](https://discourse.mozilla.org/t/html-interactive-editor-user-testing/26368/), and hope to start writing examples soon.

As I hope this post makes clear, this project has been shaped by many people contributing a wide range of different skills. If you’d like to help out with the project, please check out the [interactive-examples repo](https://github.com/mdn/interactive-examples) and the [MDN Discourse forum](https://discourse.mozilla.org/c/mdn), where we regularly announce updates.

## About Will Bamberg

Will is a technical writer working on MDN.

## 24 comments

MarkMarch 20th, 2018 at 08:57Schalk NeethlingMarch 20th, 2018 at 09:54ChristophMarch 21st, 2018 at 00:16Will BambergMarch 21st, 2018 at 06:55Kshitij ChawlaMarch 22nd, 2018 at 08:22Will BambergMarch 22nd, 2018 at 10:08kshitij ChawlaMarch 22nd, 2018 at 08:27TimonMarch 22nd, 2018 at 08:41Will BambergMarch 22nd, 2018 at 14:57JamesMarch 22nd, 2018 at 16:47Joe ZMarch 22nd, 2018 at 07:50Will BambergMarch 22nd, 2018 at 08:24Will FastieMarch 22nd, 2018 at 08:41Will BambergMarch 22nd, 2018 at 15:01RichMarch 22nd, 2018 at 09:11MarijnMarch 22nd, 2018 at 09:57Will BambergMarch 23rd, 2018 at 06:24Russell BeattieMarch 22nd, 2018 at 12:42Will BambergMarch 23rd, 2018 at 06:16David BarthMarch 22nd, 2018 at 18:57Will BambergMarch 22nd, 2018 at 21:31David NobreMarch 23rd, 2018 at 11:08Will BambergMarch 23rd, 2018 at 11:43Jeromie KirchoffMarch 27th, 2018 at 18:42