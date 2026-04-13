---
title: Rust Game - Part 3 - Unlock the Message Loop
url: https://www.jendrikillner.com/post/rust-game-part-3/
author: Jendrik Illner
published: '2019-11-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

With the implementation from the previous post, the game loop stops updating when dragging the window.

This happens because the windows message loop is continuously receiving new messages. This causes `process_window_messages`

to enter an endless loop until the user stops dragging the window.

I personally like to keep my game updating at all times; therefore, I move my windows message loop processing into a background thread.

The following two steps are required to make sure that game loop updates at all times:

- Create a window in a thread and run the message pump in the window thread
- Setup thread-safe communication between game thread and message loop thread

### Creating window in a thread

Creating the window in a thread requires very few changes to the code shown in the previous post.

Moving the code from `create_window`

into a `std::thread::spawn`

closure

```
std::thread::spawn(move || {
let mut window_class_name: Vec<u16> =
OsStr::new("Match3WindowClass").encode_wide().collect();
window_class_name.push(0);
let window_class = WNDCLASSW {
style: 0,
lpfnWndProc: Some(window_proc),
........
let h_wnd_window = CreateWindowExW(
........
```


This will make sure the window is created in a new thread.

The message loop needs to run in the same thread as the window was created. Therefore the ‘process_window_messages’ logic needs to be moved into the thread closure as well.

```
ShowWindow(h_wnd_window, SW_SHOW);
while !IS_WINDOW_CLOSED {
if PeekMessageA(&mut msg, h_wnd_window, 0, 0, PM_REMOVE) > 0 {
TranslateMessage(&msg);
DispatchMessageA(&msg);
}
}
```


With this in place, the new thread will be receiving and processing all messages that are sent to the window.

When specific messages (window closed, key pressed, …), are received, they need to be sent to the game so it can react to it.

### Setup thread-safe communication between game and message loop thread

One common communication primitive between threads provided by Rust is `std::sync::mpsc::channel`

This is a “multi-producer, single-consumer FIFO queue.”

My communication strategy is:

- The window is the producer of messages, the game is the receiver
- All messages will be expressed as
`enum WindowMessages`

to be sent between threads

If I remember it correctly, some transitions, such as fullscreen, also require the game thread to be able to send messages to the window thread, but I will implement that if necessary in the future.

For now, I am going to define two messages.

- WindowCreated
- WindowClosed

```
enum WindowMessages {
WindowCreated,
WindowClosed,
}
```


A channel needs to be created so that communication between the two threads is possible.

The channel is created on the main thread, and the `move`

at the closure level means that ownership for variables accessed from the thread will be moved onto the spawned thread.

```
fn create_window() -> Result<Window, ()> {
let (channel_sender, channel_receiver) = std::sync::mpsc::channel();
std::thread::spawn(move || {
----
```


After the window has been created and show the ‘WindowCreated’ message will be sent from the window thread.

```
ShowWindow(h_wnd_window, SW_SHOW);
channel_sender.send(WindowMessages::WindowCreated)
```


Because `channel_sender`

is used inside of the closure, ownership will be moved to the window thread.
`channel_receiver`

is not used, and therefore ownership stays with the game thread.

Before `create_window`

returns, the window creation on the separate thread has to be completed, therefor we wait until the window creation on the separate thread has been completed.

This is done as below, `channel_receiver.recv()`

will block until a message has been received.

```
fn create_window() -> Result<Window, ()> {
let (channel_sender, channel_receiver) = std::sync::mpsc::channel();
std::thread::spawn(move || { ...... } );
// wait for window created before returning
if let WindowMessages::WindowCreated = channel_receiver.recv().unwrap() {
return Ok(Window {
message_receiver: channel_receiver,
});
}
Err(())
}
```


`process_window_messages`

needs to be adjusted so that it checks for the arrival of new messages from the window channel.

```
fn process_window_messages(window: &Window) -> Option<WindowMessages> {
if let Ok(x) = window.message_receiver.try_recv() {
return Some(x);
}
None
}
```


`try_recv`

will not block and returns an Optional

The one message to be handled for now is WindowClosed. For this, to work, the message pump on the window thread needs to send a WindowClosed event when a WM_DESTROY message has been received.

```
while !IS_WINDOW_CLOSED {
if PeekMessageA(&mut msg, h_wnd_window, 0, 0, PM_REMOVE) > 0 {
TranslateMessage(&msg);
DispatchMessageA(&msg);
if IS_WINDOW_CLOSED {
channel_sender.send(WindowMessages::WindowClosed).unwrap();
}
}
```


With all this in place, we can now drag the window, and the game loop continues to update. When the user closes the window, the game loop will close as expected.

One thing that is still problematic is the global state (`IS_WINDOW_CLOSED`

) that is used for communication between the window_proc and the message loop on the message loop thread.

Next, I will try to solve this and see if it’s possible to attach Rust objects to native objects.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-3)