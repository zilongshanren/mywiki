---
title: Accelerated Game Of Life with CUDA / Triton
url: https://www.boristhebrave.com/2025/09/11/accelerated-game-of-life-with-cuda-triton/
author: Boris
published: '2025-09-11'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Let’s look at implementing [Conway’s Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using a graphics card. I want to experiment with different libraries and techniques, to see how to get the best performance. I’m going to start simple, and get increasingly complex as we dive in.

The Game Of Life is a simple cellular automata, so should be really amenable to GPU acceleration. The rules are simple: Each cell in the 2d grid is either alive or dead. At each step, count the alive neighbours of the cell (including diagonals). If the cell is alive, it remains alive if 2 or 3 neighbours are alive. Otherwise it dies. If the cell is dead, it comes ot life if exactly 3 neighbours are alive. These simple rules cause an amazing amount of emergent complexity which has been written about copiously elsewhere.

For simplicity, I’ll only consider N×N grids, and skip calculations on the boundary. I ran everything with an A40, and I’ll benchmark performance at N=216 . For now, we’ll store each cell as 1 byte so this array is which equates to 4 GB of data.

All code is shared in the ** GitHub repo**.

Table of Contents

An A40 has a memory bandwidth of 696 GB/s. That is the speed of transferring data from DRAM to the cores that actually perform calculation. To calculate the cell, the GPU needs to load **at least** one byte and store one byte when done. So, considering nothing but memory transfer, we need at least 4 GB * 2 / 696 GB/s = **11.5 ms**.

As the game’s rules are relatively simple, we’re rarely going to be able to saturate the compute capabilities of the GPU, which is the other common limiting factor. So 11.5 ms is the target we want to get as close as possible to.

** Pytorch** is a popular Python library for Machine Learning that comes with a useful set of operations. Torch has built-in support for convolutions, but they are designed for floating-point and include unneeded multiplications. Instead I use a separable box blur to compute the number of alive cells in each 3

**×**3 rectangle. From there some simple logic covers the game of life rules.

```
def gol_torch_sum(x: torch.Tensor) -> torch.Tensor:
y = x[2:] + x[1:-1] + x[:-2]
z = y[:, 2:] + y[:, 1:-1] + y[:, :-2]
z = torch.nn.functional.pad(z, (1, 1, 1, 1), value=0)
return ((x == 1) & (z == 4)) | (z == 3).to(torch.int8)
```


I benchmarked this at **223 ms**. Torch has a lot of overhead as every operation dispatches a separate operation to the GPU, causing a lot of unnecessary transfers.

We can use [ torch.compile](https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html) to combine and optimize as many operations as possible, giving a much more respectable

**38.1 ms**, or

**30% of max performance**.

The traditional way of maximizing compute on GPUs is [CUDA](https://en.wikipedia.org/wiki/CUDA). This is a programming interface proprietary to NVIDIA GPUs. You write **kernels** in C/C++ that get compiled into programs that are run directly on the graphics card. CUDA gives a vast amount of control over your computation, but to start with, we’ll write a simple kernel. It looks like a C function that computes the value for a single cell – CUDA will then run that code in parallel over millions of cells at once.

```
__global__ void gol_kernel_i8(const int8_t* __restrict__ x_ptr,
int8_t* __restrict__ out_ptr,
int64_t rowstride, int64_t n) {
int64_t x = blockIdx.x * blockDim.x + threadIdx.x;
int64_t y = blockIdx.y * blockDim.y + threadIdx.y;
if (x >= n - 2 || y >= n - 2) return;
int8_t r00 = x_ptr[y * rowstride + x + 0 * rowstride + 0];
int8_t r01 = x_ptr[y * rowstride + x + 0 * rowstride + 1];
int8_t r02 = x_ptr[y * rowstride + x + 0 * rowstride + 2];
int8_t r10 = x_ptr[y * rowstride + x + 1 * rowstride + 0];
int8_t r11 = x_ptr[y * rowstride + x + 1 * rowstride + 1];
int8_t r12 = x_ptr[y * rowstride + x + 1 * rowstride + 2];
int8_t r20 = x_ptr[y * rowstride + x + 2 * rowstride + 0];
int8_t r21 = x_ptr[y * rowstride + x + 2 * rowstride + 1];
int8_t r22 = x_ptr[y * rowstride + x + 2 * rowstride + 2];
int8_t sum = r00 + r01 + r02 + r10 + r12 + r20 + r21 + r22;
int8_t result = (r11 > 0) ? ((sum == 2) || (sum == 3) ? 1 : 0) : (sum == 3 ? 1 : 0);
out_ptr[(y + 1) * rowstride + (x + 1)] = result;
}
void gol(torch::Tensor x, torch::Tensor out, int block_size_row, int block_size_col) {
const long n = x.size(0);
const int row_blocks = (n - 2 + block_size_row - 1) / block_size_row;
const int col_blocks = (n - 2 + block_size_col - 1) / block_size_col;
auto stream = at::cuda::getCurrentCUDAStream();
dim3 grid(col_blocks, row_blocks);
dim3 block(block_size_col, block_size_row);
gol_kernel_i8<<<grid, block, 0, stream>>>(
x.data_ptr<int8_t>(), out.data_ptr<int8_t>(), x.stride(0), n);
TORCH_CHECK(cudaGetLastError() == cudaSuccess, "kernel launch failed");
}
```


This code features tunable parameters `block_size_row `

and `block_size_col`

. The kernel will split our N×N cells into a grid of thread blocks each sized `block_size_row×block_size_col`

. Each block is dispatched to one of the 84 streaming multiprocessors (SM) for execution. All calculations in a thread block occur on the same SM, and thus share the same L1 cache.

Caching makes a huge difference to the performance of our kernel. If there was no caching, then the above kernel would be naively reading 9 cells, and writing back to 1. That much data transfer would take over 55 ms. But the various layers of internal caching mean cells typically only need to be read once, stored in the cache, and then re-used for all 9 cells nearby that need the value.

The interaction between block size and caching is complicated. If the blocks are square, then we minimise the amount of perimeter, which the cells that will need to be loaded in multiple thread blocks. But on the other hand, columns are arranged consecutively in memory and there are optimizations for that, so you might prefer wider rectangles. The block area cannot be more than 1024 due to internal GPU limits, and needs to be a multiple of 32 to avoid wasting threads. If the block is too large it occupies a lot of registers and becomes hard to schedule several concurrently, reducing occupancy.

In short, it’s hard to reason about exactly. Typically, you’d just benchmark and pick the best combination. In my case, the best result is a 1×128 sized block, which is a typical size for bandwidth-limited kernels.

![](../../assets/52647334f1b03e9e.png)

This gets us a respectable **26 ms** or **44%** of peak performance.

We saw above that torch.compile gave a 5x performance enhancment. Internally, torch.compile works by scanning your torch program, and converting it to a [Triton](https://en.wikipedia.org/wiki/Triton_(programming_language)) kernel. Triton is a custom programming language that both simplifies writing GPU kernels, and can handle a lot of performance enhancements that are pretty tedious to implement manually in CUDA. Code in Triton works similarly to CUDA, but it’s written in python, and you are encouraged to do bulk vector operations with `triton.language.tensor`

. We can use it directly instead of using torch.compile and get even better performance.

Triton doesn’t have any ability to slice, but you can offset the base pointer. So I compute 3 different row offsets and column offsets to get 9 distinct tensors that heavily overlap.

Note: This kernel is a little tricky to read. You might prefer to start with the [1d kernel](https://github.com/BorisTheBrave/gol/blob/main/gol_triton.py#L8), which assumes BLOCK_SIZE_ROW=1.

```
@triton.jit
def gol_triton_2d_kernel(x_ptr, out_ptr, row_stride: tl.int64, N: tl.int64, BLOCK_SIZE_ROW: tl.constexpr, BLOCK_SIZE_COL: tl.constexpr):
row_id = tl.program_id(1)
col_id = tl.program_id(0)
col_offsets0 = (col_id * BLOCK_SIZE_COL + tl.arange(0, BLOCK_SIZE_COL) + 0)[None, :]
col_offsets1 = (col_id * BLOCK_SIZE_COL + tl.arange(0, BLOCK_SIZE_COL) + 1)[None, :]
col_offsets2 = (col_id * BLOCK_SIZE_COL + tl.arange(0, BLOCK_SIZE_COL) + 2)[None, :]
row_offsets0 = (row_id * BLOCK_SIZE_ROW + tl.arange(0, BLOCK_SIZE_ROW) + 0)[:, None]
row_offsets1 = (row_id * BLOCK_SIZE_ROW + tl.arange(0, BLOCK_SIZE_ROW) + 1)[:, None]
row_offsets2 = (row_id * BLOCK_SIZE_ROW + tl.arange(0, BLOCK_SIZE_ROW) + 2)[:, None]
col_mask0 = (col_offsets0 >= 0) & (col_offsets0 < N)
col_mask1 = (col_offsets1 >= 0) & (col_offsets1 < N)
col_mask2 = (col_offsets2 >= 0) & (col_offsets2 < N)
row_mask0 = (row_offsets0 >= 0) & (row_offsets0 < N)
row_mask1 = (row_offsets1 >= 0) & (row_offsets1 < N)
row_mask2 = (row_offsets2 >= 0) & (row_offsets2 < N)
row00 = tl.load(x_ptr + row_offsets0 * row_stride + col_offsets0, mask=row_mask0 & col_mask0, other=0)
row01 = tl.load(x_ptr + row_offsets0 * row_stride + col_offsets1, mask=row_mask0 & col_mask1, other=0)
row02 = tl.load(x_ptr + row_offsets0 * row_stride + col_offsets2, mask=row_mask0 & col_mask2, other=0)
row10 = tl.load(x_ptr + row_offsets1 * row_stride + col_offsets0, mask=row_mask1 & col_mask0, other=0)
row11 = tl.load(x_ptr + row_offsets1 * row_stride + col_offsets1, mask=row_mask1 & col_mask1, other=0)
row12 = tl.load(x_ptr + row_offsets1 * row_stride + col_offsets2, mask=row_mask1 & col_mask2, other=0)
row20 = tl.load(x_ptr + row_offsets2 * row_stride + col_offsets0, mask=row_mask2 & col_mask0, other=0)
row21 = tl.load(x_ptr + row_offsets2 * row_stride + col_offsets1, mask=row_mask2 & col_mask1, other=0)
row22 = tl.load(x_ptr + row_offsets2 * row_stride + col_offsets2, mask=row_mask2 & col_mask2, other=0)
sum = row00 + row01 + row02 + row10 + row12 + row20 + row21 + row22
result = tl.where(row11 > 0, (sum == 2) | (sum == 3), sum == 3).to(tl.int8)
tl.store(out_ptr + row_offsets1 * row_stride + col_offsets1, result, mask=row_mask1 & col_mask1)
def gol_triton_2d(x: torch.Tensor, BLOCK_SIZE_ROW, BLOCK_SIZE_COL):
output = torch.empty_like(x)
grid = (
triton.cdiv(x.shape[1] - 2, BLOCK_SIZE_COL),
triton.cdiv(x.shape[0] - 2, BLOCK_SIZE_ROW),
)
gol_triton_2d_kernel[grid](x, output, x.stride(0), x.shape[0],
BLOCK_SIZE_ROW=BLOCK_SIZE_ROW, BLOCK_SIZE_COL=BLOCK_SIZE_COL)
return output
```


Again, we need to measure performance for different block sizes. Block size in Triton isn’t quite the same thing as CUDA. Triton uses a thread group of size 128 – if you make the block larger than that, it starts computing more elements in a single thread.

![](../../assets/4359a17c9653b8e5.png)

With 1024 elements in a thread block, and 128 threads per block, each thread will compute 8 cells. Triton arranges the loads to be consecutive so it can use wide or vectorised load/stores. Triton can also take advantage of shared memory 1. I confirmed that the generated code

is doing something like this.

[2](https://www.boristhebrave.com#0af2348f-f09b-4414-a1fc-c0e16c882ebf)All in, this gives a runtime of **22.5 ms** or **51%** of peak.

My original CUDA kernel evaluated a single cell per thread. One of Triton’s key optimizations is reducing the thread count per block, and evaluating more cells per thread. A way of doing that in CUDA is simply to add additional loops around the whole kernel.

```
#define COL_GROUP_SIZE 4
#define ROW_GROUP_SIZE 2
__global__ void gol_kernel_grouped(const int8_t* __restrict__ x_ptr, int8_t* __restrict__ out_ptr, int64_t rowstride, int64_t n) {
for (int j = 0; j < ROW_GROUP_SIZE; j++) {
int64_t y = (blockIdx.y * blockDim.y + threadIdx.y) * ROW_GROUP_SIZE + j;
if (y >= n - 2) break;
for (int i = 0; i < COL_GROUP_SIZE; i++) {
int64_t x = (blockIdx.x * blockDim.x + threadIdx.x) * COL_GROUP_SIZE + i;
if (x >= n - 2) break;
int8_t r00 = x_ptr[y * rowstride + x + 0 * rowstride + 0];
int8_t r01 = x_ptr[y * rowstride + x + 0 * rowstride + 1];
int8_t r02 = x_ptr[y * rowstride + x + 0 * rowstride + 2];
int8_t r10 = x_ptr[y * rowstride + x + 1 * rowstride + 0];
int8_t r11 = x_ptr[y * rowstride + x + 1 * rowstride + 1];
int8_t r12 = x_ptr[y * rowstride + x + 1 * rowstride + 2];
int8_t r20 = x_ptr[y * rowstride + x + 2 * rowstride + 0];
int8_t r21 = x_ptr[y * rowstride + x + 2 * rowstride + 1];
int8_t r22 = x_ptr[y * rowstride + x + 2 * rowstride + 2];
int8_t sum = r00 + r01 + r02 + r10 + r12 + r20 + r21 + r22;
int8_t result = (r11 > 0) ? ((sum == 2) || (sum == 3) ? 1 : 0) : (sum == 3 ? 1 : 0);
out_ptr[(y + 1) * rowstride + (x + 1)] = result;
}
}
}
void gol(torch::Tensor x, torch::Tensor out, int block_size_row, int block_size_col) {
TORCH_CHECK(block_size_col % COL_GROUP_SIZE == 0, "block_size_col must be divisible by COL_GROUP_SIZE");
TORCH_CHECK(block_size_row % ROW_GROUP_SIZE == 0, "block_size_row must be divisible by ROW_GROUP_SIZE");
TORCH_CHECK(x.size(0) % COL_GROUP_SIZE == 0, "n must be divisible by COL_GROUP_SIZE");
TORCH_CHECK(x.size(1) % ROW_GROUP_SIZE == 0, "n must be divisible by ROW_GROUP_SIZE");
const long n = x.size(0);
const int row_blocks = (n - 2 + block_size_row - 1) / block_size_row;
const int col_blocks = (n - 2 + block_size_col - 1) / block_size_col;
auto stream = at::cuda::getCurrentCUDAStream();
dim3 grid(col_blocks, row_blocks);
dim3 block(block_size_col / COL_GROUP_SIZE, block_size_row / ROW_GROUP_SIZE);
gol_kernel_grouped<<<grid, block, 0, stream>>>(
x.data_ptr<int8_t>(), out.data_ptr<int8_t>(), x.stride(0), n);
TORCH_CHECK(cudaGetLastError() == cudaSuccess, "kernel launch failed");
}
```


After some profiling, I found this gave best results at `ROW_GROUP_SIZE`

=1, `BLOCK_SIZE_ROW`

=1, `COL_GROUP_SIZE`

=4, `BLOCK_SIZE_COL`

=512. This comes in at **14.7 ms** or **78%** of peak performance. For typical CUDA programming getting to 60% is considered good and 80% excellent!

I was honestly surprised this kernel performs so well. It still reads and writes one byte at a time 3. Presumably the combination of loop unrolling caching and out of order exeuction is enough to maximize gains.

I did a few other CUDA experiments: loading 4-bytes in a single instruction instead of setting COL_GROUP_SIZE=4 gave equivalent peformance. I also experimented with using shared memory, but it performed horribly compared with more naive things. So I think this is as good as we’ll get for now. Let me know if you have any futher suggestions.

When starting this project, I wanted to experiment with 1 byte per cell as that is closer to a typical ML kernel which uses quantized floats. So I have ignored the obvious approach: for the Game of Life we really only need a single bit per cell. As we’re limited by memory bandwidth, shrinking the storage by a factor of 8 will completely smash any incremental improvements we can make on the kernel.

I made a [Triton kernel](https://github.com/BorisTheBrave/gol/blob/main/gol_triton.py#L107) that unpacks the 8 bits, (and loads more bits from adjacent bytes), and computes 8 cells. I also made 32 and 64 bit variants, that use bit-fiddling tricks to compute many cells in a single instruction.

| Theoretical Limit | 1.4 ms |
| Bitpacked 8-bit Triton | 14.9 ms |
| Bitpacked 32-bit Triton | 5.21 ms |
| Bitpacked 64-bit Triton | 6.44 ms |

As you can see, these kernels are way more efficient than the theoretical maximum without bit packing. But they don’t actually get close to an 8x speedup. I expect what is happening is that I’m finally getting compute bound. These kernels have a great deal of bitwise calculation. Ideally I’d use Nsight Systems or Nsight Compute to confirm this, but I couldn’t get it running on my virtual server.

Naturally I tried the same thing in CUDA. This works much better than Triton, I’m not sure why. Then I had ChatGPT write the bitpacked kernel that processes all 64-bits at once with uint64 bitwise operations.

| Theoretical Limit | 1.4 ms |
| Bitpacked 8-bit CUDA | 8.04 ms |
| Bitpacked 64-bit CUDA | 1.84 ms |

![](../../assets/a592a61d366d4ef8.png)

These kernels are pretty agnostic to block size. I expect this is because the individual threads are already loading wide enough to take advantage of cachelines, etc. So it doesn’t matter if two threads are consecutive or not – they don’t share much caching. There’s no performance gain to grouping either – these threads are already handling 64 cells each, which is chunky enough.

Here are all the results again, in a convenient table:

| Duration | % of peak bandwidth | |
|

**223 ms**[torch.compile](https://github.com/BorisTheBrave/gol/blob/main/gol_torch.py#L60)**38.1 ms**[Naive CUDA](https://github.com/BorisTheBrave/gol/blob/main/gol_cuda.cpp)**26 ms**[Naive Triton](https://github.com/BorisTheBrave/gol/blob/main/gol_triton.py#L54)**22.5 ms**[Grouped CUDA](https://github.com/BorisTheBrave/gol/blob/main/gol_cuda_grouped.cpp)**14.7 ms**[Bitpacked 8-bit Triton](https://github.com/BorisTheBrave/gol/blob/main/gol_triton.py#L107)**14.9 ms**[Bitpacked 32-bit Triton](https://github.com/BorisTheBrave/gol/blob/main/gol_triton.py#L214)**5.21 ms**[Bitpacked 64-bit CUDA](https://github.com/BorisTheBrave/gol/blob/main/gol_cuda_grouped_bitpacked_64.cpp)**1.84 ms**![](../../assets/3f1736c97019ad1e.png)

Overall, we’ve increased performance 120 times! And that was starting from GPU-accelerated code, which is already orders of magnitude faster than CPU code.

I was pretty impressed with the accelerator/compiler stack for both Triton and CUDA. They have a lot of magic inside to ensure that if you do the naive thing, they will sort out a lot of the details for you. The main improvements I was able to make came more from tuning block and group sizes than from doing anything really clever.

Triton itself was a mixed bag. It is definitely a bit friendlier to use than CUDA, particularly if you don’t know C/C++. It comes with more stuff out of the box, so you can get good performance with less work than CUDA. But ultimately, it wasn’t able to equal the performance of a relatively easy-to-write CUDA kernel, and there is less to fiddle with when it goes wrong. To be fair, this is partly due to my workload – I’m using an older gen GPU, and have no floating point operations, so miss out on many of the best operations of Triton. But I think I’ll still reach for CUDA when I have the time for extreme effort.

- Triton has other tricks, like using async copy and tensor operations, but they are not available on an A40 or relevant to this particular kernel.
[↩︎](https://www.boristhebrave.com#17f5f218-3e5e-43db-a101-2e8ee592846b-link) - To extract the compiled output, I used:
`k = gol_triton_2d_kernel.warmup(x, out, x.stride(0), x.shape[0],`


BLOCK_SIZE_ROW=4, BLOCK_SIZE_COL=256, grid=(1, 1))

print(k.asm['llir'])

print(k.asm['ptx'])

LLIR is[LLVM](https://en.wikipedia.org/wiki/LLVM)intermediate representation, which is modestly readable, and[PTX](https://en.wikipedia.org/wiki/Parallel_Thread_Execution)is the bytecode that Nvidia GPUs use.

[↩︎](https://www.boristhebrave.com#0af2348f-f09b-4414-a1fc-c0e16c882ebf-link) - You can inspect the compiled PTX and SASS with
`cuobjdump --dump-ptx <file>`

[↩︎](https://www.boristhebrave.com#fc6eb66f-7708-4e42-bb51-cafe8ac55f66-link)

Your theoretical limit calculation is incorrect. Game of life is not memory bound by DRAM access, but by the bandwidth of your local SRAM. To compute an N^2 grid K steps into the future requires knowledge of (N+K)^2 cells and no additional communication at all. At the cost of evaluating the border regions multiple times. By selecting (N+K)^2 to fit into your shared memory (or even local registers) and tuning K you can make sure you are never DRAM-memory bound.

By going through DRAM, you are leaving many orders of magnitude of performance improvement on the table 🙂

Yes, that is true. I did consider simulating more than 1 step at once, but then forgot about it. You also won’t be able to see intermediate steps with that approach. We’ll have to leave it for a followup.

I put off bitpacking for similar reasons – i wanted to experiment with kernels that are close to the median kernel, rather than focus too hard on the game of life itself. Otherwise we’d have to start getting into the Hashlife algorithm.