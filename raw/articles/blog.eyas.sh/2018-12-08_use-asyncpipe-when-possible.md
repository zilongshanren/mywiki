---
title: Use AsyncPipe When Possible
url: https://blog.eyas.sh/2018/12/use-asyncpipe-when-possible/
author: Eyas Sharaiha
published: '2018-12-08'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

I typically review a fair amount of Angular code at work. One thing I typically
encourage is using plain `Observable`

s in an Angular Component, and using
[ AsyncPipe](https://angular.io/api/common/AsyncPipe) (

`foo | async`

) from the
template html to handle subscription, rather than directly subscribing to an
observable in a component TS file.### Subscribing in Components

Unless you know a subscription you’re starting in a component is very finite (e.g. an HTTP request with no retry logic, etc), subscriptions you make in a Component must:

- Be closed, stopped, or cancelled when exiting a component (e.g. when navigating away from a page),
- Only be opened (subscribed) when a component is actually loaded/visible (i.e.
in
`ngOnInit`

rather than in a constructor).

Consider:

```
@Component()
export class Foo implements OnInit, OnDestroy {
someStringToDisplay = "";
private readonly onDestroy = new ReplaySubject<void>(1);
ngOnInit() {
someObservable
.pipe(takeUntil(this.onDestroy), map(/* ... */))
.subscribe((next) => {
this.someStringToDisplay = next;
this.ref.markForCheck();
});
}
ngOnDestroy() {
this.onDestroy.next(undefined);
}
}
```


```
@Component()
export class Foo implements OnInit, OnDestroy {
someStringToDisplay = "";
private subscription = Subscription.EMPTY;
ngOnInit() {
this.subscription = someObservable
.pipe(map(/*...*/))
.subscribe((next) => {
this.someStringToDisplay = next;
this.ref.markForCheck();
});
}
ngOnDestroy() {
this.subscription.unsubscribe();
}
}
```


```
<span>{{someStringToDisplay}}</span>
```


`AsyncPipe`

can take care of that for you

```
@Component()
export class Foo {
someStringToDisplay = someObservable.pipe(map(/*...*/));
}
```


```
<span>{{someStringToDisplay | async}}</span>
```


Much better! No need to remember to manage unsubscribe. No need to implement
`OnDestroy`

. `AsyncPipe`

does its own unsubscribe on destruction, etc. If you
only implement `OnInit`

to make a new subscription, you can forego that too.

#### Best Practice: Use `publishReplay`

and `refCount`

if accessing the same `Observable`

from multiple places

If you need to access a value multiple times, consider using the `publishReplay`

and `refCount`

RxJS operators:

```
pageTitle = this.route.params.pipe(
map((params) => params["id"]),
flatMap((id) =>
this.http.get(`api/pages/${id}/title`, { responseType: "text" })
),
publishReplay(1),
refCount()
);
```


```
<h1>{{pageTitle | async}}</h1>
<p>You are viewing {{pageTitle | async}}.</p>
```


This will cause the template rendering to make a single request for `pageTitle`

,
and cache the result between both uses.

#### Best Practice: Combine `@if`

, `as`

, and `else`

with `AsyncPipe`


If you need to handle the loading state, and need to display nested properties of an object returned from an observable, you can do something like:

```
@if (pageObservable | async; as page) {
<!-- can refer to 'page' here -->
<h1>{{page.title}}</h1>
<p>{{page.paragraph}}</p>
} else {
<span>Loading...</span>
}
```


Or, in the old `ngIf`

syntax:

```
<ng-container *ngIf="(pageObservable | async) as page; else loading">
<!-- can refer to 'page' here -->
<h1>{{page.title}}</h1>
<p>{{page.paragraph}}</p>
</ng-container>
<ng-template #loading>Loading…</ng-template>
```


Note that this doesn’t distinguish between the case where `pageObservable`

is
still loading, and the case where `pageObservable`

resolved to a falsey value.