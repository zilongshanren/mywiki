---
title: Fast, Bump-Allocated Virtual DOMs with Rust and Wasm – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2019/03/fast-bump-allocated-virtual-doms-with-rust-and-wasm/
author: Nick Fitzgerald
published: '2019-03-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Dodrio](https://github.com/fitzgen/dodrio) is a virtual DOM library written in Rust and WebAssembly. It takes advantage of both Wasm’s linear memory and Rust’s low-level control by designing virtual DOM rendering around bump allocation. Preliminary benchmark results suggest it has best-in-class performance.

[Background](https://hacks.mozilla.org#background)[Dodrio from a User’s Perspective](https://hacks.mozilla.org#dodrio-from-a-users-perspective)[Internal Design](https://hacks.mozilla.org#internal-design)[Preliminary Benchmarks](https://hacks.mozilla.org#preliminary-benchmarks)[Future Work](https://hacks.mozilla.org#future-work)[Conclusion](https://hacks.mozilla.org#conclusion)

### Virtual DOM Libraries

Virtual DOM libraries provide a declarative interface to the Web’s imperative DOM. Users describe the desired DOM state by generating a virtual DOM tree structure, and the library is responsible for making the Web page’s physical DOM reflect the user-generated virtual DOM tree. Libraries employ some diffing algorithm to decrease the number of expensive DOM mutation methods they invoke. Additionally, they tend to have facilities for caching to further avoid unnecessarily re-rendering components which have not changed and re-diffing identical subtrees.

### Bump Allocation

Bump allocation is a fast, but limited approach to memory allocation. The allocator maintains a chunk of memory, and a pointer pointing within that chunk. To allocate an object, the allocator rounds the pointer up to the object’s alignment, adds the object’s size, and does a quick test that the pointer didn’t overflow and still points within the memory chunk. Allocation is only a small handful of instructions. Likewise, deallocating every object at once is fast: reset the pointer back to the start of the chunk.

The disadvantage of bump allocation is that there is no general way to deallocate individual objects and reclaim their memory regions while other objects are still in use.

These trade offs make bump allocation well-suited for phase-oriented allocations. That is, a group of objects that will all be allocated during the same program phase, used together, and finally deallocated together.

```
bump_allocate(size, align):
aligned_pointer = round_up_to(self.pointer, align)
new_pointer = aligned_pointer + size
if no overflow and new_pointer < self.end_of_chunk:
self.pointer = new_pointer
return aligned_pointer
else:
handle_allocation_failure()
```


First off, we should be clear about what Dodrio is and is not. Dodrio is only a virtual DOM library. It is not a full framework. It does not provide state management, such as Redux stores and actions or two-way binding. It is not a complete solution for everything you encounter when building Web applications.

Using Dodrio should feel fairly familiar to anyone who has used Rust or virtual DOM libraries before. To define how a `struct`

is rendered as HTML, users implement the `dodrio::Render`

trait, which takes an immutable reference to `self`

and returns a virtual DOM tree.

Dodrio uses the [builder pattern](https://en.wikipedia.org/wiki/Builder_pattern) to create virtual DOM nodes. We intend to support optional [JSX](https://reactjs.org/docs/introducing-jsx.html)-style, inline HTML templating syntax with compile-time procedural macros, but we’ve left it as [future work](https://hacks.mozilla.org#future-work).

The `'a`

and `'bump`

lifetimes in the `dodrio::Render`

trait’s interface and the `where 'a: 'bump`

clause enforce that the `self`

reference outlives the bump allocation arena and the returned virtual DOM tree. This means that if `self`

contains a string, for example, the returned virtual DOM can safely use that string by reference rather than copying it into the bump allocation arena. Rust’s lifetimes and borrowing enable us to be aggressive with cost-saving optimizations while simultaneously statically guaranteeing their safety.

```
struct Hello {
who: String,
}
impl Render for Hello {
fn render<'a, 'bump>(&'a self, bump: &'bump Bump) -> Node<'bump>
where
'a: 'bump,
{
span(bump)
.children([text("Hello, "), text(&self.who), text("!")])
.finish()
}
}
```


Event handlers are given references to the root `dodrio::Render`

component, a handle to the virtual DOM instance that can be used to schedule re-renders, and the DOM event itself.

```
struct Counter {
count: u32,
}
impl Render for Counter {
fn render<'a, 'bump>(&'a self, bump: &'bump Bump) -> Node<'bump>
where
'a: 'bump,
{
let count = bumpalo::format!(in bump, "{}", self.count);
div(bump)
.children([
text(count.into_bump_str()),
button(bump)
.on("click", |root, vdom, _event| {
let counter = root.unwrap_mut::<Counter>();
counter.count += 1;
vdom.schedule_render();
})
.children([text("+")])
.finish(),
])
.finish()
}
}
```


Additionally, Dodrio also has a proof-of-concept API for defining rendering components in JavaScript. This reflects the Rust and Wasm ecosystem’s strong integration story for JavaScript, that enables both incremental porting to Rust and heterogeneous, polyglot applications where just the most performance-sensitive code paths are written in Rust.

```
class Greeting {
constructor(who) {
this.who = who;
}
render() {
return {
tagName: "p",
attributes: [{ name: "class", value: "greeting" }],
listeners: [{ on: "click", callback: this.onClick.bind(this) }],
children: [
"Hello, ",
{
tagName: "strong",
children: [this.who],
},
],
};
}
async onClick(vdom, event) {
// Be more excited!
this.who += "!";
// Schedule a re-render.
await vdom.render();
console.log("re-rendering finished!");
}
}
```


```
#[wasm_bindgen]
extern "C" {
// Import the JS `Greeting` class.
#[wasm_bindgen(extends = Object)]
type Greeting;
// And the `Greeting` class's constructor.
#[wasm_bindgen(constructor)]
fn new(who: &str) -> Greeting;
}
// Construct a JS rendering component from a `Greeting` instance.
let js = JsRender::new(Greeting::new("World"));
```


Finally, Dodrio exposes a safe public interface, and we have never felt the need to reach for `unsafe`

when authoring Dodrio rendering components.

Both virtual DOM tree rendering and diffing in Dodrio leverage bump allocation. Rendering constructs bump-allocated virtual DOM trees from component state. Diffing batches DOM mutations into a bump-allocated “change list” which is applied to the physical DOM all at once after diffing completes. This design aims to maximize allocation throughput, which is often a performance bottleneck for virtual DOM libraries, and minimize bouncing back and forth between Wasm, JavaScript, and native DOM functions, which should improve temporal cache locality and avoid out-of-line calls.

### Rendering Into Double-Buffered Bump Allocation Arenas

Virtual DOM rendering exhibits phases that we can exploit with bump allocation:

- A virtual DOM tree is constructed by a
`Render`

implementation, - it is diffed against the old virtual DOM tree,
- saved until the next time we render a new virtual DOM tree,
- when it is diffed against that new virtual DOM tree,
- and then finally it and all of its nodes are destroyed.

This process repeats ad infinitum.

```
------------------- Time ------------------->
Tree 0: [ render | ------ | diff ]
Tree 1: [ render | diff | ------ | diff ]
Tree 2: [ render | diff | ------ | diff ]
Tree 3: [ render | diff | ------ | diff ]
...
```


At any given moment in time, only two virtual DOM trees are alive. Therefore, we can double buffer two bump allocation arenas that switch back and forth between the roles of containing the new or the old virtual DOM tree:

- A virtual DOM tree is rendered into bump arena A,
- the new virtual DOM tree in bump arena A is diffed with the old virtual DOM tree in bump arena B,
- bump arena B has its bump pointer reset,
- bump arenas A and B are swapped.

```
------------------- Time ------------------->
Arena A: [ render | ------ | diff | reset | render | diff | -------------- | diff | reset | render | diff ...
Arena B: [ render | diff | -------------- | diff | reset | render | diff | -------------- | diff ...
```


### Diffing and Change Lists

Dodrio uses a naïve, single-pass algorithm to diff virtual DOM trees. It walks both the old and new trees in unison and builds up a change list of DOM mutation operations whenever an attribute, listener, or child differs between the old and the new tree. It does not currently use any sophisticated algorithms to minimize the number of operations in the change list, such as longest common subsequence or patience diffing.

The change lists are constructed during diffing, applied to the physical DOM, and then destroyed. The next time we render a new virtual DOM tree, the process is repeated. Since at most one change list is alive at any moment, we use a single bump allocation arena for all change lists.

A change list’s DOM mutation operations are encoded as [instructions for a custom stack machine](https://github.com/fitzgen/dodrio/blob/ef4fb9a4895695fe3ea50c936d163da4506390d6/src/change_list.rs#L101-L241). While an instruction’s discriminant is always a 32-bit integer, instructions are variably sized as some have immediates while others don’t. The machine’s stack contains physical DOM nodes (both text nodes and elements), and immediates encode pointers and lengths of UTF-8 strings.

The instructions are [emitted on the Rust and Wasm side](https://github.com/fitzgen/dodrio/blob/ef4fb9a4895695fe3ea50c936d163da4506390d6/src/change_list.rs#L267-L379), and then [batch interpreted and applied to the physical DOM in JavaScript](https://github.com/fitzgen/dodrio/blob/ef4fb9a4895695fe3ea50c936d163da4506390d6/js/change-list.js#L12-L173). Each JavaScript function that interprets a particular instruction takes four arguments:

- A reference to the JavaScript
`ChangeList`

class that represents the stack machine, - a
`Uint8Array`

view of Wasm memory to decode strings from, - a
`Uint32Array`

view of Wasm memory to decode immediates from, - and an offset
`i`

where the instruction’s immediates (if any) are located.

It returns the new offset in the 32-bit view of Wasm memory where the next instruction is encoded.

There are instructions for:

- Creating, removing, and replacing elements and text nodes,
- adding, removing, and updating attributes and event listeners,
- and traversing the DOM.

For example, the `AppendChild`

instruction has no immediates, but expects two nodes to be on the top of the stack. It pops the first node from the stack, and then calls `Node.prototype.appendChild`

with the popped node as the child and the node that is now at top of the stack as the parent.

`AppendChild`

instruction```
// Allocate an instruction with zero immediates.
fn op0(&self, discriminant: ChangeDiscriminant) {
self.bump.alloc(discriminant as u32);
}
/// Immediates: `()`
///
/// Stack: `[... Node Node] -> [... Node]`
pub fn emit_append_child(&self) {
self.op0(ChangeDiscriminant::AppendChild);
}
```


`AppendChild`

instruction```
function appendChild(changeList, mem8, mem32, i) {
const child = changeList.stack.pop();
top(changeList.stack).appendChild(child);
return i;
}
```


On the other hand, the `SetText`

instruction expects a text node on top of the stack, and does not modify the stack. It has a string encoded as pointer and length immediates. It decodes the string, and calls the `Node.prototype.textContent`

setter function to update the text node’s text content with the decoded string.

`SetText`

instruction```
// Allocate an instruction with two immediates.
fn op2(&self, discriminant: ChangeDiscriminant, a: u32, b: u32) {
self.bump.alloc([discriminant as u32, a, b]);
}
/// Immediates: `(pointer, length)`
///
/// Stack: `[... TextNode] -> [... TextNode]`
pub fn emit_set_text(&self, text: &str) {
self.op2(
ChangeDiscriminant::SetText,
text.as_ptr() as u32,
text.len() as u32,
);
}
```


`SetText`

instruction```
function setText(changeList, mem8, mem32, i) {
const pointer = mem32[i++];
const length = mem32[i++];
const str = string(mem8, pointer, length);
top(changeList.stack).textContent = str;
return i;
}
```


To get a sense of Dodrio’s speed relative to other libraries, we added it to [Elm’s Blazing Fast HTML benchmark](https://elm-lang.org/blog/blazing-fast-html-round-two) that compares rendering speeds of TodoMVC implementations with different libraries. They claim that the methodology is fair and that the benchmark results should generalize. They also subjectively measure how easy it is to optimize the implementations to improve performance (for example, by adding well-placed `shouldComponentUpdate`

hints in React and `lazy`

wrappers in Elm). We followed their same methodology and disabled Dodrio’s on-by-default, once-per-animation-frame render debouncing, giving it the same handicap that the Elm implementation has.

That said, there are some caveats to these benchmark results. The React implementation had bugs that prevented it from completing the benchmark, so we don’t include its measurements below. If you are curious, you can look at the original Elm benchmark results to see how it generally fared relative to some of the other libraries measured here. Second, we made an initial attempt to update the benchmark to the latest version of each library, but quickly got in over our heads, and therefore *this benchmark is not using the latest release of each library*.

With that out of the way let’s look at the benchmark results. We ran the benchmarks in Firefox 67 on Linux. Lower is better, and means faster rendering times.

![Benchmark results graph](../../assets/6672499649995b9e.png)


![Benchmark results graph](../../assets/6672499649995b9e.png)

| Library | Optimized? | Milliseconds |
|---|---|---|
| Ember 2.6.3 | No | 3542 |
| Angular 1.5.8 | No | 2856 |
| Angular 2 | No | 2743 |
| Elm 0.16 | No | 4295 |
| Elm 0.17 | No | 3170 |
Dodrio 0.1-prerelease |
No |
2181 |
| Angular 1.5.8 | Yes | 3175 |
| Angular 2 | Yes | 2371 |
| Elm 0.16 | Yes | 4229 |
| Elm 0.17 | Yes | 2696 |

**Dodrio is the fastest library measured in the benchmark.** This is not to say that Dodrio will always be the fastest in every scenario — that is undoubtedly false. But these results validate Dodrio’s design and show that it already has best-in-class performance. Furthermore, there is room to make it even faster:

- Dodrio is brand new, and has not yet had the years of work poured into it that other libraries measured have. We have not done any serious profiling or optimization work on Dodrio yet!
-
The Dodrio TodoMVC implementation used in the benchmark does not use

`shouldComponentUpdate`

-style optimizations, like other implementations do. These techniques are still available to Dodrio users, but you should need to reach for them much less frequently because idiomatic implementations are already fast.

So far, we haven’t invested in polishing Dodrio’s ergonomics. We would like to explore adding [type-safe HTML templates](https://crates.io/crates/typed-html) that boil down to Dodrio virtual DOM tree builder invocations.

Additionally, there are a few more ways we can potentially improve Dodrio’s performance:

[We can create new instructions for common DOM mutation operations.](https://github.com/fitzgen/dodrio/issues/27)For example, we can avoid decoding attribute name strings from immediates if we have instructions for the setting the most common attributes directly (e.g.`"id"`

,`"class"`

, etc…)-
[We can investigate smarter diffing algorithms.](https://github.com/fitzgen/dodrio/issues/28)Initial profiling shows that Dodrio spends much more time applying diffs than generating diffs or constructing virtual DOM trees. It is possible that improving the diffing algorithm could emit smaller diffs that are faster to apply. -
Dodrio’s caching mechanisms (similar to React’s

`shouldComponentUpdate`

)[currently avoid reconstructing virtual DOM subtrees, but do not yet avoid re-diffing them.](https://github.com/fitzgen/dodrio/issues/31)Extending the caching mechanisms to also avoid re-diffing them should be relatively straight forward and yield speed ups when caching is used.

For both ergonomics and further performance improvements, we would like to start gathering feedback informed by real world usage before investing too much more effort.

[Evan Czaplicki](https://twitter.com/czaplic) pointed us to a second benchmark — [ krausest/js-framework-benchmark](https://github.com/krausest/js-framework-benchmark) — that we can use to further evaluate Dodrio’s performance. We look forward to implementing this benchmark for Dodrio and gathering more test cases and insights into performance.

Further in the future, the [WebAssembly host bindings proposal](https://github.com/WebAssembly/host-bindings/blob/master/proposals/host-bindings/Overview.md) will enable us to interpret the change list’s operations in Rust and Wasm without trampolining through JavaScript to invoke DOM methods.

Dodrio is a new virtual DOM library that is designed to leverage the strengths of both Wasm’s linear memory and Rust’s low-level control by making extensive use of fast bump allocation. If you would like to learn more about Dodrio, we encourage you to check out its [repository](https://github.com/fitzgen/dodrio) and [examples](https://github.com/fitzgen/dodrio/tree/master/examples)!

Thanks to [Luke Wagner](http://lukewagner.name/) and [Alex Crichton](https://github.com/alexcrichton) for their contributions to Dodrio’s design, and participation in brainstorming and rubber ducking sessions. We also discussed many of these ideas with core developers on the React, Elm, and Ember teams, and we thank them for the context and understanding these discussions ultimately brought to Dodrio’s design. A final round of thanks to [Jason Orendorff](http://jorendorff.blogspot.com/), [Lin Clark](https://twitter.com/linclark), [Till Schneidereit](https://tillschneidereit.net/), [Alex Crichton](https://github.com/alexcrichton), [Luke Wagner](http://lukewagner.name/), [Evan Czaplicki](https://twitter.com/czaplic), and [Robin Heggelund Hansen](https://twitter.com/robheghan) for providing valuable feedback on early drafts of this document.

## About
[
Nick Fitzgerald ](http://fitzgeraldnick.com)

I like computing, bicycles, hiphop, books, and pen plotters. My pronouns are he/him.

## 9 comments

Taylor HuntMarch 14th, 2019 at 13:12Nick FitzgeraldMarch 15th, 2019 at 18:12VladanMarch 14th, 2019 at 13:51Nick FitzgeraldMarch 15th, 2019 at 18:10archnodeMarch 15th, 2019 at 11:52Sabir AnsariMarch 16th, 2019 at 01:31Jim HurdMarch 16th, 2019 at 05:29Nick FitzgeraldMarch 18th, 2019 at 09:07Richard DoddMarch 24th, 2019 at 15:45