---
title: Observables, Side-effects, and Subscriptions
url: https://blog.eyas.sh/2018/12/observables-side-effects-and-subscriptions/
author: Eyas Sharaiha
published: '2018-12-21'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

My previous articles on [using AsyncPipe](https://blog.eyas.sh/2018/12/use-asyncpipe-when-possible/)
and
[data refresh patterns in Angular](https://blog.eyas.sh/2018/12/data-and-page-content-refresh-patterns-in-angular/)
hint at some common anti-patterns dealing with Observables. If there’s any
common thread in my advice, it is: **delay unpacking an Observable into its
scalar types** when performing logic you can rewrite as side-effect-free,
leaving code with side-effects for subscription callbacks and other downstream
logic.

My two earlier articles focused on cases users can benefit from handling more of
the object’s lifecycle in its Observable form. In other words, cases where the
Observable was being subscribed to and unpacked *too soon*. Instead, I suggested
transforming the Observable using operators like `map`

, `switchMap`

, `filter`

,
etc. and taking advantage of the power offered by this form. In the case of
Angular, it provides `AsyncPipe`

, which takes the care of the step with
side-effects (actually rendering the page) in template code.

There are some exceptions to this line of thinking, namely
`do`

[and](http://reactivex.io/documentation/operators/do.html)`tap`

are reactive
operators exclusively there *for* functions with side effects. I’ll leave a
discussion of *right* vs *less right* reasons to use `do`

/`tap`

for a later
article. But I’ll mention logging, error reporting, and caching of otherwise
pure functions as one valid use of side-effects.

*This article uses RxJS in code examples, but
applies to broader reactive concepts.*

Let’s explore a few of these cases:

## 1. Displaying data represented by Observables

Say I have two Observables wrapping some object in a storage format (e.g. JSON), and I’d like to display it.

### Unpacking an observable *too soon*

```
let customerName: string;
let customerBalance: number;
nameObservable.subscribe((name) => {
customerName = name;
if (customerName && customerBalance) {
processAndDraw();
}
});
balanceObservable.subscribe((balance) => {
customerBalancer = balance;
if (customerName && customerBalance) {
processAndDraw();
}
});
function processAndDraw() {
alert(`${customerName}: $${customerBalance.toFixed(2)} USD`);
}
```


If a caller unpacks an observable too soon, it means they’re dealing with scalars, passing things around by global state. Developers might have trouble handling changes, such as adding a third data source to show.

### Unpacking an Observable *too late*

```
combineLatest(nameObservable, balanceObservable)
.pipe(
map(([name, balance]) => {
alert(`${name}: $${balance.toFixed(2)} USD`);
})
)
.subscribe();
```


On the one hand, this is much shorter and more expressive! This is effectively
maps `Observable<[string, number]>`

into an `Observable<void>`

which *happens to
perform side effects when subscribed to*. The subscriber, however, has no idea
what action will take place from just looking at a type or signature. Even with
the code snippet above used as-is, it is very easy to forget about that last
`.subscribe()`

call, which—given that Observables are lazy by default and only
perform useful actions when subscribed to—renders this whole snippet a no-op.

One final reason side-effects are bad in operators: that these side-effects can
be performed an arbitrary number of times *per event* based on how many distinct
subscribers are listening to an Observable.

### A better trade-off

```
combineLatest(nameObservable, balanceObservable)
.pipe(map(([name, balance]) => `${name}: $${balance.toFixed(2)} USD`))
.subscribe((text) => alert("Text"));
```


## 2. Avoiding Unnecessary Indirection through `Subject`

s

In some ReactiveX implementation, a
[Subject](http://reactivex.io/documentation/subject.html)is a powerful concept
that allows an event publisher to share events with subscribers, as an
Observable. It is also quite overused.
[Dave Sexton wrote a great piece in 2013 about whether or not to use a Subject](http://davesexton.com/blog/post/To-Use-Subject-Or-Not-To-Use-Subject.aspx),
and further quoted Eric Meijer’s reasoning for disliking them:

[Subjects] are the “mutable variables” of the Rx world and in most cases you do not need them.

Erik Meijer, via[To Use Subject or Not To Use Subject?]

In particular, I’ve come across many examples in the wild violating Sexton’s
first piece of advice, ”*What is the source of the notifications?*” Here’s an
egregious anti-pattern:

```
class DogNewsProvider {
constructor(news: Observable<News>) {
news.subscribe((newsItem) => {
if (newsItem.category === "Dog") {
this._dogNews.next(new DogNews(newsItem));
}
});
}
private readonly _dogNews = new ReplaySubject<DogNews>(1);
get(): Observable<DogNews> {
return this._dogNews.asObservable();
}
}
```


Here, we’re providing `Observable<DogNews>`

, based on source data contained by
another observable. In between, however, we’re routing information from an
Observable to a `ReplaySubject`

, which we are manually triggering on each event
from the source observable.

This has a few problems:

- The code above is flawed in that the
`news`

observable provided to`DogNewsProvider`

is never unsubscribed to. Modifying the class to support unsubscribing is easy, but not ergonomic and easy to miss. - A bunch of indirection is happening between the source and the output, making the flow of data less clear.
- The advantage of a
*replay*Subject (namely that someone subscribing to an Observable will get some number of events the missed—1 in this example) can be replicated by applying the`shareReplay`

operator to the source observable.

### A better approach

```
class DogNewsProvider {
constructor(news: Observable<News>) {
this.dogNews = news.pipe(
filter((newsItem) => newsItem.category === "Dog"),
map((newsItem) => new DogNews(newsItem)),
shareReplay(1)
);
}
readonly dogNews: Observable<DogNews>;
}
```


A subscription to `dogNews`

is not leaked in this case, and events will only
fire while there are active listeners to this Observable. Further, the flow from
`news`

all the way to `dogNews`

is clearly and directly explained by looking at
the code, without jumping between callbacks.

One way to think about this indirection is in the way Sexton described: there’s some unnecessary indirection in unpacking an Observable, just to pack it into an Observable again and send it off.

Another way to think about this indirection is to look at the `subscribe()`

method. *Does it have side-effects?* Yes, it does. It calls a method with side
effects on a variable outside its scope. *Can it be rewritten in a way that
doesn’t?* It can. There’s no incremental state we’re trying to maintain on
purpose (other than the *replay* operator semantics); no I/O in the
subscription; the side-effects outside of our scope that we’re modifying is
mainly to pipe data from one place to another. These provide clues that there
might be a better way to rewrite our callback into a series of monadic operators
on an `Observable`

.

## 3. Subscribing when `switchMap`

or `flatMap`

would do

Seeing nested `subscribe`

callbacks is a good sign some logic can be reworked.
Let’s take a simplified example:

```
function getBalance(name: string, showBalance: (balance: number) => void) {
backend.getAccountIdByName(name).subscribe((id) => {
backend.getBalanceById(id).subscribe((balance) => {
showBalance(balance);
});
});
}
```


Other than the same issues with unsubscriptions as above, the callback hell also obscures what would be a relatively simple data flow:

```
function getBalance(
name: string,
showBalance: (balance: number) => void) {
backend.getAccountIdByName(name).pipe(
switchMap(id => backend.getBalanceById(id)
).subscribe(balance => {
showBalance(balance);
});
}
```


Keep `showBalance`

in a subscription, and transform an account holder name all
the way to an account balance through operators on Observables.

The bigger advantage to organizing code like this is that it promotes opportunities to refactor:

### Use opportunities to factor out Observable-returning functions

We can actually factor out part of `getBalance`

that actually returns an
`Observable<number>`

. This allows it to be reused, combined, and multiplexed
with other Observables and Observable operators as needed. Observables are also
a uniform, ubiquitous API that is cancelable, retryable, etc.

```
function getBalance(name: string) {
backend.getAccountIdByName(name).pipe(
switchMap(id => backend.getBalanceById(id)
);
}
```


Observables are a uniform, ubiquitous API that is cancelable, retryable, etc.


## Summary

An Observable going through a series of transformation operators from source to final result is:

- Cancelable through-and-through; cancelling a subscription to a resultant Observable will cancel any underlying subscriptions opened to that end.
- Composable in its own right; and
- A ubiquitous immutable API that gives callers flexibility in manipulating return values.

I propose side-effects being a great first-order heuristic as far as what can
reasonably be kept within a composed Observable. When needed, operators like
`do`

[and](http://reactivex.io/documentation/operators/do.html) `tap`

will
sometimes make sense.