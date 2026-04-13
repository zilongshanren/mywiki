---
title: Data and Page Content Refresh patterns in Angular
url: https://blog.eyas.sh/2018/12/data-and-page-content-refresh-patterns-in-angular/
author: Eyas Sharaiha
published: '2018-12-14'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Part of why I recommend using RxJS `Observable`

s all the way through in Angular
TypeScript code, and
[only unpacking them at the closest point to where the UI is declared (often using the | async pipe)](https://blog.eyas.sh/2018/12/use-asyncpipe-when-possible/),
is because it makes other transformations on an

`Observable`

available and
convenient. Two such examples include retry and refresh logic.Two common reasons to reload/refresh data being displayed by a component include:

- A user action in the application causes the data to change (especially, if it does so in ways that might result in complex state changes, etc.), and/or
- The data being displayed can change over time (e.g. due to a progression/change of its state in the backend, or by another user, etc.)

Let’s start with a simple example:

```
@Component({
selector: "task",
template: `@if (task$ | async; as task) {
<h1>{{task.name}}</h1>
<p>Status: {{task.status}}</p>
@for (subTask of task.subtasks; track subTask.id) {
<sub-task [subTask]="subTask"></sub-task>
}
}`,
})
export class TaskComponent {
constructor(private readonly http: HttpClient) {}
readonly task$ = this.http.get("/api/tasks/foo");
}
```


Suppose the user adds a ‘Mark as Complete’ button, that mutates the server-side state of all sub-tasks. How do we obtain the latest authoritative data from the server about the state of our side? Here’s an approach:

```
export class TaskComponent {
constructor(private readonly http: HttpClient) {}
private readonly refreshToken$ = new BehaviorSubject(undefined);
private readonly task$ = this.refreshToken$.pipe(
switchMap(() => this.http.get("/api/tasks/foo"))
);
markAsComplete() {
this.http
.post("/api/tasks/foo", { state: State.Done })
// N.B. contrary to my advice elsewhere, I'm happy to
// directly subscribe here because this subscribe
// callback has side effects.
// Further, I don't worry about unsubscribing since
// this returned Observable is a one-shot observable
// that will complete after a single request.
.subscribe(() => this.refreshToken$.next(undefined));
}
}
```


Adding refresh logic this way will minimally affect our template code and looks
relatively clean. Better yet, adding additional mutating functions simply need
to call `refreshToken$.next`

to make sure new data is loaded.

What about **regularly polling for updates**? This can be implemented simply as
well:

```
export class TaskComponent {
constructor(private readonly http: HttpClient) {}
private readonly autoRefresh$ = interval(TASK_REFRESH_INTERVAL_MS).pipe(
startWith(0)
);
private readonly refreshToken$ = new BehaviorSubject(undefined);
private readonly task$ =
// Notice that combineLatest will only trigger the first
// time when an event triggers on all input Observables
// you are combining.
// BehaviorSubject always triggers its latest value when
// you subscribe to it, so we're good there.
// An interval() Observable will need a 'startWith' to
// give you an initial event.
combineLatest(this.autoRefresh$, this.refreshToken$).pipe(
switchMap(() => this.http.get("/api/tasks/foo"))
);
markAsComplete() {
this.http
.post("/api/tasks/foo", { state: State.Done })
.subscribe(() => this.refreshToken$.next(undefined));
}
}
```


**What if we didn’t want to hardcode foo as the task we lookup?** Well,
Angular’s

`ActivatedRoute`

already uses `Observable`

s. Rather than using
`route.snapshot.params['task_id']`

or similar, we can use the actual Observable
results and get our minds off manually refreshing that data:```
export class TaskComponent {
constructor(
private readonly http: HttpClient,
private readonly route: ActivatedRoute
) {}
private readonly autoRefresh$ = interval(TASK_REFRESH_INTERVAL_MS).pipe(
startWith(0)
);
private readonly refreshToken$ = new BehaviorSubject(undefined);
private readonly task$ = combineLatest(
this.route.params,
this.autoRefresh$,
this.refreshToken$
).pipe(
switchMap(([params]) =>
this.http.get(`/api/tasks/${params["task_id"]}`)
)
);
markAsComplete() {
this.route.params
.pipe(
take(1), // only take the first event
map(([params]) => params["task_id"]),
switchMap((taskId) =>
this.http.post(`/api/tasks/${taskId}`, {
state: State.Done,
})
)
)
.subscribe(() => this.refreshToken$.next(undefined));
}
}
```


As a monad, an Observable is a neat and tidy functional construct. You can
transform it using a rich set of operators. In RxJS, those also include
`catchError`

for error handling and retrying, timed events, and combinations of
multiple monads into a monad of multiple items. With the view of Observables as
just another monad 1, reactive programming becomes just a simple extension on
top of functional programming.

Dealing with these Observables for as much of the data lifecycle as possible means that you can take advantage of these constructs to transform immutable data using neat operators, rather than dealing with unpacking this data into mutable scalars.

Further Reading:

- For a more theoretical approach:
[RxJS in Action](https://amzn.to/3gEy958) - For a more practical approach:
[Build Reactive Websites with RxJS](https://amzn.to/3defsTC) [Better Loading and Error Handling in Angular](https://blog.eyas.sh/2020/05/better-loading-and-error-handling-in-angular)[Observables, Side-effects, and Subscriptions](https://blog.eyas.sh/2018/12/observables-side-effects-and-subscriptions)

## Footnotes

-
A great resource for learning about Functional Programming and Monads in JavaScript is Dan Mantyla’s

[Functional Programming in JavaScript](https://amzn.to/3gwqG8b). Or keep reading this blog![↩](../../assets/73cd9c9dd8ab26ae.img)