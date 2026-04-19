---
title: The Incremental Machine
url: https://acko.net/blog/the-incremental-machine/
author: Steven Wittens
published: '2019-08-03'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![The Incremental Machine](../../assets/ea61bbf1a016b9b5.png)

# The Incremental Machine

Let's try and work our way through the oldest problem in computer science, or close to it: cache invalidation and naming things. Starting with the fact that we misnamed it.

In my view, referring to *it* as "cache invalidation" is somewhat like referring to crime prevention as "death minimization." While the absense of preventable death is indeed a desirable aspect of quality policing, it would suggest a worrying lack of both concern and ambition if that were the extent of a police force's mission statement.

So too should you run away, not walk, from anyone who treats some stale data and a necessary hard-refresh as a minor but unavoidable inconvenience. You see, this person is telling you that expecting to trust your eyes is too much to ask for when it comes to computers. I don't mean correctness or truth value, no, I just mean being able to see what is there so you can make sense of it, right or wrong. They expect you to sanity check every piece of information you might find, and be ready to Shift-Refresh or Alt-F4 if you suspect a glitch in the matrix. It should be pretty obvious this seriously harms the utility of such an environment, for work or pleasure. Every document becomes a potential sticky indicator gauge, requiring you to give it a good whack to make sure it's unstuck.

This should also puzzle you. A discipline whose entire job it is to turn pieces of data into other pieces of data, using precise instructions, is unable to figure out when its own results are no longer valid? This despite having the complete paper trail at our disposal for how each result is produced, in machine readable form.

Why hasn't this been solved by tooling already? We love tools, right? Is it possible? Is it feasible? Which parts?

## Adders in the Grass

I'm going to start at the bottom (or at least a bottom) and work my way up and you'll see why. Let's start with a trivial case of a side-effect-free function, integer addition, and anally dissect it:

`(a, b) => a + b`


The result changes when either `a`

or `b`

do. However, there is a special case: if `a`

and `b`

each change in opposite amounts, the output is unchanged. Here we have a little microcosm of larger issues.

First, it would be perfectly possible to cache this result, and to check whether `a`

or `b`

have changed since the last time. But just computing the sum is faster than two comparisons. You also need permanent extra storage for at least one extra `a`

and `b`

each, and much more if you want a multi-valued cache rather than just a safety valve. Then you need a pruning policy too to keep it from growing.

Second, if you wish to know whether and how the output will actually change, then you must double check. You have to diff the old and the new values, track the resulting deltas through the same computation as the original. So you can compare to the previous result. The requirement that `a + b != (a + Δa) + (b + Δb)`

can then be reduced to `Δa != -Δb`

. Though this is still more actual work.

If this were multiplication instead of a sum, then:

`(a, b) => a * b`


`a * b != (a + Δa) * (b + Δb)`


which reduces to:

`Δa * b + Δb * a + Δa * Δb != 0`


Here there is a non-linear relationship which involves both values and deltas together. The first two terms depend on one delta and value each, but the last term only kicks in if both inputs change at the same time. This shows how deltas can interfere both constructively and destructively, either triggering or defusing other effects on other inputs. It also implies there are no easy shortcuts to be found in delta-land, because there are many more ways for values and deltas to combine, than just values by themselves.

In fact you already knew this. Because if you could provide a concise summary of the delta-behavior of a certain class of functions, you'd break a good chunk of the internet and win a few awards:

`m => SHA256(m)`


The deltas in a hash function don't just get cozy, they have an all-out orgy of computation, the kind they invented 55 gallon drums of lube for.

This is also your first hint of an answer as to y u no tools. What looks well-behaved and cacheable at a small scale may in fact be part of a larger, unpredictable algorithm, which is why trying to automate caching everywhere is generally a non-starter. That is, it is perfectly possible to imagine a sort of God's eye view of a fully incremental piece of code at the opcode level, and to watch as a change in inputs begins the siege of a thousand memoized gates. But it wouldn't be useful because it's far too granular.

This also means caching is not a computer science problem, it is a computer engineering problem. We are fighting against entropy, against the computational chaos we ourselves create. It is not a science, it is damage control.

![4-bit adder 4-bit adder](../../assets/63b608eb0453d562.jpg)


On the other hand, we should not give up, because neither `+`

or `*`

are elementary operations in reality. They are abstractions realized as digital circuits. Given a diagram of a binary adder, we could trace the data flow from each input bit, following the potential effects of each delta. But if you know your arithmetic you already know each bit in a sum can only affect itself and the ones to its left.

What's interesting though is that this complicated dance can be entirely ignored, because it serves to realize an abstraction, that of integers. Given integers, we can reason about changes at a different level. By looking at the level of arithmetic, we were able to discover that two specific patterns of matching differences, `Δa == -Δb`

, cancel out, regardless of the specific value of `a`

and `b`

.

In this case, that only gave us counterproductive "optimizations", but that's because we aren't looking at the right level of abstraction yet. The point is abstraction boundaries don't necessarily have to be black boxes like the hash function, they can also be force fields that allow you to contain deltas, or at least, transmute them into more well-behaved ones. So let's climb up, like Bret [wants us to](http://worrydream.com/LadderOfAbstraction/).

## I Spy With My Little API

For instance, if we look at the maximum operator applied to an entire list of numbers, again a pure function:

`xs => xs.reduce(max, -Infinity)`


A simple `reduce`

creates a linear dependency between successive elements, with every delta potentially affecting all `max()`

calls after it. However, the output changes more predictably.

If all elements are unique, the result will only change if a new value `x + Δx`

exceeds the previous result (increasing it), or if an old value `x`

was equal to the previous result and its `Δx < 0`

(decreasing it). Note we don't need to remember which element index it actually was, and we don't need to care about the elements that didn't change either (at least to merely *detect* a change).

If there are duplicates, things are a bit more complicated. Now there is a multi-delta-term `Δa * Δb * ...`

between each set, which won't trigger unless all of them decrease at the same time. Writing out the full delta equation for the `max`

of a list is more fun than I can handle, but you get the idea, and actually, it doesn't really matter much. If we pretend all elements are unique regardless, we simply trigger the occasional false positive (change falsely detected), but crucially no false negatives (change falsely ignored).

Either way, the sequential nature of the computation is no longer relevant at this level, because `max()`

is associative (and commutative too), and `reduce`

is a higher-order function whose deltas cancel out in convenient ways when you give it that sort of operator.

Which means we're almost there. Actually dissecting the `max`

operator was still too tedious, too special-cased. But it gives us hints of what to look for.

One such winning combo is [Map-Reduce](https://en.wikipedia.org/wiki/MapReduce), using the same properties. By mapping each element in isolation, the effects of any change in any input is initially contained, in a way that is independent of the position of an element in a collection. Second, by using an associative reduction operator, this reduction can be done incrementally, as a tree instead of as a flat list. You reduce the list in chunks, and then re-reduce the list of reductions, recursively until you get one result. When some of the items in the list change, only a few chunks are affected, and the overall recomputation along the tree is minimized. The price you pay is to retain all the intermediate reductions in the tree each time.

Map-Reduce is a universal incremental evaluation strategy, which can schedule and execute any pure function of the individual inputs, provided you reduce the result in an algebraically closed fashion. So that exists. Any others?

Well, many sequential/batch processes are universally incrementalizable too. Take for example a lexer, which processes a stream of text and produces tokens. In this case, the input cannot be chunked, it must be traversed start-to-end.

The lexer tracks its syntax in an internal state machine, while consuming one or more characters to produce zero or more tokens.

Conveniently, the lexer tells you everything you need to know through its behavior in consuming and producing. Roughly speaking, as long as you remember the tuple (lexer state, input position, output position) at every step, you can resume lexing at any point, reusing partial output for partially unchanged input. You can also know when to stop re-lexing, namely when the inputs match again and the internal state does too, because the lexer has no other dependencies.

Lining up the two is left as an exercise for the reader, but [there's a whole thesis if you like](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1997/CSD-97-946.pdf). With some minor separation of concerns, the same lexer can be used in batch or incremental mode. They also talk about Self-Versioned Documents and manage to apply the same trick to incremental parse *trees*, where the dependency inference is a bit trickier, but fundamentally still the same principle.

What's cool here is that while a lexer is still a pure function in terms of its state and its input, there crucially is inversion of control: it decides to call `getNextCharacter()`

and `emitToken(...)`

itself, whenever it wants, and the incremental mechanism is subservient to it on the small scale. Which is another clue, imo. It seems that pure functional programming is in fact neither necessary nor sufficient for successful incrementalism. That's just a very convenient straightjacket in which it's hard to hurt yourself. Rather you need the application of consistent evaluation strategies. Blind incrementalization is exceedingly difficult, because you don't know anything actionable about what a piece of code does with its data a priori, especially when you're trying to remain ignorant of its specific ruleset and state.

As an aside, the resumable-sequential approach also works for map-reduce, where instead of chunking your inputs, you reduce them in-order, but keep track of reduction state at every index. It only makes sense if your reducer is likely to reconverge on the same result despite changes though. It also works for resumable flatmapping of a list (that is, `.map(...).flatten()`

), where you write out a new contiguous array on every change, but copy over any unchanged sections from the last one.

Each is a good example of how you can separate logistics from policy, by reducing the scope and/or providing inversion of control. The effect is not unlike building a personal assistant for your code, who can take notes and fix stuff while you go about your business.

## Don't Blink

This has all been about caching, and yet we haven't actually seen a true cache invalidation problem. You see, a cache invalidation problem is when you have a problem knowing when to invalidate a cache. In all the above, this is not a problem. With a pure function, you simply compare the inputs, which are literal values or immutable pointers. The program running the lexer also knows exactly which part of the output is in question, it's everything after the edit, same for the flatmap. There was never a time when a cache became invalid without us having everything right there to trivially verify and refresh it with.

No, these are cache *conservation* problems. We were actually trying to reduce unnecessary misses in an environment where the baseline default is an easily achievable zero false hits. We tinkered with that at our own expense, hoping to squeeze out some performance.

There is one bit of major handwavium in there: `a != b`

in the real world. When `a`

and `b`

are composite and enormous, i.e. mutable like your mom, or for extra points, async, making that determination gets somewhat trickier. Async means a gap of a client/server nature and [you know what that means](https://acko.net/blog/apis-are-about-policy).

Implied in the statement `(a, b) => 🦆`

is the fact that you have an `a`

and a `b`

in your hands and we're having duck tonight. If instead you have the name of a store where you can buy some `a`

, or the promise of `b`

to come, then now your computation is bringing a busload of extra deltas to dinner, and btw they'll be late. If `a`

and `b`

have large dependent computations hanging off them, it's your job to take this additional cloud of uncertainty and somehow divine it into a precise, granular determination of what to keep and what to toss out, now, not later.

1) You don't have an image, you have the URL of an image, and now you need to decide whether the URL will resolve to the same binary blob that's in your local cache. Do they still represent the same piece of data? The cache invalidation problem is that you weren't notified when the source of truth changed. Instead you have to make the call based on the metadata you originally got with the data and hope for the best.

Obviously it's not possible for every browser to maintain long-lived subscriptions to every meme and tiddy it downloaded. But we can brainstorm. The problem is that you took a question that has a mutable answer but you asked it to be immutable. The right answer is "here's the local cache and some refreshments while you wait, ... ah, there's a newer version, here". Protocol. Maybe a short-lived subscription inside the program itself, from the part that wants to show things, subscribing to the part that knows what's in them, until the latter is 100% sure. You just have to make sure the part that wants to show things is re-entrant.

2) You want to turn your scene graph into a flattened list of drawing commands, but the scene graph is fighting back. The matrices are cursed, they change when you blink, like the statues from Doctor Who. Because you don't want to remove the curse, you ask everyone to write *IS DIRTY* in chalk on the side of any box they touch, and you clean the marks back off 60 times per second when you iterate over the entire tree and put everything in order.

I joke, but what's actually going on here is subtle enough to be worth teasing apart. The reason you use dirty flags on mutable scene graphs has nothing to do with not knowing when the data changes. You know exactly when the data changes, it's when you set the dirty flag to true. So what gives?

The reason is that when children depend on their parents, changes cascade down. If you react to a change on a node by immediately updating all its children, this means that further updates of those children will trigger redundant refreshes. It's better to wait and gather all the changes, and then apply and refresh from the top down. Mutable or immutable matrix actually has nothing to do with it, it's just that in the latter case, the dirty flag is implicit on the matrix itself, and likely on each scene node too.

Push vs pull is also not really a useful distinction, because in order to cleanly pull from the outputs of a partially dirty graph, you have to cascade towards the inputs, and then return (i.e. push) the results back towards the end. The main question is whether you have the necessary information to avoid redundant recomputation in either direction and can manage to hold onto it for the duration.

The dirty flag is really a deferred and debounced line of code. It is read and cleared at the same time in the same way every frame, within the parent/child context of the node that it is set on. It's not data, it's a covert pre-agreed channel for a static continuation. That is to say, you are signaling the janitor who comes by 60 times a second to please clean up after you.

What's interesting about this is that there is nothing particularly unique about scene graphs here. Trees are ubiquitous, as are parent/child dependencies in both directions (inheritance and aggregation). If we reimagine this into its most generic form, then it might be a tree on which dependent changes can be applied in deferred/transactional form, whose derived triggers are re-ordered by dependency, and which are deduplicated or merged to eliminate any redundant refreshes before calling them.

## In Case It Wasn't Obvious

So yes, exactly like the way the React runtime can gather multiple `setState()`

calls and re-render affected subtrees. And exactly like how you can pass a reducer function instead of a new state value to it, i.e. a deferred update to be executed at a more opportune and coordinated time.

In fact, remember how in order to properly cache things you have to keep a copy of the old input around, so you can compare it to the new? That's what `props`

and `state`

are, they are the `a`

and the `b`

of a React component.

```
Δcomponent = Δ(props * state)
= Δprops * state + Δstate * props + Δprops * Δstate
= Props changed, state the same (parent changed)
+ State changed, props the same (self/child changed)
+ Props and state both changed (parent's props/state change
triggered a child's props/state change)
```


The third term is rare though, and the React team has been trying to deprecate it for years now.

I prefer to call Components a re-entrant function call in an incremental deferred data flow. I'm going to recap React 101 quickly, because there is a thing that hooks do that needs to be pointed out.

The way you use React nowadays is, you render some component to some native context like an HTML document:

`ReactDOM.render(<Component />, context);`


The `<Component />`

in question is just syntactic sugar for a regular function:

```
let Component = (props) => {
// Allocate some state and a setter for it
let [state, setState] = useState(initialValue);
// Render a child component
return <OtherComponent foo={props.bar} onChange={e => setState(...)}/>;
// aka
return React.createElement(OtherComponent, {foo: props.bar, onChange: e => setState(...)}, null);
};
```


This function gets called because we passed a `<Component />`

to `React.render()`

. That's the inversion of control again. In good components, `props`

and `state`

will both be some immutable data. `props`

is feedforward from parents, `state`

is feedback from ourselves and our children, i.e. respectively the exterior input and the interior state.

If we call `setState(...)`

, we cause the `Component()`

function to be run again with the same exterior input as before, but with the new interior state available.

The effect of returning `<OtherComponent .. />`

is to schedule a deferred call to `OtherComponent(...)`

. It will get called shortly after. It too can have the same pattern of allocating state and triggering self-refreshes. It can also trigger a refresh of its parent, through the `onChange`

handler we gave it. As the HTML-like syntax suggests, you can also nest these `<Elements>`

, passing a tree of deferred children to a child. Eventually this process stops when components have all been called and expanded into native elements like `<div />`

instead of React elements.

Either way, we know that `OtherComponent(...)`

will not get called unless we have had a chance to respond to changes first. However if the changes don't concern us, we don't need to be rerun, because the exact same rendered output would be generated, as none of our props or state changed.

This incidentally also provides the answer to the question you may not have realized you had: if everything is eventually a function of some Ur-input at the very start, why would anything ever need to be resumed from the middle? Answer: because some of your components want to semi-declaratively self-modify. The outside world shouldn't care. If we do look inside, you are sometimes treated to topping-from-the-bottom, as a render function is passed down to other components, subverting the inversion of control ad-hoc by extending it inward.

So what is it, exactly, that `useState()`

does then that makes these side-effectful functions work? Well it's a *just-in-time allocation of persistent storage for a temporary stack frame*. That's a mouthful. What I mean is, forget React.

Think of `Component`

as just a function in an execution flow, whose arguments are placed on the stack when called. This stack frame is temporary, created on a call and destroyed as soon as you return. However, this particular *invocation* of `Component`

is not equally ephemeral, because it represents a specific component that was mounted by React in a particular place in the tree. It has a persistent lifetime for as long as its parent decides to render/call it.

So `useState`

lets it anonymously allocate some permanent memory, keyed off its completely ephemeral, unnamed, unreified execution context. This only works because React is always the one who calls these magic reentrant functions. As long as this is true, multiple re-runs of the same code will retain the same local state in each stack frame, provided the code paths did not diverge. If they did, it's just as if you ran those parts from scratch.

What's also interesting is that hooks were first created to reduce the overuse of `<Component />`

nesting as a universal hammer for the nail of code composition, because much of the components had nothing to do with UI directly. In fact, it may be that UI just provided us with convenient boundaries around things in the form of widgets, which suggestively taught us how to incrementalize them.

This to me signals that `React.render()`

is somewhat misnamed, but its only mistake is a lack of ambition. It should perhaps be `React.apply()`

or `React.incremental()`

. It's a way of calling a deferred piece of code so that it can be re-applied later with different inputs, including from the inside. It computes minimum updates down a dependency tree of other deferred pieces of code with the same power.

Right now it's still kind of optimized for handling UI trees, but the general strategy is so successful that variants incorporating other reconciliation topologies will probably work too. Sure, code doesn't look like React UI components, it's a DAG, but we all *write* code in a sequential form, explicitly ordering statements even when there is no explicit dependency between them, using variable names as the glue.

The incremental strategy that React uses includes something like the resumable-sequential flatmap algorithm, that's what the `key`

attribute for array elements is for, but instead of `.map(...).flatten()`

it's more like an incremental version of `let render = (el, props) => recurse(el.render(props))`

where `recurse`

is actually a job scheduler.

The tech under the hood that makes this work is the React reconciler. It provides you with the illusion of a persistent, nicely nested stack of props and state, even though it never runs more than small parts of it at a time after the initial render. It even provides a solution for that old bugbear: resource allocation, in the form of the `useEffect()`

hook. It acts like a constructor/destructor pair for one of these persistent stack frames. You initialize any way you like, and you return to React the matching destructor as a closure on the spot, which will be called when you're unmounted. You can also pass along dependencies so it'll be un/remounted when certain props like, I dunno, a texture size and every associated resource descriptor binding need to change.

There's even a neat trick you can do where you use one reconciler as a `useEffect()`

inside another, bridging from one target context (e.g. HTML) into a different one that lives inside (e.g. WebGL). The transition from one to the other is then little more than a footnote in the resulting component tree, despite the fact that execution- and implementation-wise, there is a complete disconnect as only fragments of code are being re-executed sparsely left and right.

You can make it sing with judicious use of the `useMemo`

and `useCallback`

hooks, two necessary evils whose main purpose is to let you manually pass in a list of dependencies and save yourself the trouble of doing an equality check. When you want to go mutable, it's also easy to box in a changing value in an unchanging `useRef`

once it's cascaded as much as it's going to. What do you eventually `<expand>`

to? Forget DOMs, why not emit a view tree of render props, i.e. deferred function calls, interfacing natively with whatever you wanted to talk to in the first place, providing the benefits of incremental evaluation while retaining full control.

It's not a huge leap from here to being able to tag any closure as re-entrant and incremental, letting a compiler or runtime handle the busywork, and forget this was ever meant to beat an aging DOM into submission. Maybe that was just the montage where the protagonist trains martial arts in the mountain-top retreat. Know just how cheap O(1) equality checks can be, and how affordable incremental convenience for all but the hottest paths. However, no tool is going to reorganize your data and your code for you, so putting the boundaries in the right place is still up to you.

I have a hunch we could fix a good chunk of GPU programming on the ground with this stuff. Open up composability without manual bureaucracy. You know, like React VR, except with LISP instead of tears when you look inside. Unless you prefer being a sub to Vulkan's dom forever?

*Previous: APIs are about PolicyNext: Model-View-Catharsis*