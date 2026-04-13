---
title: Run Serial and Parallel Asynchronous Tasks in Unity3D and C# - Seba's Lab
url: https://www.sebaslab.com/run-serial-parallel-asynchronous-tasks-unity3d-c/
author: Sebastiano Mandalà
published: '2012-05-22'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

*Please note, this article refers to an old version of the TaskRunner which is not supported anymore. *[The latest version is here.](http://www.sebaslab.com/svelto-taskrunner-run-serial-and-parallel-asynchronous-tasks-in-unity3d/)

*Please note, this article refers to an old version of the TaskRunner which is not supported anymore.*

[The latest version is here.](http://www.sebaslab.com/svelto-taskrunner-run-serial-and-parallel-asynchronous-tasks-in-unity3d/)Every now and then it is necessary to run a series of tasks in a given order, for example to guarantee that some data has been downloaded before to continue the execution of the application. C# 4.0 offers powerful tools in order to perform these operations, like the [Task Parallel Library]( http://msdn.microsoft.com/en-us/library/dd537609.aspx), which seems very straightforward to use.

However Unity3D supports c# 3.5 only and beside the **System.Threading** routines, there are not easy way to accomplish the task.

All the Unity3D programmers know that Unity 3D exploits nicely the **yield** instruction to simulate multi-threading using ** coroutines **(which are, of course, single threaded), but what are they exactly?

As explained in many [tutorials](http://startbigthinksmall.wordpress.com/2008/06/09/behind-the-scenes-of-the-c-yield-keyword/), once an * iterator block* is met, the compiler creates a special switch case function that allows even complicated methods to be

*time-sliced*; Something very similar to the various pseudo threading framework implementations that exist for single-threading environments (like in actionscript).

Time sliced techniques have been used for ages in the game industry, mostly to spread complicated routine execution over several rendering frames. So nothing new here, except the fact that c# is so smart to be able to create very sophisticated time-sliced routine on its own, so that the code stays very readable. Albeit, using yield for the execution of several tasks could get awkward.

This is why I decided to create a library that could accept, combine and run async tasks in parallel and serial. An example of the way it can be used is given by the following method:

public void RunSerialTasksExecutedInParallel () { SerialTasks serialTasks1 = new SerialTasks (); SerialTasks serialTasks2 = new SerialTasks (); ParallelTasks parallelTasks1 = new ParallelTasks (); ITask task1 = new Task (); ITask task2 = new Task (); IEnumerable iterable1 = new Enumerable (); IEnumerable iterable2 = new Enumerable (); serialTasks1.Add (iterable1); serialTasks1.Add (iterable2); serialTasks1.onComplete += () => { Debug.Log("First bunch of serial tasks completed"); }; serialTasks2.Add (task1); serialTasks2.Add (task2); serialTasks2.onComplete += () => { Debug.Log("Second bunch of serial tasks completed"); }; parallelTasks1.Add (serialTasks1); parallelTasks1.Add (serialTasks2); parallelTasks1.onComplete += () => { Debug.Log("All Done"); }; TaskRunner.Instance.Run(parallelTasks1); }

As you can see, the code is pretty straightforward, there are just some notes to take in consideration:

- TaskRunner is a Monobehaviour that exploits the StartRoutine function to register the task(list) to run. You must have one enabled in order to start the execution.
- SerialTasks and ParallelTasks are two classes of the framework, they are quite self-explanatory
- SerialTasks and ParallelTasks can execute both standard IEnumerable and ITask objects
- ITask is a special interface added in order to manage special cases, but it is not mandatory to use.

The following is a naive example (for testing purposes) of an ITask object:

class Task : ITask { public event TasksComplete onComplete; public bool isDone { get; private set; } public void Execute () { isDone = false; //wait synchronously for 1 second //usually it is an async operation IEnumerator e = WaitHalfSecond (); while (e.MoveNext()); isDone = true; if (onComplete != null) onComplete (); } private IEnumerator WaitHalfSecond () { float time = Time.realtimeSinceStartup; while (Time.realtimeSinceStartup - time < 0.5) yield return null; } }

So what is the trick that let the sequential and parallel tasks be mixed together? The idea behind this code is to create a simple stack structure that recognize when a new IEnumerable (or IEnumerator) object is returned from a yield return. Nothing harder than:

foreach (IEnumerator enumerator in registeredEnumerators) { //create a stack for each task to run Stack stack = new Stack(); //push the first task stack.Push(enumerator); //until the stack is not empty while (stack.Count > 0) { //get the first task without removing it IEnumerator ce = stack.Peek(); //iterate over it if (ce.MoveNext() == false) //is it done? { stack.Pop(); //now it can be popped } else //ok the iteration is not over if (ce.Current != null && ce.Current != ce) //the interesting part { //is the current task actually another Enumerator (or IEnumerable)? if (ce.Current is IEnumerable) stack.Push(((IEnumerable)ce.Current).GetEnumerator()); //push it, this will be next task to be executed else if (ce.Current is IEnumerator) stack.Push(ce.Current as IEnumerator); //push it, this will be next task to be executed } yield return null; } }

In this way I can run a set of sequential tasks from parallel tasks and viceversa, but as you probably got the code is not limited just to these two cases, it actually can handle all the possible combinations deriving from the use of IEnumerable functions or objects.

I wish to thank my friend [Amedeo Margarese](http://www.linkedin.com/pub/amedeo-margarese/6/498/58?_mSplash=1) who gave me the idea to write this code and [Francesco Carucci](http://www.linkedin.com/in/fcarucci?_mSplash=1) who helped to write the unit tests for [NunitLite](https://github.com/zoon/NUnitLiteUnityRunner)

Please, I wish to see more examples. 😛

I’m trying to figure out how to use this… And I’m stuck in 2 points.

First, very basic, how should I implement the actual task?

Second, how can I serialize it within the task?

Thanks in advance, and great job!

Thanks for the comment. You can use the task sequencer in 3 different ways. You are not forced to create tasks, you can also use IEnumerable classes or IEnumerable functions.

I will try to add more examples as soon as I can!

Yes, that I can see in the current examples… But then, how would I implement the `IEnumerable`? 😀

I’ll eventually figure it out and I’m actually having some progress with good old trial and error, but since you asked about needing more examples I thought those would be nice additions.

Also, we can use it just like IEnumerators, can’t we? Make RunSerialTasksExecutedInParallel a IEnumerator (rather than void) and insert a `while (! parallelTasks1.isDone) yield return null;` in the end. Is there any problems in doing this?

Hello,

I was about to write more examples, but then I realized that inside the TaskRunnerTests.cs you can already find a lot of examples, although they are not real user case scenarios. I just added a new test to run IEnumerable functions.

If you are interested, eDriven has the TaskQueue class for synchronizing subsequent tasks (i.e. waiting for each task to end before handling the consequent one): https://github.com/dkozar/eDriven/blob/master/eDriven.Core/Tasks/TaskQueue.cs (and does it single threaded)

(seems we share the interest in this area :))

Hello, one question!

Are those parallel Tasks multi-threaded? Thanks for this script, I hope it will be usefull 🙂

I need to process multiple meshes at startup and I really want to use multi-threading for this.

hello, I will update this library soon with some initial multithread support. However it makes sense to use it only because Unity doesn’t support the Task class yet.

courutines neither parallel nor async. They are synchronous, but concurrent. Learn the difference.

Hello Sebastiano ! Your Asyncronius Tasks is very good and helpfull ! SerialTaskCollection codestyle allow keep all sequence in one function. That make async logic clear. But some times we need to pass result from one async function to next, without using this result elsewhere. So I write args helper .. ( may be not elegant but do job ). Take a look. May be it will be usefull for You and Your library. http://www.codeshare.io/jufP5 Usage : public void Run() { mutual = new MutableArgs(); SerialTaskCollection st = new SerialTaskCollection(); st.Add(Print(1, mutual.Out)); st.Add(AsyncWaitAndCreateURL(mutual.In, mutual.Out)); st.Add(WWWTest(mutual.In)); StartCoroutine(st.GetEnumerator()); } IEnumerator Print(int i,… Read more »

Hi Michael, I do the same, but I don’t think you need to use Func (unless I misunderstood what you want to solve), I solved the same problem using simple references. Assuming we are talking about a single thread scenario, we can safely pass references as parameters of IEnumerator functions and they will work as well. I also implemented the “token” parameter to solve the same problem when ITask are used instead. I once wrote an elegant solution for a quite complicated scenario. I needed the serial tasks to branch according a parameter. It worked more or less like this:… Read more »