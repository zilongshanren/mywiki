---
title: Asynchronous Serial Communication - Alan Zucconi
url: https://www.alanzucconi.com/2016/12/01/asynchronous-serial-communication/
author: Alan Zucconi
published: '2016-12-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In a previous post, [How To Integrate Arduino With Unity](https://www.alanzucconi.com/?p=2979), we have shown how data can be sent and received through the **serial port**. The main problem encountered was dealing with the latency and the delays that communicating across different devices introduces. The solution proposed in that tutorial used a **coroutine**; decoupling the device communication from the game logic attenuates the problem, but it doesn’t remove it. The main problem is that, despite the name, Unity coroutines are not *really* executed in parallel with the rest of the game. Unity, by design, is not **thread safe**. This means that true parallelism is intentionally avoided by the engine, as it could result in race conditions. To solve the problem of the communication between Unity and Arduino, once and for all, we need actual threads.

- Step 1.
[Creating the Thread](https://www.alanzucconi.com#step1) - Step 2.
[Callbacks and Queues](https://www.alanzucconi.com#step2) - Step 3.
[Queue Communication](https://www.alanzucconi.com#step3) - Step 4.
[Thread Loop](https://www.alanzucconi.com#step4) - Step 5.
[Improvements](https://www.alanzucconi.com#step5) [Conclusion & Download](https://www.alanzucconi.com#conclusion)

At the end of this tutorial, you can find a link to download the Unity package.

#### Step 1. Creating the Thread

C# supports threads with its `System.Threading`

library. When a new thread is created, a function has to be provided. In the following example, that function is called `ThreadLoop`

.

using UnityEngine; using System.Threading; public class ArduinoThread : MonoBheaviour { private Thread thread; public void StartThread () { // Creates and starts the thread thread = new Thread (ThreadLoop); thread.Start(); } public void ThreadLoop () { // The code of the thread goes here... } }

#### Step 2. Callbacks and Queues

When code is executed in parallel, the traditional pattern of request and response typical of most imperative languages breaks. We cannot expect a function that, once invoked, returns when some data from Arduino is available. A very common approach relies on **callbacks**. With callbacks, the logic flow of the game is as follow:

- A
`MonoBehavior`

sends a request to the thread; - The thread executes the request in the background;
- When ready, the thread invoked a callback function that the
`MonoBehavior`

has provided.

This was exactly the approach used in [How To Integrate Arduino With Unity](https://www.alanzucconi.com/?p=2979), implemented in the coroutine `AsynchronousReadFromArduino`

.

That approach, unfortunately, won’t work with threads. The thread that communicates with Arduino can complete its request at any moment in time. As a result, its callback could potentially be executed in an environment that is not thread safe. To make it simple: Unity objects cannot be touched or manipulated in a thread.

The solution revolves around the concept of **synchronised queues**. When a `MonoBehavior`

script wants to send a request to Arduino, it places it in a *input queue*. The thread reads it, executes it and when its done it places it into an *output queue*. The thread never accesses any Unity objects. Those two queues are used to safely send and receive messages across threads.

C# has an effective implementation of synchronised queues that are safe to use between different threads:

private Queue outputQueue; // From Unity to Arduino private Queue inputQueue; // From Arduino to Unity public void StartThread () { outputQueue = Queue.Synchronized( new Queue() ); inputQueue = Queue.Synchronized( new Queue() ); thread = new Thread (ThreadLoop); thread.Start(); }

Please note that the class `Queue`

, by itself, is not guaranteed to be thread safe. The `Queue.Synchronzed`

wrapper makes an existing queue thread safe ([MSDN](https://msdn.microsoft.com/en-us/library/system.collections.queue.synchronized(v=vs.110).aspx)).

### ⭐ Recommended Unity Assets

### Part 3. Queue Communication

Now that we have two queues, we need some code that allows an external `MonoBehavior`

script to send and receive data. Using the queue in this setup is relatively straightforward:

public void SendToArduino (string command) { outputQueue.Enqueue(command); } public string ReadFromArduino () { if (inputQueue.Count == 0) return null; return (string) inputQueue.Dequeue(); }

Please, note that now that we are using queues, it is your script’s responsibility to periodically query the queue for incoming messages.

#### Part 4. Thread Loop

The final part of code necessary is the actual body of the thread. It consists of two parts; a setup, and a loop. The setup opens the serial connection with Arduino. The loop keeps it open, sending and receiving messages through the synchronised queues:

public void ThreadLoop () { // Opens the connection on the serial port stream = new SerialPort(port, baudRate) stream.ReadTimeout = 50; stream.Open(); // Looping while (true) { // Send to Arduino if (outputQueue.Count != 0) { string command = outputQueue.Dequeue(); WriteToArduino(command); } // Read from Arduino string result = ReadFromArduino(timeout); if (result != null) inputQueue.Enqueue(result); } }

Note that the functions `WriteToArduino`

and `ReadFromArduino`

are taken from the first part of this tutorial, [How To Integrate Arduino With Unity](https://www.alanzucconi.com/?p=2979).

#### Part 5. Improvements

The code shown so far is not very reliable, as it doesn’t take into account possible errors and exceptions. A better implementation should always make sure that all the possible exceptions are captures and properly handled.

Another aspect that has not been considered is the closure of the serial port. There are several approaches that can be done, but they all need a way for a Unity script to alter the state of a thread. For instance, by adding a boolean variable called `looping`

that can be used a guard for the thread loop.

To be pedantic, a script should never directly change the variable used by a thread. Given how simple this script is, it’s safe to assume that there are virtually no side effects. If you want to play safe with thread, each access to a shared variable between different threads should be mediated through a **lock**, like this:

public bool looping = true; public void StopThread () { lock (this) { looping = false; } }

The keyword `lock`

ensures that no two threads can edit the object at the same time. This is who thread safe code is developed in C#. But it can also be the start of an endless stream of drama called **deadlocks**.

To ensure thread safety, every potentially concurrent access to the variable `looping`

must be enclosed in a lock block. This also includes the access that is done in the guard of the while loop in the `ThreadLoop`

function:

public void IsLooping () { lock (this) { return looping; } } public void ThreadLoop () { ... // Looping while ( IsLooping() ) { ... } // Close the stream stream.Close(); }

The method `StopThread`

can now be invoked safely from any Unity script.

### 🪛 Recommended Components

#### Conclusion & Download

This post extends the original tutorial on Arduino and Unity. It shows how a thread can be used to avoid delays when waiting for data on the serial port. This post was inspired by Daniel Wilches’ asset [SerialCommUnity](https://github.com/DWilches/SerialCommUnity).

- Part 1.
[How To Integrate Arduino With Unity](https://www.alanzucconi.com/?p=2979) - Part 2.
**Asynchronous Serial Communication In Unity**

You can download the Unity package for this tutorial on [Patreon](https://www.patreon.com/posts/35519472). The package allows connecting Unity and Arduino for efficient and effective two-way communication using threads. It also contains several examples to test your setup.

## Leave a Reply Cancel reply