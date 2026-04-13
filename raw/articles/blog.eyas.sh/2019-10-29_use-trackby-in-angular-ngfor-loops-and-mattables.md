---
title: Use trackBy in Angular ngFor Loops and MatTables
url: https://blog.eyas.sh/2019/10/use-trackby-in-angular-ngfor-loops-and-mattables/
author: Eyas Sharaiha
published: '2019-10-29'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Note:This article was written for the old`*ngFor`

syntax, when`trackBy`

(called`track`

in the new`@for`

syntax) wasoptional. For much of the same reasons outlined in this post,`track`

in the a`@for`

template is required.In most cases,

`TrackByFunction`

is no longer needed with the new syntax, since the example mentioned in this article could simply be written in the template as:`@for (taskItem of getTasks(category); track taskItem.id) { <!-- Content Goes Here--> }`

Angular Material Tables (

`<mat-table>`

) still need a`TrackByFunction`

passed to them to perform well.

A missing `trackBy`

in an `ngFor`

block or a data table can often result in
hard-to-track and seemingly glitchy behaviors in your web app. Today, I’ll
discuss the signs that you need to use `trackBy`

. But first—some context:

More often than not, you’ll want to render some repeated element in Angular. You’ll see code that looks like this:

```
<ng-container *ngFor="let taskItem of getTasks(category)"></ng-container>
```


In cases where the `ngFor`

is looping over the results of a function that are
created anew each time (*e.g.* an array being constructed using `.map`

and
`.filter`

), you’ll run into some issues.

Every time the template is re-rendered, a new array is created with new
elements. While newly-created array elements might be *equivalent* to the
previous ones, Angular uses
[strict equality](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Equality_comparisons_and_sameness)
on each element to determine how to handle it.

In cases where the elements are an object type, strict equality will show that each element of the array is new. This means that a re-render would have a few side-effects:

-
Angular determines all the old elements are no longer a part of the block, and

- destroys their components recursively,
- unsubscribes from all Observables accessed through an
`| async`

pipe from within the`ngFor`

body.

-
Angular finds newly-added elements, and

- creates their components from scratch,
- subscribing to new Observables (i.e. by making a new HTTP request) to each
Observable it accesses via an
`| async`

pipe.


This also leads to a bunch of state being lost:

- selection state inside the
`ngFor`

is lost on re-render, - state like a link being in focus, or a text-box having filled-in values, would go away.
- if you have
[side-effects in your Observable pipes](https://blog.eyas.sh/2018/12/observables-side-effects-and-subscriptions/), you’ll see those happen again.

## The Solution

`trackBy`

gives you the ability to define custom equality operators for the
values you’re looping over. This allows Angular to better track insertions,
deletions, and reordering of elements and components within an `ngFor`

block.

```
<ng-container
*ngFor="let taskItem of getTasks(category); trackBy: trackTask"
></ng-container>
```


… where `trackTask`

is a `TrackByFunction<Task>`

, such as:

```
trackTask(index: number, item: Task): string {
return `${item.id}`;
}
```


If you run into situations where you have Observables that are being subscribed
more often than you expect, seemingly duplicate HTTP calls being made, DOM
elements that lose interaction and selection state sporadically, you might be
missing a `trackBy`

somewhere.

## It’s not just For Loops

Any kind of data source that corresponds to repeated rows or items, especially
ones that are fetched via Observables, should ideally allow you to use
`trackBy`

-style APIs. Angular’s `MatTable`

(and the more general `CdkTable`

)
[support their own version of](https://material.angular.io/cdk/table/overview#connecting-the-table-to-a-data-source)`trackBy`

[for that purpose](https://material.angular.io/cdk/table/overview#connecting-the-table-to-a-data-source).

Since a table’s `dataSource`

will often by an `Observable`

or Observable-like
source of periodically-updating data, understanding row-sameness across updates
is very important.

Symptoms of not specifying `trackBy`

in data tables are similar to `ngFor`

loops; lost selections and interaction states when items are reloaded, and any
nested components rendered will be destroyed and re-created. The experience of
`trackBy`

-less tables might be even worse, in some cases: changing a table sort
or filtering will often be implemented at the data source level, causing a new
array of data to render once more, with all the side effects entailed.

For a table of tasks fetched as Observables, we can have:

```
<table mat-table [dataSource]="category.tasksObs" [trackBy]="trackTask"></table>
```


Where `trackTask`

is implemented identically as a `TrackByFunction<Task>`

.