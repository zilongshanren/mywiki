---
title: 云风的 BLOG
url: https://blog.codingnow.com/2017/09/
published: '2017-09-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### Direct3D12 的接口设计 bug

昨天被 D3D12 的一个 bug 坑了一晚上，这个问题很值得一写。

最初是发现 [LUID ID3D12Device::GetAdapterLuid()](https://msdn.microsoft.com/en-us/library/windows/desktop/dn914411(v=vs.85).aspx) 这个函数有问题。我用 mingw64 gcc 编译后的程序，只要调用了一个 api ，d3d12device 设备对象的虚函数表就被破坏掉了。下一次对这个设备的任何 api 调用都会 crash 掉。

由于这个函数的实现在 d3d12.dll 中，是没有源码的，所以只能用 gdb 调试了一下。发现了一个问题：这个 api 的返回值是 LUID ，它是一个结构体。C/C++ 函数返回结构体是没有统一的调用规范的，按道理 COM 的实现应该避免设计这种 API 。

**按 COM 的规定，所有 API 必须返回 HRESULT** ，只有少量例外可以返回 ULONG 整数。其实之前的 D3D 版本在设计类似 API 的时候都符合了这个约定，例如 D3D9 就有一个类似的 API ：

我猜想，微软的新同学在重新设计 D3D12 的时候已经忘记了 COM 规范，也不清楚这个世界上还有 VC 以外的 C++ 编译器的存在。实现 D3D12.DLL 的时候，按 VC 的调用规范，当 API 返回一个结构体的时候，是把调用方在栈上预留出的返回结构的地址作为一个参数传入的。

所以，这个 API 其实本质上是这样的：

void ID3D12Device::GetAdapterLuid(LUID *)

而 gcc 呢，它会根据结构体的实际大小来优化调用。如果结构体小于等于 64bit ，就通过寄存器返回结果，而不会传入堆栈地址。在 gcc 上，这个 API 就只有一个参数，就是 this 指针了。按 64 位系统的函数调用规范，第一个和第二个参数分别通过 rcx 和 rdx 传递。用 gcc 生成的调用代码，调用方认为没有第二个参数，rdx 是无意义的。这里恰巧 rdx 也保存了 this 。而被调用方，也就是 d3d12.dll 的实现，认为第二个参数是有意义的，是返回结构的地址，结果就把返回数据写入了 *this 中，这里恰好是这个对象的虚表之所在，程序就这么挂了。

那么是否可以指定 gcc 不要对小结构体返回优化呢？

gcc 提供了参数 [-fpcc-struct-return](https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html) 。不过，即使设置了这个参数，gcc 的 ABI 依旧和 vc 的不一致。因为对于 gcc 来说，返回值的地址是第一个参数，而 vc 似乎放在了第二个，它把第一个参数留给了 this 。

在微软更新 sdk 前，怎么绕过这个问题呢？我写了一个辅助函数：

static inline LUID D3D12DeviceGetAdapterLuid(ID3D12Device *device) { typedef void (STDMETHODCALLTYPE ID3D12Device::*GetAdapterLuid_f)(LUID *); LUID ret; (device->*(GetAdapterLuid_f)(&ID3D12Device::GetAdapterLuid))(&ret); return ret; }

同样存在问题的 API 还有 ID3D12DescriptorHeap 等，我还没有一一核查。

更糟糕的问题存在于 ID3D12Resource::GetDesc 这个 API ，它也返回了一个结构体 `D3D12_RESOURCE_DESC`

，这个 API 居然在 d3dsdk 的 d3dx12.h 中的 inline 函数 UpdateSubresources 里被调用了。

也就是说，如果你不修改 d3dsdk 的 .h 文件，几乎无法解决这个 bug :(

我一开始想到一个 trick ，实现一个 proxy 类，把这个 GetDesc 函数重定义一下：

static inline D3D12_RESOURCE_DESC ID3D12ResourceGetDesc(ID3D12Resource *res) { typedef void (STDMETHODCALLTYPE ID3D12Resource::*GetDesc_f)(D3D12_RESOURCE_DESC *); D3D12_RESOURCE_DESC ret; (res->*(GetDesc_f)(&ID3D12Resource::GetDesc))(&ret); return ret; } struct D3D12ResourceProxy : public ID3D12Resource { D3D12ResourceProxy(ID3D12Resource *p) : m_ptr(p) {} virtual HRESULT STDMETHODCALLTYPE Map(UINT Subresource, const D3D12_RANGE *pReadRange, void **ppData) { return m_ptr->Map(Subresource, pReadRange, ppData); } virtual void STDMETHODCALLTYPE Unmap(UINT Subresource, const D3D12_RANGE *pWrittenRange) { m_ptr->Unmap(Subresource, pWrittenRange); } virtual D3D12_RESOURCE_DESC STDMETHODCALLTYPE GetDesc(void) { // return struct 重新定义 return ID3D12ResourceGetDesc(m_ptr); } virtual D3D12_GPU_VIRTUAL_ADDRESS STDMETHODCALLTYPE GetGPUVirtualAddress( void) { return m_ptr->GetGPUVirtualAddress(); } virtual HRESULT STDMETHODCALLTYPE WriteToSubresource(UINT DstSubresource, const D3D12_BOX *pDstBox, const void *pSrcData, UINT SrcRowPitch, UINT SrcDepthPitch) { return m_ptr->WriteToSubresource(DstSubresource, pDstBox, pSrcData, SrcRowPitch, SrcDepthPitch); } virtual HRESULT STDMETHODCALLTYPE ReadFromSubresource(void *pDstData,UINT DstRowPitch,UINT DstDepthPitch, UINT SrcSubresource, const D3D12_BOX *pSrcBox) { return m_ptr->ReadFromSubresource(pDstData,DstRowPitch,DstDepthPitch,SrcSubresource,pSrcBox); } virtual HRESULT STDMETHODCALLTYPE GetHeapProperties(D3D12_HEAP_PROPERTIES *pHeapProperties,D3D12_HEAP_FLAGS *pHeapFlags) { return m_ptr->GetHeapProperties(pHeapProperties,pHeapFlags); } virtual HRESULT STDMETHODCALLTYPE GetDevice(REFIID riid, void **ppvDevice) { return m_ptr->GetDevice(riid, ppvDevice); } virtual HRESULT STDMETHODCALLTYPE GetPrivateData(REFGUID guid, UINT *pDataSize, void *pData) { return m_ptr->GetPrivateData(guid,pDataSize,pData); } virtual HRESULT STDMETHODCALLTYPE SetPrivateData(REFGUID guid, UINT DataSize, const void *pData) { return m_ptr->SetPrivateData(guid, DataSize, pData); } virtual HRESULT STDMETHODCALLTYPE SetPrivateDataInterface(REFGUID guid, const IUnknown *pData) { return m_ptr->SetPrivateDataInterface(guid, pData); } virtual HRESULT STDMETHODCALLTYPE SetName(LPCWSTR Name) { return m_ptr->SetName(Name); } virtual ULONG AddRef() { return m_ptr->AddRef(); } virtual HRESULT QueryInterface(REFIID riid, void **ppvObject) { return m_ptr->QueryInterface(riid, ppvObject); } virtual ULONG Release() { return m_ptr->Release(); } private: ID3D12Resource *m_ptr; };

然后，在调用 UpdateSubresources 的地方修改一下，先把 ID3D12Resource * 转换为 &D3D12ResourceProxy(p) 再传进去。后来发现这样不行，因为在 UpdateSubresources 内部又调用了 ID3D12GraphicsCommandList::CopyTextureRegion ，它会接收 ID3D12Resource * 。而 ID3D12GraphicsCommandList::CopyTextureRegion 已经实现在 d3d12.dll 中，这样又会回到调用协议不一致的问题。

把 sdk 实现放在公开的 .h 中真是个糟糕的设计。