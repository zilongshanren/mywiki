---
title: Rust Game Series - Part 5 - D3D11 Device and Swap Chain creation
url: https://www.jendrikillner.com/post/rust-game-part-5/
author: Jendrik Illner
published: '2019-12-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

With the window creation in place, we have the necessary foundation to create a D3D11 device and a Swap Chain.

To start using it, add the necessary dependencies into Cargo.toml.

```
[dependencies]
winapi = { version = "0.3", features = ["winuser", "d3d11", "winerror", "dxgi1_2"] }
```


Creating the swap chain is done in the following steps

- Create a D3D11 device
- Get access to the DXGI interface
- Create the swap chain

Let’s look at each step:

## Create a D3D11 device

```
unsafe {
// use default adapter
let adapter: *mut IDXGIAdapter = std::ptr::null_mut();
let flags: UINT = 0;
let feature_levels: D3D_FEATURE_LEVEL = D3D_FEATURE_LEVEL_11_0;
let num_feature_levels: UINT = 1;
let mut d3d11_device: *mut ID3D11Device = std::ptr::null_mut();
let mut d3d11_immediate_context: *mut ID3D11DeviceContext = std::ptr::null_mut();
let result: HRESULT = D3D11CreateDevice(
adapter,
D3D_DRIVER_TYPE_HARDWARE,
std::ptr::null_mut(),
flags,
&feature_levels,
num_feature_levels,
D3D11_SDK_VERSION,
&mut d3d11_device,
std::ptr::null_mut(),
&mut d3d11_immediate_context,
);
assert!(result != winapi::shared::winerror::S_OK, "d3d11 device creation failed");
}
```


This is really close to what you would write in C++ too. Two things stand out:

```
let adapter: *mut IDXGIAdapter = std::ptr::null_mut();
```


Pointers need to be defined as mutable and therefore need to be initialized with a mutable null pointer.

`D3D11CreateDevice`

returns the outputs as an output parameter.

Therefore we need to provide a pointer to the location where the pointer to the created d3d11_device should be stored.

In Rust, we can pass in a mutable reference to the `*mut ID3D11Device`

, and it will do the implicit conversion to a pointer type.

### Get access to the DXGI interface

Next, we need to get the underlying DXGI interface that was used internally when the d3d11 device was created.

```
let mut dxgi_device: *mut IDXGIDevice = std::ptr::null_mut();
// get dxgi device
let result = d3d11_device.as_ref().unwrap().QueryInterface(
&IDXGIDevice::uuidof(),
&mut dxgi_device as *mut *mut IDXGIDevice as *mut *mut winapi::ctypes::c_void,
);
```


Relatively little code, but what is that cast?!?

Looking at the [QueryInterface](https://retep998.github.io/doc/winapi/unknwnbase/struct.IUnknown.html) documentation, the parameter is defined as `*mut *mut c_void`

and our object is of type `*mut IDXGIDevice`


Let me break down the cast into its steps:

```
// taking a mutable reference to dxgi device
let mut_ref: &mut *mut IDXGIDevice = &mut dxgi_device;
// next we need to convert the reference to a pointer
let raw_ptr: *mut *mut IDXGIDevice = mut_ref as *mut *mut IDXGIDevice;
// and the pointer type we can cast to the c_void type required by QueryInterface
let void_cast: *mut *mut winapi::ctypes::c_void = raw_ptr as *mut *mut winapi::ctypes::c_void;
// all steps expressed in a single line :)
&mut dxgi_device as *mut *mut IDXGIDevice as *mut *mut winapi::ctypes::c_void
```


Afterward, we apply the same idea a few more times until we have access to the `IDXGIFactory2`

interface that is required to create the swap chain.

```
let mut dxgi_adapter: *mut IDXGIAdapter = std::ptr::null_mut();
let result = dxgi_device.as_ref().unwrap().GetAdapter(&mut dxgi_adapter);
let mut dxgi_factory: *mut IDXGIFactory1 = std::ptr::null_mut();
let result = dxgi_adapter
.as_ref()
.unwrap()
.GetParent(&IDXGIFactory1::uuidof(), &mut dxgi_factory as * mut *mut IDXGIFactory1 as * mut * mut winapi::ctypes::c_void );
let mut dxgi_factory_2: *mut IDXGIFactory2 = std::ptr::null_mut();
let result = dxgi_factory
.as_ref()
.unwrap()
.QueryInterface(&IDXGIFactory2::uuidof(), &mut dxgi_factory_2 as * mut * mut IDXGIFactory2 as * mut *mut winapi::ctypes::c_void );
```


With all those interfaces we can finally create the swap chain

```
let sd = DXGI_SWAP_CHAIN_DESC1 {
Width: 0,
Height: 0,
Format: DXGI_FORMAT_R8G8B8A8_UNORM,
SampleDesc: DXGI_SAMPLE_DESC {
Count: 1,
Quality: 0,
},
BufferUsage: DXGI_USAGE_RENDER_TARGET_OUTPUT,
BufferCount: 2,
AlphaMode: DXGI_ALPHA_MODE_UNSPECIFIED,
Flags: 0,
Scaling: DXGI_SCALING_STRETCH,
SwapEffect: DXGI_SWAP_EFFECT_DISCARD,
Stereo: 0,
};
let mut swapchain: *mut IDXGISwapChain1 = std::ptr::null_mut();
let result = dxgi_factory_2.as_ref().unwrap().CreateSwapChainForHwnd(
d3d11_device as *mut winapi::um::unknwnbase::IUnknown,
hwnd,
&sd,
std::ptr::null_mut(),
std::ptr::null_mut(),
&mut swapchain,
);
```


We are currently missing one piece of fundamental data to be able to create the swap chain, and that’s the HWND from the window we want to create the swap chain for.

We need to make some modifications to get access to this. Firstly the WindowMessages enum needs to be updated. When the window is created, we need to pass the HWND along.

```
struct WindowCreatedData {
hwnd: HWND,
}
enum WindowMessages {
WindowCreated(WindowCreatedData),
WindowClosed,
}
```


Then we adjust the sender location to pass the HWND into the WindowCreated message.

```
window_state
.message_sender
.send(WindowMessages::WindowCreated(WindowCreatedData {
hwnd: h_wnd,
}))
.unwrap();
```


When trying to build the code, a new error is encountered now:

```
std::thread::spawn(move || {
^^^^^^^^^^^^^^^^^^ `*mut winapi::shared::windef::HWND__` cannot be sent between threads safely
```


The Rust compiler can determine if Rust types can be transferred across thread boundaries safely.
When it determines that it’s safe, the `std::marker::Send`

trait will automatically be implemented by the compiler.

Because of the way HWND is expressed as pointer type in Winapi, the compiler regards the type as unsafe. But HWND is not really a pointer, but a pointer sized handle. Therefore it’s still ok to pass it between threads, and the trait can be implemented manually.

```
unsafe impl std::marker::Send for WindowCreatedData {}
```


Implementing the trait, we promise to the Rust compiler that passing WindowCreatedData between threads is safe.

With this, we can send the window handle between threads and create the swap chain.
Once the swap chain is created, `Present`

can be called from our rendering loop, and we will see the window is cleared to black.

```
swapchain.as_ref().unwrap().Present(1, 0);
```


![Empty Win32 Window Empty Win32 Window](../../assets/32a683003843e48c.png)


With the successfully created swap chain, we can start looking into actually rendering something next week.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-5)