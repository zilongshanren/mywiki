---
title: 'Reloaded: Compute Shader Optimizations for AMD GPUs: Parallel Reduction'
url: http://diaryofagraphicsprogrammer.blogspot.com/2015/01/reloaded-compute-shader-optimizations.html
author: Wolfgang Engel
published: '2015-01-12'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

After nearly a year, it was time to revisit the last blog entry. The source code of the example implementation was still on one of my hard-drives and needed to be cleaned-up and released, which I had planned for the first quarter of last year.

I also did receive a comment high-lighting a few mistakes I made in the previous blog post and on top of that I wanted to add numbers for other GPUs as well.


Now while looking at the code the few hours of time I had reserved for the task turned into a day and then a bit more. On top of that getting some time off from my project management duties at Confetti was quite enjoyable :-)


In the previous blog post I forgot to mention that I used INTEL's GPA to measure all the performance numbers. Several runs of the performance profiler always generated slightly different results but I felt the overall direction is becoming clear.

My current setup uses the currently latest AMD driver 14.12.


All the source code can be found at




While comparing the current performance numbers with the previous setup from the previous post, it becomes obvious that not much has changed for the first three rows. Here is the new chart:



In the fourth column ("Pre-fetching two color values into TGSM with 64 threads"), the numbers for the 6770 are nearly cut in half while they stay roughly the same for the other cards; only a slight improvement on the 290X. This is the first shader that fetches two values from device memory, converts them to luminance, stores them into shared memory and then kicks off the Parallel Reduction.

Here is the source code.


StructuredBuffer Input : register( t0 );


















Looking at the performance results ("Pre-fetching four color values into TGSM with 64 threads"), the difference between the performance numbers is not significant. This seems to be the first sign that the shader might be read memory bandwidth limited. Just reading the 1080p memory area takes the longest time.


While all the previous shaders were writing the reduced image into a 120 x 68 area, The following two shaders in the chart are writing into a 60 x 34 area. This is mostly achieved by decreasing the grid size, or in other words running less thread groups. To make up for the decrease in grid size we had to increase the size of each thread group to 256 and then 512.


#define THREADX 8

#define THREADY 32



// thread groups in x is 1920 / 32 = 60

// thread groups in y is 1080 / 32 = 34

// index in x (1920) goes from 0 to 60 (thread groups) * 8 (threads) = 480 indices in x

// index in y (1080) goes from 0 to 34 (thread groups) * 32 (threads) = 1088 indices in y

uint idx = ((DTid.x * 4) + DTid.y * c_width);


// 1920 * 1080 = 2073600 pixels

// 60 * 34 * 256 (number of threads : 8 * 32) * 4 (number of fetches) = 2088960

float temp = (dot(Input[idx], LumVector) + dot(Input[idx + 1], LumVector))

+ (dot(Input[idx + 2], LumVector) + dot(Input[idx + 3], LumVector));


// store in shared memory

sharedMem[IndexOfThreadInGroup] = temp;


// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();


// hard-coded for 256 threads

if (IndexOfThreadInGroup < 128)

sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 128];

GroupMemoryBarrierWithGroupSync();


if (IndexOfThreadInGroup < 64)

sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 64];

GroupMemoryBarrierWithGroupSync();


if (IndexOfThreadInGroup < 32) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 32];

if (IndexOfThreadInGroup < 16) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 16];

if (IndexOfThreadInGroup < 8) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 8];

if (IndexOfThreadInGroup < 4) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 4];

if (IndexOfThreadInGroup < 2) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 2];

if (IndexOfThreadInGroup < 1) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 1];






I also did receive a comment high-lighting a few mistakes I made in the previous blog post and on top of that I wanted to add numbers for other GPUs as well.

Now while looking at the code the few hours of time I had reserved for the task turned into a day and then a bit more. On top of that getting some time off from my project management duties at Confetti was quite enjoyable :-)

In the previous blog post I forgot to mention that I used INTEL's GPA to measure all the performance numbers. Several runs of the performance profiler always generated slightly different results but I felt the overall direction is becoming clear.

My current setup uses the currently latest AMD driver 14.12.

All the source code can be found at

[https://code.google.com/p/graphicsdemoskeleton/source/browse/#svn%2Ftrunk%2F04_DirectCompute%20Parallel%20Reduction%20Case%20Study](https://code.google.com/p/graphicsdemoskeleton/source/browse/#svn%2Ftrunk%2F04_DirectCompute%20Parallel%20Reduction%20Case%20Study)While comparing the current performance numbers with the previous setup from the previous post, it becomes obvious that not much has changed for the first three rows. Here is the new chart:

*Latest Performance numbers from January 2015*

In the fourth column ("Pre-fetching two color values into TGSM with 64 threads"), the numbers for the 6770 are nearly cut in half while they stay roughly the same for the other cards; only a slight improvement on the 290X. This is the first shader that fetches two values from device memory, converts them to luminance, stores them into shared memory and then kicks off the Parallel Reduction.

Here is the source code.

StructuredBuffer

RWTexture2D Result : register (u0);

#define THREADX 8

#define THREADY 16

cbuffer cbCS : register(b0)

{

int c_height : packoffset(c0.x);

int c_width : packoffset(c0.y); // size view port

/*

This is in the constant buffer as well but not used in this shader, so I just keep it in here as a comment

float c_epsilon : packoffset(c0.z); // julia detail

int c_selfShadow : packoffset(c0.w); // selfshadowing on or off

float4 c_diffuse : packoffset(c1); // diffuse shading color

float4 c_mu : packoffset(c2); // julia quaternion parameter

float4x4 rotation : packoffset(c3);

float zoom : packoffset(c7.x);

*/

};

//

// the following shader applies parallel reduction to an image and converts it to luminance

//

#define groupthreads THREADX * THREADY

groupshared float sharedMem[groupthreads];

[numthreads(THREADX, THREADY, 1)]

void PostFX( uint3 Gid : SV_GroupID, uint3 DTid : SV_DispatchThreadID, uint3 GTid : SV_GroupThreadID, uint GI : SV_GroupIndex )

{

const float4 LumVector = float4(0.2125f, 0.7154f, 0.0721f, 0.0f);

// thread groups in x is 1920 / 16 = 120

// thread groups in y is 1080 / 16 = 68

// index in x (1920) goes from 0 to 119 | 120 (thread groups) * 8 (threads) = 960 indices in x

// index in y (1080) goes from 0 to 67 | 68 (thread groups) * 16 (threads) = 1080 indices in y

uint idx = ((DTid.x * 2) + DTid.y * c_width);

// 1920 * 1080 = 2073600 pixels

// 120 * 68 * 128(number of threads : 8 * 16) * 2 (number of fetches) = 2088960

// 120 * 68 * 128(number of threads : 8 * 16) * 2 (number of fetches) = 2088960

float temp = (dot(Input[idx], LumVector) + dot(Input[idx + 1], LumVector));

sharedMem[GI] = temp;

// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();

// hard-coded for 128 threads

if (GI < 64)

sharedMem[GI] += sharedMem[GI + 64];

GroupMemoryBarrierWithGroupSync();

if (GI < 32) sharedMem[GI] += sharedMem[GI + 32];

if (GI < 16) sharedMem[GI] += sharedMem[GI + 16];

if (GI < 8) sharedMem[GI] += sharedMem[GI + 8];

if (GI < 4) sharedMem[GI] += sharedMem[GI + 4];

if (GI < 2) sharedMem[GI] += sharedMem[GI + 2];

if (GI < 1) sharedMem[GI] += sharedMem[GI + 1];

// Have the first thread write out to the output

if (GI == 0)

{

// write out the result for each thread group

Result[Gid.xy] = sharedMem[0] / (THREADX * THREADY * 2);

}

}

The grid size in x and why is 1920 / 16 and 1080 / 16. In other words this is the number of thread groups kicked off by the dispatch call.

The next shader extends the idea to fetching four values. It fetches four instead of two values from device memory.

// thread groups in x is 1920 / 16 = 120

// thread groups in y is 1080 / 16 = 68

// index in x (1920) goes from 0 to 119 | 120 (thread groups) * 4 (threads) = 480 indices in x

// index in y (1080) goes from 0 to 67 | 68 (thread groups) * 16 (threads) = 1080 indices in y

uint idx = ((DTid.x * 4) + DTid.y * c_width);

// 1920 * 1080 = 2073600 pixels

// 120 * 68 * 64 (number of threads : 4 * 16) * 4 (number of fetches) = 2088960

float temp = (dot(Input[idx], LumVector) + dot(Input[idx + 1], LumVector))

+ (dot(Input[idx + 2], LumVector) + dot(Input[idx + 3], LumVector));

// store in shared memory

sharedMem[IndexOfThreadInGroup] = temp;

// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();

if (IndexOfThreadInGroup < 32) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 32];

if (IndexOfThreadInGroup < 16) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 16];

if (IndexOfThreadInGroup < 8) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 8];

if (IndexOfThreadInGroup < 4) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 4];

if (IndexOfThreadInGroup < 2) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 2];

if (IndexOfThreadInGroup < 1) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 1];

Looking at the performance results ("Pre-fetching four color values into TGSM with 64 threads"), the difference between the performance numbers is not significant. This seems to be the first sign that the shader might be read memory bandwidth limited. Just reading the 1080p memory area takes the longest time.

While all the previous shaders were writing the reduced image into a 120 x 68 area, The following two shaders in the chart are writing into a 60 x 34 area. This is mostly achieved by decreasing the grid size, or in other words running less thread groups. To make up for the decrease in grid size we had to increase the size of each thread group to 256 and then 512.

#define THREADX 8

#define THREADY 32

... // more code here

// thread groups in y is 1080 / 32 = 34

// index in x (1920) goes from 0 to 60 (thread groups) * 8 (threads) = 480 indices in x

// index in y (1080) goes from 0 to 34 (thread groups) * 32 (threads) = 1088 indices in y

uint idx = ((DTid.x * 4) + DTid.y * c_width);

// 1920 * 1080 = 2073600 pixels

// 60 * 34 * 256 (number of threads : 8 * 32) * 4 (number of fetches) = 2088960

float temp = (dot(Input[idx], LumVector) + dot(Input[idx + 1], LumVector))

+ (dot(Input[idx + 2], LumVector) + dot(Input[idx + 3], LumVector));

// store in shared memory

sharedMem[IndexOfThreadInGroup] = temp;

// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();

// hard-coded for 256 threads

if (IndexOfThreadInGroup < 128)

sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 128];

GroupMemoryBarrierWithGroupSync();

if (IndexOfThreadInGroup < 64)

sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 64];

GroupMemoryBarrierWithGroupSync();

if (IndexOfThreadInGroup < 32) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 32];

if (IndexOfThreadInGroup < 16) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 16];

if (IndexOfThreadInGroup < 8) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 8];

if (IndexOfThreadInGroup < 4) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 4];

if (IndexOfThreadInGroup < 2) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 2];

if (IndexOfThreadInGroup < 1) sharedMem[IndexOfThreadInGroup] += sharedMem[IndexOfThreadInGroup + 1];

... // more code here

The next shader decreases the grid size even more and increases the number of threads of each thread group to 1024; the current maximum that the Direct3D run-time allows. For both shaders ("Pre-fetching four color values into TGSM with 1024 threads" and then "Pre-fetching four color values into 2x TGSM with 1024 threads"), the performance numbers do not change much compared to the previous shaders, although the reduction has to do more work, because the dimension of the target area halve in each direction. Here is the source code for the second of the two shaders that fetch four color values with 1024 threads per thread group:


#define THREADX 16

#define THREADY 64

//.. constant buffer code here

//

// the following shader applies parallel reduction to an image and converts it to luminance

//

#define groupthreads THREADX * THREADY

groupshared float sharedMem[groupthreads * 2]; // double the number of shared mem slots


[numthreads(THREADX, THREADY, 1)]

void PostFX( uint3 Gid : SV_GroupID, uint3 DTid : SV_DispatchThreadID, uint3 GTid : SV_GroupThreadID, uint GI : SV_GroupIndex )

{

const float4 LumVector = float4(0.2125f, 0.7154f, 0.0721f, 0.0f);


// thread groups in x is 1920 / 64 = 30

// thread groups in y is 1080 / 64 = 17

// index in x (1920) goes from 0 to 29 | 30 (thread groups) * 16 (threads) = 480 indices in x

// index in y (1080) goes from 0 to 16 | 17 (thread groups) * 64 (threads) = 1088 indices in y

uint idx = ((DTid.x * 4) + DTid.y * c_width); // index into structured buffer


// 1920 * 1080 = 2073600 pixels

// 30 * 17 * 1024 (number of threads : 16 * 64) * 4 (number of fetches) = 2088960

uint idSharedMem = GI * 2;

sharedMem[idSharedMem] = (dot(Input[idx], LumVector) + dot(Input[idx + 1], LumVector));

sharedMem[idSharedMem + 1] = (dot(Input[idx + 2], LumVector) + dot(Input[idx + 3], LumVector));


// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();


// hard-coded for 1024 threads

if (GI < 1024)

sharedMem[GI] += sharedMem[GI + 1024];

GroupMemoryBarrierWithGroupSync();


if (GI < 512)

sharedMem[GI] += sharedMem[GI + 512];

GroupMemoryBarrierWithGroupSync();


if (GI < 256)

sharedMem[GI] += sharedMem[GI + 256];

GroupMemoryBarrierWithGroupSync();


if (GI < 128)

sharedMem[GI] += sharedMem[GI + 128];

GroupMemoryBarrierWithGroupSync();


if (GI < 64)

sharedMem[GI] += sharedMem[GI + 64];

GroupMemoryBarrierWithGroupSync();


if (GI < 32) sharedMem[GI] += sharedMem[GI + 32];

if (GI < 16) sharedMem[GI] += sharedMem[GI + 16];

if (GI < 8) sharedMem[GI] += sharedMem[GI + 8];

if (GI < 4) sharedMem[GI] += sharedMem[GI + 4];

if (GI < 2) sharedMem[GI] += sharedMem[GI + 2];

if (GI < 1) sharedMem[GI] += sharedMem[GI + 1];


One thing I wanted to try here, is utilize double the amount of shared memory and therefore saturate the 1024 threads more by having the first addition happening in shared memory. At the end that didn't change much because the shader is not utilizing temp registers much, so replacing a temp register with using shared memory didn't increase performance much.


My last test was aiming at fetching 16 color values while decreasing the 1080p image to 15x9. The result is shown in the last column. This shader also uses 1024 threads and fetches into 2x the shared memory like the previous one. It runs slower than the previous shaders. Here is the source code:


#define THREADX 16

#define THREADY 64

//.. some constant buffer code here

//

// the following shader applies parallel reduction to an image and converts it to luminance

//

#define groupthreads THREADX * THREADY

groupshared float sharedMem[groupthreads * 2]; // double the number of shared mem slots


[numthreads(THREADX, THREADY, 1)]

void PostFX( uint3 Gid : SV_GroupID, uint3 DTid : SV_DispatchThreadID, uint3 GTid : SV_GroupThreadID, uint GI : SV_GroupIndex )

{

const float4 LumVector = float4(0.2125f, 0.7154f, 0.0721f, 0.0f);


// thread groups in x is 1920 / 128 = 15

// thread groups in y is 1080 / 128 = 9

// index in x (1920) goes from 0 to 14 | 15 (thread groups) * 16 (threads)

// = 240 indices in x | need to fetch 8 in x direction

// index in y (1080) goes from 0 to 8 | 9 (thread groups) * 64 (threads)

// = 576 indices in y | need to fetch 2 in y direction

uint idx = ((DTid.x * 8) + (DTid.y * 2) * c_width); // index into structured buffer


// 1920 * 1080 = 2073600 pixels

// 15 * 9 * 1024 (number of threads : 16 * 64) * 15 (number of fetches) = 2073600

uint idSharedMem = GI * 2;

sharedMem[idSharedMem] = (dot(Input[idx], LumVector)

+ dot(Input[idx + 1], LumVector)

+ dot(Input[idx + 2], LumVector)

+ dot(Input[idx + 3], LumVector)

+ dot(Input[idx + 4], LumVector)

+ dot(Input[idx + 5], LumVector)

+ dot(Input[idx + 6], LumVector)

+ dot(Input[idx + 7], LumVector));

sharedMem[idSharedMem + 1] = (dot(Input[idx + 8], LumVector)

+ dot(Input[idx + 9], LumVector)

+ dot(Input[idx + 10], LumVector)

+ dot(Input[idx + 11], LumVector)

+ dot(Input[idx + 12], LumVector)

+ dot(Input[idx + 13], LumVector)

+ dot(Input[idx + 14], LumVector)

+ dot(Input[idx + 15], LumVector));


// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();


// hard-coded for 1024 threads

if (GI < 1024)

sharedMem[GI] += sharedMem[GI + 1024];

GroupMemoryBarrierWithGroupSync();


if (GI < 512)

sharedMem[GI] += sharedMem[GI + 512];

GroupMemoryBarrierWithGroupSync();


if (GI < 256)

sharedMem[GI] += sharedMem[GI + 256];

GroupMemoryBarrierWithGroupSync();


if (GI < 128)

sharedMem[GI] += sharedMem[GI + 128];

GroupMemoryBarrierWithGroupSync();


if (GI < 64)

sharedMem[GI] += sharedMem[GI + 64];

GroupMemoryBarrierWithGroupSync();


if (GI < 32) sharedMem[GI] += sharedMem[GI + 32];

if (GI < 16) sharedMem[GI] += sharedMem[GI + 16];

if (GI < 8) sharedMem[GI] += sharedMem[GI + 8];

if (GI < 4) sharedMem[GI] += sharedMem[GI + 4];

if (GI < 2) sharedMem[GI] += sharedMem[GI + 2];

if (GI < 1) sharedMem[GI] += sharedMem[GI + 1];

#define THREADX 16

#define THREADY 64

//.. constant buffer code here

//

// the following shader applies parallel reduction to an image and converts it to luminance

//

#define groupthreads THREADX * THREADY

groupshared float sharedMem[groupthreads * 2]; // double the number of shared mem slots

[numthreads(THREADX, THREADY, 1)]

void PostFX( uint3 Gid : SV_GroupID, uint3 DTid : SV_DispatchThreadID, uint3 GTid : SV_GroupThreadID, uint GI : SV_GroupIndex )

{

const float4 LumVector = float4(0.2125f, 0.7154f, 0.0721f, 0.0f);

// thread groups in x is 1920 / 64 = 30

// thread groups in y is 1080 / 64 = 17

// index in x (1920) goes from 0 to 29 | 30 (thread groups) * 16 (threads) = 480 indices in x

// index in y (1080) goes from 0 to 16 | 17 (thread groups) * 64 (threads) = 1088 indices in y

uint idx = ((DTid.x * 4) + DTid.y * c_width); // index into structured buffer

// 1920 * 1080 = 2073600 pixels

// 30 * 17 * 1024 (number of threads : 16 * 64) * 4 (number of fetches) = 2088960

uint idSharedMem = GI * 2;

sharedMem[idSharedMem] = (dot(Input[idx], LumVector) + dot(Input[idx + 1], LumVector));

sharedMem[idSharedMem + 1] = (dot(Input[idx + 2], LumVector) + dot(Input[idx + 3], LumVector));

// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();

// hard-coded for 1024 threads

if (GI < 1024)

sharedMem[GI] += sharedMem[GI + 1024];

GroupMemoryBarrierWithGroupSync();

if (GI < 512)

sharedMem[GI] += sharedMem[GI + 512];

GroupMemoryBarrierWithGroupSync();

if (GI < 256)

sharedMem[GI] += sharedMem[GI + 256];

GroupMemoryBarrierWithGroupSync();

if (GI < 128)

sharedMem[GI] += sharedMem[GI + 128];

GroupMemoryBarrierWithGroupSync();

if (GI < 64)

sharedMem[GI] += sharedMem[GI + 64];

GroupMemoryBarrierWithGroupSync();

if (GI < 32) sharedMem[GI] += sharedMem[GI + 32];

if (GI < 16) sharedMem[GI] += sharedMem[GI + 16];

if (GI < 8) sharedMem[GI] += sharedMem[GI + 8];

if (GI < 4) sharedMem[GI] += sharedMem[GI + 4];

if (GI < 2) sharedMem[GI] += sharedMem[GI + 2];

if (GI < 1) sharedMem[GI] += sharedMem[GI + 1];

One thing I wanted to try here, is utilize double the amount of shared memory and therefore saturate the 1024 threads more by having the first addition happening in shared memory. At the end that didn't change much because the shader is not utilizing temp registers much, so replacing a temp register with using shared memory didn't increase performance much.

My last test was aiming at fetching 16 color values while decreasing the 1080p image to 15x9. The result is shown in the last column. This shader also uses 1024 threads and fetches into 2x the shared memory like the previous one. It runs slower than the previous shaders. Here is the source code:

#define THREADX 16

#define THREADY 64

//.. some constant buffer code here

//

// the following shader applies parallel reduction to an image and converts it to luminance

//

#define groupthreads THREADX * THREADY

groupshared float sharedMem[groupthreads * 2]; // double the number of shared mem slots

[numthreads(THREADX, THREADY, 1)]

void PostFX( uint3 Gid : SV_GroupID, uint3 DTid : SV_DispatchThreadID, uint3 GTid : SV_GroupThreadID, uint GI : SV_GroupIndex )

{

const float4 LumVector = float4(0.2125f, 0.7154f, 0.0721f, 0.0f);

// thread groups in x is 1920 / 128 = 15

// thread groups in y is 1080 / 128 = 9

// index in x (1920) goes from 0 to 14 | 15 (thread groups) * 16 (threads)

// = 240 indices in x | need to fetch 8 in x direction

// index in y (1080) goes from 0 to 8 | 9 (thread groups) * 64 (threads)

// = 576 indices in y | need to fetch 2 in y direction

uint idx = ((DTid.x * 8) + (DTid.y * 2) * c_width); // index into structured buffer

// 1920 * 1080 = 2073600 pixels

// 15 * 9 * 1024 (number of threads : 16 * 64) * 15 (number of fetches) = 2073600

uint idSharedMem = GI * 2;

sharedMem[idSharedMem] = (dot(Input[idx], LumVector)

+ dot(Input[idx + 1], LumVector)

+ dot(Input[idx + 2], LumVector)

+ dot(Input[idx + 3], LumVector)

+ dot(Input[idx + 4], LumVector)

+ dot(Input[idx + 5], LumVector)

+ dot(Input[idx + 6], LumVector)

+ dot(Input[idx + 7], LumVector));

sharedMem[idSharedMem + 1] = (dot(Input[idx + 8], LumVector)

+ dot(Input[idx + 9], LumVector)

+ dot(Input[idx + 10], LumVector)

+ dot(Input[idx + 11], LumVector)

+ dot(Input[idx + 12], LumVector)

+ dot(Input[idx + 13], LumVector)

+ dot(Input[idx + 14], LumVector)

+ dot(Input[idx + 15], LumVector));

// wait until everything is transfered from device memory to shared memory

GroupMemoryBarrierWithGroupSync();

// hard-coded for 1024 threads

if (GI < 1024)

sharedMem[GI] += sharedMem[GI + 1024];

GroupMemoryBarrierWithGroupSync();

if (GI < 512)

sharedMem[GI] += sharedMem[GI + 512];

GroupMemoryBarrierWithGroupSync();

if (GI < 256)

sharedMem[GI] += sharedMem[GI + 256];

GroupMemoryBarrierWithGroupSync();

if (GI < 128)

sharedMem[GI] += sharedMem[GI + 128];

GroupMemoryBarrierWithGroupSync();

if (GI < 64)

sharedMem[GI] += sharedMem[GI + 64];

GroupMemoryBarrierWithGroupSync();

if (GI < 32) sharedMem[GI] += sharedMem[GI + 32];

if (GI < 16) sharedMem[GI] += sharedMem[GI + 16];

if (GI < 8) sharedMem[GI] += sharedMem[GI + 8];

if (GI < 4) sharedMem[GI] += sharedMem[GI + 4];

if (GI < 2) sharedMem[GI] += sharedMem[GI + 2];

if (GI < 1) sharedMem[GI] += sharedMem[GI + 1];

Looking at all those numbers it seems that the performance is mostly limited by the speed on how to read the 1080p source buffer. In the moment I would like to predict that reducing the source resolution to 720p or 480p would lead to a more differentiated view of performance. Maybe something to try in the future ...

## 2 comments:

A question perhaps not only for you, but for everyone reading this:


Are the applied optimization techniques roughly applicable for NVIDIA GPUs, and the AMD GPUs used in the PS4 and XBox One? Are there specific ones of these optimizations one should be careful with when applying them when using another form of GPU?

NVIDIA GPUs: you might get different results there. I haven't tried ... maybe something to do in a future blog.

In the past I saw more benefits from using compute on AMD GPUs than on NVIDIA GPUs. I suspect this is coming from the fact that replacing temporary register usage in a compute shader with thread group shared memory is more beneficial on AMD GPUs compared to NVIDIA GPUs. This might be the case because on certain generations of Hardware, NVIDIA had a much higher count of temp registers available ... but this is just speculation :-)

Console platforms: I need to be careful because Confetti is a developer for both platforms. In a broad sense the GPUs in the consoles are belonging to certain families that might share performance characteristics with Desktop GPUs. That being said the console platforms might have platform specific extensions that allow to optimize even further. So my performance numbers might not be fully representative for console GPUs.

Post a Comment