---
title: Rust Game Series - Part 11 - Mouse Input
url: https://www.jendrikillner.com/post/rust-game-part-11/
author: Jendrik Illner
published: '2020-04-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

## Goal

At the end of this part, we will have the necessary support to receive mouse input in the Game.

## Overview

The task can be split into three parts:

- Receive Mouse input from Win32
- Convert mouse input into a Rust format and pass this to the Game
- React to the mouse input in the Game code

## Implementation

Processing mouse input on Windows is fundamentally quite simple. They use the same windows message loop I am already using to process window messages.

For Mouse input, I am going to handle these three events: WM_MOUSEMOVE, WM_LBUTTONDOWN, WM_LBUTTONUP

Each time the mouse will be moved over the window a WM_MOUSEMOVE is sent. We unpack the arguments and send them to the game layer for further processing.

```
if msg == WM_MOUSEMOVE {
// retrieve the window state
let window_state_ptr = GetWindowLongPtrW(h_wnd, GWLP_USERDATA) as *mut WindowThreadState;
let window_state: &mut WindowThreadState = window_state_ptr.as_mut().unwrap();
// unpack the arguments of the event
// the position is stored in l_param
let x = winapi::shared::windowsx::GET_X_LPARAM(l_param);
let y = winapi::shared::windowsx::GET_Y_LPARAM(l_param);
// and send a message to the Rust message processor
window_state
.message_sender
.send(WindowMessages::MousePositionChanged(
MousePositionChangedData { x, y },
))
.unwrap();
}
```


The functionality for WM_LBUTTONDOWN and WM_LBUTTONUP is even more straightforward as there are no arguments to unpack, and we only need to send a message.

To make this all work, we need to extend the WindowMessages enum. I really love the flexibility of Rust enums btw :)

```
pub struct MousePositionChangedData {
pub x: i32,
pub y: i32,
}
pub enum WindowMessages {
// mouse related messages
MousePositionChanged(MousePositionChangedData),
MouseLeftButtonDown,
MouseLeftButtonUp,
// window related messages
WindowCreated(WindowCreatedData),
WindowClosed,
}
```


With this functionalliy added we will be greeted with a new compiler error:

```
error[E0004]: non-exhaustive patterns: `MousePositionChanged(_)`, `MouseLeftButtonDown` and `MouseLeftButtonUp` not covered
```


All enum handling by default needs to be exhaustive. Meaning all possible cases need to be handled.

This is really useful as each time a new enum is added, the compiler will emit an error until we investigated each use case of the events.

For now, I will just print the information to the console. Responding to the input will be done in a later part.

```
match x {
WindowMessages::MousePositionChanged(pos) => {
println!("cursor position changed: x {0}, y {1}", pos.x, pos.y);
}
WindowMessages::MouseLeftButtonDown => {
println!("mouse:left down");
}
WindowMessages::MouseLeftButtonUp => {
println!("mouse:left up");
}
```


This is all we need to implement input processing. Well, there is one more small part to deal with. Testing the application like this, we will notice an issue.

Messages are only sent while the mouse is hovering over the window, and that can be a problem.

For example, if the user presses the left mouse button while insider the window, moves the mouse out of the window and releases the mouse. We will never receive a WM_LBUTTONUP event, and the Game might think the mouse button is still pressed.

To deal with this, I am extending the messages with two more cases: MouseFocusGained and MouseFocusLost When the mouse is moved outside of the window, I will send a MouseFocusLost to the Game, and the Game can react to it appropriatly.

To enable this, I will be using the win32 function [TrackMouseEvent](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-trackmouseevent)
The following code needs to be added to the WM_MOUSEMOVE event. Telling windows, we would like to receive additional mouse tracking events.

Additionally, I am also sending a MouseFocusGained to make the API symmetrical with MouseFocusLost

```
if !window_state.is_tracking {
let mut tme = TRACKMOUSEEVENT {
dwFlags: TME_LEAVE,
hwndTrack: h_wnd,
dwHoverTime: 0,
cbSize: core::mem::size_of::<TRACKMOUSEEVENT>() as u32,
};
TrackMouseEvent(&mut tme);
window_state.is_tracking = true;
window_state
.message_sender
.send(WindowMessages::MouseFocusGained)
.unwrap();
}
```


```
if msg == WM_MOUSELEAVE {
let window_state_ptr = GetWindowLongPtrW(h_wnd, GWLP_USERDATA) as *mut WindowThreadState;
let window_state: &mut WindowThreadState = window_state_ptr.as_mut().unwrap();
if window_state.is_tracking {
window_state.is_tracking = false;
window_state
.message_sender
.send(WindowMessages::MouseFocusLost)
.unwrap();
}
}
```


Of course, the two new events will need to be added to the WindowMessages enum. Rust will thankfully throw an error again, and we can update the appropriate receiver logic in the Game.

And that’s it, we receive the necessary mouse input information in the Game.

## Next Part

Next time I will connect these individual features into a first small prototype.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-10)