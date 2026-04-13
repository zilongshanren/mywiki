---
title: Rust Game - Part 2 - Win32 Window
url: https://www.jendrikillner.com/post/rust-game-part-2/
author: Jendrik Illner
published: '2019-11-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Creating a window from Rust requires interfacing with the Win32 API.

I started out using the Foreign Function Interface(FFI) to call the Win32 APIs directly. Even though I got it working it takes a tremendous amount of effort;

Thankfully, there is the [winapi](https://crates.io/crates/winapi) crate.
Happy to support Peter Atashian on [patreon](https://www.patreon.com/retep998/overview) for maintaining this project.

To start using it, add the necessary dependency into Cargo.toml.

```
[dependencies]
winapi = { version = "0.3", features = ["winuser"] }
```


The features list defines what win32 APIs are required and should be imported.

To detect which features are required to be compiled, search the [documentation](https://docs.rs/winapi/latest/winapi/) for the function you want to call. It will show which module it is defined in.

For example, in this case, winuser needs to be imported.

```
winapi::um::winuser::CreateWindowExW
------
```


Creating a Win32 window is broken down into 3 steps:

- register a window class
- create a window
- start processing the message loop

Let’s look at each step:

## register a window class

```
unsafe {
let mut window_class_name: Vec<u16> =
OsStr::new("Match3WindowClass").encode_wide().collect();
// encode_wide does NOT add a null terminator
window_class_name.push(0);
let window_class = WNDCLASSW {
style: 0,
lpfnWndProc: Some(window_proc),
cbClsExtra: 0,
cbWndExtra: 0,
hInstance: 0 as HINSTANCE,
hIcon: 0 as HICON,
hCursor: 0 as HICON,
hbrBackground: 16 as HBRUSH,
lpszMenuName: 0 as LPCWSTR,
lpszClassName: window_class_name.as_ptr(),
};
let error_code = RegisterClassW(&window_class);
assert!(error_code != 0, "failed to register the window class");
```


### OS String handling

I am using the wide version of the Win32 API. Therefore I need to convert from the Rust OsStr into a wide-character array.

`encode_wide()`

provides the conversion into UTF16 characters. The conversion is implemented lazily as an iterator and `collect()`

collects all the u16 values into a `Vec`

.

It’s important to remember that `encode_wide()`

does not add null termination, and explicit zero termination is required.

### window proc handler

You might have noticed `Some(window_proc)`

in the previous class registration.
This defines the function that will be called by Win32 to process the window messages.

The function needs a bit of extra information to be passed across the Rust <-> Win32 boundary.

```
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


`unsafe extern "system"`

marks the function as unsafe and to use the system [ABI](https://doc.rust-lang.org/reference/items/external-blocks.html#abi). This is the cross-platform string that maps to stdcall on Windows.

## Create window

```
let h_wnd_window = CreateWindowExW(
0,
window_class_name.as_ptr(),
0 as LPCWSTR,
WS_OVERLAPPED | WS_MINIMIZEBOX | WS_SYSMENU,
0,
0,
400,
400,
0 as HWND,
0 as HMENU,
0 as HINSTANCE,
std::ptr::null_mut(),
);
assert!(h_wnd_window != (0 as HWND), "failed to open the window");
ShowWindow(h_wnd_window, SW_SHOW);
```


Creating the window is pretty straightforward. Passing in the required settings and the name of the class we registered previously.

## Message loop

```
let mut msg: MSG = std::mem::zeroed();
// process messages
while !IS_WINDOW_CLOSED {
if PeekMessageA(&mut msg, h_wnd_window, 0, 0, PM_REMOVE) > 0 {
TranslateMessage(&msg);
DispatchMessageA(&msg);
}
}
```


Running the message loop is very close to the native Win32 version.
`std::mem::zeroed`

makes sure that MSG is set to an all-zero byte-pattern.

Every message will now call the `window_proc`

function that was registered with the window class.

Running the application will now show a default Win32 window.

![Empty Win32 Window Empty Win32 Window](../../assets/14aaf096f698f6c2.png)


When running the application and starting to drag the window, the main game loop stops updating. Next week I am going to change that and look at threading in Rust.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-2)