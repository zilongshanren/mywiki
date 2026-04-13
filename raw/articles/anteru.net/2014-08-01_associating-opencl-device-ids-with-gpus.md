---
title: Associating OpenCL device ids with GPUs
url: https://anteru.net/blog/2014/associating-opencl-device-ids-with-gpus
published: '2014-08-01'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

What’s more fun than one GPU? Two of them, of course. However, if you are using OpenCL from multiple processes, things get a bit hairy once you have multiple GPUs in a machine. A typical example would be [MPI](http://en.wikipedia.org/wiki/Message_Passing_Interface): With MPI, you’ll want to spawn one process per GPU. The problem you’re going to run into is how to assign GPUs, or rather, OpenCL devices, to processes.

The issue is that if you have two identical GPUs, you can’t distinguish between them. If you call `clGetDeviceIds`

, the order in which they are returned is actually unspecified, so if the first process picks the first device and the second takes the second device, they both may wind up oversubscribing the same GPU and leaving the other one idle.

What we need is to get a persistent, unique identifier for each device which remains stable between processes, so we can match an OpenCL device id to a physical GPU. There’s no such thing in standard OpenCL, but luckily for us, there are some severely under-documented, vendor specific extensions which can help us.

## AMD

**Updated 2021-02-11**: Replaced `cl_amd_device_topology`

by `cl_amd_device_attribute_query`

, added OpenCL SDK link.

On AMD, you want to use the [ cl_amd_device_attribute_query](https://www.khronos.org/registry/OpenCL/extensions/amd/cl_amd_device_attribute_query.txt) extension. This extension works on both Linux and Windows and can be used to query the PCIe bus, which is unique for each GPU. Let’s take a look how this works:

```
// This cl_ext is provided as part of the AMD OpenCL SDK. See below for how
// to get hold of this
#include <CL/cl_ext.h>
cl_device_topology_amd topology;
status = clGetDeviceInfo (devices[i], CL_DEVICE_TOPOLOGY_AMD,
sizeof(cl_device_topology_amd), &topology, NULL);
if(status != CL_SUCCESS) {
// Handle error
}
if (topology.raw.type == CL_DEVICE_TOPOLOGY_TYPE_PCIE_AMD) {
std::cout << "INFO: Topology: " << "PCI[ B#" << (int)topology.pcie.bus
<< ", D#" << (int)topology.pcie.device << ", F#"
<< (int)topology.pcie.function << " ]" << std::endl;
}
```


This will give you a unique id for each GPU in your machine. You can also find this information in the AMD APP OpenCL programming guide, in the appendix. You can find the extension header in the [AMD OpenCL SDK light package](https://github.com/GPUOpen-LibrariesAndSDKs/OCL-SDK).

## NVIDIA

For NVIDIA, the approach is very similar. The `cl_nv_device_attribute_query`

extension supports two undocumented tokens for `clGetDeviceInfo`

, `CL_DEVICE_PCI_BUS_ID_NV`

(`0x4008`

) and `CL_DEVICE_PCI_SLOT_ID_NV`

(`0x4009`

), which return the same information. Testing indicates that the return value is an integer. Unfortunately, I couldn’t find any documentation about this, but trust me, this works :)

## Combined approach

The combined approach is to query the device vendor first, and then try to obtain the information. I combine it into an opaque 64-bit number which I associate with a device (on AMD, I merge the device and bus, on NVIDIA, the slot and bus.) I’m curious to hear how this is supposed to work for multiple Intel Xeon Phi, if you know, please drop me a line or comment!

## Acknowledgements

Thanks to Herve & Marcus for their help! Undocumented functions are sure fun ;)