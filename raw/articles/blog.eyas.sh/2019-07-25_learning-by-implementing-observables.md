---
title: 'Learning by Implementing: Observables'
url: https://blog.eyas.sh/2019/07/learning-by-implementing-observables/
author: Eyas Sharaiha
published: '2019-07-25'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Sometimes, the best way to learn a new concept is to try to implement it. With my journey with reactive programming, my attempts at implementing Observables were key to to my ability to intuit how to best use them. In this post, we’ll be trying various strategies of implementing an Observable and see if we can make get to working solution.

I’ll be using TypeScript and working to implement something similar to
[RxJS](https://rxjs-dev.firebaseapp.com/) in these examples, but the intuition
should be broadly applicable.

First thing’s first, though: *what are we trying to implement?* My favorite way
or motivating Observables is by analogy. If you have some type, `T`

, you might
represent it in asynchronous programming as `Future<T>`

or `Promise<T>`

. Just as
futures and promises are the asynchronous analog of a plain type, an
`Observable<T>`

is the asynchronous construct representing as collection of `T`

.

The basic API for `Observable`

is a subscribe method that takes as bunch of
callbacks, each triggering on a certain event:

```
interface ObservableLike<T> {
subscribe(
onNext?: (item: T) => void,
onError?: (error: unknown) => void,
onDone?: () => void
): Subscription;
}
interface Subscription {
unsubscribe(): void;
}
```


With that, let’s get to work!

### First Attempt: Mutable Observables

One way of implementing an Observable is to make sure it keeps tracks of it’s subscribers (in an array) and have the object send events to listeners as they happen.

For the purpose of this and other implementations, we’ll define an internal representation of a Subscription as follows:

```
interface SubscriptionInternal<T> {
onNext?: (item: T) => void;
onError?: (error: unknown) => void;
onDone?: () => void;
}
```


Therefore, we could define an Observable as such:

```
class Observable<T> implements ObservableLike<T> {
private readonly subscribers: Array<SubscriptionInternal<T>> = [];
triggerNext(item: T) {
this.subscribers.forEach((sub) => sub.onNext && sub.onNext(item));
}
triggerError(err: unknown) {
this.subscribers.forEach((sub) => sub.onError && sub.onError(err));
}
triggerDone() {
this.subscribers.forEach((sub) => sub.onDone && sub.onDone());
this.subscribers.splice(0, this.subscribers.length);
}
subscribe(
onNext?: (item: T) => void,
onError?: (error: unknown) => void,
onDone?: () => void
): Subscription {
const subInternal: SubscriptionInternal<T> = {
onNext,
onError,
onDone,
};
this.subscribers.push(subInternal);
return {
unsubscribe: () => {
const index = this.subscribers.indexOf(subInternal);
if (index !== -1) {
onDone && onDone(); // Maybe???
this.subscribers.splice(index, 1);
}
},
};
}
}
```


This would be used as follows:

```
// Someone creates an observable:
const obs = new Observable<number>();
obs.triggerNext(5);
obs.triggerDone();
// Someone uses an observable
obs.subscribe(
(next) => alert(`I got ${next}`),
undefined,
() => alert("done")
);
```


There are a few fundamental problems going on here:

- The implementer doesn’t know when subscribers will start listening, and thus won’t know if triggering an event will be heard by no one,
- Related to the above, this implementation always creates
[hot](https://codingblast.com/hot-and-cold-observable/)[observables](https://codingblast.com/hot-and-cold-observable/); the Observable can start triggering events immediately after creation, depending on the creator, and **Mutable:**Anyone who receives the Observable can call`triggerNext`

,`triggerError`

, and`triggerDone`

on it, which would interfere with everyone else.

There are some limitations of the current implementation: can error multiple
times, a “done” Observable can trigger again, and an Observable can move back
and forth between “done”, triggering, and “errored” states. But state tracking
here wouldn’t be fundamentally more complicated. We also need to think more
about errors in the callback, and what the effect of that should be on *other*
subscribers.

### Second Attempt: *Hot* Immutable Observables

Let’s first solve the mutability problem. One approach is to pass a
`ReadonlyObservable`

interface around which hides the mutating methods. But any
downstream user up-casting the Observable could wreck havoc, never mind plain JS
users who just see these methods on an object.

A cleaner approach in JavaScript is to borrow from the
`Promise`

[constructor’s executor pattern](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise#Parameters),
where the constructor is must be passed a user-defined function that defines
when an Observable triggers:

```
class Observable<T> implements ObservableLike<T> {
private readonly subscribers: Array<SubscriptionInternal<T>> = [];
constructor(
executor: (
next: (item: T) => void,
error: (err: unknown) => void,
done: () => void
) => void
) {
const next = (item: T) => {
this.subscribers.forEach((sub) => sub.onNext && sub.onNext(item));
};
const error = (err: unknown) => {
this.subscribers.forEach((sub) => sub.onError && sub.onError(err));
};
const done = () => {
this.subscribers.forEach((sub) => sub.onDone && sub.onDone());
this.subscribers.splice(0, this.subscribers.length);
};
executor(next, error, done);
}
subscribe(
onNext?: (item: T) => void,
onError?: (error: unknown) => void,
onDone?: () => void
): Subscription {
const subInternal: SubscriptionInternal<T> = {
onNext,
onError,
onDone,
};
this.subscribers.push(subInternal);
return {
unsubscribe: () => {
const index = this.subscribers.indexOf(subInternal);
if (index !== -1) {
onDone && onDone(); // Maybe???
this.subscribers.splice(index, 1);
}
},
};
}
}
```


Much better! We can use this as such:

```
// Someone creates an observable:
const obs = new Observable<number>((next, error, done) => {
next(5);
done();
});
// Someone uses an observable
obs.subscribe(
(next) => alert(`I got ${next}`),
undefined,
() => alert("done")
);
```


This cleans up the API quite a bit. But in this example, calling this code in this order will still cause the subscriber to see no events.

#### Good Examples

We can already use this type of code to create helpful Observables:

```
// Create an Observable of a specific event in the DOM.
function fromEvent<K extends keyof HTMLElementEventMap>(
element: HTMLElement,
event: K
): Observable<HTMLElementEventMap[K]> {
return new Observable<HTMLElementEventMap[K]>((next, error, done) => {
element.addEventListener(event, next);
// Never Done.
});
}
const clicks: Observable<MouseEvent> = fromEvent(document.body, "click");
```


Or an event stream from a timed counter:

```
function timer(millis: number): Observable<number> {
return new Observable<number>((next, error, done) => {
let count = 0;
setInterval(() => {
next(count);
++count;
}, millis);
});
}
```


Even these examples have some issues: they keep running even when no one is listening. That’s sometimes fine, if we know we’ll only have one Observable, or we’re sure callers are listening and so tracking that state is unnecessary overhead, but it’s starting to point to certain smells.

#### Bad Examples

One common Observable factory is `of`

, which create an Observable that emits one
item. The assumption being that:

```
const obs: Observable<number> = of(42);
obs.subscribe((next) => alert(`The answer is ${next}`));
```


… would work, and result in “The answer is 42” being alerted. But a naive implementation, such as:

```
function of<T>(item: T): Observable<T> {
return new Observable<T>((next, error, done) => {
next(item);
done();
};
}
```


… would result in the event happening before anyone has the chance to
subscribe. Tricks like `setTimeout`

work for code that subscribes immediately
after, but is fundamentally broken if we want to generalize this to someone who
subscribes at a later point.

### The case for *Cold* Observables

We can try to make our Observables *lazy*, meaning they only start acting on the
world once subscribed to. Note that by *lazy* I don’t just mean that a shared
Observable will only start triggering once someone subscribes to it — I mean
something stronger: an Observable will trigger for each subscriber.

For example, we’d like this to work properly:

```
const obs: Observable<number> = of(42);
obs.subscribe((next) => alert(`The answer is ${next}`));
obs.subscribe((next) => alert(`The answer is still ${next}`));
setTimeout(() => {
obs.subscribe((next) => alert(`Even now, the answer is ${next}`));
}, 1000);
```


Where we get 3 alert messages the contents of the event.

### Third Attempt: *Cold* Observables (v1)

```
type UnsubscribeCallback = (() => void) | void;
class Observable<T> implements ObservableLike<T> {
constructor(
private readonly executor: (
next: (item: T) => void,
error: (err: unknown) => void,
done: () => void
) => UnsubscribeCallback
) {}
subscribe(
onNext?: (item: T) => void,
onError?: (error: unknown) => void,
onDone?: () => void
): Subscription {
const noop = () => {};
const unsubscribe = this.executor(
onNext || noop,
onError || noop,
onDone || noop
);
return {
unsubscribe: unsubscribe || noop,
};
}
}
```


In this attempt, each `Subscription`

will run the executor separately,
triggering `onNext`

, `onError`

, and `onDone`

for each subscriber as needed. This
is pretty cool! The naive implementation of `of`

works just fine. I also snuck
in a pretty simple method to allow us to add cleanup logic to our executors.

`fromEvent`

would benefit from that, for example:

```
// Create an Observable of a specific event in the DOM.
function fromEvent<K extends keyof HTMLElementEventMap>(
element: HTMLElement,
event: K
): Observable<HTMLElementEventMap[K]> {
return new Observable<HTMLElementEventMap[K]>((next, error, done) => {
element.addEventListener(event, next);
// Never Done.
return () => {
element.removeEventListener(event, next);
};
});
}
```


The nice thing about this is that we remove our listeners when a particular subscriber unsubscribes. Except now, we open as many listeners as subscribers. That might be okay for this one case, but we’ll want to figure out how to let users “multicast” (reuse underlying events, etc.) when they want to.

We still haven’t figured out error handling and proper cleanup and error handling. For example:

- It is generally regarded that a subscription that errors is closed (just like
how throwing an error while iterating over a
`for`

loop will terminate that loop) - When a subscriber unsubscribes, we should probably get that ”
`onDone`

” event. - When there’s an error, we should probably do some cleanup.

### Better *Cold* Observables

Here’s a re-implementation of `subscribe`

that might satisfy these conditions:

```
class Observable<T> implements ObservableLike<T> {
constructor(
private readonly executor: (
next: (item: T) => void,
error: (err: unknown) => void,
done: () => void
) => UnsubscribeCallback
) {}
subscribe(
onNext?: (item: T) => void,
onError?: (error: unknown) => void,
onDone?: () => void
): Subscription {
let dispose: UnsubscribeCallback;
let running = true;
const unsubscribe = () => {
// Do not allow retriggering:
onNext = onError = undefined;
onDone && onDone();
// Don't notify someone of "done" again if we unsubscribe.
onDone = undefined;
if (dispose) {
dispose();
// Don't dispose twice if we unsubscribe.
dispose = undefined;
}
running = false;
};
const error = (err: unknown) => {
onError && onError(err);
unsubscribe();
};
const done = () => {
unsubscribe();
};
const next = (item: T) => {
try {
onNext && onNext(item);
} catch (e) {
error(e);
}
};
dispose = this.executor(next, error, done);
// We just assigned dispose. If the executor itself already
// triggered done() or fail(), then unsubscribe() has gotten called
// before assigning dispose.
// To guard against those cases, call dispose again in that case.
if (!running) {
dispose && dispose();
}
return {
unsubscribe: () => unsubscribe(),
};
}
}
```


## Using Observables

Taking the ”*Better Cold Observables*” example, let’s see how we can use
Observables:

### Useful Factories

We already discussed `fromEvent`

and `of`

, which work with the new form of
`Observable`

. A few others we can create:

```
// Throws an error immediately
function throwError(err: unknown): Observable<never> {
return new Observable((next, error) => {
error(err);
});
}
// Combines two Observables into one.
function zip<T1, T2>(
o1: Observable<T1>,
o2: Observable<T2>
): Observable<[T1, T2]> {
return new Observable<[T1, T2]>((next, error, done) => {
const last1: T1[] = [];
const last2: T2[] = [];
const sub1 = o1.subscribe(
(item) => {
last1.push(item);
if (last1.length > 0 && last2.length > 0) {
next([last1.shift(), last2.shift()]);
}
},
(err) => error(err),
() => done()
);
const sub2 = o2.subscribe(
(item) => {
last2.push(item);
if (last2.length > 0 && last1.length > 0) {
next([last1.shift(), last2.shift()]);
}
},
(err) => error(err),
() => done()
);
return () => {
sub1.unsubscribe();
sub2.unsubscribe();
};
});
}
```


### Useful Operators

Another nice thing about Observables is that they’re nicely composable. Take
`map`

for instance:

```
function map<T, R>(observable: Observable<T>, mapper: (item: T) => R) {
return new Observable<R>((next, fail, done) => {
const sub = observable.subscribe(
(item) => next(mapper(item)),
fail,
done
);
return () => {
sub.unsubscribe();
};
});
}
```


This allows us to do things like:

```
function doubled(input: Observable<number>): Observable<number> {
return map(input, (n) => n * 2);
}
```


Or we could define `filter`

:

```
function filter<T>(observable: Observable<T>, predicate: (item: T) => boolean) {
return new Observable<T>((next, fail, done) => {
const sub = observable.subscribe(
(item) => {
if (predicate(item)) next(item);
},
fail,
done
);
return () => {
sub.unsubscribe();
};
});
}
```


Which allows us to do:

```
function primeOnly(input: Observable<number>): Observable<number> {
return filter(input, isPrime);
}
```


## Conclusion

I didn’t really try to sell you, dear reader, on *why* you should use
Observables as helpful tools in your repertoire. Some of my other writing
showing their use cases ([here](https://blog.eyas.sh/2018/12/use-asyncpipe-when-possible/),
[here](https://blog.eyas.sh/2018/12/data-and-page-content-refresh-patterns-in-angular/), and
[here](https://blog.eyas.sh/2018/12/data-and-page-content-refresh-patterns-in-angular/)) might be
helpful. But really, what I wanted to demonstrate is some of the intuition on
how `Observable`

s work. The implementation I shared isn’t a complete one, for
that, you better consult with
`Observable.ts`

[in the RxJS implementation](https://github.com/ReactiveX/rxjs/blob/master/src/internal/Observable.ts).
This implementation is notably missing a few things:

- We could still do much better on error handling (especially in my operators)
- RxJS observables include the
`pipe()`

method, which makes applying one or more of those operators to transform an Observable much more ergonomic - Lot’s of things here and there