---
title: 'Fathom: a framework for understanding web pages – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2017/04/fathom-a-framework-for-understanding-web-pages/
author: Erik Rose
published: '2017-04-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It’s time we went beyond a browser that just renders pages. On the modern web, trying to accomplish a simple task can get you buffeted by pop-overs, squinting at content crammed into a tiny column, and trying to suss out the behavior of yet another site’s custom widgets. To restore a balance of power and reclaim user efficiency, we need a smarter browser.

Imagine if Firefox understood pages like a human does:

- Arduous sign-on could be a thing of the past. The browser could recognize a Log In link, follow it in the background, and log you in, all without losing your place. The links could disappear from the page and be moved into a standard browser UI.
- Products could be recognized as such and manipulated as cohesive chunks. You could drag them to a shopping cart, complete with pictures and prices, for cross-site comparison shopping. You could enjoy easily scannable columns rather than a circus of tabs.
- Inefficient and inconsistent UI could be ironed out at last. We could have browser-provided hotkeys for dismissing popovers, navigating to the next logical page, standardizing the look of interface elements, or recognizing and flattening out needlessly paginated slideshows.
- On small screens or windows, superfluous navigation or header sections could be hidden, even on pages that don’t use responsive design. We could intelligently figure out what to print, even in the absence of print stylesheets.

These possible futures all assume the browser can identify meaningful parts of the page. Over the decades, there have been many attempts to make this easier. But microformats, semantic tags, RDF, and link/rel header elements have failed to take over the world, due both to sites’ incentive to remain unscrapeable and to the extra work they represent. As a result, modern search engines and browsers’ reader modes have taken an alternative tack: they extract meaning by embracing the mess, bulling straight through unsemantic markup with a toolbelt full of heuristics.

But a problem remains: these projects are single-purpose and expensive to produce. [Readability](https://medium.com/@readability/an-important-announcement-for-all-readability-api-users-32dbee232b29), the basis of Safari and Firefox’s reader modes, is 1,800 lines of JavaScript and was recently shut down. Chrome’s DOM Distiller is 23,000 lines of Java. These imperative approaches get bogged down in the mechanics of DOM traversal and state accumulation, obscuring the operative parts of the *“*understanders*”* and making them arduous to write and difficult to comprehend. They are further entangled with the ad hoc fuzzy scoring systems and the site-specific heuristics they need to include. The economics are against them from the start, and consequently few of them are created, especially outside large organizations.

But what if understanders were cheap to write? What if Readability could be implemented in just 4 simple rules?

```
const rules = ruleset(
rule(dom('p,div,li,code,blockquote,pre,h1,h2,h3,h4,h5,h6'),
props(scoreByLength).type('paragraphish')),
rule(type('paragraphish'),
score(fnode => (1 - linkDensity(fnode,
fnode.noteFor('paragraphish')
.inlineLength))
* 1.5)),
rule(dom('p'),
score(4.5).type('paragraphish')),
rule(type('paragraphish')
.bestCluster({splittingDistance: 3,
differentDepthCost: 6.5,
differentTagCost: 2,
sameTagCost: 0.5,
strideCost: 0}),
out('content').allThrough(domSort))
);
```


That scores within 7% of Readability’s output on a selection of its own test cases, measured by Levenshtein distance1. The framework enabling this is Fathom, and it drives the cost of writing understanders through the floor.

Fathom is a mini-language for writing semantic extractors. The sets of *rules* that make up its programs are embedded in JavaScript, so you can use it client- or server-side as privacy dictates. And Fathom handles all your bookkeeping so you can concentrate on your heuristics:

- Tree-walking goes away. Fathom is a data-flow language like Prolog, so data conveniently “turns up” when there are applicable rules that haven’t yet seen it.
- Flow control goes away. Fathom determines execution order based on dependencies, running only what it needs to answer your query and caching intermediate results.
- The temptation to write plugin systems goes away. Fathom rules are unordered, so additional ones can be added as easily as adding a new element to a JavaScript array. This makes Fathom programs (or
*rulesets*) inherently pluggable. They commingle like streams of water, having only to agree on type names, making them ripe for collaborative experimentation or special-casing without making a mess. - The need to keep parallel data structures to the DOM goes away. Fathom provides proxy DOM nodes you can scribble on, along with a black-and-white system of types and a shades-of-grey system of scores to categorize nodes and guide decisions.
- The need to come up with the optimal balance of weights for your heuristics goes away, thanks to an
[optimization harness](https://mozilla.github.io/fathom/optimization.html)based on[simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing). All those fiddly numerical constants in the code above were figured out by siccing the machine on a selection of input and correct output and walking away.

The best part is that Fathom rulesets are data. They look like JavaScript function calls, but the calls are just making annotations in a sort of syntax tree, making the whole thing easily machine-manipulable. Today, that gets us automatic tuning of score constants. Tomorrow, it could get us automatic generation of rules themselves!

Fathom is young but feisty. It’s already in production powering [Firefox’s Activity Stream](https://testpilot.firefox.com/experiments/activity-stream), where it picks out page descriptions, main images, and such. In 70 lines, it replaced a well-known commercial metadata-parsing service.

What we need now is imagination. Scoop up all those ideas you threw away because they required too much understanding by the browser. We can do that now. It’s cheap.

Have an idea? Great! Check out the [full documentation](https://mozilla.github.io/fathom/) to get started, grab the [npm package](https://www.npmjs.com/package/fathom-web), [submit patches](https://github.com/mozilla/fathom), and join us in the #fathom channel on irc.mozilla.org and on the [mailing list](https://mail.mozilla.org/listinfo/fathom) as you build. Let’s make a browser that is, in bold new ways, the user’s agent!

1The caveats of the example are quite manageable. It’s slower than Readability, because clustering is O(n2 log n). But there is also much low-hanging fruit left unpicked: we do nothing in the above to take advantage of CSS classes or semantic tags like `<article>`

, both rich sources of signal, and we don’t try to pare down the clustering candidates with thresholds. Finally, some of the 7% difference actually represents improvements over Readability’s output.

## About
[
Erik Rose ](https://www.grinchcentral.com/)

Erik chips away at the barrier between human cognition and machine execution, through projects like DXR (search & static analysis on Mozilla codebases), Fathom (semantic extraction from web pages), parsers, new languages, and a whole mess of Python libraries.

## 6 comments

Steve GlickApril 26th, 2017 at 17:05Taylor HuntApril 27th, 2017 at 11:24Gerd NeumannApril 27th, 2017 at 02:27Erik RoseApril 27th, 2017 at 05:12Gerd NeumannApril 28th, 2017 at 01:24Erik RoseApril 28th, 2017 at 10:45