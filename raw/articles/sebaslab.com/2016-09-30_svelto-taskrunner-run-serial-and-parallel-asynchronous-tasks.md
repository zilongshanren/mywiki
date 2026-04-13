---
title: Svelto TaskRunner - Run Serial and Parallel Asynchronous Tasks in Unity3D -
  Seba's Lab
url: https://www.sebaslab.com/svelto-taskrunner-run-serial-and-parallel-asynchronous-tasks-in-unity3d/
author: Sebastiano Mandalà
published: '2016-09-30'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

*Note: this is an on-going article and is updated with the new features introduced over the time. *

In this article I will introduce a better way to run coroutines using the **Svelto.Tasks TaskRunner**. I will also show how to run coroutine between threads, easily and safely. You can finally exploit the power of your processors, even if you don’t know much about multithreading. If you use Unity, you will be surprised about how simple is to pass results computed from the multithreaded coroutines to the main thread coroutines.

*What we got already: Unity and StartCoroutine*

If you are a Unity developer, chances are you know already how *StartCoroutine* works and how it exploits the powerful c# [yield](http://csharpindepth.com/Articles/Chapter6/IteratorBlockImplementation.aspx) keyword to time slice complex routines. A coroutine is a quite handy and clean way to execute procedures over time or better, asynchronous tasks.

Lately Unity improved the support of *Coroutines* and new fancy things are now possible to achieve. For example, it was already possible to run tasks in serial doing something like:

public class ExampleSingleTask : MonoBehaviour { // Use this for initialization IEnumerator Start () { yield return StartCoroutine(Task1()); yield return StartCoroutine(Task2()); yield return StartCoroutine(Task3()); } IEnumerator Task1() { ... } IEnumerator Task2() { ... } IEnumerator Task3() { ... } }

And apparently* it was also possible to exploit a basic form of continuation starting a coroutine from another coroutine:

public class ExampleSingleTask : MonoBehaviour { // Use this for initialization IEnumerator Start () { yield return StartCoroutine(Task1()); } IEnumerator Task1() { yield return StartCoroutine(Task2()); } IEnumerator Task2() { yield return StartCoroutine(Task3()); } IEnumerator Task3() { ... } }

*apparently because I never tried this on unity 4 and I wasn’t aware at that time that it was possible.

However lately it’s also possible to return an *IEnumerator* directly from another *IEnumerator* without running a new coroutine, which is actually almost 3 times faster, in terms of overhead, than the previous method:

public class ExampleSingleTask : MonoBehaviour { // Use this for initialization IEnumerator Start () { yield return StartCoroutine(Task1()); } IEnumerator Task1() { yield return Task2(); } IEnumerator Task2() { yield return Task3(); } IEnumerator Task3() { ... } }

Run parallel routines is also possible, however there is no elegant way to exploit continuation when multiple **StartCoroutine** happen at once. Basically there is no simple way to know when all the coroutines are completed.

I should add that Unity tried to extend the functionality of the Coroutines introducing new concepts like the [CustomYieldInstruction](https://docs.unity3d.com/ScriptReference/CustomYieldInstruction.html), however it fails to create a tool that can be used to solve more complex problems in a simple and elegant way, problems like, but not limited to, running several sets of parallel and serial asynchronous tasks.

*Introducing Svelto.Tasks*

Being limited by what Unity can achieve, a couple of years ago I started to work on my **TaskRunner** library and spent the last few months to evolve it in something more powerful and interesting. The set of use cases that the TaskRunner can now solve elegantly, is quite broad, but before to show a subset of them as example, I will list the main reasons why TaskRunner should be used in place of StartCoroutine:

- you can use the TaskRunner everywhere, you don’t need to be in a
*Monobehaviour*. The whole Svelto framework focuses on shifting the Unity programming paradigm from the use of the Monobehaviour class to more modern and flexible patterns. - you can use the TaskRunner to run Serial and Parallel tasks, exploiting continuation without needing to use callbacks.
- you can pause, resume and stop whatever set of tasks running.
- you can catch exceptions from whatever set of tasks running.
- you can pass parameters to whatever set of tasks running.
- you can exploit continuation between threads (!).
- Whatever the number of tasks you are running is, the TaskRunner will always run just one Unity coroutine (with some exceptions).
- you can run tasks on different schedulers (including schedulers on different threads!).
- you can transform whatever asynchronous operation into a task, thanks to the
*ITask*interface.

A subset of use cases that the TaskRunner is capable to handle, is what I am going to show you soon, and I am sure you will be surprised by some of them :). TaskRunner can be used in multiple ways and, while the performance doesn’t change much between methods, you would fully exploit the power of the library only knowing when to use what. Let’s start:

The simplest way to use the TaskRunner is to use the function Run, passing whatever IEnumerator in it.

public void TestComplexCoroutine() { _taskRunner.Run(ComplexEnumerator((i) => Assert.That(i == 100, Is.True))); } IEnumerator ComplexEnumerator(Action<int> callback) { int i = 0; int j = 0; while (j < 10) { j++; var enumerator = SubEnumerator(i); yield return enumerator; //it will be executed on the same frame i = (int)enumerator.Current; //carefull it will be unboxed } callback(i); } IEnumerator SubEnumerator(int i) { int count = i + 10; while (i++ < count) yield return null; //enable asynchronous execution yield return i; //careful it will be boxed; }

This simply does what says on the tin. It’s very similar to the *StartCoroutine* function, but it can be called from everywhere. Just pay attention to the fact that

TaskRunner uses the not generic IEnumerator underneath, so using generic IEnumerator, with a value type as parameter, will always result in boxing (as shown in the example above).

TaskRunner can be also used to run every combination of serial and parallel tasks in this way:

public void TestParallelTasksAreExecutedInSerial() { bool parallelTasks1Done = false; bool parallelTasks2Done = false; parallelTasks1.Add(task1); parallelTasks1.Add(iterable1); parallelTasks1.onComplete += () => { Assert.That(parallelTasks2Done, Is.False); parallelTasks1Done = true; }; parallelTasks2.Add(task2); parallelTasks2.Add(iterable2); parallelTasks2.onComplete += () => { Assert.That(parallelTasks1Done, Is.True); parallelTasks2Done = true; }; serialTasks1.Add(parallelTasks1); serialTasks1.Add(parallelTasks2); serialTasks1.onComplete += () => { Assert.That(parallelTasks1Done == true && parallelTasks2Done == true); }; TaskRunner.Instance.Run(serialTasks1); }

But why not exploit the IEnumerator continuation? It’s more elegant than using callbacks and we don’t need to use a SerialTaskCollection explicitly (with no loss of performance). We won’t even need to use two ParallelTasks:

public void TestParallelTasks1IsExecutedBeforeParallelTask2 () { TaskRunner.Instance.Run(SerialContinuation()); } IEnumerator SerialContinuation() { bool parallelTasks1Done = false; bool parallelTasks2Done = false; parallelTasks1.Add(task1); parallelTasks1.Add(iterable1); yield return parallelTasks1; Assert.That(parallelTasks2Done, Is.False); parallelTasks1Done = true; parallelTasks1.Reset(); parallelTasks1.Add(task2); //at this point parallelTasks1 is empty again parallelTasks1.Add(iterable2); yield return parallelTasks1; Assert.That(parallelTasks1Done, Is.True); parallelTasks2Done = true; Assert.That(parallelTasks1Done && parallelTasks2Done); }

if you feel fancy, you can also use the extension methods provided:

public void TestParallelTasks1IsExecutedBeforeParallelTask2 () { SerialContinuation().Run(); }

*Svelto.Tasks and Unity compatibility*

you are used to yield special objects like *WWW*, *WaitForSeconds* or *WaitForEndOfFrame.* Those functions are not enumerators and they work because Unity is able to recognize them and run special functions accordingly. For example, when you return WWW, Unity will run a background thread to execute the http request. If WWW is not able to reach Unity framework, it will never be able to run properly. For this reason, the **MainThreadRunner** is actually compatible with all the Unity functions. You can yield them, however there are limitations: you cannot yield them, as they are, from a **ParallelTaskCollection**. If you do it, the ParallelTaskCollection will stop executing and will wait Unity to return the result, effectively loosing the benefits of the process. Whenever you return a Unity special async function from inside a ParallelTaskCollection, you’ll need to wrap it inside an *IEnumerator* if you want to take advantage of the parallel execution. This is the reason why *WWWEnumerator*, *WaitForSecondsEnumerator* and *AsyncOperationEnumerator *exist.

*TaskRoutines and Promises*

When c# coders think about asynchronous tasks, they think about the .net [Task Library](https://msdn.microsoft.com/en-us/library/dd460717(v=vs.110).aspx). The Task Library is an example of an easy to use tool that can be used to solve very complex problems. The main reason why the Task Library is so flexible, is because it’s [Promises](http://www.what-could-possibly-go-wrong.com/promises-for-game-development/?utm_source=ash&utm_medium=unity-answers&utm_campaign=promises) compliant. While the Promises design has been proved proficient through many libraries, it can also be implemented in several ways, but in every case, what makes the promises powerful, is the idea to implement continuation without using messy events all over the code.

In Sveto.Tasks, the promises pattern is implemented through the ITaskRoutine interface. let’s see how it works: an *ITaskRoutine* is a coroutine already prepared and ready to start at your command. To create a new *ITaskRoutine* simply run this function:

ITaskRoutine reusableTaskRoutine = TaskRunner.Instance.AllocateNewTaskRoutine();

Since an allocation actually happens, it’s best to preallocate and prepare a routine during the initialization phase and run it during the execution phase. A task routine can also be reused, changing all the parameters, before to run it again. Running an empty *ITaskRoutine* will result in an exception thrown, so we need to prepare it first. You can do something like:

_reusableTaskRoutine = TaskRunner.Instance.AllocateNewTaskRoutine().SetEnumeratorProvider(EnumeratorFunction);

In this case I used the function *SetEnumeratorProvider* instead of *SetEnumerator*. In this way the Task Runner is able to recreate the enumerator in case you want to start the same function multiple times. Let’s see what we can do:

We can Start the routine like this using

_reusableTaskRoutine.Start();

We can Pause the routine using

_reusableTaskRoutine.Pause();

We can Resume the routine using

_reusableTaskRoutine.Resume()

we can Stop the routine using (it’s getting tedious)

_reusableTaskRoutine.Stop()

we can Restart the routine using

_reusableTaskRoutine.Start()

You can check the **ExampleTaskRoutine** example out to see how it works.

Let’s see how *ITaskRoutine* are compliant with Promises. As we have seen, we can pipe serial and/or parallel tasks and exploit continuation. We can get the result from the previous enumerator as well, using the current properties. We can pass parameters, through the enumerator function itself. The only feature we haven’t seen yet is how to handle failures, which is obviously possible too.

For the failure case I used an approach similar to the .net Task library. You can either stop a routine from a routine, yielding Break.It; or throwing an exception. All the exceptions, including the ones threw on purpose, will interrupt the execution of the current coroutine chain. Let’s see how to handle both cases with some, not so practical, examples.

using System; using System.Collections; using Svelto.Tasks; using UnityEngine; public class ExamplePromises : MonoBehaviour { // Use this for initialization void Start() { TaskRunner.Instance.AllocateNewTaskRoutine().SetEnumerator(RunTasks(2)).Start(onStop: OnStop); } void OnStop() { Debug.LogWarning("oh oh, did't happen on time, let's try again"); TaskRunner.Instance.AllocateNewTaskRoutine().SetEnumerator(RunTasks(1000)).Start(OnFail); } void OnFail(PausableTaskException obj) { Debug.LogError("tsk tsk"); } IEnumerator RunTasks(int timeout) { var enumerator = GetURLAsynchronously(); yield return enumerator; string url = enumerator.Current as string; //yep it will be converted to a Parallel task yield return new[] { BreakOnTimeOut(timeout), new LoadSomething(new WWW(url)).GetEnumerator() }; } IEnumerator GetURLAsynchronously() { //well not real reason to wait, let's assume we were running a web service yield return new WaitForSecondsEnumerator(1); yield return "http://download.thinkbroadband.com/50MB.zip"; } IEnumerator BreakOnTimeOut(int timeout) { var time = DateTime.Now; yield return new WaitForSecondsEnumerator(timeout); Debug.Log("time passed: " + (DateTime.Now - time).TotalMilliseconds); //basically is the inverse of the Race Promises function, achieve the same result yield return Break.It; } class LoadSomething : IEnumerable { public LoadSomething(WWW wWW) { this.wWW = wWW; } public IEnumerator GetEnumerator() { Debug.Log("download started"); yield return new[] { new WWWEnumerator(wWW), PrintProgress(wWW) }; foreach (string s in wWW.responseHeaders.Values) Debug.Log(s); Debug.Log("Success! Let's throw an Exception because I am crazy"); throw new Exception("Dayyym"); } IEnumerator PrintProgress(WWW wWW) { while (wWW.isDone == false) { Debug.Log(wWW.progress); yield return null; } } WWW wWW; } }

In the example above we can see several new concepts. First of all, it shows how to use the *Start()* method providing what to execute when the ITaskRoutine is stopped or if an exception is thrown from inside the routine. It shows how to **yield Break.It **to emulate the *Race* function of the promises pattern. **Break.It** is not like returning yield break, it will actually break the whole coroutine from where the current enumerator has been generated. At last it shows how to yield an array of *IEnumerator* as syntactic sugar in place of the normal Parallel Task generation. Just to be precise, *OnStop* will NOT be called when the task routine completes, it will be called only when *ITaskRoutine Stop()* or *yield Break.It* are used.

**Update:**

*Break.it *will now break the current running task collection. This means that if you run Break.It inside a *ParallelTaskCollection* or *SerialTaskCollection* it will break the current collection only and not the whole *ITaskRoutine*. In this case *Stop()* won’t be called, but the TaskCollection completes. This is how to use Break.It in a real life scenario:

IEnumerator LaunchFinalSteps(ParallelTaskCollection parallelTasks, float seconds) { yield return new WaitForSecondsEnumerator(seconds); yield return new[] { TasksCompetitor(parallelTasks), TimeOutCompetitor() }; ReturnAllConnectedPlayersToMothership(); ExecuteShutServerCommand(); } IEnumerator TasksCompetitor(ParallelTaskCollection parallelTasks) { yield return parallelTasks; yield return Break.It; } IEnumerator TimeOutCompetitor() { yield return new WaitForSecondsEnumerator(PARALLELTASK_TIMEOUT_SEC); Utility.Console.LogError("TimeOutCompetitor"); yield return Break.It; }

Now let’s talk about something quite interesting: the schedulers. So far we have seen our tasks running always on the standard scheduler, which is the Unity main thread scheduler. However you are able to define your own scheduler and you can run the task whenever you want! For example, you may want to run tasks during the *LateUpdate* or the *PhysicUpdate*. In this case you may implement your own *IRunner* scheduler or even inherit from **MonoRunner **and run the *StartCoroutineInternal* as a callback inside the Monobehaviour that will drive the *LateUpdate* or *PhysicUpdate*. Using a different scheduler than the default one is pretty straightforward:

_taskRunner.RunOnSchedule(StandardSchedulers.syncScheduler,serialTasks1); _reusableTaskRoutine = TaskRunner.Instance.AllocateNewTaskRoutine().SetScheduler(StandardSchedulers.syncScheduler); EnumeratorFunction().RunOnSchedule(StandardSchedulers.syncScheduler);

*Multithread and Continuation between threads*

But what if I tell you that you can run tasks also on other threads? Yep that’s right, your scheduler can run on another thread as well and, in fact, one Multithreaded scheduler is already available. However you may wonder, what would be the practical way to use a multithreaded scheduler? Well, let’s spend some time on it, since what I came out with, is actually quite intriguing. Caution, we are now stepping in the twilight zone.

First of all, all the features so far mentioned work on whatever scheduler you put them on. This is fundamental in the design, however some limitations may be present due to the Unity not thread safe nature. For example, the **MultiThreadRunner**, won’t be able to detect special Unity coroutines, like WWW, AsyncOperation or YieldInstruction, which is obvious, since they cannot run on anything else than the main thread. You may wonder what the point of using a MultiThreadRunner is, if eventually it cannot be used with Unity functions. The answer is continuation! With continuation you can achieve pretty sweet effects.

Let’s see an example, enabling the **PerformanceMT** GameObject from the scene included in the library code. It compares the same code running on a normal StartCoroutine (*SpawnObjects*) and on another thread (*SpawnObjectsMT*). Enable only the MonoBehaviour you want test to compare the performance. What’s happening? Both MBs spawn 150 spheres that will move along random directions. In both cases, a slow coroutine runs. The coroutine goal is to compute the largest prime number smaller than a given random value between 0 and 1000; The result will be used to compute the current sphere color which will be updated as soon as it’s ready. The following is the multithreaded version:

public class DoSomethingHeavy2 : MonoBehaviour { Vector2 direction; void Start() { TaskRunner.Instance.RunOnSchedule(StandardSchedulers.multiThreadScheduler, CalculateAndShowNumber()); direction = new Vector2(Mathf.Cos(Random.Range(0, 3.14f)) / 1000, Mathf.Sin(Random.Range(0, 3.14f) / 1000)); } IEnumerator CalculateAndShowNumber() //this will run on another thread { while (true) { IEnumerator enumerator = FindPrimeNumber((rnd1.Next() % 1000)); yield return enumerator; long result = (long)enumerator.Current * 333; //yep the thread will wait for this other task to finish on the mainThreadScheduler yield return SetColor(result).ThreadSafeRunOnSchedule(StandardSchedulers.mainThreadScheduler); } } IEnumerator SetColor(long result) { GetComponent<Renderer>().material.color = new Color((result % 255) / 255f, ((result * result) % 255) / 255f, ((result / 44) % 255) / 255f); yield return null; } void OnApplicationQuit() { //Unity will get stuck for ever if you don't do this StandardSchedulers.StopSchedulers(); } void Update() { transform.Translate(direction); } public IEnumerator FindPrimeNumber(int n) { int count = 0; long a = 2; while (count < n) { long b = 2; int prime = 1;// to check if found a prime while (b * b <= a) { if (a % b == 0) { prime = 0; break; } b++; } if (prime > 0) count++; a++; } yield return --a; } static System.Random rnd1 = new System.Random(); //not a problem, multithreaded coroutine are threadsafe within the same runner }

Well I hope it’s clear to you at glance. First we run **CalculateAndShowNumber** on the **multiThreadScheduler**. We use the same **MultiThreadRunner** instance for all the game objects, because otherwise we would spawn a new thread for each sphere and we don’t want that. One extra thread is more than enough (I will spend few words on it in a bit).

**FindPrimeNumber** is supposed to be a slow function, which it is. As a matter of fact, if you run the single threaded version (enabling the SpawnObject monobehaviour instead of SpawnObjectMT) you will notice that the frame rate is fairly slow. In fact, the GPU must wait the CPU to compute the prime number.

The Multithreaded version runs the main enumerator on another thread, but how can the color be set since it’s impossible to use the Renderer component from anything else than the main thread? This is where a bit of magic happens. Returning the enumerator from a task, running on another scheduler, will actually continue its execution on that scheduler. You may think that at this point the thread will wait for the enumerator running on the main thread to continue. This is partially true, since differently than a *Thread.Join()*, the thread is actually not stalled, it will continue yielding, so if other tasks are running on the same thread, they will be actually processed. At the end of the main thread enumerator, the path will return to the other thread and continue from there. Quite fascinating, I’d say, also because you could expect great difference in performance.

How to use the multithreaded tasks with the new Svelto.Tasks. I didn’t use it in production yet, how does it look?

[https://t.co/pFz8egB6TX][pic.twitter.com/MEp2DVHBcA]— Sebastiano Mandalà (@sebify)

[October 3, 2016]

So, We have seen some advanced applications of the TaskRunner using different threads, but since Unity will soon support c#6, you could wonder why to use the Svelto TaskRunner instead of the Task.Net library. Well, they serve two different purposes. Task.Net library has not been designed for applications that could run heavy routines on threads. The Task.Net and the await/async keywords heavily exploit the *Thread.Pool* to use as many threads as possible, with the condition that most of the time, these threads are very short-lived. Basically it’s designed to serve applications that run hundreds of short lived and light asynchronous tasks. This is usually true when we talk about server applications.

For games instead, what we generally need, are few threads where to run heavy operations that can go in parallel with the main thread and this is what the TaskRunner has been designed for. You will also be sure that all the routines running on the same MultiThreadRunner scheduler instance, won’t occur in any concurrency issue. In fact, you may see every Multithread runner as a [Fiber](https://www.quora.com/What-is-the-difference-between-a-fiber-and-a-thread) (if you feel brave, you can also check this very [interesting video](http://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine)). It’s also worth to notice that the MultiThreadRunner will keep the thread alive as long as it is actually used, effectively letting the Thread.Pool (used underneath) to manage the threads properly.

*Other stuff…*

To complete this article, I will spend few words on other two minor features. As previously mentioned, the TaskRunner will identify *IAbstractTask* implementations as well. Usually you will need to implement an *ITask* interface to be useful. The ITask is meant to transform whatever class in a task that can be executed through the task runner. For example, it could be used to run web services, which result will be yielded on the main thread.

class Task : ITask { //ITask Implementation public bool isDone { get; private set; } public Task() { isDone = false; } //ITask Implementation public void Execute() { _delayTimer = new System.Timers.Timer { Interval = 1000, Enabled = true }; _delayTimer.Elapsed += _delayTimer_Elapsed; _delayTimer.Start(); } public void OnComplete(Action action) { _onComplete += action; } void _delayTimer_Elapsed(object sender, System.Timers.ElapsedEventArgs e) { isDone = true; if (_onComplete != null) _onComplete(); _delayTimer.Stop(); _delayTimer = null; } System.Timers.Timer _delayTimer; Action _onComplete; }

The *ITaskChain* interface is something still at its early stage and it could be changed or deprecated in future. It could be useful to know parameters that are passed through tasks, like a sort of Chain Of Responsibility pattern.

public void Setup () { vo = new ValueObject(); serialTasks1 = new SerialTaskCollection<ValueObject>(vo); parallelTasks1 = new ParallelTaskCollection<ValueObject>(vo); serialTasks2 = new SerialTaskCollection<ValueObject>(vo); parallelTasks2 = new ParallelTaskCollection<ValueObject>(vo); taskChain1 = new TaskChain(); taskChain2 = new TaskChain(); } public void TestSerialTasks1ExecutedInParallelWithToken () { serialTasks1.Add(taskChain1); serialTasks1.Add(taskChain1); serialTasks2.Add(taskChain2); serialTasks2.Add(taskChain2); parallelTasks1.Add(serialTasks1); parallelTasks1.Add(serialTasks2); parallelTasks1.onComplete += () => Assert.That(vo.counter, Is.EqualTo(4)); _taskRunner.Run(parallelTasks1); } class TaskChain: ITaskChain<ValueObject> //the execute function gets the token { public bool isDone { get; private set; } public TaskChain() { isDone = false; } public void Execute(ValueObject token) { token.counter++; isDone = true; } }

The very last thing to take in consideration is the compatibility with Unity WWW, AsyncOperation and YieldInstruction objects. As long as you are not using parallel task, you can yield them from your enumerator and they will work as you expect! However you cannot use them from a parallel collection unless you wrap them in another IEnumerator, that’s why *WWWEnumerator* and *AsyncOperationEnumerator* classes exist.

The source code and examples are available from here: [https://github.com/sebas77/Svelto.Task](https://github.com/sebas77/Svelto.Task). Every feedback is more than welcome. Please let me know if you find any bug!

*Notes on Optimizations*

TaskRunner has been designed with optimizations in mind. Without counting the multithreaded runner, extensive use of TaskRunner will actually results in performance increase over the normal use of *StartCoroutine* and the normal *Update* functions. MonoRunner works using one single unity coroutine (Except in the few cases when they are handled to Unity) for all the performing tasks., this will eliminate all the overhead needed to run hundreds of separate Updates. TaskRunner is also very useful to run time-slicing tasks.

**03/11/16 Notes**

I realised that *MonoRunner* was behaving differently than the Unity *StartCoroutine* function since the latter runs the enumerator immediately, while MonoRunner was waiting for the next available slot. I changed its behaviour now, but this meant to introduce a not so elegant ThreadSafe version of every *Run* function.

**08/01/17 Notes**

Some minor changes and improvement of examples

- Added a Editor Profiler to keep track of the tasks performance
- WWW is not handed to Unity anymore, yield it always through WWWEnumerator
- To avoid confusion, IEnumerable cannot be yielded directly anymore

**22/10/17 Notes**

A ton of features have been introduced and I have not been diligent enough to keep track of them properly. I will list the highlights:

- Surely I have introduced some breaking changes, but they will be simple to fix
- Massively improved the multi-threading related features, I know I need to write a good example on how to use them
- The unit tests now run through the official Unity tests runner
- improved examples and unit tests
- Pausing/Resuming/Stopping/Starting
**ITaskroutines**now works better and makes more sense - The profiler now can recognize tasks running on other threads and profile them (very cool)
- Rewritten the
**MultiThreadedParallelTaskCollection**and now is usable. A good example has been written as well and you can found it[here](http://www.sebaslab.com/svelto-ecs-svelto-tasks-new-example-plus-whats-coming-and-optimization-related-thoughts/). - yield break will stop the current Enumeration only, yield Break.It stops the current TaskCollection, yield.BreakAndStop stops the whole ITaskRoutine and triggers the stop callback
- several optimizations
- Important:
**TaskCollection**logic has been rewritten to be able to reuse them after the enumeration ends (They can restart). In order to Clear them the new Clear function is added as Reset won’t clear them anymore - Added
**LateMonoRunner**and**UpdateMonoRunner**(you can guess when they run 🙂 ) - Added
**StaggeredMonoRunner**. It allows to spread tasks over N frames - It’s now possible to create several MonoRunners. In this way you can manage and leave the “standard” ones alone when you need to do weird stuff
- Breaking change: the
**TaskCollection**doesn’t accept Enumerables anymore. This is because it was bad to hide the GetEnumerator() allocation that should have been done anyway. - The code after any
*WaitForEndOfFrame*,*WaitForFixedUpdate*and similar will be now executed when it’s expected

Check out the new articles:

If it’s promises you are interested in please check out my articles and open source work on this:

Using promises for Unity async operations: http://www.what-could-possibly-go-wrong.com/using-promises-for-unity-async-operations/

Promises for game dev: http://www.what-could-possibly-go-wrong.com/promises-for-game-development/

Promises library: https://github.com/Real-Serious-Games/C-Sharp-Promise

Your article is already linked 😉

Just two quick comments: [..]”I realised that MonoRunner was behaving differently than the Unity StartCoroutine function since the latter runs the enumerator immediately, while MonoRunner was waiting for the next available slot. I changed its behaviour now, but this meant to introduce a not so elegant ThreadSafe version of every Run function.” [..] How did this impact your solution ? Is the new ThreadSafe version of Run worse of the predecessor in some way ? [..]”The very last thing to take in consideration is the compatibility with Unity WWW, AsyncOperation and YieldInstruction objects. As long as you are not using… Read more »

This crash on unity 5.4

Do you have a backup for unity 5.4 version?

Or you mean the example? In that case I’ll check this weekend

Yes the example, already logs out 59 errors and when i press play Unity crashes.

I understand, it’s possible that I upgraded it to 5.5 and it’s not back compatible, I’ll need to check to confirm.

We are using it on 5.4, can you show me the stack please?

I got this error from the project. NUnit.Framework.TestFixtureAttribute is defined multiple times

Also, SpawnObjects and SpawnObjectsMT have exactly the same code.

I use Unity 5.6.1

If you just got the files from the repo it means I still have to update it to the last version. I’ll try to do it today.