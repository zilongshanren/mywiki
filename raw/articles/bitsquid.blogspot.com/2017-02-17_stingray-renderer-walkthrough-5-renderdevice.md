---
title: 'Stingray Renderer Walkthrough #5: RenderDevice'
url: https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-5.html
author: Tobias
published: '2017-02-17'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

The `RenderDevice`

is essentially our abstraction layer for platform specific rendering APIs. It is implemented as an abstract base class that various rendering back-ends (D3D11, D3D12, OGL, Metal, GNM, etc.) implement.

The `RenderDevice`

has a bunch of helper functions for initializing/shutting down the graphics APIs, creating/destroying swap chains, etc. All of which are fairly straightforward so I won’t cover them in this post, instead I will put my focus on the two `dispatch`

functions consuming `RenderResourceContexts`

and `RenderContexts`

:

```
class RenderDevice {
public:
virtual void dispatch(uint32_t n_contexts, RenderResourceContext **rrc,
uint32_t gpu_affinity_mask = RenderContext::GPU_DEFAULT) = 0;
virtual void dispatch(uint32_t n_contexts, RenderContext **rc,
uint32_t gpu_affinity_mask = RenderContext::GPU_DEFAULT) = 0;
};
```


As covered in the post about [ RenderResourceContexts](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-2.html), they provide a free-threaded interface for allocating and deallocating GPU resources. However, it is not until the user has called

`RenderDevice::dispatch()`

handing over the `RenderResourceContexts`

as their representation gets created on the `RenderDevice`

side.All implementations of a `RenderDevice`

have some form of resource management that deals with creating, updating and destroying of the graphics API specific representations of resources. Typically we track the state of all various types of resources in a single struct, here’s a stripped down example from the DX12 `RenderDevice`

implementation called `D3D12ResourceContext`

:

```
struct D3D12VertexBuffer
{
D3D12_VERTEX_BUFFER_VIEW view;
uint32_t allocation_index;
int32_t size;
};
struct D3D12IndexBuffer
{
D3D12_INDEX_BUFFER_VIEW view;
uint32_t allocation_index;
int32_t size;
};
struct D3D12ResourceContext
{
Array<D3D12VertexBuffer> vertex_buffers;
Array<uint32_t> unused_vertex_buffers;
Array<D3D12IndexBuffer> index_buffers;
Array<uint32_t> unused_index_buffers;
// .. lots of other resources
Array<uint32_t> resource_lut;
};
```


As you might [remember](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-2.html), the linking between the engine representation and the `RenderDevice`

representation is done using the `RenderResource::render_resource_handle`

. It encodes both the type of the resource as well as a handle. The `resource_lut`

is an indirection to go from the engine handle to a local index for a specific type (e.g `vertex_buffers`

or `index_buffers`

in the sample above). We also track freed indices for each type (e.g. `unused_vertex_buffers`

) to simplify recycling of slots.

The implementation of the dispatch function is fairly straight forward. We simply iterate over all the `RenderResourceContexts`

and for each context iterate over its commands and either allocate or deallocate resources in the `D3D12ResourceContext`

. It is important to note that this is a synchronous operation, nothing else is peeking or poking on the `D3D12ResourceContext`

when the dispatch of `RenderResourceContexts`

is happening, which makes our life a lot easier.

Unfortunately that isn’t the case when we dispatch `RenderContexts`

as in that case we want to go wide (i.e. forking the workload and process it using multiple worker threads) when translating the commands into API calls. While we don’t allow allocating and deallocating new resources from the `RenderContexts`

we do allow updating them which mutates the state of the `RenderDevice`

representations (e.g. a `D3D12VertexBuffer`

).

At the moment our solution for this isn’t very nice, basically we don’t allow asynchronous updates for anything else than `DYNAMIC`

buffers. `UPDATABLE`

buffers are always updated serially before we kick the worker threads no matter what their sort_key is. All worker threads access resources through their own copy of something we call a `ResourceAccessor`

, it is responsible for tracking the worker threads state of dynamic buffers (among other things). In the future I think we probably should generalize this and treat `UPDATABLE`

buffers in a similar way.

(Note: this limitation doesn’t mean you can’t update an `UPDATABLE`

buffer more than once per frame, it simply means you cannot update it more than once per `dispatch`

).

Resources in the `D3D12ResourceContext`

are typically buffers. One exception that stands out is the `RenderDevice`

representation of a “shader”. A “shader” on the `RenderDevice`

side maps to a `ShaderTemplate::Context`

on the engine side, or what I guess we could call a multi-pass shader. Here’s some pseudo code:

```
struct ShaderPass
{
struct ShaderProgram
{
Array<uint8_t> bytecode;
struct ConstantBufferBindInfo;
struct ResourceBindInfo;
struct SamplerBindInfo;
};
ShaderProgram vertex_shader;
ShaderProgram domain_shader;
ShaderProgram hull_shader;
ShaderProgram geometry_shader;
ShaderProgram pixel_shader;
ShaderProgram compute_shader;
struct RenderStates;
};
struct Shader
{
Vector<ShaderPass> passes;
enum SortMode { IMMADIATE, DEFERRED };
uint32_t sort_mode;
};
```


The pseudo code above is essentially the `RenderDevice`

representation of a shader that we serialize to disk during data compilation. From that we can create all the necessary graphics API specific objects expressing an executable shader together with its various state blocks (Rasterizer, Depth Stencil, Blend, etc.).

As discussed in the last [post](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-4-sorting.html) the `sort_key`

encodes the shader pass index. Using `Shader::sort_mode`

, we know which bit range to extract from the `sort_key`

as pass index, which we then use to look up the `ShaderPass`

from `Shader::passes`

. A `ShaderPass`

contains one `ShaderProgram`

per active shader stage and each `ShaderProgram`

contains the byte code for the shader to compile as well as “bind info” for various resources that the shader wants as input.

We will look at this in a bit more detail in the post about “Shaders & Materials”, for now I just wanted to familiarize you with the concept.

Let’s move on and look at the dispatch for translating `RenderContexts`

into graphics API calls:

```
class RenderDevice {
public:
virtual void dispatch(uint32_t n_contexts, RenderContext **rc,
uint32_t gpu_affinity_mask = RenderContext::GPU_DEFAULT) = 0;
};
```


The first thing all `RenderDevice`

implementation do when receiving a bunch of `RenderContexts`

is to merge and sort their `Commands`

. All implementations share the same code for doing this:

```
void prepare_command_list(RenderContext::Commands &output, unsigned n_contexts, RenderContext **contexts);
```


This function basically just takes the `RenderContext::Commands`

from all `RenderContexts`

and merges them into a new array, runs a stable radix sort, and returns the sorted commands in `output`

. To avoid memory allocations the `RenderDevice`

implementation owns the memory of the output buffer.

Now we have all the commands nicely sorted based on their `sort_key`

. Next step is to do the actual translation of the data referenced by the commands into graphics API calls. I will explain this process with the assumption that we are running on a graphics API that allows us to build graphics API command lists in parallel (e.g. DX12, GNM, Vulkan, Metal), as that feels most relevant in 2017.

Before we start figuring out our per thread workloads for going wide, we have one more thing to do; “instance merging”.

I’ve mentioned the idea behind instance merging before [[1](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-3-render.html),[2](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-4-sorting.html)], basically we want to try to reduce the number of `RenderJobPackages`

(i.e. draw calls) by identifying packages that are similar enough to be merged. In Stingray “similar enough” basically means that they must have identical inputs to the input assembler as well as identical resources bound to all shader stages, the only thing that is allowed to differ are constant buffer variables. (Note: by todays standards this can be considered a bit old school, new graphics APIs and hardware allows to tackle this problem more aggressively using “bindless” concepts. )

The way it works is by filtering out ranges of `RenderContexts::Commands`

where the “instance bit” of the `sort_key`

is set and all bits above the instance bit are identical. Then for each of those ranges we fork and go wide to analyze the actual `RenderJobPackage`

data to see if the `instance_hash`

and the shader are the same, and if so we know its safe to merge them.

The actual merge is done by extracting the instance specific constants (these are tagged by the shader author) from the constant buffers and propagating them into a dynamic `RawBuffer`

that gets bound as input to the vertex shader.

Depending on how the scene is constructed, instance merging can significantly reduce the number of draw calls needed to render the final scene. The instance merger in itself is not graphics API specific and is isolated in its own system, it just happens to be the responsibility of the `RenderDevice`

to call it. The interface looks like this:

```
namespace instance_merger {
struct ProcessMergedCommandsResult
{
uint32_t n_instances;
uint32_t instanced_batches;
uint32_t instance_buffer_size;
};
ProcessMergedCommandsResult process_merged_commands(Merger &instance_merger,
RenderContext::Commands &merged_commands);
}
```


Pass in a reference to the sorted `RenderContext::Commands`

in `merged_commands`

and after the instance merger is done running you hopefully have fewer commands in the array. :)

You could argue that merging, sorting and instance merging should all happen before we enter the world of the `RenderDevice`

. I wouldn’t argue against that.

Last step before we can start translating our commands into state / draw / dispatch calls is to split the workload into reasonable chunks and prepare the execution contexts for our worker threads.

Typically we just divide the number of `RenderContext::Commands`

we have to process with the number of worker threads we have available. We don’t care about the type of different commands we will be processing and trying to load balance differently. The reasoning behind this is that we anticipate that draw calls will always represent the bulk of the commands and the rest of the commands can be considered as unavoidable “noise”. We do, however, make sure that we don’t do less than *x*-number of commands per worker threads, where *x* can differ a bit depending on platform but is usually ~128.

For each execution context we create a `ResourceAccessors`

(described above) as well as make sure we have the correct state setup in terms of bound render targets and similar. To do this we are stuck with having to do a synchronous serial sweep over all the commands to find bigger state changing commands (such as `RenderContext::set_render_target`

).

This is where the `Command::command_flags`

bit-flag comes into play, instead of having to jump around in memory to figure out what type of command the `Command::head`

points to, we put some hinting about the type in the `Command::command_flags`

, like for example if it is a “state command”. This way the serial sweep doesn’t become very costly even when dealing with large number of commands. During this sweep we also deal with updating of `UPDATABLE`

resources, and on newer graphics APIs we track fences (discussed in the post about [Render Contexts](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-3-render.html)).

The last thing we do is to set up the execution contexts with create graphics API specific representations of command lists (e.g. `ID3D12GraphicsCommandList`

in DX12),

When getting to this point doing the actual translation is fairly straight forward. Within each worker thread we simply loop over its dedicated range of commands, fetch its data from `Command::head`

and generate any number of API specific commands necessary based on the type of command.

For a `RenderJobPackage`

representing a draw call it involves:

- Look up the correct shader pass and, unless already bound, bind all active shader stages
- Look up the state blocks (Rasterizer, Depth stencil, Blending, etc.) from the shader and bind them unless already bound
- Look up and bind the resources for each shader stage using the
`RenderResource::render_resource_handle`

translated through the`D3D12ResourceAccessor`

- Setup the input assembler by looping over the
`RenderResource::render_resource_handles`

pointed to by the`RenderJobPackage::resource_offset`

and translated through the`D3D12ResourceAccessor`

- Bind and potentially update constant buffers
- Issue the draw call

The execution contexts also holds most-recently-used caches to avoid unnecessary binds of resources/shaders/states etc.

Note: In DX12 we also track where resource barriers are needed during this stage. After all worker threads are done we might also end up having to inject further resource barriers between the command lists generated by the worker threads. We have ideas on how to improve on this by doing at least parts of this tracking when building the `RenderContexts`

but haven’t gotten around looking into it yet.

When the translation is done we pass the resulting command lists to the correct queues for execution.

Note: In DX12 this is a bit more complicated as we have to interleave signaling / waiting on fences between command list execution (`ExecuteCommandList`

).

I’ve deliberately not dived into too much details in this post to make it a bit easier to digest. I think I’ve manage to cover the overall design of a `RenderDevice`

though, enough to make it easier for people diving into the code for the first time.

With this post we’ve reached half-way through this series, we have covered the “low-level” aspects of the Stingray rendering architecture. As of next post we will start looking at more high-level stuff, starting with the `RenderInterface`

which is the main interface for other threads to talk with the renderer.

Very interesting series, thanks a lot!

ReplyDelete






ReplyDeleteIn love with this post.thankyou for the information.

Please do find the attached files and download it form our website.

http://acmarketap11993.yolasite.com/

https://happychickapk1960.weebly.com/

https://happychickapk.jimdofree.com/

http://site-1760435-9004-6622.strikingly.com/

https://acmarket541.jimdofree.com/

http://acmarket541.over-blog.com/2019/04/ac-market.html

https://sites.google.com/view/livenettvapk541/home

https://livenettvapk541.yolasite.com/

Top airlines in the world



ReplyDeleteAn airline is an organization that gives air transport administrations to voyaging travelers and cargo. Carriers use flying machine to supply these administrations, and may frame organizations or coalitions with different airlines for codeshare understandings. For the most part, airline organizations are perceived with an air working testament or permit issued by a legislative aeronautics body

Visit for more :-Qantas Airlines Phone Number

PosLaju parcel tracker of the Malaysia & World. Add tracking number to track your PosLaju packages as well as obtain delivery status online.

ReplyDeletehttps://poslajutracking.xyz/

poslaju tracking

poslaju track and trace

poslaju tracking number

poslaju tracking express

This is a great article, with lots of information in it, These types of articles interest users in your site. Please continue to share more interesting articles!


ReplyDeleteAmong, Infrastructure as a Service (IaaS), Software as a Service (SaaS), and Platform as a Service (PaaS), AWS chooses right kind of distributed computing and gives it to the business. AWS is known for adaptability with recognizable design, databases, operating systems, and programming dialects. It likewise guarantees security for the framework including physical, operational and programming measures. Thusly, in every one of the ways, AWS enables organizations to bring down their IT costs.


ReplyDeleteFor More Info:- AWS Institute in Gurgaon

Superb topic Resource Management you share.Thanks for taking the time to discuss this. I feel about it and love learning more on this topic. If possible, as you gain expertise, would you mind updating your blog with more information? It is extremely helpful for me.Get best Mobile App Development Dubai you visit here for more info.

ReplyDeleteHello! I think these information Will be helpful for you.


ReplyDeleteopenergroup.com

kopithecat25.wixsite.com/style1982

Thank you!

Such a great post you share with us, I really appreciate your work and content idea and I have found here lots of knowledgeable information this website perfect for my need. for More Information Please Visit: Outsource SEO Link Building Services

ReplyDeleteI am really appreciating very much by seeing your interesting posts.



ReplyDeleteHotschedules login employee hot schedule

Rasmussen student portal

Gmglobalconnect

Suggest good information in this message, click here.

ReplyDeleteไพ่ป๊อก เด้ง เล่น ยัง ไง

เซียนคาสิโน

what great info. It is truly amazing. I have not read this type of post to date. Thank you very much for sharing this information.

ReplyDeleteIs the print job being interrupted by Epson Error Code 0XF1? Do not waste outside. You can find a solution. In this report, we have provided a list of solutions for Epson Printer Error 0XF1. To remove this Epson 0XF1 printer error code, you may visit our website.

Some facts I agree to your points but some I don't. Yes, I want to appreciate your hardwork for sharing this information but at my part I have to research more. Though there are some interesting view angle I could find in your remark. Thanks for sharing.


ReplyDeletehire wordpress developer india

php developers

outsource digital marketing services

google 1867

ReplyDeletegoogle 1868

google 1869

google 1870

google 1871

This is the best article

ReplyDeleteitubego youtube download crack

wnsoft pte av studio

comodo internet Security license key

Water damage can be a homeowner’s worst nightmare. Not only is your home rendered unlivable for the foreseeable future, but you’ve got a massive

ReplyDeletewater damage cleanupand restoration process to deal with.I think this article is useful to everyone.

ReplyDeleteเว็บบาคาร่าที่คนเล่นเยอะที่สุด

สูตรยี่กีรวย

สล็อตโรม่า

The Original Forex Trading System: tradeatf Is The Original Forex Trading System. It Is 100% Automated And Provides An Easy-to-follow Trading System. You Get Access To Real-time Signals, Proven Methods, And A Money-back Guarantee.


ReplyDeleteDaebak!! this was an extremely good post. Taking the time and actual effort to produce a top notch article… But what can I say… Just check my website and see more 카지노사이트



ReplyDeleteGreat article, This post helps me a lot Thank you. Anyways I have this site recommendation for you, Just follow the given link here:



ReplyDelete스포츠토토

토토

안전놀이터

토토사이트

Thanks for your post! Through your pen I found the problem up interesting! I believe there are many other people who are interested in them just like me! How long does it take to complete this article? I have read through other blogs, but they are cumbersome and confusing.




ReplyDeletehappy wheels

토토사이트

메이저사이트 목록

I have read your blog and I gathered some new information through your blog. Thanks for sharing the information


ReplyDelete온라인카지노

카지노

It's perfect time to make a few plans for the future and it is time to be happy. I've learn this submit and if I may just I desire to recommend you some attention-grabbing things or advice. Maybe you could write subsequent articles referring to this article. I want to read even more issues approximately it!







ReplyDeleteAlso visit my web page :

카지노사이트추천

온라인카지노

Nice Blog. Thanks for sharing with us. Such amazing information.


ReplyDeleteWhy Dogs becomes so anxious about separating from their Master

AximTrade Review Offers A Safe And Secure Platform To Do Forex Trading And CFDs And Our Customer Support Is Ready To Help You 24/7. You Can Easily Sign Up Your Aximtrade Login Account Here.


ReplyDeleteThanks for sharing this amazing and nice post. Looking for the best dissertation help uk turnout to Assignments Planet for all dissertation services at a cheap price.

ReplyDeleteHello ! I am the one who writes posts on these topics크레이지슬롯 I would like to write an article based on your article. When can I ask for a review?




ReplyDeleteI accidentally searched and visited your site. I still saw several posts during my visit, but the text was neat and readable. I will quote this post and post it on my blog. Would you like to visit my blog later? keonha cai




ReplyDeleteI've learn a few excellent stuff here. Definitely value bookmarking




ReplyDeletefor revisiting. I wonder how so much effort you set to create

such a magnificent informative website. 토토사이트

I've been troubled for several days with this topic. 메이저놀이터추천, But by chance looking at your post solved my problem! I will leave my blog, so when would you like to visit it?




ReplyDeleteWow, that’s what I was searching for, what a information! present here at this blog, thanks admin of this web page. 더킹카지노



ReplyDeleteI have read your article; it is very informative and helpful for me. I admire the valuable information you offer in your articles. Thanks for posting it. Feel free to visit my website; 카지노사이트위키



ReplyDeleteconsultar cita sepe


ReplyDeleteinem noia

cita previa inem belmonte

servempleo

cita previa sexpe llerena

I hope you're doing really well and enjoying the day ahead. We are a Forex Trading agency focusing on the Stock information Brokers Review And Login Details. Get Latest information On Uavs Stocktwits . Our goal is to provide you with comprehensive data and analysis on this stock in order to help you determine if it is a good fit for your portfolio.

ReplyDeleteThe Truff Stock Overview, keep track of all your favorite stocks in real time across multiple screens, tailored to only show information you need and see as it happens.


ReplyDeleteTrack your stocks in all major markets instantly with our unique live stock overview. See Ecdp stock live prices changes as they occur and view change details, including volume and share changes.


ReplyDeleteDbd Forums Real-Time Overview Of A Stock, Including Recent And Historical Price Charts, News, Events, Analyst Rating Changes And Other Key Stock Information.


ReplyDeleteI think these must be useful to you.

ReplyDeleteวิธีเล่นไพ่ป๊อกเด้ง ให้ได้เงิน

CHIN SHI HUANG รีวิวเกมสล็อตออนไลน์

OCTAGON GEM 2 รีวิวเกมสล็อตออนไลน์

สูตรน้ำแตงโมปั่น

สูตรน้ำพันซ์แอปเปิลพาย

Thank you for your interest.

The best top 1 casino website

ReplyDeleteเว็บคาสิโน ไม่ผ่านเอเยนต์

I think these must be useful to you.

ReplyDeleteซื้อหวยฮานอย ออนไลน์

Thank you for your interest.

This is a great article and great read for me. It's my first visit to your blog, and I have found it so useful and informative especially this article


ReplyDeleteYellowstone Dutton Ranch Merch

Our list of the Best MT5 Forex Brokers In Malaysia is compiled solely of trusted, regulated and reputable forex brokers. We have selected well-known brokers that offer great customer service, low fees, an easy-to-use online platform, and education for new investors.


ReplyDeleteAfter receiving your Payday Loans 400 dollars money, you can spend it for any needs without limits. On the due date, the lender will withdraw the initial payday loan for unemployment benefits amount plus fees from your bank account.

ReplyDeleteExpresses gratitude and acknowledges the value of the blog post.

ReplyDelete


ReplyDeletePlayground surfacing plays a crucial role in ensuring the safety of children while they engage in play activities. Its main purpose is to absorb impact and minimize injuries, acting as a protective cushion beneath swings, slides, and climbing structures. There are several common materials used for

Playground Surfacing, including rubber mulch, poured-in-place rubber, and engineered wood fiber. Rubber options are known for their durability and shock absorption properties, effectively reducing the risk of falls.Poured-in-place rubber offers a seamless and accessible surface that can be customized with various designs. On the other hand, engineered wood fiber, which is made from shredded wood, provides a natural aesthetic while still meeting safety standards. It is important to have proper playground surfacing in order to comply with safety regulations and create a secure environment where children can freely play, explore, and develop essential motor skills.

Efficient sorting in rendering engines plays a crucial role in performance, just like structured data management is essential in healthcare. In the same way, medical coding ensures accuracy in patient records and billing. For those in Delhi, quality medical coding courses can be a great way to step into this growing field!

ReplyDeleteMedical Coding Courses in Delhi

I have purchased from Ashirwad Minerals for several years, and they have never disappointed me. They certainly have a reputation as a trusted Soapstone Powder Manufacturer and the quality of their powder is a reflection of that. Their customer service is efficient and helpful.

ReplyDeleteI wished to present a Ganesh idol to a friend, and GajArts made it easy to buy online Ganesh murti Udaipur. The designs are tastefully done and full of religiosity, representing great craftsmanship. The idol that was delivered to me was delicately crafted and well delivered. I greatly admire the professionalism and quality that GajArts provides- truly worth it!

ReplyDeleteChoosing Vasundhara Micron as our mineral supplier proved to be a sound decision for our operations. The soapstone powder quality was consistent stable and suitable for our production needs. Their structured workflow and technical clarity reflected strong industry expertise. As a reputed Soapstone powder supplier in India Vasundhara Micron maintains high standards in both product delivery and professional conduct. We appreciate their reliability transparent communication and commitment to building lasting business relationships.

ReplyDeleteTripura Stonnes is a well established and trusted institute specializing in premium quality granite supply for various construction and architectural projects across India. My experience during my visit to their facility was highly positive as I personally observed their large inventory modern cutting process and strict quality inspection standards. While looking for a dependable Indian Granite Supplier in India offering high grade polished granite slabs for residential commercial infrastructure and export requirements I chose Tripura Stonnes for my project. The material quality is outstanding the finishing is flawless and their team maintained clear communication timely delivery and professional service throughout which made my overall experience completely satisfactory.


ReplyDelete