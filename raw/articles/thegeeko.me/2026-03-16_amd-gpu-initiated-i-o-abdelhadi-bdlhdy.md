---
title: AMD GPU-Initiated I/O · Abdelhadi | عبدالهادي
url: https://thegeeko.me/blog/nvme-amdgpu-p2pdma/
published: '2026-03-16'
source_blog: thegeeko.me
source_site: https://thegeeko.me
category: Graphics Programming Weekly — Jendrik Illner → linked
fetched: '2026-04-13'
---

[index](https://thegeeko.me/)

# AMD GPU-Initiated I/O

Traditionally, NVMe is driven from the CPU side. The CPU sets up the queues, programs BAR0, and rings the doorbells, and the GPU mostly shows up later when it is time to consume the data.

Lately I was wondering if we can change that. This experiment started with me reading
[Dr. Stephen Bates’s](https://www.linkedin.com/in/stephen-bates-8791263/) work. The main experiment is wire up an
NVMe device and an AMD GPU and make them talk directly. Conveniently I found some recent patches that will enable
us to do just that.

To make the GPU and the NVMe device talk there are two paths we need to pave.

First NVMe -> VRAM, the NVMe needs to be able to read and write to GPU VRAM directly. A
[recent patch](https://lore.kernel.org/linux-iommu/0-v1-b5cab63049c0+191af-dmabuf_map_type_jgg@nvidia.com)
by Jason Gunthorpe reworked some parts of DMA-BUF system in the Linux kernel which would help us.

Second GPU -> NVMe BAR0, the GPU needs to talk to the NVMe to inform it about commands to process. Also
there’s [some patches](https://lore.kernel.org/all/20250307052248.405803-1-vivek.kasireddy@intel.com)
by Vivek Kasiredd to enable a VFIO device to export it’s PCIe BAR0 as a DMA-BUF.

Both of the patches are a WIP I based my work on Gunthrope’s Linux tree 1, which have both of the patches. But
first let’s take a look at some basics about how NVMe, VFIO, and IOMMUFD work to make it easier to understand the
latter parts.

# NVMe

On a high level NVMe works with queue pairs SQs(Submission Queues), CQs(Completion Queues), and doorbells. SQs/CQs live in a memory the NVMe controller can access, usually system RAM. Then we just write commands in those queues and ring the doorbells to inform the controller, it will DMA and access the SQ to read the commands and write to the CQ.

There’s a special pair of queues called the admin queue which can be used to create I/O queues to transfer data, and can also respond to an Identify command that gives us some information about the NVMe device.

For a proof of concept, we need a minimal test: submit an Identify command to the admin queue from
CPU, notify the controller from the GPU side, and place the returned data in VRAM. If that works, then the basic
NVMe -> VRAM and GPU -> BAR0 path is real.[2](https://thegeeko.me#user-content-fn-2)

# VFIO, IOMMUFD, and IOAS

Now for the Linux side of things.

VFIO lets user-space manage a physical PCIe device in a controlled way. For this post, the important part is that it gives us access to PCIe BARs and lets us bind the device to an IOMMU-managed address space.

The latter part matters because the NVMe controller is a DMA-capable device. If user-space could just write any physical addresses into the queue registers, the device would happily DMA there, which would be a complete disaster.

Instead of handing the device raw physical addresses, we give it IOVAs, and the IOMMU translates those to the real backing memory. So from the controller’s point of view it is reading and writing some virtual I/O address space, and the kernel controls what that actually maps to.

IOMMUFD is the interface we use to program the IOMMU. It gives us the concept of an IOAS, an I/O address space. We can create one, attach our VFIO-managed NVMe device to it, and then map either normal user memory or DMA-BUF-backed memory into it.

This is what makes Path 1 possible. If we can map a VRAM-backed DMA-BUF into an IOAS, then the NVMe controller can DMA directly into VRAM.

For Path 2 VFIO allows us to export the NVMe BAR0 as DMA-BUF 3 which then we can map to the GPU VM.

# What Is Missing

At this point the shape of the problem is pretty clear.

For Path 1, we need IOMMUFD to accept a GPU allocation exported as a DMA-BUF and map it into the IOAS in a way a VFIO device could use.

For Path 2, we need the NVMe BAR to be exportable as a DMA-BUF, and we need a way to import that into GPU-visible address space.

The [DMA-BUF patches](https://lore.kernel.org/linux-iommu/0-v1-b5cab63049c0+191af-dmabuf_map_type_jgg@nvidia.com) is already
moving in the right direction, it replaces the old way of mapping the DMA-BUF `sg_tables`

by a system of
negotiation, which allows both the exporter and the importer to agree on a mapping type that works for both.

The new mapping type which interest us here is PAL(Physical Address List), which allows us to share raw physical
address with the importer. IOMMUFD only accepts this type 4, but the AMDGPU driver doesn’t support the PAL
mapping type.

# Path 1: NVMe -> GPU

We need to make the AMDGPU driver support PAL.

The first thing we need to do is pin the buffer. Once we expose physical address ranges, relocation becomes dangerous: if the driver moves the buffer after we hand those addresses to another device, the NVMe controller would keep DMAing to stale memory. Fortunately, AMDGPU already has DMA-BUF pinning.

```
static struct dma_buf_phys_list *
amdgpu_dma_buf_map_phys(struct dma_buf_attachment *attach)
{
...
r = amdgpu_dma_buf_pin(attach);
if (r)
return ERR_PTR(r);
```


Next we check that the buffer is actually backed by VRAM. If it lives in normal system memory, there is no need to go through this DMA-BUF path at all, because IOMMUFD can already map system memory directly.

```
if (bo->tbo.resource->mem_type != TTM_PL_VRAM) {
r = -EINVAL;
goto error_free;
}
```


Once the buffer is pinned and confirmed to live in VRAM, we can walk its backing store and build a PAL from the underlying physical ranges.

```
r = amdgpu_vram_mgr_alloc_pal(adev, bo->tbo.resource, 0,
bo->tbo.base.size, &pal);
```


The function `amdgpu_vram_mgr_alloc_pal`

is simple. It walks the VRAM resource block by block, counts how many ranges are needed, allocates the PAL, and then fills each entry with a physical address and a length. In this implementation, the physical address comes from the blocks offset into VRAM plus the GPU aperture base.

```
int amdgpu_vram_mgr_alloc_pal(struct amdgpu_device *adev,
struct ttm_resource *res, u64 offset, u64 length,
struct dma_buf_phys_list **pal)
{
...
while (cursor.remaining) {
u64 i = (*pal)->length;
(*pal)->phys[i].paddr = cursor.start + adev->gmc.aper_base;
(*pal)->phys[i].len = cursor.size;
(*pal)->length += 1;
amdgpu_res_next(&cursor, cursor.size);
}
...
}
```


Then, we mark the buffer as uncached. The NVMe controller is now writing to this memory directly, outside the GPU’s normal virtual-memory and cache-management path, so we need to avoid stale cached views of the data.

` bo->flags |= AMDGPU_GEM_CREATE_UNCACHED;`


Now this function `amdgpu_dma_buf_map_phys`

can get a PAL representing this buffer safely, we need to advertise
that we support PAL mapping. This function get invoked when negotiating. It should provide a list of
supported mappings we just add a struct that holds the `amdgpu_dma_buf_map_phys`

and `amdgpu_dma_buf_unmap_phys`

functions.

```
static int amdgpu_dma_buf_match_mapping(struct dma_buf_match_args *args) {
...
if (peer2peer) {
match[num_match++] = DMA_BUF_EMAPPING_PAL(&amdgpu_dma_buf_pal_ops);
}
...
}
```


This should be enough to map VRAM-backed buffers to an IOAS.

# Path 2: GPU -> NVMe BAR0

Here, we don’t need any changes on the AMDGPU driver side 5. The heavy lifting is being done by the patches
that allows exporting NVMe BAR0 as a DMA-BUF, allowing us to map it directly to the GPU VM which makes the BAR0
visible to the GPU.

Something worth mentioning here, is that if use the HIP API to import the DMA-BUF aka use
`hipMemImportFromShareableHandle`

function it assumes the imported buffer is being exported by another AMD GPU.
Thankfully HSA EXT API does have `hsa_amd_interop_map_buffer`

which its implementation much simpler and direct. A
small problem with `hsa_amd_interop_map_buffer`

that internally it calls the IOCTL `AMDKFD_IOC_GET_DMABUF_INFO`

,
which would error if the DMA-BUF is not exported by AMDGPU driver itself. I modified the function that handles
the ioctl to return a dummy info, I believe this should be fixed at the HSA level, but this would do for now.

```
int amdgpu_amdkfd_get_dmabuf_info(...)
{
...
if (dma_buf->ops != &amdgpu_dmabuf_ops) {
if (dmabuf_adev)
*dmabuf_adev = adev;
if (bo_size)
*bo_size = dma_buf->size;
if (metadata_size)
*metadata_size = 0;
if (flags)
*flags = KFD_IOC_ALLOC_MEM_FLAGS_GTT |
KFD_IOC_ALLOC_MEM_FLAGS_UNCACHED |
KFD_IOC_ALLOC_MEM_FLAGS_WRITABLE;
if (xcp_id)
*xcp_id = -1;
r = 0;
goto out_put;
}
...
}
```


Now this should be enough for the most basic P2P communication.

# The User-Space Perspective

Let’s make a simple prove of concept to assert that our plumbing here worked. A simple driver that rings the admin queues doorbell from a shader(kernel), and should use the VRAM as the location of the command result. The rest will be done from the CPU to make it simple for now.

The next part assumes that we have an NVMe device that is being managed by the VFIO driver. `lspci`

command output
should look like this:

```
lspci -k -nn -s 0000:04:00.0
04:00.0 Non-Volatile memory controller [0108]: Samsung Electronics Co Ltd NVMe SSD Controller SM981/PM981/PM983 [144d:a808]
Subsystem: Samsung Electronics Co Ltd SSD 970 EVO/PRO [144d:a801]
Kernel driver in use: vfio-pci # notice here
Kernel modules: nvme
```


We can start by opening the IOMMUFD which will allow us to allocate an IOAS

```
s32 iommu_fd = open("/dev/iommu", O_RDWR);
struct iommu_ioas_alloc iommu_alloc_request = { ... };
ioctl(iommu_fd, IOMMU_IOAS_ALLOC, &iommu_alloc_request);
```


Then we can open the VFIO char device and associate it with our IOAS

```
s32 vfio_fd = open("/dev/vfio/devices/vfio0", O_RDWR);
struct vfio_device_bind_iommufd vfio_bind_request = { ... };
ioctl(vfio_fd, VFIO_DEVICE_BIND_IOMMUFD, &vfio_bind_request);
struct vfio_device_attach_iommufd_pt vfio_attach_request = { ... };
ioctl(vfio_fd, VFIO_DEVICE_ATTACH_IOMMUFD_PT, &vfio_attach_request);
```


By now we have control over our nvme device, we can query info about PCIe regions, etc. We care about exporting NVMe BAR0 we can make use of the features added by patches I mentioned earlier, as we can see here:

```
pci_feature_req->argsz = pci_feature_req_size;
pci_feature_req->flags =
VFIO_DEVICE_FEATURE_GET | VFIO_DEVICE_FEATURE_DMA_BUF;
pci_feature_req_dma->region_index = 0;
pci_feature_req_dma->open_flags = O_RDWR | O_CLOEXEC;
pci_feature_req_dma->nr_ranges = 1;
pci_feature_req_dma->dma_ranges[0].offset = 0;
pci_feature_req_dma->dma_ranges[0].length = vfio_bar0_region_info.size;
s32 bar0_dmabuf_fd =
ioctl(vfio_device_file_descriptor, VFIO_DEVICE_FEATURE, pci_feature_req);
```


At this point `bar0_dmabuf_fd`

refers to the NVMe BAR0 we can map that using the function
`hsa_amd_interop_map_buffer`

I mentioned earlier.

Now let’s allocate some buffer on the VRAM and export them, thankfully the HIP API makes this simple.

```
hipMemAllocationProp props = { ... };
hipMemGenericAllocationHandle_t alloc_handle;
hipMemCreate(&alloc_handle, dma_buffer_size, &props, 0);
void *gpu_va;
hipMemAddressReserve(&gpu_va, dma_buffer_size, 4096, NULL, 0);
hipMemMap(gpu_va, dma_buffer_size, 0, alloc_handle, 0);
hipMemAccessDesc access = { ... };
hipMemSetAccess(gpu_va, dma_buffer_size, &access, 1);
int result_dmabuf_fd;
hipMemExportToShareableHandle(&result_dmabuf_fd, alloc_handle,
hipMemHandleTypePosixFileDescriptor, 0);
```


At this point `result_dmabuf_fd`

refers to the buffer we allocated for the NVMe to store the result of Identify
command into, and we can map it into our IOAS using `IOMMU_IOAS_MAP_FILE`

IOCTL.

Here we should map the NVMe BAR0 to the CPU side too and set up the NVMe controller and admin queues I won’t
include those here but you can see the full source code of this proof of concept
[here](https://codeberg.org/a_hadi/nvme_gpu_p2p_amdgpu/src/branch/master/standalone-basic).

After we set up admin queues and we can write an Identify command that uses the VRAM for the result as follows:

```
nvme_sqe_t identify_cmd = {
.opc = 0x06, // Identify command opcode
.cid = 1,
.prp1 = result_iova, // we got this from the IOMMU_IOAS_MAP_FILE ioctl
.cdw10 = 1,
};
admin_submission_queue[0] = identify_cmd;
```


Now everything is ready to run the GPU shaders and ring the doorbell, the shader is very simple just writes 1 to the doorbell register

```
__global__ void ring_doorbell_kernel(volatile u32* queue_doorbell) {
*queue_doorbell = 1;
}
```


From the CPU side, we just poll the admin CQ and once it’s done, we can copy back the data from the GPU VRAM and we see:

```
NVMe Identfication Info:
Vendor ID: 0x144d
Subsystem Vendor ID: 0x144d
Serial Number: S5H7NS0N845653J
Model Number: Samsung SSD 970 EVO 500GB
Firmware Revision: 2B2QEXE7
```


It works! Now let’s do data transfers and enqueue and do the polling from the GPU side.

# GPU Driven I/O

At this point, I did not want to write a user-space NVMe driver from scratch just to validate the kernel plumbing.
I already had a much better starting point [libnvm](https://github.com/enfiskutensykkel/ssd-gpu-dma), Jonas
Markussen’s user-space NVMe library, which was built around the same general idea of low-level queue control and
GPU-driven I/O.

I won’t talk much about the porting process since we already talked about the interesting parts if you’re curious
take a look at the port and some examples [here](https://codeberg.org/a_hadi/nvme_gpu_p2p_amdgpu).

Now with the port in place, let’s take a look at an example shader that writes or reads a file from the NVMe
device. Again there’s a lot of boilerplate code I won’t show here but can see it and run it for yourself
[here](https://codeberg.org/a_hadi/nvme_gpu_p2p_amdgpu/src/branch/master/examples).

In this shader, each GPU thread owns one queue pair, takes responsibility for one slice of the transfer, submits NVMe read or write commands through its own submission queue, and then drains completions from the respective completion queue.

The first thing the kernel does is assign one queue pair per GPU thread. That keeps the control flow simple.

```
uint32_t tid = blockIdx.x * blockDim.x + threadIdx.x;
if (tid >= n_queues) return;
nvm_queue_t* sq = sqs + tid;
nvm_queue_t* cq = cqs + tid;
```


Now we can construct our read or write commands, libnvm handles that nicely for us the thing to notice here is
we are using address directly which was made possible by the plumbing work we did earlier. The NVMe can DMA
directly into `sq->vaddr`

which holds the VRAM memory for the SQ, and `sq->ioaddr`

is the IOVA of that same
memory.

```
nvm_cmd_header(cmd, cid, write ? NVM_IO_WRITE : NVM_IO_READ, ns_id);
size_t global_page = thread_base_page + page_offset;
size_t start_block = NVM_PAGE_TO_BLOCK(page_size, block_size, global_page);
size_t n_blocks = NVM_PAGE_TO_BLOCK(page_size, block_size, xfer_pages);
nvm_cmd_rw_blks(cmd, start_block, n_blocks);
nvm_cmd_data(
cmd, page_size, xfer_pages,
NVM_PTR_OFFSET(sq->vaddr, page_size, prp_slot),
NVM_ADDR_OFFSET(sq->ioaddr, page_size, prp_slot),
data_ioaddrs + global_page
);
```


Now the thread can submit the work and drain the CQ, this is easy because libnvm is built around polling rather
than interrupts. The next code will show the 2 paths we paved earlier in action. `nvm_sq_submit`

will ring the
NVMe doorbell(GPU -> NVMe), and the NVMe will write back to the CQ which lives in GPU VRAM.

```
nvm_sq_submit(sq);
while (cmds_completed < cmds_submitted) {
nvm_cpl_t* cpl = nvm_cq_dequeue(cq);
if (cpl == NULL)
continue;
if (!NVM_ERR_OK(cpl)) {
printf("NVMe completion error ...\n");
return;
}
nvm_sq_update(sq);
nvm_cq_update(cq);
cmds_completed++;
}
```


Running this, and it doesn’t work it gets stuck in CQ polling

# Cache Coherency

The first path is the tricky one, so let’s start with the second path GPU -> NVMe. Here we have to just make sure
we skip L2 and MALL cache. From [the debugger experiments](https://thegeeko.me/blog/amd-gpu-debugging/), we know
if we set the mapping type(MTYPE) to uncached(UC) the RDNA3 GPUs skip it. So we make sure our SQs are allocated
with uncached flag.

```
hsa_err = hsa_amd_memory_pool_allocate(
vram_pool, size, HSA_AMD_MEMORY_POOL_UNCACHED_FLAG, &ptr
);
```


This is probably overkill and we can do a `__threadfence_system()`

before ringing the doorbell, but allocating
both SQs and CQs the same way makes the code simpler so I’m ignoring this for now. It’s also worth mentioning
when we export the buffer as PAL we do add uncached flag but it wasn’t reliable in my experience 6.

Now for the other side NVMe -> VRAM, when the NVMe controller is done it writes back to CQs and it DMA directly using the physical address. We need to make sure that there’s no inbound PCIe traffic buffering, and all our GPU reads skip all possible caches.

For the later part the combination of `MTYPE=UC`

and `glc slc dlc`

modifers on the load instruction should suffice
as you can see here:

```
__host__ __device__ static inline nvm_cpl_t*
nvm_cq_poll(const nvm_queue_t* cq) {
...
#ifdef __HIP_DEVICE_COMPILE__
asm volatile(
"global_load_u16 %0, %1, off glc slc dlc\n\t"
"s_waitcnt vmcnt(0)"
: "=v"(raw)
: "v"(status_addr)
: "memory"
);
...
}
```


Now by just running this it still reads stale data, not the NVMe CQ entries.

**This was tough to debug, and I learned from it, but take the next part with a grain of salt, it may contain wrong information if you saw any please contact me, I’ll fix, and I want to know ;).**

So I had no idea how to approach this, but I noticed when I open anything that uses the AMD GPU for
rendering 7 it works but it was a bit random it always worked but not at set intervals. I minimized the
surface and switched to raw PM4 packets submissions and tracked down to a couple of things.

I found something called HDP(Host Data Path) cache, but in the [amdgpu_discovery.c](https://codeberg.org/a_hadi/linux_p2p_dma_amdgpu/src/commit/8ab25043a85358758c771259ab298ee3d2ddd4af/drivers/gpu/drm/amd/amdgpu/amdgpu_discovery.c#L2965) file there’s no mention for GFX11(RX 7900XTX) and HDP together, but I looked into the `nbio_v7_7.c`

version, and found this:

```
static u32 nbio_v7_7_get_hdp_flush_req_offset(struct amdgpu_device *adev)
{
return SOC15_REG_OFFSET(NBIO, 0, regBIF_BX_PF0_GPU_HDP_FLUSH_REQ);
}
```


Using UMR to poke around the `BIF_BX_PF<X>_GPU_HDP_FLUSH_REQ`

didn’t do anything, and the shader was stuck
polling still.

Next up I tracked a couple of paths and found `GCR_GENERAL_CNTL`

, `GCVM_L2_CNTL2`

and
`GCVM_INVALIDATE_ENG<X>_REQ`

registers, playing with the first two triggered a GPU reset, but the last one did
the trick and made the CQs entries visible to the GPU.

There’s multiple `GCVM_INVALIDATE_ENG<X>_REQ`

registers 0-17, and the structure of the register is:

```
typedef union {
struct {
uint32_t per_vmid_invalidate_req : 16;
uint32_t flush_type : 3;
uint32_t invalidate_l2_ptes : 1;
uint32_t invalidate_l2_pde0 : 1;
uint32_t invalidate_l2_pde1 : 1;
uint32_t invalidate_l2_pde2 : 1;
uint32_t invalidate_l1_ptes : 1;
uint32_t clear_protection_fault_status_addr : 1;
uint32_t log_request : 1;
uint32_t invalidate_4k_pages_only : 1;
};
uint32_t raw;
} reg_gcvm_invalidate_eng17_req_t;
```


Turned out that only `eng17`

register, `flush_type = 2`

, and a nonzero `per_vmid_invalidate_req`

work. The
`per_vmid_invalidate_req`

is a mask with each bit corresponding to a VMID 8, and it feels like an early return
check if it has no VMID bit enabled. The

`flush_type`

is the interesting part here on `flush_type = 2`

from
[this patch](https://lists.freedesktop.org/archives/amd-gfx/2025-February/120529.html)we can know it stands for heavy-weight flush.

And from [here](https://codeberg.org/a_hadi/linux_p2p_dma_amdgpu/src/commit/8ab25043a85358758c771259ab298ee3d2ddd4af/drivers/gpu/drm/amd/amdgpu/amdgpu_gmc.c#L577) we know ENG17 is allocated for GART flushes. The kernel documentation
define GART as:

Graphics Address Remapping Table. This is the name we use for the GPUVM page table used by the GPU kernel driver. It remaps system resources (memory or MMIO space) into the GPU’s address space so the GPU can access them. The name GART harkens back to the days of AGP when the platform provided an MMU that the GPU could use to get a contiguous view of scattered pages for DMA. The MMU has since moved on to the GPU, but the name stuck.


This whole thing didn’t make sense to me. `GCVM_INVALIDATE_ENG<X>_REQ`

seems to be used to flush TLB, and this
shouldn’t affect the data visibility if we already have the correct address mapped. I verified using UMR page
decoding before and after the flush it was the exact same, and the page tables are per VMID, and toggling any of
the VMID bits works not the one specific to our PSID.

What I think is going here is this is an unintended side effect of a heavy-weight flush which is unlikely, or
this GART have an internal buffering or cache that is not exposed to the KMD. It’s also worth mentioning that
`GCVM_INVALIDATE_ENG<X>_REQ`

are a `gfxhub`

registers and there’s another `MMVM_INVALIDATE_ENG<X>_REQ`

group of
registers which are a `mmhub`

registers but those don’t have the same effect as the `gfxhub`

ones, so maybe
it’s something inside the `gfxhub`

. We can’t truly know without knowing how those parts of the hardware work.

I made a simple program that uses debugfs interface to keep poking the register and invalidate the cache it assumes GFX11 tho. If you want to run the code on another GPU use UMR to poke it manually.

With those things in place the examples work correctly, writing a file and then reading it back result in the same file.

# You can run them yourself

**Hi again, if you liked what you read I’m graduating at the end of this month. Consider hiring me or referring me:**

[Linkedin](https://linkedin.com/in/thegeeko)[Resume](https://thegeeko.me/resume.pdf)- Email me at:
[[email protected]](https://thegeeko.me/cdn-cgi/l/email-protection#b0d1d2d4d5dcd8d1d4d9ddc3f0d9d3dcdfc5d49ed3dfdd)

## Footnotes

-
It got updated by the time I published this post you can find a copy of V1

[here](https://codeberg.org/a_hadi/linux_p2p_dma_amdgpu/commit/2cec044416a08d09da27f368b3f6f6b46ee7629e).[↩](https://thegeeko.me#user-content-fnref-1) -
Later we will use I/O queues to write a file and read back using

[libnvm](https://github.com/enfiskutensykkel/ssd-gpu-dma)by Jonas Markussen.[↩](https://thegeeko.me#user-content-fnref-2) -
The patches thread expands on this.

[↩](https://thegeeko.me#user-content-fnref-4) -
At least in my setup.

[↩](https://thegeeko.me#user-content-fnref-5) -
We can check the actual MTYPE value at the end by decoding the page table using UMR.

[↩](https://thegeeko.me#user-content-fnref-6) -
I use an Nvidia GPU for display so the AMD GPU stays idle unless I force some workload to use it.

[↩](https://thegeeko.me#user-content-fnref-7)