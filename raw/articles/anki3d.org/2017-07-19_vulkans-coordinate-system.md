---
title: Vulkan’s coordinate system
url: https://anki3d.org/vulkan-coordinate-system/
author: Panagiotis Christopoulos Charitos
published: '2017-07-19'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

One of the key differences between OpenGL and Vulkan -and something that needs careful consideration when porting to Vulkan- is the coordinate system. Khronos’ Vulkan working group decided not to use GL’s commonly used coordinate conventions in favor of something more widely used and accurate and that’s the main reason behind this shift.


The first thing to note is that Vulkan requires the right hand **NDC space** compared to GL that requires the left hand. In other words the (-1, -1) NDC coordinate maps to the top left corner for Vulkan and to the bottom left corner for GL. In practice, if a Vulkan application ignored this convention the final output will end up flipped in the Y axis and inside out. Khronos group understood that this difference is not easy to workaround that’s why they tried to fix it as part of **KHR_VK_maintainance1** extension. What KHR_VK_maintainance1 basically does is to allow a negative height in VkViewport structure. In practice this allows us to flip the viewport in the Y axis during the viewport transform.

How AnKi is flipping the viewport is a bit weird and I’m not sure if it’s the best way to go.

- The first thing that needs to happen is to enable KHR_VK_maintainance1 extension when creating the device.
- When drawing to offscreen framebuffers the
**VkPipelineRasterizationStateCreateInfo::frontFace**is the opposite of what it supposed to be. The result is rendered to the offscreen framebuffers flipped. - The final piece of the puzzle is what happens when drawing into the swapchain images (a.k.a. default framebuffer). Unlike offscreen rendering the VkPipelineRasterizationStateCreateInfo::frontFace is not changed but the viewport’s height gets negated and that will cause a flip.

The logical question here is why do we need the second step? Why not flip the viewport at all times and for all types of render passes? Vulkan not only expects a right hand NDC space but it also requires gl_FragCoord’s origin to be at the top left corner as well. gl_FragCoord’s origin is configurable in GL but SPIR-V doesn’t allow us to move it to the bottom left corner. The SPIR-V specification has some wording in place for a bottom left origin but at the moment it’s an error to use it. The fact that offscreen render passes are logically flipped helps us to workaround this limitation.

This is the code that changes the frontFace (in AnKi the frontFace is not configurable and it’s always CCW):

VkPipelineRasterizationStateCreateInfo rastCi; rastCi.frontFace = (!m_defaultFb) ? VK_FRONT_FACE_CLOCKWISE : VK_FRONT_FACE_COUNTER_CLOCKWISE;

And this is the code that flips the viewport:

const Bool flipvp = m_defaultFb; const int minx = m_viewport[0]; const int miny = m_viewport[1]; const int maxx = m_viewport[2]; const int maxy = m_viewport[3]; unsigned fbWidth, fbHeight; getBoundFramebufferAttachmentsSize(fbWidth, fbHeight); VkViewport s; s.x = minx; s.y = (flipvp) ? (fbHeight - miny) : miny; // Move to the bottom; s.width = maxx - minx; s.height = (flipvp) ? -(maxy - miny) : (maxy - miny); s.minDepth = 0.0; s.maxDepth = 1.0; vkCmdSetViewport(m_handle, 0, 1, &s);

The **next difference** between the two APIs is the range or Z in NDC space (a.k.a. Zd). In GL, by using a typical GL projection matrix Zd ends up in [-1, 1] after the perspective division just like X and Y. The viewport transform for the Z component is given by this equation:

((f-n)/2)*Zd + (n+f)/2

The f and n are the far and near limits and they are typically 0.0 and 1.0 respectively. So the equation above gives a new range in [0, 1] and that’s the depth value that will be used for depth testing and will be stored in the depth buffer. The fact that GL expects Zd in [-1, 1] gives some kind of consistency since all 3 components (X, Y and Z) end up in the same range.

One interesting property of floating point numbers (in the [0.0, 1.0] range) is that they have better precision closer to 0.0. This property has an interesting impact in the accuracy of the depth buffer. For GL’s range it practically gives OK accuracy close to the near plane (Zd==-1) the best quality somewhere close to the camera (Zd==0.0) and worse close to the far plane (Zd==1). Direct3D is using another convention where it expects Zd in [0.0, 1.0] for optimal depth accuracy. Vulkan went the same road.

In Vulkan, the viewport transform for the Z component is given by this equation instead:

(maxDepth-minDepth)*Zd + minDepth

maxDepth is typically 1.0 and minDepth 0.0. If Zd is mapped in [0, 1] then depth will be in [0, 1] as well.

It’s worth noting that GL 4.5 supports Vulkan’s convention through **GL_ARB_clip_control** extension. To switch to the new system you can call **glClipControl(XXX, GL_ZERO_TO_ONE)** to move from GL’s default GL_NEGATIVE_ONE_TO_ONE to Vulkan’s GL_ZERO_TO_ONE.

Having a common system for Zd for both GL and Vulkan is a bit tricky but there are two solutions. The first is to use GL’s convention for both APIs and append this at the end of every Vulkan vertex shader:

gl_Position.z = (gl_Position.z + gl_Position.w) / 2.0;

Without going into much detail the above code re-maps the Zd to what Vulkan expects.

The second solution is to **use Vulkan’s convention** and use GL_ARB_clip_control extension to move GL to what Vulkan prefers. This sounds like a better solution because it allows for a better depth buffer accuracy and no extra overhead in the vertex shader. Unfortunately it requires a big code refactoring to move from one coordinate system to another. It’s also worth noting that GL_ARB_clip_control is not part of OpenGL ES and that limits this solution to desktop GL only.

Initially, AnKi was using the vertex shader trick but eventually I decided to use the second solution. That required a few careful changes but overall everything worked just fine. For AnKi these changes were:

- Alter all the projection matrices to map Zd to the new range. In AnKi there are a few functions that generate projection matrices so this change was easy enough.
- Change the shader code that unprojects depth to view space Z. In AnKi there are quite a few places that do that but overall no issues. The shader code became a bit simpler as well.
- Align the software rasterizer to the new system as well. No big issues there as well.

Overall the current way of handling GL and Vulkan’s coordinates in the same codebase works quite well for AnKi without any major issues at the moment. If you found yourself in a similar situation and you want to share your thoughts don’t hesitate to drop a comment bellow.

Greetings,

can you explain me again why you treat offscreen targets differently with viewport and front face? I’m not aware that offscreen render targets had different coordinate systems from swap chain images.

Regards.

KHR_VK_maintainance1 should be VK_KHR_maintainance

KHR_VK_maintainance1 should be VK_KHR_maintainance1