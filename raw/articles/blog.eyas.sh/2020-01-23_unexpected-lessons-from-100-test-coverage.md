---
title: Unexpected Lessons from 100% Test Coverage
url: https://blog.eyas.sh/2020/01/unexpected-lessons-from-100-test-coverage/
author: Eyas Sharaiha
published: '2020-01-23'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

The conventional wisdom of the software engineering community is that striving to 100% test coverage is a fool’s errand. It won’t necessarily help you catch all bugs, and it might lead you down questionable paths when writing your code.

My recent attempts at 100% test coverage showed me the answer is much more
subtle. At times I was tempted to make questionable code changes just for the
sake of coverage. In some of those times, I did succumb. Yet, I found that
often, there is an enlightened way to *both* cover a branch *and* make the code
better for it. Blind 100% coverage can cause us to make unacceptable
compromises. If we constrain ourselves with only making the codebase better,
however, then thinking about 100% coverage can change the way we think about a
codebase. The story of my 100% test coverage attempt is a story of both the good
and the bad.

Last year I came across a thread from NPM creator Isaac Z. Schlueter advocating for 100% test coverage:

100% test coverage: because seatbelts are good, even though they don’t provide immortality.

— isaacs 💙💜💖🏳️🌈 ∞ (@izs)

[July 22, 2019]

Schlueter alluded to a *mentality shift* that a developer achieves that piqued
my interest:

The mindset change from writing code with full coverage took me a while to fully incorporate into my work. It’s made me a better developer, because I’ve gotten into the habit of asking “How does one get here?” whenever I’m writing or reading code.

— isaacs 💙💜💖🏳️🌈 ∞ (@izs)

[July 24, 2019]

## Road to 100

![Coveralls.io screen grab for schema-dts showing how it got to 100% Test Coverage](../../assets/f28e40c99690e5d5.img)

I decided that [schema-dts](https://github.com/google/schema-dts) would be the
perfect candidate for the 100% test coverage experiment. Given
[N-Triples](https://en.wikipedia.org/wiki/N-Triples) as an input, schema-dts
[generates TypeScript types describing valid JSON-LD literals](https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/)
for that ontology. I’ve been more and more interested recently in getting it to
stability, and understanding where there’s headroom in the codebase.

### The Setup

To start, I didn’t have a way to compute test coverage of my project in its
current state. I ended up switching my test runner from Jasmine to
[Mocha](https://mochajs.org/) for its lcov support. This being a TypeScript
project, though, I had to enable source maps, and use `ts-node`

to get coverage
numbers of my actual .ts source
([PR #56](https://github.com/google/schema-dts/pull/56)). I used Istanbul’s
[nyc](https://istanbul.js.org/) to get coverage runs working locally.
[Coveralls](https://coveralls.io/) integrates with nyc nicely to host online
tracking of code coverage time. Coveralls also integrates seamlessly with Travis
CI and gates all PRs by their ΔCoverage
([PR #57](https://github.com/google/schema-dts/pull/57)).

My first *real* run after setting things up had a
[%78.72 test coverage](https://coveralls.io/builds/28108326). That’s not too
bad, I thought. My existing tests belonged to broadly two general categories:

- A small amount of unit tests.
- Since my project is outputting a bunch of code, I relied heavily on a large
suite of
*baseline tests*inspired by[TypeScript’s own suite of baseline tests](https://github.com/microsoft/TypeScript/wiki/systems-baselines).

These baseline tests definitely *covered* a lot of lines of code that they
didn’t really exercise, which is part of why that number was high. That itself
can be an argument that 100% test coverage is a meaningless number. Schlueter’s
promise of 100% test coverage, however, is that the act of *getting to that long
tail* can have transformative effects of *how I think about my own code*. I
wanted to try my luck at that first hand. If we wanted to be more confident
about our covered lines are truly being *tested*,
[mutation testing](https://en.wikipedia.org/wiki/Mutation_testing) might do
better wonders than test coverage.

### Happy Times: The Low Hanging Fruit

A Schema.org-like ontology can declare a certain class, property, or enum value
as *deprecated* by marking it with a
[supersededBy](https://schema.org/supersededBy) predicate. schema-dts handles
this in one of two ways: either marking it with `@deprecated`

JSDoc comments in
the code, or stripping those declarations entirely.

Looking at my coverage report, swaths of untested code become apparent. For
example, I
[never attempted to generate a @deprecated class](https://coveralls.io/builds/28108326/source?filename=src/ts/class.ts#L125).
Ok, let’s fix that. And I

[catch a real bug](https://github.com/google/schema-dts/pull/60)that my few unit tests hadn’t caught. I increased coverage by 9.8%, added some baseline tests of deprecation, and added some N-Triple parsing unit tests that I had never gotten around to.

Testing my Argparse setup showed me
[one of my default flag values was wrong](https://github.com/google/schema-dts/pull/76)
(albeit in a harmless way).

### Questionable Times

#### Log Tests?

A lot of uncovered lines I was seeing had to do with logging statements for
things we skip or drop, or recoverable conditions we handle. A lot of these logs
are warnings that happen in real Schema.org N-Triple files. For example, we
never handle the `sameAs`

or `inverseOf`

triples describing properties. And if
we see two comments describing the same class or property, the newer one wins.

Intuition would have it that a log statement should not be tested. But for good and bad reasons, I decided some baseline tests on log output might be desirable.

And I used that to
[add a log test for the multiple comments case](https://github.com/google/schema-dts/pull/64/commits/60afa0d9ddb09f0fd5118e6b73876f4eeae3976e)
when a unit test would have sufficed. That’s pretty questionable. But I was
caught up in my zeal.

*Some* level of logging-based test might be defensible insofar as (1) we’re
observing changes to our user interactions, and (2) it’s documenting the
warnings/limitations of our code. Maybe one can view *some* logging-based tests
as an equivalent to a screenshot diffing UI test? Or maybe I’m really trying to
explain myself. Still, I felt less bad about adding
[a test showing a warning when parsing a common triple](https://github.com/google/schema-dts/pull/64/commits/2da73f6df3a04c17777e3e33ea45c9694addbe2d)
than I did about that comment test.

#### Code Golf?

Another way to get around some of these `if (case) { Log(...); }`

cases is to
instead write `warnIf(case, ...)`

. I think most people would agree a change like
this is unhelpful at best. One might make the Machiavellian argument that such
code golf is justified by the ends: once you get to 100% test coverage, you’ll
stay there, and you’ll think critically about all your future diffs.

### Constraining myself to *Neutral* and *Positive* ‘Code Golf’

One thing I tried doing halfway through is to make sure I don’t engage in any ‘code golf’ that makes the codebase worse in the name of test coverage. (Depending on how you define code golf, it might tautologically mean it makes the codebase worse; here, I really just mean it as any creative rearranging of code for the sake of coverage.)

What I found, though, is some code golf actually helped me think more clearly about the code. Even in cases where the codebase itself looked about the same, I now had a new vocabulary to talk about error conditions. In some other cases, covering lines of code drove me from making run-time guarantees in the code to making compile-time guarantees in the code (definitely a positive).

Let’s walk through some examples.

#### Neutral: Clarifying Assertions *versus* Errors

I had transformation functions that took RDF triples and converted them to an intermediate representation of classes. These functions had some issues:

##### A: Intra-function Impossibility

There was a
[line](https://coveralls.io/builds/28158052/source?filename=src/transform/toClass.ts#L91)
in my code that my tests never covered. It looked something like this:

```
// Top-level module:
const wellKnownTypes = [ ... ]; // Top-level var with more than one "Type".
const dataType = ...;
function ForwardDeclareClasses(topics: ReadonlyArray<TypedTopic>): ClassMap {
const classes = new Map<string, Class>();
for (const wk of wellKnownTypes) {
classes.set(wk.subject.toString(), wk);
}
classes.set(dataType.subject.toString(), wk);
for (const topic of topics) {
// ...
}
if (classes.size === 0) {
throw new Error('Expected Class topics to exist.');
}
return classes;
}
```


As you can see just reading this function and knowing: `(classes.size === 0)`

will never happen. For one, there’s a `classes.set(K, V)`

a few sections above.
And we set a few other key-value pairs from this `wellKnownTypes`

array that is
hard-coded to always have a set number of elements.

One can try to understand the point of this error: It could be to show that none
of the RDF triples we got are turned into classes (in which case we might want
to compare `classes.size`

with `wellKnownTypes.length + 1`

instead).
Alternatively, it can be a poorly-placed verification for when we had less
confidence that we were building classes properly, and had no clear concept of
such “well known” types.

In my case, creating a map with just the well knows seemed fine. If the ontology is empty or missing data, we’ll likely find it at earlier steps or later ones. And the error gives no clear context as to what’s going wrong. So in my case, the answer was to kill it:

```
- if (classes.size === 0) {
- throw new Error('Expected Class topics to exist.');
- }
```


##### B: Inter-Function Assertion

Another error I saw looked like this:

```
function ForwardDeclareClasses(topics: ReadonlyArray<TypedTopic>): ClassMap {
// ...
// ...
for (const topic of topics) {
if (!IsClass(topic)) continue;
// ...
classes.set(
topic.Subject.toString(),
new Class(topic.Subject /* ... */)
);
}
// ...
return classes;
}
function BuildClasses(topics: ReadonlyArray<TypedTopic>, classes: ClassMap) {
for (const topic of topics) {
if (!IsClass(topic)) continue;
const cls = classes.get(topic.Subject.toString());
if (!cls) {
throw new Error(/**... class should have been forward declared */);
}
toClass(cls, topic, classes);
}
}
```


In this case, the `(!cls)`

condition was always false. This should make sense:
`ForwardDeclareClasses`

literally checks if a `TypedTopic`

satisfies
`IsClass()`

, and, if so, *unconditionally* adds it to the map. `BuildClasses`

assert that a topic matching `IsClass`

exists in the map.

One way to get test coverage for this line is to export `BuildClasses`

and test
it. But that seems like it goes against the spirit of making the codebase
better. A better approach is ask what this line is trying to do:

##### Interlude: Expectations, Errors, and Assertions

Sometimes, we assert things because they either…

- are
*error conditions*that can happen in the wild due to poor data or input, *shouldn’t happen*, and*if they did*it’s a sign of a bug in our code, or*shouldn’t happen*, and*if they did*it’s a sign of cosmic radiation.

I decided to differentiate these. If my test coverage report complains about an uncovered…

*error condition*, I should test it. If I can’t, I should refactor my code to make it testable;*assertion*that might indicate a bug, some code golf to make these always run might be in order (more on that in a bit);*assertion*that is totally impossible, maybe I should delete it.

I refer to #1 as an **error condition**. Test these. For assertions, I often
found that the line between #2 and #3 is often the *function* boundary (this
isn’t always true). Cases of *intra-function* assertions (like case study **A**
above) seem so useless that we’re better off removing them. Cases of
*inter-function* assertions (like this case) seem useful enough to stay.

##### The Fix

I found that this distinction is not just helpful to split hairs: it’s also very
helpful for someone reading the code: Is this error something that *can happen
in normal operation*? or, is it *a sign of a bug*? I decided to make this clear:

- Normal error conditions:
`if`

+`throw`

, or similar. - Bug assertions:
`assert`

and`assertXyz`

variants.

With that, I ended up with
[this change](https://github.com/google/schema-dts/pull/73/commits/11c9f64397e0ddbe29f09ac1b8945fd72d7ad213):

```
+import {ok} from 'assert';
+
+const assert: <T>(item: T|undefined) => asserts
+
function BuildClasses(topics: ReadonlyArray<TypedTopic>, classes: ClassMap) {
for (const topic of topics) {
if (!IsClass(topic)) continue;
const cls = classes.get(topic.Subject.toString());
+ assert(cls);
- if (!cls) {
- throw new Error(/**... class should have been forward declared */);
- }
toClass(cls, topic, classes);
}
}
```


![The fix increased my code coverage totals by 1.3% to 99.053% at the itme](../../assets/ae9188b85c5a745d.img)

Here, thinking about covering a line of code fundamentally helped me communicate
what my code does more effectively. A lot of the “moving things around” that I
had to do is very much semantic code golf (that *happily* happens to give a
better test coverage score), but I’d like to think it’s net positive.

#### Positive: Restructure code to achieve *compile-time* guarantees rather than *run-time* guarantees

I already showed that some lines that are *never* covered by test runs are
assertions that *should never happen*. Sometimes, we can restructure our code to
make compile-time claims about our code’s structure, rather than worry about it.

I’ll be more specific: my code has a `parseComment`

function that uses
[htmlparser2](https://www.npmjs.com/package/htmlparser2) to turn HTML comments
in [JSDoc](https://jsdoc.app/) tagged comments. In that code, we define a new
`htmlparser2.Parser`

that handles known tags and throws on unknown tags. It
looks something like this:

```
function parseComment(comment: string): string {
const result: string[] = [];
const parser = new Parser({
ontext: text => result.push(replace(text)),
onopentag: (tag, attrs) => {
switch (tag) {
case 'a': result.push(`{@link ${attrs['href']} `); break;
case 'em': case 'i': result.push('_'); break;
case 'strong': case 'b': reslt.push('__'); break;
// ...
default: throw new Error(`Unknown tag "${tag}".`); /* 1 */
},
onclosetag: tag => {
case 'a': result.push('}'); break;
case 'em': case 'i': result.push('_'); break;
case 'strong': case 'b': reslt.push('__'); break;
// ...
default: throw new Error(`Unknown tag "${tag}".`); /* 2 */
}
}
});
parser.write(comment);
parser.end();
// ... turn result into 'lines'
return lines.length === 1 ? `* lines[0] ` :
('*\n *' + lines.join('\n *') + '\n ');
}
```


Initially, the two `default`

cases in the above snippet where uncovered. I can
easily cover the default in `onopentag`

: I added a test for an unknown tag and
saw it failed. Great. Our test coverage now includes this line.

It’s much harder to get the second covered, though: If an unknown opening tag
exists, it will throw on open. A self-closing tag counts as an open tag. Closing
a never-opened tag is bad HTML, but doesn’t actually register as a closed tag.
[This is valid HTML](https://html.spec.whatwg.org/multipage/parsing.html#tokenization):
an end tag token with no matching start tag is not a valid token.

In other words, this line will never trigger.

##### The Fix

Should we remove it? Well… right now, with the code as stated, this line
actually has *some utility*: if the developer adds some handling for a start tag
(e.g. `<table>`

or `<td>`

), we’ll notice a run-time error if we omit adding the
end tag handler as well.

That’s kind of useful. But the nice thing about using TypeScript is that we can structure our code so that run-time guarantees are turned into compile-time guarantees.

In our case, [this change](https://github.com/google/schema-dts/pull/80) made
things much better. Here’s a summarized version:

```
// Tag Management: Define functions describing what to do with HTML tags in our
// comments.
interface OnTag {
open(attrs: { [key: string]: string }): string;
close(): string;
}
// Some handlers for behaviors that apply to multiple tags:
const em: OnTag = { open: () => "_", close: () => "_" };
const strong = { open: () => "__", close: () => "__" };
// ...
// Our top-level tag handler.
const onTag = new Map<string, OnTag>([
["a", { open: (attrs) => `{@link ${attrs["href"]} `, close: () => "}" }],
["em", em],
["i", em],
["strong", strong],
["b", strong],
// ...
]);
function parseComment(comment: string): string {
const result: string[] = [];
const parser = new Parser({
ontext: (text: string) => result.push(replace(text)),
onopentag: (tag: string, attrs: { [key: string]: string }) => {
const handler = onTag.get(tag);
if (!handler) {
throw new Error(`Unknown tag "${tag}".`);
}
if (handler.open) {
result.push(handler.open(attrs));
}
},
onclosetag: (tag: string) => {
const handler = onTag.get(tag);
assert(handler);
if (handler.close) {
result.push(handler.close());
}
},
});
parser.write(comment);
parser.end();
// ... turn result into 'lines'
return lines.length === 1
? `* ${lines[0]} `
: "*\n * " + lines.join("\n * ") + "\n ";
}
```


By unifying tag handlers between *open* and *close* tags, a user wouldn’t forget
to add a closed tag handler or *vice-versa*, as the compiler defines a unified
interface for what ”*handling a tag*” looks line.

In general, assertions and guarantees about parallel *code* structures (e.g.
parallel switch cases, etc.) *and* parallel *data structures* (e.g. parallel
lists or maps) are tenuous. If you have two structures (code, or a data
structure) that need to agree about what elements they have, etc. you might
often benefit from rearranging them structurally. Google’s Testing Blog covered
the *data structure version of this* in it’s
[Code Health: Obsessed With Primitives?](https://testing.googleblog.com/2017/11/obsessed-with-primitives.html#docs-internal-guid-c44fb159-b745-02ec-a269-ec156b175826)
episode.

### Uncovering Historical Choices and Fixes

Some of the lines we never covered very clearly looked like edge cases/fixes for
*something*. Yet, it often was not clear what the edge case was or why we did
it.

Ideally, as one introduces fixes for edge cases, they will also introduce the tests that exercise them. If you ever skip introducing a test, however, you might never get around to it. Until you look at the results of your test coverage run, that is.

Once we see an uncovered line, it becomes a great opportunity to track *why* it
was added, and retroactively add the tests for it. Tools like `git blame`

and
`git log`

are great resources to pinpoint the edge case in time, and find the
relevant commit message.

I ran into two of these cases:
[a parser-level term that was being skipped](https://github.com/google/schema-dts/pull/73/commits/df8c97e199bc235cba76a008ab15b5cde8a24a97#diff-38d6d4505badf711e266526e2c572310)
and some
[specific enum handling](https://github.com/google/schema-dts/pull/74/commits/3beea7319520c8ddaa5956947c46563287a08f88#diff-55504ee5640737677ebdfceb255d5bd5).
Both of these looked like big issues in
[Schema.org 3.4](https://schema.org/docs/releases.html) that were silently fixed
after. In both cases, I added comments explaining the triple that causes this,
and where to find it, and added tests exercising this case. Great!

### Opportunity to Simplify Code

As test coverage approaches 100%, it starts to become a proxy for code unreachability analysis. While sometimes it will simply point out shortcomings in your testing (also good), at others, it will point to unreachable code that your traditional static analysis tools won’t detect. This is because test coverage is calculated on code that actually runs, rather than some inspection of the control flow graph.

Here’s an example:

```
export class Class {
// ...
private baseNode(skipDeprecatedProperties: boolean, context: Context):
TypeNode {
// ...
const parentNode = /* ... */;
const isRoot = parentNode === null;
const propLiteral = createTypeLiteralNode([
// Add an '@id' property for the root.
...(isRoot ? [IdPropertyNode()] : []),
// ... then everything else.
...this.properties()
.filter(property => !property.deprecated || !skipDeprecatedProperties)
.map(prop => prop.toNode(context))
]);
if (parentNode && propLiteral.members.length > 0) {
return createIntersectionTypeNode([parentNode, propLiteral]);
} else if (parentNode) {
return parentNode;
} else if (propLiteral.members.length > 0) {
return propLiteral;
} else {
return createTypeLiteralNode([]);
}
}
}
```


Here, the tests never covered the final `else`

branch. This makes sense: this
line only happens if `parentNode`

was null *and* `propLiteral`

had 0 members.
Except `propLiteral`

will always have at least 1 member (`@id`

) when it has no
parent.

The other interesting part about this branch, by the way, is that `propLiteral`

is itself a type literal node. Therefore, if `propLiteral.members.length === 0`

,
it would be equivalent to the node being returned in line 25, an empty type
literal node.

Here,
[the fix](https://github.com/google/schema-dts/pull/72/files#diff-0d6e1b40580e3ffa5cb049dd023d0610)
was simple:

```
- } else if (propLiteral.members.length > 0) {
- return propLiteral;
} else {
- return createTypeLiteralNode([]);
+ return propLiteral;
}
```


## Reflections on 100

While getting to 100 involved making some sacrifices, it also allowed me to:

- fix a lot of bugs,
- catch and fix redundancies in my code,
- reason about my unreachable code,
- delineate thoughtfully between
*error*cases and*assertions*, and - thoughtfully shift run-time assertions into compile-time guarantees.

Was it worth it? One way to take a crack at this is to quantify the *harm* of
the downsides and compare it to the *gain* from the upsides. Using this method,
for me, getting to 100 is clearly a net positive.

The real question, however, is not only whether the downsides are worth the
upsides: **but whether the upsides could have been achieved without the
downsides**. This, I think, is where the real opposition to 100% test coverage
comes from.

I think I could achieved *some* of these downsides by *looking at* test coverage
runs without obsessing over getting to 100%. Maybe *most*, I’m not sure. Yet, I
find it true that:

*obsessing*over every single uncovered line helped me think about reachability in a way I wouldn’t have if I just*glanced*at an unreached line;- some of the
*interesting*cases outlined above might not have been caught in a sea of red.

To me, a lot of the interesting reflections I have had over the code, and a lot of the interesting changes I made to the code, seem like they would have been hard to spot and truly think about if I wasn’t already at 95% coverage.

Ultimately, my sense is that 100% test coverage is definitely a *useful
exercise* to do at least once. It’s likely also a useful exercise to do more
than once. For me and schema-dts, I’ll be *keeping it* at 100% test coverage.
How can I not, after all? “100” is just a really, really nice number.