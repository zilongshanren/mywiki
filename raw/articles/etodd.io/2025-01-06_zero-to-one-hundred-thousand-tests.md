---
title: Zero to One Hundred Thousand Tests
url: https://etodd.io/2025/01/06/zero-to-one-hundred-thousand-tests/
published: '2025-01-06'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Zero to One Hundred Thousand Tests

When I started at [StrongDM](https://strongdm.com) five years ago (woah), we had zero automated tests.
Last year we had [50,000 tests](https://etodd.io/2024/01/01/waiting-on-tests/).
Today, around 70% of our code is covered by over 100,000 tests, most of which run on every pull request.

What follows is my personal opinion about what constitutes a “good” automated test based on my observation of this colossal increase in test coverage. The goal is not to convince you I’m right, but to draw some contrasts and provoke you to question assumptions and form your own opinions.

I’ll start by asking: what is the purpose of automated tests?

Actually, let’s start even more basic: what is the purpose of a software company?

## What Are We Doing Here?

StrongDM is a private for-profit company. Its purpose is to make money.

How do we do that?

At a very high level, this [xkcd comic](https://xkcd.com/722/) explains:

![xkcd 722: Computer Problems](../../assets/53eac249038c684b.png)


When it comes down to it, we push buttons to steadily improve our pattern of lights to make more money.

## The Perfect Pattern of Lights

Let’s imagine Software Nirvana: the perfect pattern of lights that makes infinite money.

I will use the following image to represent this pattern of lights:

![Rick Astley](../../assets/52fc0fe1edcb768b.png)


Now in reality, at any given time, our software looks more like this:

![Some lights make money, some might make money, and some are not making money](../../assets/f779aada295b676b.png)


Some of the lights are dialed in and making money. Some are a work in progress; we don’t know if they will make money yet. We’re still pressing buttons and trying to get them to light up the way we want. And then there a ton of lights that we haven’t touched at all yet, making no money.

So how do we reach Software Nirvana? Let’s establish two concrete goals to help us get there.

## Goal #1: Ensure the “Money” Lights Don’t Change

Here’s a scenario we want to avoid.
Call it the [CrowdStrike](https://en.wikipedia.org/wiki/2024_CrowdStrike-related_IT_outages) scenario.

![“Money” lights suddenly decrease](../../assets/c353a37a7f6768f7.png)


The number of “Money” lights is steadily increasing, and then suddenly, kaboom. A bunch of lights stop working.

We want the number of “Money” lights to increase monotically. That is, never go down.

## Goal #2: Quickly Change “Maybe” Lights to “Money” Lights

Here’s another scenario we want to avoid:

![Too many “Maybe” lights](../../assets/f6ebc9ad43f6c95e.png)


We want the “Maybe” zone to be as small as possible. We can’t afford to keep a bunch of lights in limbo, waiting around to see if they end up making money or not. We need to convert “Maybe” lights into “Money” lights at a certain speed or else we die.

This is what we want:

![Quickly convert “Maybe” lights to “Money” lights without losing any “Money” lights](../../assets/7b49e1532eb299d7.png)


We can’t control everything and we can’t predict the future. The best we can do is minimize risk and maximize predictability. That means a small, harmless collection of “Maybe” lights and a steadily increasing collection of “Money” lights.

## Automated Tests Applied to Goal #1

Do automated tests help us achieve **Goal #1: Ensure the “Money” Lights Don’t Change**?

Think of automated tests like a powerful special ability card in a board game:

![Automated tests as a special ability card](../../assets/daf3f14f85160041.png)


It takes some investment to play this card, but once we do, our “Money” lights are much safer. We can write a test once and run it over and over to make sure those lights are still green. By comparison, a manual test is kind of a crappy special ability.

![Manual test as a special ability card](../../assets/2b8df3d1056008a3.png)


Manual testing worked great for the first few years of StrongDM’s life, because we only had a few “Money” lights to check. But as the number of “Money” lights grew, it became a huge burden to keep checking them all every time we changed something. Regressions inevitably slipped through the cracks. These days, it would take StrongDM’s entire engineering team a full month to manually check every single light, and we would surely miss a few.

Automated tests pretty much completely solve this.
If you don’t believe me, perhaps a logical fallacy might convince you.
Here’s my [argument from authority](https://en.wikipedia.org/wiki/Argument_from_authority):

Think of automated tests as “bug repellent” that keeps nasty little bugs from crawling back into our software after we have made sure it doesn’t contain any bugs.


[xUnit Test Patterns], p. 22

## Automated Tests Applied to Goal #2

Do automated tests help us achieve **Goal #2: Quickly Change “Maybe” Lights to “Money” Lights**?

Goal #2 is a bit more nuanced. Let’s try to make this goal more concrete, and then we’ll see how automated tests affect it. Here is another way of describing Goal #2:

![Minimize how long it takes to design, build, test, release, make money, and repeat](../../assets/62daa7bd9bd6723c.png)


We are in the “Maybe” zone until the very last step of the development process. We want to minimize the time we spend in the “Maybe” zone and get into the “Money” zone ASAP. Goal #2 is all about speed.

Notice that the process includes time spent on any kind of testing, automated or otherwise.
So oddly, the time we spend on testing actually *grows* the “Maybe” zone.
We might be tempted to try and shrink it down by eliminating testing entirely.

![Without testing we might get stuck in the “Maybe” zone forever](../../assets/c664d434eb5a0980.png)


Sure, it looks like our development cycle is super fast now, but in the real world, testing still occurs. It’s just that now it happens the first time the customer tries to use it. And they might not feel like telling us about a failed test result. They might just take their money elsewhere.

This is a delicate balance. If we spend too much time on testing…

![Too much testing grows the “Maybe” zone](../../assets/78b158c8ab0edbc8.png)


We might get to the end and find out the product wasn’t quite what the customer wanted. All that effort was wasted.

Testing needs to be fast, and automated tests take a long time to set up. Other kinds of tests are actually more useful for determining whether those “Maybe” lights will convert to “Money” lights.

![Manual tests and beta tests are effective for new features](../../assets/75cb62ded3473464.png)


For “Maybe” lights, manual tests are often nearly as effective as automated tests. In both cases, we think up every test case we can imagine and try them out. The difference is, manual tests tend to be much quicker and cheaper.

And beta tests are *super* effective for Goal #2.
Not only do they address the risk that the lights are subtly wrong, they also address the much bigger risk that the lights are *completely and fundamentally* wrong.

All this leads me to conclude…

## Automated Tests Are Not Particularly Great for “Maybe” Lights

Anecdotally, despite huge investment in automated tests and much higher test coverage, our new features at StrongDM have about the same number of issues we used to have with manual testing. We can only test what we can predict, and we can’t predict everything. Manual tests are often nearly as effective as automated tests and require much less up-front investment.

Don’t believe me? Here’s another argument from authority:

Yes, tests find bugs—but that really isn’t what automated testing is about.


[xUnit Test Patterns], p. 22

So then, what *is* it about?

I think it’s really about Goal #1, **Ensure the “Money” Lights Don’t Change**.
In fact, it’s *just so freaking amazing* for Goal #1 that it can also help us with the delicate balance of Goal #2.

![Automate the testing of existing code](../../assets/b6c6a862ef151a31.png)


If we have reliable, fast automated tests, we can be confident within a few minutes that a change doesn’t break our existing code. That’s an enormous speed boost that’s well worth the extra investment.

## Finally Arriving at the Point

Automated tests should aim to achieve what they’re great at, **Goal #1: Ensure the “Money” Lights Don’t Change**…

…without becoming so burdensome that they hinder **Goal #2: Quickly Change “Maybe” Lights to “Money” Lights**.

Let’s look at a real (albeit slightly altered) test from our codebase and judge how well it helps us achieve these two goals.

This test creates a role, then tries to create another role with the same name, and expects to receive a name conflict error.

```
func TestCreateRoleDuplicateName(t *testing.T) {
t.Parallel()
fixture := gesturetest.NewFixture(t)
role := gesturetest.CreateRole(t, fixture.AdminContext())
_, err := roles.Create(fixture.AdminContext(), role.Name)
testutil.ErrorIsAlreadyExists(t, err)
}
```


Does it ensure the “Money” lights don’t change (Goal #1)?

Yes, if someone tries to remove the name conflict check from `roles.Create`

, this test will fail.

Does it hinder us from quickly changing lights (Goal #2)?

Not really, we could completely rewrite `roles.Create`

and as long as it still checks for name conflicts somehow, we shouldn’t have to worry about this test at all.

Now let’s look at another real test.
This one checks for the same thing, but one layer down in our system.
Instead of creating two roles with conflicting names, this test essentially rewrites one specific bit of code inside the `Create`

function to behave differently.
This is called [mocking](https://en.wikipedia.org/wiki/Mock_object).

```
func TestCreateRoleDuplicateName(t *testing.T) {
t.Parallel()
s := newTestStep()
fixture := steptest.NewFixture(t)
ctx := fixture.MockStepsContext()
s.dao.Roles = &mocks.RolesDAOMock{
GetByNameFunc: func(ctx dao.ReadContext, name string) (*models.Role, error) {
return &models.Role{}, nil
},
}
_, err := s.Create(ctx, "a")
testutil.ErrorIsAlreadyExists(t, err)
}
```


Does it ensure the “Money” lights don’t change (Goal #1)?

Sure, kind of.
There’s no actual name conflict here so it’s not clear what we’re checking for.
Without diving deep into the code, all we can say for sure is that this test uses secret knowledge about the inner workings of the `Create`

function to reach inside it and trigger a specific code path.
That said, if we completely deleted the contents of the `Create`

function, this test would surely fail.
So it does catch some things at least!

Does it hinder us from quickly changing lights (Goal #2)?

Definitely.
If we even so much as change the order of operations inside the `Create`

function, this test could break.
And if we say, rename the `GetByName`

function, the test won’t even compile anymore.
We’ll have to update both the mock and the test.
That’s a big blast radius for a tiny internal rename that our other test wouldn’t care about at all.

And that actually brings us back to Goal #1, and another reason why this test fails to achieve it. Let me illustrate the problem with another real example. If I make a one-line change like this:

And then end up having to change 100 lines of mocks in completely unrelated tests like this:

How do I know I didn’t change any “Money” lights? If the tests changed that much, it’s possible the “Money” lights changed too.

Time to wrap this up. We’ve seen a good test that achieves both our goals, and a not-so-great test that achieves neither.

Interestingly, when we first started writing automated tests, they were all like the good test. Only recently did we start to see these not-so-great tests. Why?

## How We Got Here, Part 1: System Boundaries

The first step of automated testing is to choose the boundary of your “system under test”. You can draw a boundary around a single pure function and write a “unit” test against it. Or you can set up a complete simulated environment and run “end to end” tests against your entire product. “Integration” tests are somewhere in between. You can draw your boundaries wherever you want, but some boundaries are better than others.

When we first started writing automated tests, we drew our boundary like this:

![Boundary around business logic and data access layer](../../assets/a34c4d04075da745.png)


If your system depends on anything outside the boundary, you will have to mock it. We mocked Postgres by running a real Postgres server and executing each test inside an isolated transaction that rolls back at the end of the test. The tests run in parallel which ends up being very fast.

Later we started writing tests for each specific layer:

![Boundaries around each layer](../../assets/80f6336c72d9f391.png)


The tests for each layer now have to mock out the layer beneath, making them brittle and strongly coupled. Mocks can’t be completely avoided, but we can minimize them by choosing better system boundaries. What makes a good boundary?

IO boundaries often make good system boundaries. Mocking IO is usually a good idea because it’s slow. But don’t mock code that you can just run for real.

Sometimes we mock code because it would be a lot of work to set up the right prerequisites for a specific test case. But I find it’s always better to write a test helper function that sets everything up for real instead of reaching for a mock. Test helpers are easy to reuse in other tests, and in contrast to mocks, I’ve never found myself thinking “man, this test helper was such a mistake.”

There is one specific case where you almost always need a mock, which brings us to our next point…

## How We Got Here, Part 2: Test Coverage

In recent years, StrongDM has made a huge push to reach 100% test coverage, meaning our tests execute every single line of code in our codebase at least once. For the record, I think 100% coverage is great as long as the tests are good.

Unfortunately, Go’s famously verbose error handling makes this difficult. It usually looks something like this. If we encounter an error, we return it up the stack.

```
func foo() error {
err := bar()
if err != nil {
return fmt.Errorf("something went wrong: %w", err)
}
...
}
```


To get test coverage on that `if`

branch, we need to create a mock for `bar()`

, make it return a synthetic error, then check that `foo()`

returns that error.
And because we’ve pursued 100% test coverage at all costs, we have thousands of tests that do exactly this.
Our coverage numbers are great, but our tests are brittle.

We recently enabled a linter that catches most error handling mistakes. My opinion is that it’s safe for us to delete almost all of these tests. Yes, our test coverage will go down, but remember, the goal is not 100% test coverage, it is…

![Quickly convert “Maybe” lights to “Money” lights without losing any “Money” lights](../../assets/7b49e1532eb299d7.png)


- Ensure the “Money” Lights Don’t Change
- Quickly Change “Maybe” Lights to “Money” Lights

At least, that’s my personal criteria for good automated tests. What do you think, what are your criteria?