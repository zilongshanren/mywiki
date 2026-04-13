---
title: In Search of Better Loading and Error-handling in Angular
url: https://blog.eyas.sh/2020/05/better-loading-and-error-handling-in-angular/
author: Eyas Sharaiha
published: '2020-05-04'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

For many, Reactive programming seems like a conceptually elegant approach that falls apart the moment you try to do any serious programming. When adding essential error handling, refreshable state, etc. into an application, many folks see their codebases move further from the promise of clean, elegant reactive transforms.

It doesn’t have to be this way. While I’ve argued before for cleaner display of
refreshable data by [using AsyncPipe](https://blog.eyas.sh/2018/12/use-asyncpipe-when-possible)

[adopting better patterns for data refresh](https://blog.eyas.sh/2018/12/data-and-page-content-refresh-patterns-in-angular), this advice on its own does not provide an end-to-end pattern of displaying data from the moment it is loading all the way to error handling and refresh.

In this post, we’ll experiment with various ways to handle loading and errors when fetching dynamic data.

## Our Starting Point

In my [Use AsyncPipe article](https://blog.eyas.sh/2018/12/use-asyncpipe-when-possible), I
contended that rendering an Observable solely through a template and AsyncPipe
was ideal. A basic “loading” example was presented, where the template looks
something like this:

```
<ng-container *ngIf="(page$ | async) as page; else loading">
<h1>{{page.title}}</h1>
<p>{{page.paragraph}}</p>
</ng-container>
<ng-template #loading>
<mat-spinner></mat-spinner>
</ng-template>
```


The main problem here is that the spinner will appear indefinitely if the observable encounters an error.

## Option A: Catch-and-Present

One promising approach is to just catch that error and make `page$`

contain
either a page or an error message/state:

```
readonly page$ = this.pageService.loadPage().pipe(
catchError(e => of({error: e.message}))
);
```


In this case `page$`

is now `Observable<Page|{error: string}>`

. We can render
this as such:

```
<ng-container *ngIf="(page$ | async) as page; else loading">
<ng-container *ngIf="!!page.error; else error">
<h1>{{page.title}}</h1>
<p>{{page.paragraph}}</p>
</ng-container>
<ng-template #error> Failed to load page: {{page.error}}. </ng-template>
</ng-container>
<ng-template #loading>Loading…</ng-template>
```


One drawback of this is that it isn’t clear how a result being reloaded can ever go back to the “Loading” state.

## Option B: Modeling Result State

One approach that *looks* more elegant on a first glance is modeling our
observable state in a more defined way:

```
enum ContentState {
LOADING,
LOADED,
ERROR,
}
type Loading = { state: ContentState.LOADING };
type Error = { state: ContentState.ERROR; error: string };
type Loaded<T> = { state: ContentState.LOADED; item: T };
type Rendered<T> = Loading | Error | Loaded<T>;
```


Given an `Observable<Rendered<T>>`

, a template can look like this:

```
<!-- Use *ngIf as a mechanism to save the variable -->
<ng-container *ngIf="(page$ | async) as result;" [ngSwitch]="result.state">
<ng-container *ngSwitchCase="ContentState.LOADING">
<mat-spinner></mat-spinner>
</ng-container>
<ng-container *ngSwitchCase="ContentState.ERROR">
Failed to load page: {{result.error}}.
</ng-container>
<ng-container *ngSwitchCase="ContentState.LOADED">
<h1>{{result.item.title}}</h1>
<p>{{result.item.paragraph}}</p>
</ng-container>
</ng-container>
```


For example, for the simple use-case:

```
@Component()
class PageComponent {
readonly ContentState = ContentState;
readonly page$ = this.pageService.loadPage().pipe(
map((item) => ({ state: ContentState.LOADED, item })),
startWith({ state: ContentState.LOADING }),
catchError((e) => of({ state: ContentState.ERROR, error: e.message }))
);
}
```


The nice thing about this approach is we can always emit a
`ContentState.LOADING`

event when the content is being reloaded.

For example…

**when content is periodically refreshed**:

```
@Component()
class PageComponent {
readonly ContentState = ContentState;
readonly page$ = timer(0, 60 * 1000).pipe(
switchMap(() =>
this.pageService.loadPage().pipe(
map((item) => ({
state: ContentState.LOADED,
item,
})),
startWith({ state: ContentState.LOADING }),
catchError((e) =>
of({
state: ContentState.ERROR,
error: e.message,
})
)
)
)
);
}
```


or **when new filters are requested**:

```
@Component()
class PageComponent {
readonly ContentState = ContentState;
readonly requestedFilter$ = new BehaviorSubject<Filter>({});
readonly page$ = this.requestedFilter$.pipe(
switchMap((filter) =>
this.pageService.loadPage(filter).pipe(
map((item) => ({
state: ContentState.LOADED,
item,
})),
startWith({ state: ContentState.LOADING }),
catchError((e) =>
of({
state: ContentState.ERROR,
error: e.message,
})
)
)
)
);
}
```


The main drawback here is that the existing content will disappear as soon as we attempt to fetch new content.

You can also see how progressively more complicated this mode becomes the moment we run into refreshing patterns.

## Option C: Modeling State with Multiple Observables

Rather than try to encompass the entire state in one rich observable, we can
take advantage of Observable caching and sharing to define a `content$`

,
`isLoading$`

, and `error$`

Observables, all driven by the same events or data.

This way, we can reason about each of these observables separately and in terms of the others.

Given the three observables, we can render out content as such:

```
<mat-progress-bar *ngIf="(isLoading$ | async)" mode="indeterminate">
</mat-progress-bar>
<div *ngIf="(error$ | async) as error">Error: {{error.message}</div>
<ng-container *ngIf="(content$ | async) as page">
<h1>{{page.title}}</h1>
<p>{{page.paragraph}}</p>
</ng-container>
```


This way, we have control to decide what content to display independently from whether a loading spinner or an error is displayed.

In the simple case, our component looks like this:

```
@Component()
class PageComponent {
readonly content$ = this.pageService
.loadPage()
.pipe(publishReplay(1), refCount());
readonly isLoading$ = this.content$.pipe(mapTo(false), startWith(true));
readonly error$ = this.content$.pipe(
mapTo(false),
catchError((e) => of(e))
);
}
```


This perhaps is too complicated to see the benefit. Once we start having more
complex uses, however, you’ll see that reasoning about `isLoading$`

and `error$`

separately is very helpful:

For example, **when content is periodically refreshed**:

```
@Component()
class PageComponent {
private readonly trigger$ = timer(0, 60 * 1000).pipe(
publishReplay(1),
refCount()
);
readonly content$ = this.trigger$.pipe(
switchMap(() => this.pageService.loadPage()),
publishReplay(1),
refCount()
);
readonly isLoading$ = merge(
this.trigger$.pipe(mapTo(true)),
this.content$.pipe(
// Even errors indicate we're not
// still loading.
catchError(() => of(undefined)),
mapTo(false)
)
);
readonly error$ = this.content$.pipe(
mapTo(false),
catchError((e) => of(e))
);
}
```


or **when new filters are requested**:

```
@Component()
class PageComponent {
readonly requestedFilter$ = new BehaviorSubject<Filter>({});
readonly content$ = this.requestedFilter$.pipe(
switchMap((f) => this.pageService.loadPage(f)),
publishReplay(1),
refCount()
);
readonly isLoading$ = merge(
this.requestedFilter$.pipe(mapTo(true)),
this.content$.pipe(
// Even errors indicate we're not
// still loading.
catchError(() => of(undefined)),
mapTo(false)
)
);
readonly error$ = this.content$.pipe(
mapTo(false),
catchError((e) => of(e))
);
}
```


These last two examples illustrate what is powerful about this approach: given
`trigger$`

(cause of refetching data) and `content$`

(result of fetching data)
we can define `isLoading$`

and `error$`

very elegantly:

```
function isLoading(
trigger$: Observable<unknown>,
content$: Observable<unknown>
): Observable<boolean> {
return merge(
trigger$.pipe(mapTo(true)),
content$.pipe(
catchError(() => of(undefined)),
mapTo(false)
)
);
}
function isError(content$): Observable<false | Error> {
return content$.pipe(
mapTo(false),
catchError((e) => of(e))
);
}
// or, alternatively: To clear error once a new fetch is triggered:
function isError(trigger$, content$): Observable<false | Error> {
return merge(trigger$, content$).pipe(
mapTo(false),
catchError((e) => of(e))
);
}
```


With this, we can take our examples from the
[Data and Page Content Refresh patterns in Angular](https://blog.eyas.sh/2018/12/data-and-page-content-refresh-patterns-in-angular/)
article and give it elegant loading and error indicators:

```
@Component()
export class TaskComponent {
constructor(
private readonly http: HttpClient,
private readonly route: ActivatedRoute
) {}
private readonly autoRefresh$ = timer(0, TASK_REFRESH_INTERVAL_MS);
private readonly refreshToken$ = new BehaviorSubject(undefined);
markAsComplete() {
this.route.params
.pipe(
map(([params]) => params["task_id"]),
switchMap((taskId) =>
this.http.post(`/api/tasks/${taskId}`, {
state: State.Done,
})
)
)
.subscribe(() => this.refreshToken$.next(undefined));
}
private readonly trigger$ = combineLatest(
this.route.params,
this.autoRefresh$,
this.refreshToken$
).pipe(publishReplay(1), refCount());
readonly task$ = this.trigger$.pipe(
switchMap(([params]) =>
this.http.get(`/api/tasks/${params["task_id"]}`)
),
publishReplay(1),
refCount()
);
readonly isLoading$ = isLoading(this.trigger$, this.task$);
readonly error$ = isError(this.trigger$, this.task$);
}
```


## Closing Thoughts

It seems like there’s some merit to look at various stateful constructs
(`isLoading`

, `error`

, etc.) as individual Observable “views” of some common
streams that drive this data.

Deriving multiple values from other underlying observables does have a downside: we now need to worry about one of the uglier parts of Observables: sharing, caching, and reference counting.