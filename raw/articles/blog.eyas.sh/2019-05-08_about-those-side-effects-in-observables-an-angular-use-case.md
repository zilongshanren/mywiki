---
title: About those Side-effects in Observables, an Angular Use Case
url: https://blog.eyas.sh/2019/05/about-those-side-effects-in-observables-an-angular-use-case/
author: Eyas Sharaiha
published: '2019-05-08'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

When testing a codebase in Angular Ivy, I ran into a bunch of test failures I
wasn’t seeing before. `ExpressionChangedAfterItHasBeenCheckedError`

s were being
thrown around. In debugging these failures, I found that many of them are the
results of side-effects in Observables and Observable `pipe`

operations. I
happened to describe these earlier in my piece on
[Observables, Side-effects, and Subscriptions](https://blog.eyas.sh/2018/12/observables-side-effects-and-subscriptions/).

Consider this minimal reproduction:

```
@Component({
selector: "widget-editor",
templateUrl: "widget_editor.html",
})
export class WidgetEditor {
constructor(private readonly service: WidgetService) {}
widgetName = "";
widgetConfig$ = this.service.getWidget("my_widget").pipe(
map((widgetDetails) => {
this.widgetName = widgetDetails.name;
return widgetDetails.config;
})
);
}
```


There’s enough code smell from looking at this alone: an unsuspecting user
subscribing to `widgetConfig$`

will result in member variables of `WidgetEditor`

getting mutated. That’s *strange* behavior, but with the right Angular template,
it can also become an outright bug:

```
<h1>Editing {{widgetName}}...</h1>
<ng-container *ngIf="(widgetConfig$ | async) as widget; else loading">
<h2>Widget Config<h2>
<widget-config-view [widget]="widget"></widget-config-view>
</ng-container>
<ng-template #loading>Loading...</ng-template>
```


Testing this code might give you an error that looks something like:

`Error: ExpressionChangedAfterItHasBeenCheckedError: Expression has changed after it was checked. Previous value: ''. Current value: 'my_widget_name'.`


### Why?

#### The normal case

At render time, `widgetConfig$`

has never been subscribed to. Therefore, no HTTP
request has been made (Observables are lazy that way), and the `map`

operator
therefore hasn’t been called. The value of `widgetName`

is `''`

. When Ivy tries
to render the `<ng-container>`

, the Async Pipe triggers subscribing to
`widgetConfig$`

, and, eventually, all the side-effects that come with it’s
operators.

When `widgetConfig$`

is subscribed to, using the Async Pipe, it kicks off the
Observable (and, eventually, all of it’s side-effects).

In most cases, we get the widget result asynchronously. Side-effects happen at
some point, and change detection forces a re-render cycle that picks up the new
`widgetName`

and `widgetConfig$`

results.

#### The error case

What if a test injected a `FakeWidgetService`

instead, whose `getWidget`

call
used the
`of`

[RxJS operator](https://www.learnrxjs.io/learn-rxjs/operators/creation/of)
to immediately return a value? The default scheduler used in the `of`

operator
immediately returns the value within the operator when subscribed. This means
that subsequent pipes are executed immediately, and, in our case, the
side-effects run immediately.

Consider that use case and follow along with the initial render: `widgetName`

is
initially rendered the first time as the empty string `''`

. Later, when
`widgetConfig$`

is subscribed to by the Async Pipe, it immediately changes the
value of `widgetName`

. By the time rendering is complete, Angular notices that
the value of `widgetName`

it *just* rendered is different than the current
value.

#### Can’t we just change the test scheduler?

We could, and that would fix *this* problem. But then you’re sort of leaking
abstractions; asking services you depend on to have Observables with schedulers
that behave a certain way, and depending on more than just the implied contract
of the interfaces you use.

### The Fix

```
@Component({
selector: "widget-editor",
templateUrl: "widget_editor.html",
})
export class WidgetEditor {
constructor(private readonly service: WidgetService) {}
private readonly widget$ = this.service
.getWidget("my_widget")
.pipe(publishReplay(1), refCount());
widgetName$ = this.widget$.pipe(map((widgetDetails) => widgetDetails.name));
widgetConfig$ = this.widget$.pipe(
map((widgetDetails) => widgetDetails.config)
);
}
```


A common reason for side-effects (as is with this case) is to reuse an intermediate value within a sequence of transformations elsewhere. Making that explicit, by exposing the intermediate piece as a private Observable itself, will clean things up quite a bit.

To make sure that a subscription to `widgetName$`

and `widgetConfig$`

wouldn’t
result in two separate HTTP requests (or underlying side-effects, whatever those
may be), making sue the `widget$`

Observable is shared between the two will be
important.