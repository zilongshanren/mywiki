---
title: Human Readable Test Data
url: https://blog.eyas.sh/2020/05/human-readable-test-data/
author: Eyas Sharaiha
published: '2020-05-10'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

One of the most transformative pieces of wisdom I’ve gotten in my career is
[Titus Winters](https://twitter.com/TitusWinters)’s ToTW #122 on test dataflow
clarity. The *Tip of the Week* (ToTW) series offers advice focused on C++. Like
* Testing on the Toilet*,
which offers advice and best practices for software engineering at Google
generally, it has become a fixture within the engineering culture, frequently
cited in code reviews.

If you haven’t already, check out
[ToTW #122: Test Fixtures, Clarity, and Dataflow](https://abseil.io/tips/122)
now—I’ll wait.

At it’s heart, the advice is simple: avoid overusing test setup and helpers to
obsure data flow. As a reader of a test, I should roughly be able to understand
what goes in and what comes out, without significant context switching,
scrolling up and down a large file, or switching between multiple files. This
tip follows a theme of best practices on
[DAMP versus DRY tests](https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html).

In this article, I’ll discuss two approaches to clearer data flow in tests that can benefit certain codebases.

### Human Readable Inputs and Expectations

Taking the advice from ToTW #122 a bit further: we can do a better job at
further clarifying the data flow by *inlining* a lot of the data construction.

Take this example, which already follows some of the advice from the tip:

```
ConcertProto ExpensiveConcert() {
ConcertProto concert;
ArtistProto* artist = concert.mutable_artist();
artist->set_id(kBeyonceId);
artist->set_name("Beyonce");
artist->set_avg_price(200);
concert.set_capacity(500);
return concert;
}
TEST(ConcertTest, ComputesPrice) {
OutcomeProto outcome;
outcome.set_expected(200 * 500);
outcome.set_variance(10_000);
EXPECT_THAT(
ForecastOutcome(ExpensiveConcert()),
EqualsProto(outcome));
}
```


and compare it to an example where the flow of data is further inlined:

```
TEST(ConcertTest, ComputesPrice) {
EXPECT_THAT(
ForecastOutcome(PARSE_TEXT_PROTO(R"(
artist {
id: 2584
name: "Beyonce"
avg_price: 200
}
capacity: 500
)")),
EqualsProto(PARSE_TEXT_PROTO(R"(
expected: 100000
variance: 10000
)"))
);
}
```


Direct, inlined expectations can be easily written out in most languages and testing frameworks. They’re especially easier if your codebase is centralized around a specific data format (e.g. Protocol Buffers) with a nice human-readable format.

#### Benefits

Here, a test *case* becomes *shorter*, but a test *file* (that uses
`ExpensiveConcert`

more than once) likely becomes *longer*. It’s fair to say the
data flow is much clearer here:

- we see the inputs and outputs together; and
- we see the inputs and outputs in a human-readable format, rather seeing
*how they’re procedurally constructed*.

#### Trade-offs

This isn’t always the right trade-off though,

- values like
`500 * 200`

or constructing a time from dates and timezones might be easier for someone debugging the failing test to understand than the multiplied result or a numeric timestamp; - for very large objects being inlined, actual contents of the proto might
include a lot of
*required but irrelevant*data (implementation details, lower levels of abstraction, etc.)

An apparent-downside for this approach is by design: Some apparent down-sides for this approach are by design:

If I use

`ExpensiveConcert()`

a lot, inlining it would make my test much longer.

Sure it would, but longer isn’t necessarily worse. Here’s one way of thinking about the development experience of writing a test:

You write and check-in a test once. Many times after that, when making code changes, you and other developers will run into failure in that test and debug them by either updating the test with new setup/assumptions, or updating their code to no longer break this test.

A longer test could affect each of these steps, but in most cases, it predominantly affects one-time costs of writing and reviewing the test case the first time.

When a change breaks one (or some) of the tests, your test harness tells you which tests failed and at which line, helpfully offering you a diff of what was off/missing. In many cases, the length of a test file doesn’t really matter after the point it’s already been checked in. When does it matter? Extra required parameters or data causing all the inputs needing to be changed (where previously just the free function can be edited), changing the format of the output means that all cases need to be updated, etc.

How likely this is to happen will depend on the code you’re testing at hand. This isn’t all-or-nothing. Sometimes, a free function will be the right trade-off for the input or the output. Sometimes, a free function for the “canonical” input will be used 20x times, but a few inlined alternate definitions might be used to test edge cases.

### Baseline and Snapshot Tests

What we end up with above is a bias towards declarative inputs and outputs, parsed from a human-friendly text representation. Over in JavaScript land, this dovetails slightly with a recent trend towards “Snapshot” or “Baseline” tests.

#### The TypeScript Baseline Tests

I first came across *baseline testing* while following the development of
TypeScript. Today, TypeScript relies on large suite of baseline tests including
[fourslash tests](https://github.com/microsoft/TypeScript/wiki/systems-fourslash)
and another suite known simply as
[baselines](https://github.com/microsoft/TypeScript/wiki/systems-baselines).
These tests effectively involve an input `.ts`

, potentially some other state
(e.g. the current selected symbol), and diff the output symbols/state from
reading this against a *baseline*.

Here’s an example test case for a simple class declaration:
[ClassDeclaration9.ts](https://github.com/microsoft/TypeScript/blob/master/tests/cases/compiler/ClassDeclaration9.ts),
which has snapshots of it’s corresponding
[output types](https://github.com/microsoft/TypeScript/blob/master/tests/baselines/reference/ClassDeclaration9.types),
[symbols](https://github.com/microsoft/TypeScript/blob/master/tests/baselines/reference/ClassDeclaration9.symbols),
[JS](https://github.com/microsoft/TypeScript/blob/master/tests/baselines/reference/ClassDeclaration9.js),
and
[errors](https://github.com/microsoft/TypeScript/blob/master/tests/baselines/reference/ClassDeclaration9.errors.txt).

This makes it easy to have *user-centric* tests that expose compiler bugs based
on *user-visible properties* (e.g. an expected error, wrong generated code,
buggy completions, etc.). Understanding a test failure is fairly simple (if
you’re used to the compiler internals), since it doesn’t report mismatched
expectations in internal representations, but rather by clear first-class
compiler concepts like symbols, findings, and generated code.

The test harness shows you your generated files and allows you to diff them to
determine if a new behavior is appropriate. If the diffs make sense, the
toolchain allows you to *accept baselines*. These diffs, when reviewed, also
serve the purpose of showcasing reviewers what behavioral difference your change
is triggering.

#### Jest’s Snapshot Tests

This style of baseline testing was recently popularized by Jest’s
[snapshot testing](https://jestjs.io/docs/en/snapshot-testing). In Jest,
Facebook’s JavaScript testing framework, the justification for this style of
testing has mostly been framed as an effecitve way of testing React components.
That is, they’re framed to serve a similar purpose as screenshot diff testing
for the frontend design. Instead of the visual frontend design, we test the
*structured, semantic ouptut* of components.

While the advent of this style of snapshot tests was not without disagreement,
snapshot tests have been on the rise. Kent C. Dodds made a
[great case for effective use of snapshot testing](https://kentcdodds.com/blog/effective-snapshot-testing)
in React and frontend settings.

Beyond just React’s output structure, or diffing HTML/CSS, Jest-style Snapshot testing can also be used to do the style of baseline testing described above in TypeScript. Jest allows snapshots to exist either as one file per test or inline, and also allows updating snapshots.

### Putting it all together

We can start thinking about what tests in the rest of our library code can benefit from this treatment. One way to think about this is:

- When procedural setup, fixtures, or factored-out methods obscure the data
flow of the
*inputs*, or - When procedural work obscures the state of the
*expectation*

then substituting one or both of the *inputs* and *expectation* with an inlined
human readable format is incredibly valuable.

I ended up making extensive use of inline snapshots when testing a toy compiler:

```
test("Parse_ParameterListSimple", () => {
expect(
AST.FormatTree(
ParseEntireExpression(Tokens("F(a+b)")),
/*includePositions=*/ false
)
).toMatchInlineSnapshot(`
"FunctionCallAST
Parameters:
[0] BinaryExpressionAST
Type: +
RHS: VariableAST
VariableName: b
LHS: VariableAST
VariableName: a
FunctionPointer: VariableAST
VariableName: F
`);
});
```


Compare this to a more manual test here:

```
test("Parse_ParameterListSimple", () => {
const { expression } = ParseEntireExpression(Tokens("F(a+b)"));
expect(expression).toBeInstanceOf(FunctionCallAST);
expect(expression.Parameters).toHaveLength(1);
expect(expression.Parameters[0]).toBeInstanceOf(BinaryExpressionAST);
expect(expression.Parameters[0].Type).toBe(TokenType.Plus);
expect(expression.Parameters[0].LHS).toBeInstanceOf(VariableAST);
expect(expression.Parameters[0].LHS.VariableName).toBe("b");
expect(expression.Parameters[0].RHS).toBeInstanceOf(VariableAST);
expect(expression.Parameters[0].RHS.VariableName).toBe("a");
expect(expression.FunctionPointer).toBeInstanceOf(VariableAST);
expect(expression.FunctionPointer.VariableName).toBe("F");
});
```


in a typed language, this becomes even more verbose:

```
expect(expression).toBeInstanceOf(FunctionCallAST);
const fn = expression as FunctionCallAST;
expect(fn.Parameters).toHaveLength(1);
expect(fn.Parameters[0]).toBeInstanceOf(BinaryExpressionAST);
const param = fn.Parameters[0] as BinaryExpressionAST;
// ... same for param.LHS and .RHS, etc.
```


On the *input* (or setup) side, the recommendation is to make the setup
*straightforward*. Less magic data that moves between effectively-global
variables. Less parameters that do *too much* magic (building an input with a
free function that takes in a few interesting parameters, e.g. in our example
`name`

, `avg_price`

, and `capacity`

, is quite appropriate). *None of this is
new,* it’s just a good practice when we do it.

On the *output* (or expectation) side, the recommendation is to make the
expected outcome *straightforward*. Less checking of specific fields
procedurally. Less jumping between functions that validate or extract data. More
reliance on “diffs” as an intuitive way of getting what’s going on.

Most of this isn’t new on it’s own, but a few tiny features make the developer experience much better. Jest’s auto-updating of snapshots (including inline snapshots) means that inspecting a test failure and updating a test assumption no longer need to be disjoint steps in the process, for example.