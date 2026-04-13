---
title: 'Getting started with OpenCL, Part #2'
url: https://anteru.net/blog/2012/getting-started-with-opencl-part-2
published: '2012-11-04'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you have followed along [the guide so far](https://anteru.net/blog/2012/11/03/2009/), you should have [a skeleton application](https://github.com/Anteru/opencltutorial/tree/6354f82a4201fa7cadf1362ff8a248a39e142a39) ready which does not yet run any OpenCL code, but prepares everything that is necessary. So let’s get a quick understanding how code is executed using OpenCL, and write our first OpenCL application. Make sure to grab [the code](https://github.com/Anteru/opencltutorial/tree/1e69b974b0fd5106a456f4a66697b37ba18e0427) before continuing to read.

Code that gets executed on a device is called a *kernel* in OpenCL. The kernels are written in a C dialect, which is mostly straightforward C with a lot of built-in functions and additional data types. For instance, 4-component vectors are a built-in type just as integers. For the first example, we’ll be implementing a simple [SAXPY](http://en.wikipedia.org/wiki/SAXPY) kernel. A quick word of warning here, before we continue: This is an example! Running SAXPY using OpenCL is most likely much slower than running it directly, not because of OpenCL, but because SAXPY is purely limited by memory bandwidth and we’ll be copying the data one additional time in this example. It may make sense if you are using data already on the device, but not if you have to copy a buffer from the CPU to the device and back.

That said, SAXPY is good to start as it is a simple and easy to understand kernel. Before we start, we have to take a quick look at how OpenCL sees the hardware. So far, we have been working on the *host* side only. In our case, the host application is written in C++ and runs on the CPU of the machine. The important part is that the host is calling the OpenCL C API functions to set up a queue and manage the data. The actual processing is done on the device. This may be also the CPU, but from the point of view of the host it doesn’t matter. In fact, the code we’re writing here will work just the same no matter if the device is a CPU or GPU.

The downside is that we must move data from the host to the device and back. This is necessary as the device can use a different memory space. GPUs for instance have on-board memory which is completely separate from the host memory. Before you ask: Yes, there are ways to optimize the copies when you are using a CPU device which is the same as the host, but for the sake of simplicity we will be copying data here.

What has to be done is thus: Allocate device memory, copy the data from the host to the device, set up a kernel, and copy the results back. Allocating memory is easily done using the buffer API:

```
cl_mem aBuffer = clCreateBuffer (context,
CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
sizeof (float) * (testDataSize),
a.data (), &error);
CheckError (error);
```


You can also specify that the memory should be copied directly while creating the buffer and that the copy should be blocking, that is, the command will only return once the operation has finished. All we need now is the kernel itself.

As mentioned before, a kernel is a piece of C code. Specifically, it’s a single function marked with the[ __kernel modifier](http://www.khronos.org/registry/cl/sdk/1.1/docs/man/xhtml/functionQualifiers.html). In our example, the kernel looks like this:

```
__kernel void SAXPY (__global float* x, __global float* y, float a)
{
const int i = get_global_id (0);
y [i] += a * x [i];
}
```


The [__global modifier](http://www.khronos.org/registry/cl/sdk/1.1/docs/man/xhtml/global.html) indicates that this is global memory, or simply memory allocated on the device. OpenCL supports different address spaces; in this sample, we’ll be using only global memory. You wonder probably where the SAXPY loop went; this is one of the key design decisions behind OpenCL, so let’s understand first how the code is executed.

Unlike C, OpenCL is designed for parallel applications. The basic assumption is that many instances of the kernel are executed in parallel, each processing a single *work item*. Multiple work items are executed together as part of a *work group*. Inside a work group, each kernel instance can communicate with other instances. This is the only execution ordering guarantee that OpenCL gives you; there is no specified order how work-items inside a group are processed. The work-group execution order is also undefined. In fact, you cannot tell if the items are executed in parallel, sequential, or in random order. This freedom and the minimal amount of data exchange and dependencies between work items makes OpenCL so fast. Work-groups allow for some order as all items in a work-group can be synchronized. This comes in handy if you want to load for instance a part of an image into cache, process it, and write it back from cache. For our example at hand however, we will ignore work-groups completely.

In order to identify the kernel instance, the runtime environment provides an id. Inside the kernel, we use `get_global_id`

which returns the id of the current work item in the first dimension. We will start as many instances as there are elements in our vector, and each work item will process exactly one entry.

Multiple kernels can be present in a single source file, called a *program*. We have to start by creating a program from the OpenCL source code, and then create the kernel from it. That sounds more complicated than it actually is:

```
CheckError (clBuildProgram (program, deviceIdCount,
deviceIds.data (), nullptr, nullptr, nullptr));
cl_kernel kernel = clCreateKernel (program, "SAXPY", &error);
CheckError (error);
```


The kernel is now ready to be used; all that is left is to bind the arguments to it. This is done using `clSetKernelArg`

. With OpenCL 1.1, it’s not possible to find out which argument has which name, so we have to set them by number:

```
clSetKernelArg (kernel, 0, sizeof (cl_mem), &aBuffer);
clSetKernelArg (kernel, 1, sizeof (cl_mem), &bBuffer);
static const float two = 2.0f;
clSetKernelArg (kernel, 2, sizeof (float), &two);
```


As mentioned above, we have to specify the size of the vector before we can run the kernel. That is, we have to tell OpenCL what dimension our work domain has and the extents in each dimension. This is done using `clEnqueueNDRangeKernel`

:

```
const size_t globalWorkSize [] = { testDataSize, 0, 0 };
CheckError (clEnqueueNDRangeKernel (queue, kernel,
1, // One dimension
nullptr,
globalWorkSize,
nullptr,
0, nullptr, nullptr));
```


This enqueues the kernel for execution. Finally, we need to get the results back, which is done using `clEnqueueReadBuffer`

. We call it with the blocking parameter set to `true`

, so the call will block until the kernel has finished working before the data is read back. We also didn’t specify the work group size, so the implementation will use something suitable.

And voilà, our first OpenCL program has run! In the next and final part, we’ll take a look at how to do image processing with OpenCL, to make it do something actually useful.