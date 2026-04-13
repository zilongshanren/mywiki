---
title: Rust Game Series - Part 4 - removing global state
url: https://www.jendrikillner.com/post/rust-game-part-4/
author: Jendrik Illner
published: '2019-11-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

The current state of the message loop is below, and the problem left to solve is the global state.

```
static mut IS_WINDOW_CLOSED: bool = false;
unsafe extern "system" fn window_proc(
h_wnd: HWND,
msg: UINT,
w_param: WPARAM,
l_param: LPARAM,
) -> LRESULT {
if msg == WM_DESTROY {
IS_WINDOW_CLOSED = true;
PostQuitMessage(0);
}
DefWindowProcW(h_wnd, msg, w_param, l_param)
}
```


`IS_WINDOW_CLOSED`

is required to communicate between the window proc and the main game loop.
Ideally, I would like to pass an object to the message handler and only rely on that state.

Luckily Windows provides a method for this. This can be achieved in 3 steps:

- pass a custom struct into CreateWindowExW
- when WM_CREATE is received, store this custom struct into the window user data
- obtain the custom user data in the window handler

The following struct will be used:

```
struct WindowThreadState {
message_sender: std::sync::mpsc::Sender<WindowMessages>,
is_window_closed : bool
}
```


This struct can be created as usual and passed into CreateWindowExW as the last parameter.

```
let mut window_state = WindowThreadState {
message_sender : channel_sender,
is_window_closed : true
};
let h_wnd_window = CreateWindowExW(
...
& mut window_state as * mut WindowThreadState as * mut winapi::ctypes::c_void,
);
```


Pretty simple besides the cast, let me break that one down

```
// taking a mutable reference
let mut_ref: &mut WindowThreadState = &mut window_state;
// next we need to convert the reference to a pointer
let raw_ptr: *mut WindowThreadState = mut_ref as *mut WindowThreadState;
// and the pointer type we can cast to the c_void type required by CreateWindowEx
let void_ptr: *mut winapi::ctypes::c_void = raw_ptr as *mut winapi::ctypes::c_void;
// all steps expressed in a single line
&mut window_state as *mut WindowThreadState as *mut winapi::ctypes::c_void
```


With the state passed into CreateWindowEx, it’s time to update the message handler and remove the use of the global state.

```
unsafe extern "system" fn window_proc(
h_wnd: HWND,
msg: UINT,
w_param: WPARAM,
l_param: LPARAM,
) -> LRESULT {
if msg == WM_CREATE {
// retrieve the message struct that contains the creation parameters
let create_struct = l_param as * mut winapi::um::winuser::CREATESTRUCTW;
// retrieve the rust window state
let window_state_ptr = create_struct.as_ref().unwrap().lpCreateParams as * mut WindowThreadState;
let window_state : & mut WindowThreadState = window_state_ptr.as_mut().unwrap();
// the pointer we can store inside of the USERDATA of the window being created
SetWindowLongPtrW(h_wnd, GWLP_USERDATA, window_state_ptr as isize );
// sent a message that the window has been created
window_state.message_sender.send(WindowMessages::WindowCreated).unwrap();
}
if msg == WM_DESTROY {
// request the state from the window USERDATA
let window_state_ptr = GetWindowLongPtrW(h_wnd, GWLP_USERDATA) as * mut WindowThreadState;
let window_state : & mut WindowThreadState = window_state_ptr.as_mut().unwrap();
// send a message that the window has been closed
window_state.message_sender.send(WindowMessages::WindowClosed).unwrap();
window_state.is_window_closed = true;
PostQuitMessage(0);
}
DefWindowProcW(h_wnd, msg, w_param, l_param)
}
```


After adjusting the message-loop, a Clippy warning needs to be disabled too.

```
#[allow(clippy::while_immutable_condition)]
while !window_state.is_window_closed {
if PeekMessageA(&mut msg, h_wnd_window, 0, 0, PM_REMOVE) > 0 {
TranslateMessage(&msg);
DispatchMessageA(&msg);
}
}
```


This needs to be done because the Rust compiler can’t see that `is_window_closed`

will ever be changed. This variable is only changed in the window message proc, and Rust is unaware that this function is ever called during TranslateMessage by the windows runtime.

Therefore we need to disable the Clippy warning for this location only.

## Update

Turns out, there is a better way to exit the message loop.
Thanks to [Michal Ziulek](https://twitter.com/MichalZiulek/) for pointing this out.

PostQuitMessage(0) pushes WM_QUIT message to the queue so you can break the main loop like this:

— Michal Ziulek (@MichalZiulek)

{

TranslateMessage(&msg);

DispatchMessageA(&msg);

if (msg.message == WM_QUIT) break;

}[November 30, 2019]

The updated code looks like this:

```
loop {
if PeekMessageA(&mut msg, h_wnd_window, 0, 0, PM_REMOVE) > 0 {
TranslateMessage(&msg);
DispatchMessageA(&msg);
// once the window has been closed we can exit the message loop
if msg.message == WM_QUIT {
break;
}
}
}
```


This is a lot better, I can remove `is_window_closed`

, and no Clippy warning need to be disabled.

With the foundation created I will focus on creating a D3D11 device next week.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-4)