---
title: Future-proofing Firefox’s JavaScript Debugger Implementation – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2020/03/future-proofing-firefoxs-javascript-debugger-implementation/
author: Jim Blandy
published: '2020-03-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Or: The Implementation of the SpiderMonkey Debugger (and its cleanup)*

We’ve made major improvements to JavaScript debugging in Firefox DevTools over the past two years. Developer feedback has informed and validated our work on performance, source maps, stepping reliability, pretty printing, and more types of breakpoints. Thank you. If you haven’t tried Firefox for debugging modern JavaScript in a while, [now is the time](https://www.mozilla.org/en-US/firefox/developer/).

Many of the aforementioned efforts focused on the Debugger frontend (written in [React and Redux](https://codetribute.mozilla.org/projects/devtools)). We were able to make steady progress. The integration with SpiderMonkey, Firefox’s JavaScript engine, was where work went more slowly. To tackle larger features like proper asynchronous call stacks (available now in [DevEdition](https://www.mozilla.org/en-US/firefox/developer/)), we needed to do a major cleanup. Here’s how we did that.

## Background: A Brief History of the JS Debugger

The JavaScript [debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger) in Firefox is based on the [SpiderMonkey](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey) engine’s [ Debugger API](https://developer.mozilla.org/en-US/docs/Tools/Debugger-API). This API was added in 2011. Since then, it has survived the addition of four JIT compilers, the retirement of two of them, and the addition of a WebAssembly compiler. All that, without needing to make substantial changes to the API’s users.

`Debugger`

imposes a performance penalty only temporarily, while the developer is closely observing the debuggee’s execution. As soon as the developer looks away, the program can return to its optimized paths.A few key decisions (some ours, others imposed by the situation) influenced the `Debugger`

‘s implementation:

- For better or worse, it is a central tenet of Firefox’s architecture that JavaScript code of different privilege levels can share a single heap. Object edges and function calls cross privilege boundaries as needed. SpiderMonkey’s
*compartments*ensure the necessary security checks get performed in this free-wheeling environment. The API must work seamlessly across compartment boundaries. `Debugger`

is an*intra-thread*debugging API: events in the debuggee are handled on the same thread that triggered them. This keeps the implementation free of threading concerns, but invites other sorts of complications.`Debugger`

s must interact naturally with garbage collection. If an object won’t be missed, it should be possible for the garbage collector to recycle it, whether it’s a`Debugger`

, a debuggee, or otherwise.- A
`Debugger`

should observe only activity that occurs within the scope of a given set of JavaScript global objects (say, a window or a sandbox). It should have no effect on activity elsewhere in the browser. But it should also be possible for multiple`Debugger`

s to observe the same global, without too much interference.

## Garbage Collection

People usually explain garbage collectors by saying that they recycle objects that are “unreachable”, but this is not quite correct. For example, suppose we write:

```
fetch("https://www.example.com/")
.then(res => {
res.body.getReader().closed.then(() => console.log("stream closed!"))
});
```


Once we’re done executing this statement, none of the objects it constructed are reachable by the rest of the program. Nonetheless, the [WHATWG](https://whatwg.org/) specification forbids the browser from garbage collecting everything and terminating the [ fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API). If it were to do so, the message would not be logged to the console, and the user would know the garbage collection had occurred.

Garbage collectors obey an interesting principle: an object may be recycled only if it never would be missed. That is, an object’s memory may be recycled only if doing so would have no observable effect on the program’s future execution—beyond, of course, making more memory available for further use.

### The Principle in Action

Consider the following code:

```
// Create a new JavaScript global object, in its own compartment.
var global = newGlobal({ newCompartment: true });
// Create a new Debugger, and use its `onEnterFrame` hook to report function
// calls in `global`.
new Debugger(global).onEnterFrame = (frame) => {
if (frame.callee) {
console.log(`called function ${frame.callee.name}`);
}
};
global.eval(`
function f() { }
function g() { f(); }
g();
`);
```


When run in SpiderMonkey’s JavaScript shell (in which `Debugger`

constructor and the `newGlobal`

function are immediately available), this prints:

```
called function g
called function f
```


Just as in the `fetch`

example, the new `Debugger`

becomes unreachable by the program as soon as we are done setting its `onEnterFrame`

hook. However, since all future function calls within the scope of `global`

will produce console output, it would be incorrect for the garbage collector to remove the `Debugger`

. Its absence would be observable as soon as `global`

made a function call.

A similar line of reasoning applies for many other `Debugger`

facilities. The `onNewScript`

hook reports the introduction of new code into a debuggee global’s scope, whether by calling `eval`

, loading a `<script>`

element, setting an `onclick`

handler, or the like. Or, setting a breakpoint arranges to call its handler function each time control reaches the designated point in the code. In all these cases, debuggee activity calls functions registered with a `Debugger`

, which can do anything the developer likes, and thus have observable effects.

This case, however, is different:

```
var global = newGlobal({ newCompartment: true });
new Debugger(global);
global.eval(`
function f() { }
function g() { f(); }
g();
`);
```


Here, the new `Debugger`

is created, but is dropped without any hooks being set. If this `Debugger`

were disposed of, no one would ever be the wiser. It should be eligible to be recycled by the garbage collector. Going further, in the `onEnterFrame`

example above, if `global`

becomes unnecessary, with no timers or event handlers or pending fetches to run code in it ever again, then `global`

, its `Debugger`

, and its handler function must all be eligible for collection.

The principle is that `Debugger`

objects are not anything special to the GC. They’re simply objects that let us observe the execution of a JavaScript program, and otherwise follow the same rules as everyone else. JavaScript developers appreciate knowing that, if they simply avoid unnecessary entanglements, the system will take care of cleaning up memory for them as soon as it’s safe to do so. And this convenience extends to code using the `Debugger`

API.

### The Implementation

Looking through the description above, it seems clear that when a `Debugger`

has an `onEnterFrame`

hook, an `onNewScript`

hook, or something else like that, its debuggee globals hold an owning reference to it. As long as those globals are alive, the `Debugger`

must be retained as well. Clearing all those hooks should remove that owning reference. Thus, the liveness of the global no longer guarantees that the `Debugger`

will survive. (References from elsewhere in the system might, of course.)

And that’s pretty much how it’s done. At the C++ level, each JavaScript global has an associated `JS::Realm`

object, which owns a table of `DebuggerLink`

objects, one for each `Debugger`

of which it is a debuggee. Each `DebuggerLink`

object holds an *optional* strong reference to its `Debugger`

. This is set when the `Debugger`

has interesting hooks, and cleared otherwise. Hence, whenever the `Debugger`

has hooks set, there is a strong path, via the `DebuggerLink`

intermediary, from its debuggee globals to the `Debugger`

. In contrast, when the hooks are clear, there is no such path.

A breakpoint set in a script behaves similarly. It acts like an owning reference from that script to the breakpoint’s handler function and the `Debugger`

to which it belongs. As long as the script is live, the handler and `Debugger`

must remain alive, too. Or, if the script is recycled, certainly that breakpoint will never be hit again, so the handler might as well go, too. And if *all* the `Debugger`

‘s breakpoints’ scripts get recycled, then the scripts no longer protect the `Debugger`

from collection.

However, things were not always so straightforward.

### What’s Changed

Originally, `Debugger`

objects had an `enabled`

flag, which, when set to `false`

, immediately disabled all the `Debugger`

‘s hooks and breakpoints. The intent was to provide a single point of control. In this way, the Firefox Developer Tools server could neutralize a `Debugger`

(say, when the toolbox is closed), ensuring that it would have no further impact on the system. Of course, simply clearing out the `Debugger`

‘s set of debuggee globals—a capability we needed for other purposes anyway—has almost exactly the same effect. So this meant the `enabled`

flag was redundant. But, we reasoned, how much trouble could a simple boolean flag really cause?

What we did not anticipate was that the presence of the `enabled`

flag made the straightforward implementation described above seem impractical. Should setting `enabled`

to `false`

really go and clear out all the breakpoints in the debuggee’s scripts? And should setting it back to `true`

go and put them all back in? That seemed ridiculous.

So, rather than treating globals and scripts as if they owned references to their interested `Debugger`

s, we added a new phase to the garbage collection process. Once the collector had found as many objects as possible to retain, we would loop over all the `Debugger`

s in the system. We would ask each one: Are any of your debuggees sure to be retained? Do you have any hooks or breakpoints set? And, are you enabled? If so, we marked the `Debugger`

itself for retention.

Naturally, once we decided to retain a `Debugger`

, we alsohad to retain any objects it or its handler functions could possibly use. Thus, we would restart the garbage collection process, let it run to exhaustion a second time, and repeat the scan of all `Debuggers`

.

### Cleaning up Garbage Collection

In the fall of 2019, [Logan Smyth](https://twitter.com/loganfsmyth), [Jason Laster](https://twitter.com/jasonlaster11), and I undertook a series of debugger cleanups. This code, named `Debugger::markIteratively`

, was one of our targets. We deleted the `enabled`

flag, introduced the owning edges described above (among others), and shrunk `Debugger::markIteratively`

down to the point that it could be safely removed. This work was filed as [bug 1592158](https://bugzilla.mozilla.org/show_bug.cgi?id=1592158): “Remove `Debugger::hasAnyLiveFrames`

and its vile henchmen”. (In fact, in a sneak attack, Logan removed it as part of a patch for a blocker, [bug 1592116](https://bugzilla.mozilla.org/show_bug.cgi?id=1592116).)

The SpiderMonkey team members responsible for the garbage collector also appreciated our cleanup. It removed a hairy special case from the garbage collector. The replacement is code that looks and behaves much more like everything else in SpiderMonkey. The idea that “this points to that; thus if we’re keeping this, we’d better keep that, too” is the standard path for a garbage collector. And so, this work turned `Debugger`

from a headache into (almost) just another kind of object.

## Compartments

The `Debugger`

API presented the garbage collector maintainers with other headaches as well, in its interactions with [SpiderMonkey compartments](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Compartments) and zones.

In Firefox, the JavaScript heap generally includes a mix of objects from different privilege levels and origins. Chrome objects can refer to content objects, and vice versa. Naturally, Firefox must enforce certain rules on how these objects interact. For example, content code might only be permitted to call certain methods on a chrome object. Or, chrome code might want to see only an object’s original, web-standard-specified methods, regardless of how content has toyed with its prototype or reconfigured its properties.

(Note that Firefox’s ongoing [‘Fission’](https://wiki.mozilla.org/Project_Fission) project will segregate web content from different origins into different processes, so inter-origin edges will become much less common. But even after Fission, there will still be interaction between chrome and content JavaScript code.)

### Runtimes, Zones, and Realms

To implement these checks, to support garbage collection, and to support the web as specified, Firefox divides up the JavaScript world as follows:

- A complete world of JavaScript objects that might interact with each other is called a
*runtime*. - A runtime’s objects are divided into
*zones*, which are the units of garbage collection. Every garbage collection processes a certain set of zones. Typically there is one zone per browser tab. - Each zone is divided into
*compartments*, which are units of origin or privilege. All the objects in a given compartment have the same origin and privilege level. - A compartment is divided into
*realms*, corresponding to JavaScript window objects, or other sorts of global objects like sandboxes or JSMs.

Each script is assigned to a particular realm, depending on how it was loaded. And each object is assigned a realm, depending on the script that creates it.

Scripts and objects may only refer directly to objects in their own compartment. For inter-compartment references, each compartment keeps a collection of specialized proxies, called *cross-compartment wrappers*. Each of these wrappers represents a specific object in another compartment. These wrappers intercept all property accesses and function calls and apply security checks. This is done to decide whether they should proceed, based on the relative privilege levels and origins of the wrapper’s compartment and its referent’s compartment. Rather than passing or returning an object from one compartment to another, SpiderMonkey looks up that object’s wrapper in the destination compartment (creating it if none exists). Then it hands over the wrapper instead of the object.

### Wrapping Compartments

An extensive system of assertions, in the garbage collector but also throughout the rest of SpiderMonkey, verify that no direct inter-compartment edges are ever created. Furthermore, scripts must only directly touch objects in their own compartments.

But since every inter-compartment reference must be intercepted by a wrapper, the compartments’ wrapper tables form a convenient registry of all inter-*zone* references as well. This is exactly the information that the garbage collector needs to collect one set of zones separately from the rest. If an object has no wrappers representing it in compartments outside its own zone, then the collector knows. All without having to examine the entire runtime. No other zone would miss that object if it were recycled.

### Inter-Compartment Debugging

The `Debugger`

API’s `Debugger.Object`

objects throw a wrench into this neat machinery. Since the debugger server is privileged chrome code, and the debuggee is usually content code, these fall into separate compartments. This means that a `Debugger.Object`

‘s pointer to its reference is an inter-compartment reference.

But the `Debugger.Objects`

cannot be cross-compartment wrappers. A compartment may have many `Debugger`

objects, each of which has its own flock of `Debugger.Objects`

, so there may be many `Debugger.Objects`

referring to the same debuggee object in a single compartment. (The same is true of `Debugger.Script`

and other API objects. We’ll focus on `Debugger.Object`

here for simplicity.)

Previously, SpiderMonkey coped with this by requiring that each `Debugger.Object`

be paired with a special entry to the compartment’s wrapper table. The table’s lookup key was not simply a foreign object, but a (`Debugger`

, foreign object) pair. This preserved the invariant that the compartments’ wrapper tables had a record of all inter-compartment references.

Unfortunately, these entries required special treatment. An ordinary cross-compartment wrapper can be dropped if its compartment’s objects no longer point there, since an equivalent wrapper can be constructed on demand. But a `Debugger.Object`

must be retained for as long as its `Debugger`

and referent are alive. A user might place a custom property on a `Debugger.Object`

or use it as a key in a weak map. That user might expect to find the property or weak map entry when encountering the corresponding debuggee object again. Also, special care is required to ensure that the wrapper table entries are reliably created and removed in sync with `Debugger.Object`

creation, even if out-of-memory errors or other interruptions arise.

### Cleaning up Compartments

As part of our Fall 2019 code cleanup, we removed the special wrapper table entries. By simply consulting the `Debugger`

API’s own tables of `Debugger.Objects`

, we changed the garbage collector find cross-compartment references. This is `Debugger`

-specific code, which we would, of course, prefer to avoid, but the prior arrangement was also `Debugger`

-specific. The present approach is more direct. It looks more like ordinary garbage collector tracing code. This removes the need for careful synchronization between two tables.

## Forced Returns and Exceptions

When SpiderMonkey calls a `Debugger`

API hook to report some sort of activity in the debuggee, most hooks can return a *resumption value* to say how the debuggee should continue execution:

`undefined`

means that the debuggee should proceed normally, as if nothing had happened.- Returning an object of the form
`{ throw: EXN }`

means that the debuggee should proceed as if the value`EXN`

were thrown as an exception. - Returning an object of the form
`{ return: RETVAL }`

means that the debuggee should return immediately from whatever function is running now, with`RETVAL`

as the return value. `null`

means that the debuggee should be terminated, as if by the slow script dialog.

In SpiderMonkey’s C++ code, there was an enumerated type named `ResumeMode`

, which had values `Continue`

, `Throw`

, `Return`

, and `Terminate`

, representing each of these possibilities. Each site in SpiderMonkey that needed to report an event to `Debugger`

and then respect a resumption value needed to have a `switch`

statement for each of these cases. For example, the code in the bytecode interpreter for entering a function call looked like this:

```
switch (DebugAPI::onEnterFrame(cx, activation.entryFrame())) {
case ResumeMode::Continue:
break;
case ResumeMode::Return:
if (!ForcedReturn(cx, REGS)) {
goto error;
}
goto successful_return_continuation;
case ResumeMode::Throw:
case ResumeMode::Terminate:
goto error;
default:
MOZ_CRASH("bad DebugAPI::onEnterFrame resume mode");
}
```


### Discovering Relevant SpiderMonkey Conventions

However, Logan Smyth noticed that, except for `ResumeMode::Return`

, all of these cases were already covered by SpiderMonkey’s convention for ‘fallible operations’. According to this convention, a C++ function that might fail should accept a `JSContext*`

argument, and return a `bool`

value. If the operation succeeds, it should return `true`

; otherwise, it should return `false`

and set the state of the given `JSContext`

to indicate a thrown exception or a termination.

For example, given that JavaScript objects can be proxies or have getter properties, fetching a property from an object is a fallible operation. So SpiderMonkey’s `js::GetProperty`

function has the signature:

```
bool js::GetProperty(JSContext* cx,
HandleValue v, HandlePropertyName name,
MutableHandleValue vp);
```


The value `v`

is the object, and `name`

is the name of the property we wish to fetch from it. On success, `GetProperty`

stores the value in `vp`

and returns `true`

. On failure, it tells `cx`

what went wrong, and returns `false`

. Code that calls this function might look like:

```
if (!GetProperty(cx, obj, id, &value)) {
return false; // propagate failure to our caller
}
```


All sorts of functions in SpiderMonkey follow this convention. They can be as complex as evaluating a script, or as simple as allocating an object. (Some functions return a `nullptr`

instead of a `bool`

, but the principle is the same.)

This convention subsumes three of the four `ResumeMode`

values:

`ResumeMode::Continue`

is equivalent to returning`true`

.`ResumeMode::Throw`

is equivalent to returning`false`

and setting an exception on the`JSContext`

.`ResumeMode::Terminate`

is equivalent to returning`false`

but setting no exception on the`JSContext`

.

The only case this doesn’t support is `ResumeMode::Return`

.

### Building on SpiderMonkey Conventions

Next, Logan observed that SpiderMonkey is already responsible for reporting all stack frame pops to the `DebugAPI::onLeaveFrame`

function, so that `Debugger`

can call frame `onPop`

handlers and perform other bookkeeping. So, in principle, to force an immediate return, we could:

- stash the desired return value somewhere;
- return
`false`

without setting an exception to force termination; - wait for the termination to propagate through the current function call, at which point SpiderMonkey will call
`DebugAPI::onLeaveFrame`

; - recover our stashed return value, and store it in the right place in the stack frame; and finally
- return
`true`

as if nothing had happened, emulating an ordinary return.

With this approach, there would be no need for the `ResumeMode`

enum or special handling at `DebugAPI`

call sites. SpiderMonkey’s ordinary rules for raising and propagating exceptions are already very familiar to any SpiderMonkey developer. Those rules do all the work for us.

As it turns out, the machinery for stashing the return value and recognizing the need for intervention in `DebugAPI::onLeaveFrame`

*already existed* in SpiderMonkey. Shu-Yu Guo had implemented it years ago to handle a rare case involving slow script timeouts and single-stepping.

With this collection of insights, Logan was able to turn the call sites at which SpiderMonkey reports activity to `Debugger`

into call sites just like those of any other fallible function. The call to `DebugAPI::onEnterFrame`

shown above now reads, simply:

```
if (!DebugAPI::onEnterFrame(cx, activation.entryFrame())) {
goto error;
}
```


## Other Cleanups

We carried out a number of other minor cleanups as part of our Fall 2019 effort:

- We split the file
`js/src/vm/Debugger.cpp`

, originally 14k lines long and containing the entire`Debugger`

implementation, into eight separate source files, and moved them to the directory`js/src/debugger`

.[Phabricator](https://www.phacility.com/phabricator/)no longer refuses to colorize the file because of its length. - Each
`Debugger`

API object type,`Debugger.Object`

,`Debugger.Frame`

,`Debugger.Environment`

,`Debugger.Script`

, and`Debugger.Source`

, is now represented by its own C++ subclass of`js::NativeObject`

. This lets us use the organizational tools C++ provides to structure and scope their implementation code. We can also replace dynamic type checks in the C++ code with types. The compiler can check those at compile time. - The code that lets
`Debugger.Script`

and`Debugger.Source`

refer to both JavaScript and WebAssembly code was simplified so that`Debugger::wrapVariantReferent`

, rather than requiring five template parameters, requires only one–and one that could be inferred by the C++ compiler, to boot.

I believe this work has resulted in a substantial improvement to the quality of life of engineers who have to deal with `Debugger`

‘s implementation. I hope it is able to continue to serve Firefox effectively in the years to come.

## About Jim Blandy

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.