---
title: Writing a React Table of Contents Component
url: https://blog.eyas.sh/2022/03/react-toc/
author: Eyas Sharaiha
published: '2022-03-11'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Last year, I wrote about
[migrating this blog to Next.js](https://blog.eyas.sh/2021/08/gatsby-to-next-js/). It ended up being
a huge post, so I wrote a `<TOC>`

React component to make it more navigable. You
can also see the TOC in action on this page:

The bulk of the logic for this component is based on
[Emma Goto](https://www.emgoto.com/)’s great examples in her
”[How to build a table of contents in React](https://www.emgoto.com/react-table-of-contents/)”,
with a few improvements worth discussing. If you haven’t yet, go read that post!
Emma does a great job showing both the final working solution and explaining the
thinking behind it step-by-step.

In this post, I’ll give a brief tour of the few “interesting” areas I iterated on top of Emma’s work.

## Computing Heading Structure

In my TOC component, we compute the heading structure dynamically at runtime
based on the structure of the emitted HTML. While some tools can give you a
nested representation of your headings for free 1, I decided against that.

### Stacks and Sentinels for Fun and Profit

Emma’s example used a `getNestedHeadings`

function that took a `HTMLElement`

array of `<h2>`

and `<h3>`

headings and returned a nested array representing the
structure. The function decided this nesting manually, which is easy enough if
you have content that isn’t highly nested. But I wanted my blog to support
nesting much deeper than that *when needed*, so I ended up writing something a
bit different:

```
interface HEntry {
text: string;
id: string;
level: number;
items?: HEntry[];
}
function getNestedHeadings(headings: readonly HTMLHeadingElement[]): HEntry[] {
const sentinel: HEntry = { text: "", id: "", level: 0 };
const traversalStack: HEntry[] = [sentinel];
for (const h of headings) {
const hLevel = level(h);
for (
let last = traversalStack[traversalStack.length - 1];
hLevel <= last.level;
traversalStack.pop(),
last = traversalStack[traversalStack.length - 1]
) {}
const last = traversalStack[traversalStack.length - 1];
last.items = last.items || [];
last.items.push({
text: h.textContent || "",
id: h.id,
level: hLevel,
});
traversalStack.push(last.items[last.items.length - 1]);
}
return sentinel.items || [];
}
function level(e: HTMLHeadingElement): number {
return parseInt(e.tagName[1]);
}
```


This code loops through each heading while also maintaining a stack representing
how deep we are in the heading tree. We use `parseInt(e.tagName[1])`

to get a
numeric representation of the heading level. The goal is to slot deeper headings
in the *item* array of the shallower headings.

The `traversalStack`

represents the path of headings from the root to the
current heading. At the start of each loop, we pop every entry from the stack
deeper than the current heading:

```
const hLevel = level(h);
for (
let last = traversalStack[traversalStack.length - 1];
hLevel <= last.level;
traversalStack.pop(), last = traversalStack[traversalStack.length - 1]
) {}
```


For fun, I do this in a small nested loop that removes the last element from the
`traversalStack`

until we have an element where `hLevel > last.level`

(i.e.,
when the current heading is deeper than the top of the stack). When we reach
that point, the top of the stack becomes the current heading’s parent.

Next, we can easily add the current heading to the parent:

```
const last = traversalStack[traversalStack.length - 1];
last.items = last.items || [];
last.items.push({
text: h.textContent || "",
id: h.id,
level: hLevel,
});
```


Here, I choose to instantiate each entry without an `items`

array and only set
it if an entry has 1 or more children. Doing so makes my code later on a bit
easier on my eyes, but your mileage may vary.

Finally, we push the current heading onto the stack:

```
traversalStack.push(last.items[last.items.length - 1]);
```


Rather than treat the “top-level” headings as a boundary condition that I have
to check for, I use a top-level `sentinel`

node (with a heading level of `0`

,
guaranteed to be shallower than any other `HTMLHeadingElement`

) that remains in
my `traversalStack`

at all times.

```
const sentinel: HEntry = { text: "", id: "", level: 0 };
const traversalStack: HEntry[] = [sentinel];
```


The direct children of the sentinel node will be the *actual* top-level children
I care about. So when it’s time to return our headings, we can return the
sentinel’s children:

```
return sentinel.items || [];
```


### A React Hook for TOC data

We can use this as a React Hook as follows:

```
const postSelector = ".e-content.entry-content";
function useHeadingsData() {
const [headings, setHeadings] = useState<HEntry[]>([]);
useEffect(() => {
const hs = getNestedHeadings(
Array.from(
document
.querySelector(postSelector)!
.querySelectorAll<HTMLHeadingElement>("h2,h3,h4,h5,h6")
)
);
setHeadings(hs);
}, []);
return { headings };
}
```


This is functionally identical
[Emma’s example hook](https://www.emgoto.com/react-table-of-contents/#create-a-hook-to-find-all-headings-on-the-page),
but restricts headings to only those within our post (`postSelector`

).

The nice thing now is that the only thing that determines how deep your nested
headings go is your `querySelectorAll`

query. You can use this hook to give you
1, 2, or 6 levels of depth without changing `getNestedHeadings`

itself.

## Rendering Nested Headings Recursively

Now that we’re handling nested headings generically, it would be a shame if our component still had to hardcode multiple nesting levels.

```
export function TOC() {
const { headings } = useHeadingsData();
return (
<>
<nav aria-label="Table of Contents" className="toc">
<div role="heading" aria-level={6}>
In this post:
</div>
<ul>
{headings.map((h) => (
<li key={h.id}>
<H entry={h} />
</li>
))}
</ul>
</nav>
</>
);
}
function H({ entry }: { entry: HEntry }) {
return (
<>
<a href={`#${entry.id}`}>{entry.text}</a>
{entry.items && (
<ul>
{entry.items.map((h) => (
<li key={h.id}>
<H entry={h} />
</li>
))}
</ul>
)}
</>
);
}
```


## Expand, Collapse, Dismiss, and Restore

My site layout doesn’t lend itself to a sidebar TOC like the example, so I decided to have a floating TOC instead. The downside of floating the TOC over the content is that, depending on the person & the circumstance, a floating TOC can either feel:

- too large and intrusive (especially on mobile, or if you’re reading at not actively using it), or
- too small (especially if you’re trying to navigate to a section in a really long post)

I tried to pick a “reasonable default” size, but I knew that easy expansion & dismissal of the TOC would be helpful.

### Make Expansion States

It is helpful to imagine three states for the TOC:

```
enum State {
// Shown at a reasonable (compact) size, floating above content.
Normal,
// Expanded to (almost) fill the screen.
Expanded,
// Hidden from view, with only a small "restore" icon.
Collapsed,
}
```


To transition between these states, I wrote small components for 4 small
buttons: `UnfoldMore`

, `UnfoldLess`

, `Dismiss`

, and `Restore`

.

### In React…

```
export function TOC() {
const { headings } = useHeadingsData();
const [expansion, setExpansion] = useState(State.Normal);
const expand = () => setExpansion(State.Expanded);
const dismissIfExpanded = () => {
if (expansion === State.Expanded) expand();
};
const normal = () => setExpansion(State.Normal);
const collapse = () => setExpansion(State.Collapsed);
return (
<nav aria-label="Table of Contents" className="toc">
{expansion != State.Collapsed && (
<div className="controls">
{expansion == State.Normal ? (
<UnfoldMore onClick={expand} />
) : (
<UnfoldLess onClick={normal} />
)}
<Dismiss onClick={collapse} />
</div>
)}
<div
className={classNames("outer-scroll", {
expanded: expansion == State.Expanded,
collapsed: expansion == State.Collapsed,
normal: expansion == State.Normal,
})}
>
{expansion == State.Collapsed ? (
<Restore onClick={normal} />
) : (
<>
<div role="heading" aria-level={6}>
In this post:
</div>
<ul>
{headings.map((h) => (
<li key={h.id}>
<H entry={h} onClick={dismissIfExpanded} />
</li>
))}
</ul>
</>
)}
</div>
</nav>
);
}
```


In addition to state changes driven by button, clicking on any TOC element while expanded will restore it to the “normal” state.

### Styling the Expansion States

![TOC in Normal State](../../assets/746e26eec689c0db.img)

The TOC floats over some content in its normal state but doesn’t take too much space. Readers might need to expand it if they are closely navigating through a long article.

![TOC in Expanded State](../../assets/8bb83a52a2e249b0.img)

While the states change which expansion buttons are visible in the component,
the most important change they’re responsible for is setting the `.expanded`

,
`.collapsed`

, and `.normal`

classes on the `.outer-scroll`

element.

With these, we can target each state to display the TOC differently:

```
.outer-scroll.normal {
height: 9rem;
max-height: 25vh;
}
.outer-scroll.expanded {
height: calc(100vh - 2rem);
bottom: 1rem;
}
.outer-scroll.normal,
.outer-scroll.expanded {
padding: 0 0.5rem;
}
@media screen and (min-width: 700px) {
/* On large screens, TOC doesn't have to fill width of screen. */
.outer-scroll.normal,
.outer-scroll.expanded {
width: 35vw;
max-width: 600px;
}
}
.outer-scroll.collapsed {
height: unset;
width: -moz-fit-content;
width: fit-content;
margin-right: 0.5rem;
margin-left: auto;
}
```


## Conclusion

Here’s a
[gist with the whole thing](https://gist.github.com/Eyas/e9645e74a15bfb99fa7f373365af9a49),
including other features described in the
[original post](https://www.emgoto.com/react-table-of-contents/).

Note that I don’t automatically include a TOC in every post. Typically, I prefer
only using a TOC when the content is long enough and has many sections. I use
MDX to write my articles and expose the TOC as a custom `<TOC>`

component that
is only included in articles where needed. Most times, users navigating to my
site will not load the JS and styles associated with a TOC.

## Footnotes

-
Gatsby allows the heading structure to be queried and retrieved through GraphQL, and some Remark plugins can be used to do the same generically.

[↩](https://blog.eyas.sh#user-content-fnref-1)