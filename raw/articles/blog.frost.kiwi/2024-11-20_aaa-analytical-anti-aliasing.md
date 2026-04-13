---
title: AAA - Analytical Anti-Aliasing
url: https://blog.frost.kiwi/analytical-anti-aliasing/
published: '2024-11-20'
source_blog: FrostKiwi's Secrets
source_site: https://blog.frost.kiwi
category: graphics
fetched: '2026-04-13'
---

Today’s journey is [Anti-Aliasing](https://en.wikipedia.org/wiki/Spatial_anti-aliasing) and the destination is **Analytical Anti-Aliasing**. Getting rid of rasterization [jaggies](https://en.wikipedia.org/wiki/Jaggies) is an art-form with decades upon decades of maths, creative techniques and non-stop innovation. With so many years of research and development, there are many flavors.

From the simple but resource intensive [ SSAA](https://en.wikipedia.org/wiki/Supersampling), over theory dense

[, to using machine learning with](https://www.iryoku.com/smaa/)

**SMAA**[. Same goal -](https://en.wikipedia.org/wiki/Deep_learning_anti-aliasing)

**DLAA****different approaches. We’ll take a look at how they work, before introducing a new way to look a the problem - the ✨**

*vastly**🌟 way. The perfect Anti-Aliasing exists and is simpler than you think.*

**analytical**Having[implemented]it multiple times over the years, I'll also share some juicy secrets I have never read anywhere before.

## The Setup [#](https://blog.frost.kiwi#the-setup)

To understand the Anti-Aliasing algorithms, we will implement them along the way! Following [WebGL canvases](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial/Getting_started_with_WebGL) draw a moving circle. Anti-Aliasing *cannot* be fully understood with just images, movement is *essential*. The red box has 4x zoom. Rendering is done at [native](https://en.wikipedia.org/wiki/1:1_pixel_mapping) resolution of your device, important to judge sharpness.

Please pixel-peep to judge sharpness and aliasing closely. Resolution of your screen too high to see aliasing? Lower the resolution with the following buttons, which will[integer-scale]the rendering.

## WebGL Vertex Shader

[circle.vs]`/* Our Vertex data for the Quad */ attribute vec2 vtx; attribute vec3 col; /* The coordinates that will be used to for our drawing operations */ varying vec2 uv; /* Color for the fragment shader */ varying vec3 color; /* Aspect ratio */ uniform float aspect_ratio; /* Position offset for the animation */ uniform vec2 offset; /* Size of the Unit Quad */ uniform float size; void main() { /* Assign the verticies to be used as the distance field for drawing. This will be linearly interpolated before going to the fragment shader */ uv = vtx; /* Sending some nice color to the fragment shader */ color = col; vec2 vertex = vtx; /* correct for aspect ratio */ vertex.x *= aspect_ratio; /* Shrink the Quad and thus the "canvas", that the circle is drawn on */ vertex *= size; /* Make the circle move in a circle, heh :] */ vertex += offset; /* Vertex Output */ gl_Position = vec4(vertex, 0.0, 1.0); }`

## WebGL Fragment Shader

[circle.fs]`precision mediump float; /* uv coordinates from the vertex shader */ varying vec2 uv; /* color from the vertex shader */ varying vec3 color; void main(void) { /* Clamped and scaled uv.y added to color simply to make the bottom of the circle white, so the contrast is high and you can see strong aliasing */ vec3 finalColor = color + clamp( - uv.y * 0.4, 0.0, 1.0); /* Discard fragments outside radius 1 from the center */ if (length(uv) < 1.0) gl_FragColor = vec4(finalColor, 1.0); else discard; }`

## WebGL Javascript

[circleSimple.js]`function setupSimple(canvasId, circleVtxSrc, circleFragSrc, simpleColorFragSrc, blitVtxSrc, blitFragSrc, redVtxSrc, redFragSrc, radioName, showQuadOpt) { /* Init */ const canvas = document.getElementById(canvasId); let circleDrawFramebuffer, frameTexture; let buffersInitialized = false; let showQuad = false; let resDiv = 1; const gl = canvas.getContext('webgl', { preserveDrawingBuffer: false, antialias: false, alpha: true, } ); /* Render Resolution */ const radios = document.querySelectorAll(`input[name="${radioName}"]`); radios.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { resDiv = event.target.value; stopRendering(); startRendering(); }); }); /* Show Quad instead of circle choise */ const showQuadOption = document.querySelectorAll(`input[name="${showQuadOpt}"]`); showQuadOption.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "false") radio.checked = true; radio.addEventListener('change', (event) => { showQuad = (event.target.value === "true"); stopRendering(); startRendering(); }); }); /* Shaders */ /* Circle Shader */ const circleShd = compileAndLinkShader(gl, circleVtxSrc, circleFragSrc); const aspect_ratioLocation = gl.getUniformLocation(circleShd, "aspect_ratio"); const offsetLocationCircle = gl.getUniformLocation(circleShd, "offset"); const sizeLocationCircle = gl.getUniformLocation(circleShd, "size"); /* SimpleColor Shader */ const simpleColorShd = compileAndLinkShader(gl, circleVtxSrc, simpleColorFragSrc); const aspect_ratioLocationSimple = gl.getUniformLocation(simpleColorShd, "aspect_ratio"); const offsetLocationCircleSimple = gl.getUniformLocation(simpleColorShd, "offset"); const sizeLocationCircleSimple = gl.getUniformLocation(simpleColorShd, "size"); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); /* Simple Red Box */ const redShd = compileAndLinkShader(gl, redVtxSrc, redFragSrc); const transformLocationRed = gl.getUniformLocation(redShd, "transform"); const offsetLocationRed = gl.getUniformLocation(redShd, "offset"); const aspect_ratioLocationRed = gl.getUniformLocation(redShd, "aspect_ratio"); const thicknessLocation = gl.getUniformLocation(redShd, "thickness"); const pixelsizeLocation = gl.getUniformLocation(redShd, "pixelsize"); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT); gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); setupTextureBuffers(); const circleOffsetAnim = new Float32Array([ 0.0, 0.0 ]); let aspect_ratio = 0; let last_time = 0; let redrawActive = false; function setupTextureBuffers() { gl.deleteFramebuffer(circleDrawFramebuffer); circleDrawFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); frameTexture = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTexture, gl.NEAREST); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTexture, 0); buffersInitialized = true; } gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); function redraw(time) { redrawActive = true; if (!buffersInitialized) { setupTextureBuffers(); } last_time = time; /* Setup PostProcess Framebuffer */ gl.viewport(0, 0, canvas.width / resDiv, canvas.height / resDiv); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(circleShd); /* Draw Circle Animation */ gl.uniform1f(aspect_ratioLocation, aspect_ratio); var radius = 0.1; var speed = (time / 10000) % Math.PI * 2; circleOffsetAnim[0] = radius * Math.cos(speed) + 0.1; circleOffsetAnim[1] = radius * Math.sin(speed); gl.uniform2fv(offsetLocationCircle, circleOffsetAnim); gl.uniform1f(sizeLocationCircle, circleSize); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); if (showQuad) { gl.useProgram(simpleColorShd); gl.uniform1f(aspect_ratioLocationSimple, aspect_ratio); gl.uniform2fv(offsetLocationCircleSimple, circleOffsetAnim); gl.uniform1f(sizeLocationCircleSimple, circleSize); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); } gl.viewport(0, 0, canvas.width, canvas.height); gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Scaled image in the bottom left */ gl.uniform4f(transformLocation, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationPost, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ gl.useProgram(redShd); gl.uniform1f(aspect_ratioLocationRed, (1.0 / aspect_ratio) - 1.0); gl.uniform1f(thicknessLocation, 0.2); gl.uniform1f(pixelsizeLocation, (1.0 / canvas.width) * 50); gl.uniform4f(transformLocationRed, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationRed, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.uniform1f(thicknessLocation, 0.1); gl.uniform1f(pixelsizeLocation, 0.0); gl.uniform4f(transformLocationRed, 0.5, 0.5, 0.0, 0.0); gl.uniform2f(offsetLocationRed, -0.75, -0.75); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); redrawActive = false; } let isRendering = false; let animationFrameId; function onResize() { const dipRect = canvas.getBoundingClientRect(); const width = Math.round(devicePixelRatio * dipRect.right) - Math.round(devicePixelRatio * dipRect.left); const height = Math.round(devicePixelRatio * dipRect.bottom) - Math.round(devicePixelRatio * dipRect.top); if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; setupTextureBuffers(); aspect_ratio = 1.0 / (width / height); stopRendering(); startRendering(); } } window.addEventListener('resize', onResize, true); onResize(); function renderLoop(time) { if (isRendering) { redraw(time); animationFrameId = requestAnimationFrame(renderLoop); } } function startRendering() { /* Start rendering, when canvas visible */ isRendering = true; renderLoop(last_time); } function stopRendering() { /* Stop another redraw being called */ isRendering = false; cancelAnimationFrame(animationFrameId); while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality this code is block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the important buffer to free up memory */ gl.deleteTexture(frameTexture); gl.deleteFramebuffer(circleDrawFramebuffer); buffersInitialized = false; } function handleIntersection(entries) { entries.forEach(entry => { if (entry.isIntersecting) { if (!isRendering) startRendering(); } else { stopRendering(); } }); } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


Let’s start out simple. Using [GLSL](https://en.wikipedia.org/wiki/OpenGL_Shading_Language) Shaders we tell the GPU of your device to draw a circle in the most simple and naive way possible, as seen in [circle.fs](https://blog.frost.kiwi/shader/circle.fs) above: If the [ length()](https://docs.gl/sl4/length) from the middle point is bigger than 1.0, we

[the pixel.](https://www.khronos.org/opengl/wiki/Fragment_Shader#Special_operations)

`discard`

The circle is blocky, especially at smaller resolutions. More painfully, there is strong “pixel crawling”, an artifact that’s very obvious when there is any kind of movement. As the circle moves, rows of pixels pop in and out of existence and the stair steps of the pixelation move along the side of the circle like beads of different speeds.

The low ¼ and ⅛ resolutions aren't just there for extreme pixel-peeping, but also to represent small elements or ones at large distance in 3D.

At lower resolutions these artifacts come together to destroy the circular form. The combination of slow movement and low resolution causes one side’s pixels to come into existence, before the other side’s pixels disappear, causing a wobble. Axis-alignment with the pixel grid causes “plateaus” of pixels at every 90° and 45° position.

### Technical breakdown [#](https://blog.frost.kiwi#technical-breakdown)

Understanding the GPU code is not necessary to follow this article, but will help to grasp whats happening when we get to the analytical bits.

4 vertices making up a quad are sent to the GPU in the vertex shader [circle.vs](https://blog.frost.kiwi/shader/circle.vs), where they are received as `attribute vec2 vtx`

. The coordinates are of a “unit quad”, meaning the coordinates look like the following image. With [one famous exception](https://www.copetti.org/writings/consoles/sega-saturn/#segas-offering), all GPUs use triangles, so the quad is actually made up of two triangles.

The vertices [here](https://blog.frost.kiwi/utility.js) are given to the fragment shader [circle.fs](https://blog.frost.kiwi/shader/circle.fs) via `varying vec2 uv`

. The fragment shader is called per [fragment](https://www.khronos.org/opengl/wiki/Fragment) (here fragments are pixel-sized) and the [ varying](http://learnwebgl.brown37.net/12_shader_language/glsl_data_types.html#storage-qualifiers) is interpolated linearly with

[perspective corrected](https://en.wikipedia.org/wiki/Texture_mapping#Affine_texture_mapping),

[barycentric coordinates](https://en.wikipedia.org/wiki/Barycentric_coordinate_system), giving us a

`uv`

coordinate per pixel from `-1`

to `+1`

with zero at the center.By performing the check `if (length(uv) < 1.0)`

we draw our color for fragments inside the circle and reject fragments outside of it. What we are doing is known as “Alpha testing”. Without diving too deeply and just to hint at what’s to come, what we have created with `length(uv)`

is the [signed distance field](https://en.wikipedia.org/wiki/Signed_distance_function#Applications) of a point.

Just to clarify, the circle isn't "drawn with geometry", which would have finite resolution of the shape, depending on how many vertices we use. It's "drawn by the shader".

## SSAA [#](https://blog.frost.kiwi#ssaa)

SSAA stands for [Super Sampling Anti-Aliasing](https://en.wikipedia.org/wiki/Supersampling). Render it bigger, downsample to be smaller. The idea is as old as 3D rendering itself. In fact, the first movies with CGI all relied on this with the most naive of implementations. One example is the 1986 movie “[Flight of the Navigator](https://en.wikipedia.org/wiki/Flight_of_the_Navigator)”, as covered by [Captain Disillusion](https://www.youtube.com/@CaptainDisillusion) in the video below.

Excerpt from

["Flight of the Navigator | VFXcool"](https://www.youtube.com/watch?v=tyixMpuGEL8)

YouTube Video by

[Captain Disillusion](https://www.youtube.com/@CaptainDisillusion)

1986 did it, so can we. Implemented in mere seconds.Easy, right?

## SSAA buffer Fragment Shader

[post.fs]`precision mediump float; uniform sampler2D u_texture; varying vec2 texCoord; void main() { gl_FragColor = texture2D(u_texture, texCoord); }`

## WebGL Javascript

[circleSSAA.js]`function setupSSAA(canvasId, circleVtxSrc, circleFragSrc, postVtxSrc, postFragSrc, blitVtxSrc, blitFragSrc, redVtxSrc, redFragSrc, radioName) { /* Init */ const canvas = document.getElementById(canvasId); let frameTexture, circleDrawFramebuffer, frameTextureLinear; let buffersInitialized = false; let resDiv = 1; const gl = canvas.getContext('webgl', { preserveDrawingBuffer: false, antialias: false, alpha: true, premultipliedAlpha: true } ); /* Setup Possibilities */ let renderbuffer = null; let resolveFramebuffer = null; /* Render Resolution */ const radios = document.querySelectorAll(`input[name="${radioName}"]`); radios.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { resDiv = event.target.value; stopRendering(); startRendering(); }); }); /* Shaders */ /* Circle Shader */ const circleShd = compileAndLinkShader(gl, circleVtxSrc, circleFragSrc); const aspect_ratioLocation = gl.getUniformLocation(circleShd, "aspect_ratio"); const offsetLocationCircle = gl.getUniformLocation(circleShd, "offset"); const sizeLocationCircle = gl.getUniformLocation(circleShd, "size"); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); /* Post Shader */ const postShd = compileAndLinkShader(gl, postVtxSrc, postFragSrc); /* Simple Red Box */ const redShd = compileAndLinkShader(gl, redVtxSrc, redFragSrc); const transformLocationRed = gl.getUniformLocation(redShd, "transform"); const offsetLocationRed = gl.getUniformLocation(redShd, "offset"); const aspect_ratioLocationRed = gl.getUniformLocation(redShd, "aspect_ratio"); const thicknessLocation = gl.getUniformLocation(redShd, "thickness"); const pixelsizeLocation = gl.getUniformLocation(redShd, "pixelsize"); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT); gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); setupTextureBuffers(); const circleOffsetAnim = new Float32Array([ 0.0, 0.0 ]); let aspect_ratio = 0; let last_time = 0; let redrawActive = false; gl.enable(gl.BLEND); function setupTextureBuffers() { gl.deleteFramebuffer(resolveFramebuffer); resolveFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, resolveFramebuffer); frameTexture = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTexture, gl.NEAREST); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTexture, 0); gl.deleteFramebuffer(circleDrawFramebuffer); circleDrawFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); frameTextureLinear = setupTexture(gl, (canvas.width / resDiv) * 2, (canvas.height / resDiv) * 2, frameTextureLinear, gl.LINEAR); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTextureLinear, 0); buffersInitialized = true; } function redraw(time) { redrawActive = true; if (!buffersInitialized) { setupTextureBuffers(); } last_time = time; gl.viewport(0, 0, (canvas.width / resDiv) * 2, (canvas.height / resDiv) * 2); /* Setup PostProcess Framebuffer */ gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(circleShd); /* Draw Circle Animation */ gl.uniform1f(aspect_ratioLocation, aspect_ratio); var radius = 0.1; var speed = (time / 10000) % Math.PI * 2; circleOffsetAnim[0] = radius * Math.cos(speed) + 0.1; circleOffsetAnim[1] = radius * Math.sin(speed); gl.uniform2fv(offsetLocationCircle, circleOffsetAnim); gl.uniform1f(sizeLocationCircle, circleSize); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.viewport(0, 0, canvas.width / resDiv, canvas.height / resDiv); gl.useProgram(postShd); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); gl.bindTexture(gl.TEXTURE_2D, frameTextureLinear); gl.bindFramebuffer(gl.FRAMEBUFFER, resolveFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.bindTexture(gl.TEXTURE_2D, frameTexture); gl.viewport(0, 0, canvas.width, canvas.height); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Scaled image in the bottom left */ gl.uniform4f(transformLocation, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationPost, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(redShd); gl.uniform1f(aspect_ratioLocationRed, (1.0 / aspect_ratio) - 1.0); gl.uniform1f(thicknessLocation, 0.2); gl.uniform1f(pixelsizeLocation, (1.0 / canvas.width) * 50); gl.uniform4f(transformLocationRed, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationRed, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.uniform1f(thicknessLocation, 0.1); gl.uniform1f(pixelsizeLocation, 0.0); gl.uniform4f(transformLocationRed, 0.5, 0.5, 0.0, 0.0); gl.uniform2f(offsetLocationRed, -0.75, -0.75); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); redrawActive = false; } let isRendering = false; let animationFrameId; function onResize() { const dipRect = canvas.getBoundingClientRect(); const width = Math.round(devicePixelRatio * dipRect.right) - Math.round(devicePixelRatio * dipRect.left); const height = Math.round(devicePixelRatio * dipRect.bottom) - Math.round(devicePixelRatio * dipRect.top); if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; setupTextureBuffers(); aspect_ratio = 1.0 / (width / height); stopRendering(); startRendering(); } } window.addEventListener('resize', onResize, true); onResize(); function renderLoop(time) { if (isRendering) { redraw(time); animationFrameId = requestAnimationFrame(renderLoop); } } function startRendering() { /* Start rendering, when canvas visible */ isRendering = true; renderLoop(last_time); } function stopRendering() { /* Stop another redraw being called */ isRendering = false; cancelAnimationFrame(animationFrameId); while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality this code is block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the important buffer to free up memory */ gl.deleteTexture(frameTexture); gl.deleteFramebuffer(circleDrawFramebuffer); gl.deleteRenderbuffer(renderbuffer); gl.deleteFramebuffer(resolveFramebuffer); buffersInitialized = false; } function handleIntersection(entries) { entries.forEach(entry => { if (entry.isIntersecting) { if (!isRendering) startRendering(); } else { stopRendering(); } }); } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


[circleSSAA.js](https://blog.frost.kiwi/circleSSAA.js) draws at twice the resolution to a texture, which fragment shader [post.fs](https://blog.frost.kiwi/shader/post.fs) reads from at standard resolution with [GL_LINEAR](https://docs.gl/es2/glTexParameter) to perform SSAA. So we have *four* input pixels for every *one* output pixel we draw to the screen. But it’s somewhat strange: There is definitely Anti-Aliasing happening, but less than expected.

There should be 4 steps of transparency, but we only get two!

Especially at lower resolutions, we can see the circle *does* actually have 4 steps of transparency, but mainly at the 45° “diagonals” of the circle. A circle has of course no sides, but at the axis-aligned “bottom” there are only 2 steps of transparency: Fully Opaque and 50% transparent, the 25% and 75% transparency steps are missing.

### Conceptually simple, actually hard [#](https://blog.frost.kiwi#conceptually-simple%2C-actually-hard)

We aren’t sampling against the circle shape at twice the resolution, we are sampling against the quantized result of the circle shape. Twice the resolution, but discrete pixels nonetheless. The combination of pixelation and sample placement doesn’t hold enough information where we need it the most: at the axis-aligned “flat parts”.

Four times the memoryandfour times the calculation requirement, but only a half-assed result.

Implementing SSAA properly is a minute craft. Here we are drawing to a 2x resolution texture and down-sampling it with linear interpolation. So actually, this implementation needs 5x the amount of VRAM. A proper implementation samples the scene multiple times and combines the result without an intermediary buffer.

With our implementation, we can't even do more than 2xSSAA with one texture read, as linear interpolation happens[only with 2x2 samples].

To combat axis-alignment artifacts like with our circle above, we need to place our SSAA samples better. There are [multiple ways to do so](https://en.wikipedia.org/wiki/Supersampling#Supersampling_patterns), all with pros and cons. To implement SSAA properly, we need deep integration with the rendering pipeline. For 3D primitives, this happens below API or engine, in the realm of vendors and drivers.

[Source](https://en.wikipedia.org/wiki/Supersampling#Supersampling_patterns)

In fact, some of the best implementations were [discovered by vendors on accident](https://web.archive.org/web/20180716171211/https://naturalviolence.webs.com/sgssaa.htm), like [SGSSAA](https://www.youtube.com/watch?v=ntlYwrbUlWo). There are also ways in which SSAA can make your scene look *worse*. Depending on implementation, SSAA messes with [mip-map](https://en.wikipedia.org/wiki/Mipmap) calculations. As a result the mip-map lod-bias may need adjustment, as explained in the [article above](https://web.archive.org/web/20180716171211/https://naturalviolence.webs.com/sgssaa.htm).

WebXR UI package[three-mesh-ui], a package mature enough to be[used by Meta], uses shader-based rotated grid super sampling to achieve sharp text rendering in VR,[as seen in the code].

## MSAA [#](https://blog.frost.kiwi#msaa)

[MSAA](https://en.wikipedia.org/wiki/Multisample_anti-aliasing) is super sampling, but only at the silhouette of models, overlapping geometry, and texture edges if “[Alpha to Coverage](https://bgolus.medium.com/anti-aliased-alpha-test-the-esoteric-alpha-to-coverage-8b177335ae4f)” is enabled. MSAA is implemented by graphics vendors on the GPU in-hardware and what is supported depends on said hardware. In the select box below you can choose different MSAA levels for our circle.

[There is up to MSAA x64](https://opengl.gpuinfo.org/displaycapability.php?name=GL_MAX_SAMPLES), but what is available is implementation defined. WebGL 1 has no support, which is why the next canvas initializes a [WebGL 2](https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext) context. In WebGL, NVIDIA limits MSAA to 8x on Windows, even if more is supported, whilst on Linux no such limit is in place. On smartphones you will only get exactly 4x, as discussed below.

## WebGL Javascript

[circleMSAA.js]`function setupMSAA(canvasId, circleVtxSrc, circleFragSrc, circleSimpleFragSrc, postVtxSrc, postFragSrc, blitVtxSrc, blitFragSrc, redVtxSrc, redFragSrc, radioName, radioSmoothSize) { /* Init */ const canvas = document.getElementById(canvasId); let frameTexture, circleDrawFramebuffer; let buffersInitialized = false; let resDiv = 1; let pixelSmoothSize = 1; const gl = canvas.getContext('webgl2', { preserveDrawingBuffer: false, antialias: false, alpha: true, premultipliedAlpha: true } ); /* Setup Possibilities */ let samples = 1; let renderbuffer = null; let resolveFramebuffer = null; const maxSamples = gl.getParameter(gl.MAX_SAMPLES); /* Enable the options in the MSAA dropdown based on maxSamples */ const msaaSelect = document.getElementById("MSAA"); for (let option of msaaSelect.options) { if (parseInt(option.value) <= maxSamples) { option.disabled = false; } } samples = parseInt(msaaSelect.value); /* Event listener for select dropdown */ msaaSelect.addEventListener('change', function () { /* Get new MSAA level and reset-init buffers */ samples = parseInt(msaaSelect.value); setupTextureBuffers(); }); /* Render Resolution */ const radios = document.querySelectorAll(`input[name="${radioName}"]`); radios.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { resDiv = event.target.value; stopRendering(); startRendering(); }); }); /* Smooth Size */ const radiosSmooth = document.querySelectorAll(`input[name="${radioSmoothSize}"]`); radiosSmooth.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { pixelSmoothSize = event.target.value; stopRendering(); startRendering(); }); }); /* Shaders */ /* Circle Shader */ const circleShd = compileAndLinkShader(gl, circleVtxSrc, circleFragSrc); const aspect_ratioLocation = gl.getUniformLocation(circleShd, "aspect_ratio"); const offsetLocationCircle = gl.getUniformLocation(circleShd, "offset"); const pixelSizeCircle = gl.getUniformLocation(circleShd, "pixelSize"); const sizeLocationCircle = gl.getUniformLocation(circleShd, "size"); const circleShd_step = compileAndLinkShader(gl, circleVtxSrc, circleSimpleFragSrc); const aspect_ratioLocation_step = gl.getUniformLocation(circleShd_step, "aspect_ratio"); const offsetLocationCircle_step = gl.getUniformLocation(circleShd_step, "offset"); const sizeLocationCircle_step = gl.getUniformLocation(circleShd_step, "size"); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); /* Post Shader */ const postShd = compileAndLinkShader(gl, postVtxSrc, postFragSrc); /* Simple Red Box */ const redShd = compileAndLinkShader(gl, redVtxSrc, redFragSrc); const transformLocationRed = gl.getUniformLocation(redShd, "transform"); const offsetLocationRed = gl.getUniformLocation(redShd, "offset"); const aspect_ratioLocationRed = gl.getUniformLocation(redShd, "aspect_ratio"); const thicknessLocation = gl.getUniformLocation(redShd, "thickness"); const pixelsizeLocation = gl.getUniformLocation(redShd, "pixelsize"); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT); gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); setupTextureBuffers(); const circleOffsetAnim = new Float32Array([ 0.0, 0.0 ]); let aspect_ratio = 0; let last_time = 0; let redrawActive = false; let animationFrameId; function setupTextureBuffers() { gl.deleteFramebuffer(circleDrawFramebuffer) circleDrawFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.deleteRenderbuffer(renderbuffer); renderbuffer = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, renderbuffer); const errorMessageElement = document.getElementById('sampleErrorMessage'); /* Here we need two branches because of implementation specific shenanigans. Mobile chips will always force any call to renderbufferStorageMultisample() to be 4x MSAA, so to have a noAA comparison, we split the Framebuffer setup */ if (samples != 1) { gl.renderbufferStorageMultisample(gl.RENDERBUFFER, samples, gl.RGBA8, canvas.width / resDiv, canvas.height / resDiv); gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.RENDERBUFFER, renderbuffer); const actualSamples = gl.getRenderbufferParameter( gl.RENDERBUFFER, gl.RENDERBUFFER_SAMPLES ); if (samples !== actualSamples) { errorMessageElement.style.display = 'block'; errorMessageElement.textContent = `⚠️ You chose MSAAx${samples}, but the graphics driver forced it to MSAAx${actualSamples}. You are probably on a mobile GPU, where this behavior is expected.`; } else { errorMessageElement.style.display = 'none'; } } else { errorMessageElement.style.display = 'none'; } gl.deleteFramebuffer(resolveFramebuffer); resolveFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, resolveFramebuffer); frameTexture = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTexture, gl.NEAREST); gl.framebufferTexture2D(gl.DRAW_FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTexture, 0); buffersInitialized = true; } function redraw(time) { redrawActive = true; if (!buffersInitialized) { setupTextureBuffers(); } last_time = time; gl.disable(gl.BLEND); gl.enable(gl.SAMPLE_ALPHA_TO_COVERAGE); /* Setup PostProcess Framebuffer */ if (samples == 1) gl.bindFramebuffer(gl.FRAMEBUFFER, resolveFramebuffer); else gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); if (samples == 1) gl.useProgram(circleShd_step); else gl.useProgram(circleShd); gl.viewport(0, 0, canvas.width / resDiv, canvas.height / resDiv); /* Draw Circle Animation */ var radius = 0.1; var speed = (time / 10000) % Math.PI * 2; circleOffsetAnim[0] = radius * Math.cos(speed) + 0.1; circleOffsetAnim[1] = radius * Math.sin(speed); if (samples == 1) { /* Here we need two branches because of implementation specific shenanigans. Mobile chips will always force any call to renderbufferStorageMultisample() to be 4x MSAA, so to have a noAA comparison, we split the demo across two shaders */ gl.uniform2fv(offsetLocationCircle_step, circleOffsetAnim); gl.uniform1f(aspect_ratioLocation_step, aspect_ratio); gl.uniform1f(sizeLocationCircle_step, circleSize); } else { gl.uniform2fv(offsetLocationCircle, circleOffsetAnim); gl.uniform1f(aspect_ratioLocation, aspect_ratio); gl.uniform1f(sizeLocationCircle, circleSize); gl.uniform1f(pixelSizeCircle, (2.0 / (canvas.height / resDiv)) * pixelSmoothSize); } gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.disable(gl.SAMPLE_ALPHA_TO_COVERAGE); gl.enable(gl.BLEND); gl.viewport(0, 0, canvas.width, canvas.height); if (samples !== 1) { gl.useProgram(postShd); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); /* Resolve the MSAA framebuffer to a regular texture */ gl.bindFramebuffer(gl.READ_FRAMEBUFFER, circleDrawFramebuffer); gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, resolveFramebuffer); gl.blitFramebuffer( 0, 0, canvas.width, canvas.height, 0, 0, canvas.width, canvas.height, gl.COLOR_BUFFER_BIT, gl.LINEAR ); } gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.bindTexture(gl.TEXTURE_2D, frameTexture); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Scaled image in the bottom left */ gl.uniform4f(transformLocation, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationPost, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(redShd); gl.uniform1f(aspect_ratioLocationRed, (1.0 / aspect_ratio) - 1.0); gl.uniform1f(thicknessLocation, 0.2); gl.uniform1f(pixelsizeLocation, (1.0 / canvas.width) * 50); gl.uniform4f(transformLocationRed, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationRed, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.uniform1f(thicknessLocation, 0.1); gl.uniform1f(pixelsizeLocation, 0.0); gl.uniform4f(transformLocationRed, 0.5, 0.5, 0.0, 0.0); gl.uniform2f(offsetLocationRed, -0.75, -0.75); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); redrawActive = false; } function onResize() { const dipRect = canvas.getBoundingClientRect(); const width = Math.round(devicePixelRatio * dipRect.right) - Math.round(devicePixelRatio * dipRect.left); const height = Math.round(devicePixelRatio * dipRect.bottom) - Math.round(devicePixelRatio * dipRect.top); if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; setupTextureBuffers(); aspect_ratio = 1.0 / (width / height); } } window.addEventListener('resize', onResize, true); onResize(); let isRendering = false; function renderLoop(time) { if (isRendering) { redraw(time); animationFrameId = requestAnimationFrame(renderLoop); } } function startRendering() { /* Start rendering, when canvas visible */ isRendering = true; renderLoop(last_time); } function stopRendering() { /* Stop another redraw being called */ isRendering = false; cancelAnimationFrame(animationFrameId); while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality this code is block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the important buffer to free up memory */ gl.deleteTexture(frameTexture); gl.deleteFramebuffer(circleDrawFramebuffer); gl.deleteRenderbuffer(renderbuffer); gl.deleteFramebuffer(resolveFramebuffer); buffersInitialized = false; } function handleIntersection(entries) { entries.forEach(entry => { if (entry.isIntersecting) { if (!isRendering) startRendering(); } else { stopRendering(); } }); } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


What is edge smoothing and how does MSAA even know what to sample against? For now we skip the shader code and implementation. First let's take a look at MSAA's pros and cons in general.

### Implementation specific headaches [#](https://blog.frost.kiwi#implementation-specific-headaches)

We rely on hardware to do the Anti-Aliasing, which obviously leads to the problem that user hardware may not support what we need. The sampling patterns MSAA uses may also do things we don’t expect. Depending on what your hardware does, you may see the circle’s edge transparency steps appearing “in the wrong order”.

![Sample pattern and circle shape clash: pixels are seemingly 'checkerboxed'](../../assets/ef47800544b89fe2.png)

When MSAA became required with [OpenGL 3](https://en.wikipedia.org/wiki/OpenGL#OpenGL_3.0) & [DirectX 10](https://en.wikipedia.org/wiki/DirectX#DirectX_10) era of hardware, support was especially hit & miss. Even latest [Intel GMA](https://en.wikipedia.org/wiki/Intel_GMA#GMA_4500) iGPUs expose the OpenGL extension [ EXT_framebuffer_multisample](https://registry.khronos.org/OpenGL/extensions/EXT/EXT_framebuffer_multisample.txt), but don’t in-fact support MSAA,

[which led to confusion](https://community.khronos.org/t/yet-another-intel-multisample-thread/69614/2). But also in more recent smartphones, support just

[wasn’t that clear-cut](https://issues.chromium.org/issues/40114751).

![iOS 2xMSAA, created by rounding transparency of 4xMSAA](../../assets/504db4d9445e41f2.png)

Mobile chips support *exactly* MSAAx4 and things are weird. Android will let you pick 2x, but the driver will force 4x anyways. iPhones & iPads do something rather stupid: Choosing 2x will make it 4x, but transparency will be rounded to the nearest 50% multiple, leading to double edges in our example. There is hardware specific reason:

### Performance cost: (maybe) Zero [#](https://blog.frost.kiwi#performance-cost%3A-(maybe)-zero)

Looking at modern video games, one might believe that MSAA is of the past. It usually brings a hefty performance penalty after all. Surprisingly, it’s still the king under certain circumstances and in very specific situations, even performance free.

As a gamer, this goes against instinct...

Excerpt from

["Developing High Performance Games for Different Mobile VR Platforms"](https://gdcvault.com/play/1024538)

GDC 2017 talk by

[Rahul Prasad](https://www.linkedin.com/in/rahulprasad2/)


[Rahul Prasad:]Use MSAA […] It’s actually not as expensive on mobile as it is on desktop, it’s one of the nice things you get on mobile. […] On some (mobile) GPUs 4x (MSAA) is free, so use it when you have it.

As explained by [Rahul Prasad](https://www.linkedin.com/in/rahulprasad2/) in the above talk, in VR 4xMSAA is a must and may come free on certain mobile GPUs. The specific reason would derail the blog post, but in case you want to go down that particular rabbit hole, here is Epic Games’ [Niklas Smedberg](https://www.linkedin.com/in/niklas-smedberg-a96466/) giving a run-down.

Excerpt from

["Next-Generation AAA Mobile Rendering"](https://gdcvault.com/play/1020756)

GDC 2014 talk by

[Niklas Smedberg](https://www.linkedin.com/in/niklas-smedberg-a96466/)and

[Timothy Lottes](https://twitter.com/NOTimothyLottes)

In short, this is possible under the condition of [forward rendering](https://gamedevelopment.tutsplus.com/forward-rendering-vs-deferred-rendering--gamedev-12342a) with geometry that is not too dense and the GPU having [tiled-based rendering architecture](https://developer.arm.com/documentation/102662/0100/Tile-based-GPUs), which allows the GPU to perform MSAA calculations without heavy memory access and thus [latency hiding](https://blog.frost.kiwi/WebGL-LUTS-made-simple/#performance-cost%3A-zero) the cost of the calculation. Here’s a [deep-dive](https://github.com/KhronosGroup/Vulkan-Samples/tree/main/samples/performance/msaa#color-resolve), if you are interested.

### A complex toolbox [#](https://blog.frost.kiwi#a-complex-toolbox)

MSAA [gives you access](https://docs.gl/gl3/glGetMultisample) to the samples, making [custom MSAA filtering curves](https://therealmjp.github.io/posts/msaa-resolve-filters/) a possibility. It also allows you to [merge both standard mesh-based and signed-distance-field rendering](https://bgolus.medium.com/rendering-a-sphere-on-a-quad-13c92025570c) via [alpha to coverage](https://bgolus.medium.com/anti-aliased-alpha-test-the-esoteric-alpha-to-coverage-8b177335ae4f). This complex features set made possible the most out-of-the-box thinking I ever witnessed in graphics programming:

[Assassin’s Creed Unity](https://en.wikipedia.org/wiki/Assassin%27s_Creed_Unity) used MSAA to render at half resolution and reconstruct only some buffers to full-res from MSAA samples, as described on page 48 of the talk “[GPU-Driven Rendering Pipelines](https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf)” by [Ulrich Haar](https://www.linkedin.com/in/ulrich-haar-730407218) and [Sebastian Aaltonen](https://x.com/SebAaltonen). Kinda like [variable rate shading](https://developer.nvidia.com/vrworks/graphics/variablerateshading), but implemented with duct-tape and without vendor support.

The brain-melting lengths to which graphics programmers go to utilize hardware acceleration to the last drop has me sometimes in awe.

## Post-Process Anti-Aliasing [#](https://blog.frost.kiwi#post-process-anti-aliasing)

In 2009 a [paper](https://web.archive.org/web/20141205052029/http://visual-computing.intel-research.net/publications/papers/2009/mlaa/mlaa.pdf) by [Alexander Reshetov](https://research.nvidia.com/person/alexander-reshetov) struck the graphics programming world like a ton of bricks: take the blocky, aliased result of the rendered image, find edges and classify the pixels into tetris-like shapes with per-shape filtering rules and remove the blocky edge. Anti-Aliasing based on the [morphology](https://en.wikipedia.org/wiki/Mathematical_morphology) of pixels - [MLAA](https://www.iryoku.com/mlaa/) was born.

Computationally cheap, easy to implement. Later it was refined with more emphasis on removing sub-pixel artifacts to become [SMAA](https://www.iryoku.com/smaa/). It became a fan favorite, with [an injector being developed early on](https://mrhaandi.blogspot.com/p/injectsmaa.html?m=1) to put SMAA into games that didn’t support it. Some considered these too blurry, the saying “vaseline on the screen” was coined.

It was the future, a sign of things to come. No more shaky hardware support. Like[Fixed-Function pipelines]died in favor of programmable shaders Anti-Aliasing too became "shader based".

### FXAA [#](https://blog.frost.kiwi#fxaa)

We’ll take a close look at an algorithm that was inspired by MLAA, developed by [Timothy Lottes](https://x.com/NOTimothyLottes). “Fast approximate anti-aliasing”, [FXAA](https://developer.download.nvidia.com/assets/gamedev/files/sdk/11/FXAA_WhitePaper.pdf). In fact, when it came into wide circulation, it received some incredible press. [Among others](https://www.realtimerendering.com/blog/fxaa-rules-ok/), [Jeff Atwood](https://blog.codinghorror.com/about-me/) pulled neither bold fonts nor punches in his [2011 blog post](https://blog.codinghorror.com/fast-approximate-anti-aliasing-fxaa/), later [republished by Kotaku](http://kotaku.com/5866780/).


[: The FXAA method is so good, in fact, it makes all other forms of full-screen anti-aliasing pretty much obsolete overnight.]Jeff AtwoodIf you have an FXAA option in your game, you should enable it immediatelyand ignore any other AA options.

Let’s see what the hype was about. The final version publicly released was FXAA 3.11 on [August 12th 2011](https://web.archive.org/web/20120121124756/http://timothylottes.blogspot.com/2011/08/fxaa-311-bug-fixes-for-360.html) and the following demos are based on this. First, let’s take a look at our circle with FXAA doing the Anti-Aliasing at default settings.

## WebGL FXAA Shader

[post-FXAA.fs]`precision mediump float; uniform sampler2D u_texture; varying vec2 texCoord; uniform vec2 RcpFrame; /* FXAA 3.11 code, after passing through the preprocessor with settings: - FXAA PC QUALITY - FXAA_PC 1 - Default QUALITY - FXAA_QUALITY_PRESET 12 - Optimizations disabled for WebGL 1 - FXAA_GLSL_120 1 - FXAA_FAST_PIXEL_OFFSET 0 - Further optimizations possible with WebGL 2 or by enabling extension GL_EXT_shader_texture_lod - GREEN_AS_LUMA is disabled - FXAA_GREEN_AS_LUMA 0 - Input must be RGBL */ float FxaaLuma(vec4 rgba) { return rgba.w; } vec4 FxaaPixelShader( vec2 pos, sampler2D tex, vec2 fxaaQualityRcpFrame, float fxaaQualitySubpix, float fxaaQualityEdgeThreshold, float fxaaQualityEdgeThresholdMin) { vec2 posM; posM.x = pos.x; posM.y = pos.y; vec4 rgbyM = texture2D(tex, posM); float lumaS = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(0, 1)) * fxaaQualityRcpFrame.xy))); float lumaE = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(1, 0)) * fxaaQualityRcpFrame.xy))); float lumaN = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(0, -1)) * fxaaQualityRcpFrame.xy))); float lumaW = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(-1, 0)) * fxaaQualityRcpFrame.xy))); float maxSM = max(lumaS, rgbyM.w); float minSM = min(lumaS, rgbyM.w); float maxESM = max(lumaE, maxSM); float minESM = min(lumaE, minSM); float maxWN = max(lumaN, lumaW); float minWN = min(lumaN, lumaW); float rangeMax = max(maxWN, maxESM); float rangeMin = min(minWN, minESM); float rangeMaxScaled = rangeMax * fxaaQualityEdgeThreshold; float range = rangeMax - rangeMin; float rangeMaxClamped = max(fxaaQualityEdgeThresholdMin, rangeMaxScaled); bool earlyExit = range < rangeMaxClamped; if (earlyExit) return rgbyM; float lumaNW = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(-1, -1)) * fxaaQualityRcpFrame.xy))); float lumaSE = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(1, 1)) * fxaaQualityRcpFrame.xy))); float lumaNE = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(1, -1)) * fxaaQualityRcpFrame.xy))); float lumaSW = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(-1, 1)) * fxaaQualityRcpFrame.xy))); float lumaNS = lumaN + lumaS; float lumaWE = lumaW + lumaE; float subpixRcpRange = 1.0 / range; float subpixNSWE = lumaNS + lumaWE; float edgeHorz1 = (-2.0 * rgbyM.w) + lumaNS; float edgeVert1 = (-2.0 * rgbyM.w) + lumaWE; float lumaNESE = lumaNE + lumaSE; float lumaNWNE = lumaNW + lumaNE; float edgeHorz2 = (-2.0 * lumaE) + lumaNESE; float edgeVert2 = (-2.0 * lumaN) + lumaNWNE; float lumaNWSW = lumaNW + lumaSW; float lumaSWSE = lumaSW + lumaSE; float edgeHorz4 = (abs(edgeHorz1) * 2.0) + abs(edgeHorz2); float edgeVert4 = (abs(edgeVert1) * 2.0) + abs(edgeVert2); float edgeHorz3 = (-2.0 * lumaW) + lumaNWSW; float edgeVert3 = (-2.0 * lumaS) + lumaSWSE; float edgeHorz = abs(edgeHorz3) + edgeHorz4; float edgeVert = abs(edgeVert3) + edgeVert4; float subpixNWSWNESE = lumaNWSW + lumaNESE; float lengthSign = fxaaQualityRcpFrame.x; bool horzSpan = edgeHorz >= edgeVert; float subpixA = subpixNSWE * 2.0 + subpixNWSWNESE; if (!horzSpan) lumaN = lumaW; if (!horzSpan) lumaS = lumaE; if (horzSpan) lengthSign = fxaaQualityRcpFrame.y; float subpixB = (subpixA * (1.0 / 12.0)) - rgbyM.w; float gradientN = lumaN - rgbyM.w; float gradientS = lumaS - rgbyM.w; float lumaNN = lumaN + rgbyM.w; float lumaSS = lumaS + rgbyM.w; bool pairN = abs(gradientN) >= abs(gradientS); float gradient = max(abs(gradientN), abs(gradientS)); if (pairN) lengthSign = -lengthSign; float subpixC = clamp(abs(subpixB) * subpixRcpRange, 0.0, 1.0); vec2 posB; posB.x = posM.x; posB.y = posM.y; vec2 offNP; offNP.x = (!horzSpan) ? 0.0 : fxaaQualityRcpFrame.x; offNP.y = (horzSpan) ? 0.0 : fxaaQualityRcpFrame.y; if (!horzSpan) posB.x += lengthSign * 0.5; if (horzSpan) posB.y += lengthSign * 0.5; vec2 posN; posN.x = posB.x - offNP.x * 1.0; posN.y = posB.y - offNP.y * 1.0; vec2 posP; posP.x = posB.x + offNP.x * 1.0; posP.y = posB.y + offNP.y * 1.0; float subpixD = ((-2.0) * subpixC) + 3.0; float lumaEndN = FxaaLuma(texture2D(tex, posN)); float subpixE = subpixC * subpixC; float lumaEndP = FxaaLuma(texture2D(tex, posP)); if (!pairN) lumaNN = lumaSS; float gradientScaled = gradient * 1.0 / 4.0; float lumaMM = rgbyM.w - lumaNN * 0.5; float subpixF = subpixD * subpixE; bool lumaMLTZero = lumaMM < 0.0; lumaEndN -= lumaNN * 0.5; lumaEndP -= lumaNN * 0.5; bool doneN = abs(lumaEndN) >= gradientScaled; bool doneP = abs(lumaEndP) >= gradientScaled; if (!doneN) posN.x -= offNP.x * 1.5; if (!doneN) posN.y -= offNP.y * 1.5; bool doneNP = (!doneN) || (!doneP); if (!doneP) posP.x += offNP.x * 1.5; if (!doneP) posP.y += offNP.y * 1.5; if (doneNP) { if (!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if (!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if (!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if (!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if (!doneN) posN.x -= offNP.x * 2.0; if (!doneN) posN.y -= offNP.y * 2.0; doneNP = (!doneN) || (!doneP); if (!doneP) posP.x += offNP.x * 2.0; if (!doneP) posP.y += offNP.y * 2.0; if (doneNP) { if (!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if (!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if (!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if (!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if (!doneN) posN.x -= offNP.x * 4.0; if (!doneN) posN.y -= offNP.y * 4.0; doneNP = (!doneN) || (!doneP); if (!doneP) posP.x += offNP.x * 4.0; if (!doneP) posP.y += offNP.y * 4.0; if (doneNP) { if (!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if (!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if (!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if (!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if (!doneN) posN.x -= offNP.x * 12.0; if (!doneN) posN.y -= offNP.y * 12.0; doneNP = (!doneN) || (!doneP); if (!doneP) posP.x += offNP.x * 12.0; if (!doneP) posP.y += offNP.y * 12.0; } } } float dstN = posM.x - posN.x; float dstP = posP.x - posM.x; if (!horzSpan) dstN = posM.y - posN.y; if (!horzSpan) dstP = posP.y - posM.y; bool goodSpanN = (lumaEndN < 0.0) != lumaMLTZero; float spanLength = (dstP + dstN); bool goodSpanP = (lumaEndP < 0.0) != lumaMLTZero; float spanLengthRcp = 1.0 / spanLength; bool directionN = dstN < dstP; float dst = min(dstN, dstP); bool goodSpan = directionN ? goodSpanN : goodSpanP; float subpixG = subpixF * subpixF; float pixelOffset = (dst * (-spanLengthRcp)) + 0.5; float subpixH = subpixG * fxaaQualitySubpix; float pixelOffsetGood = goodSpan ? pixelOffset : 0.0; float pixelOffsetSubpix = max(pixelOffsetGood, subpixH); if (!horzSpan) posM.x += pixelOffsetSubpix * lengthSign; if (horzSpan) posM.y += pixelOffsetSubpix * lengthSign; return vec4(texture2D(tex, posM).xyz, rgbyM.w); } void main() { gl_FragColor = FxaaPixelShader( texCoord, u_texture, RcpFrame, 0.75, 0.166, 0.0833); }`

## WebGL Javascript

[circleFXAA.js]`function setupFXAA(canvasId, circleVtxSrc, circleFragSrc, postVtxSrc, postFragSrc, blitVtxSrc, blitFragSrc, redVtxSrc, redFragSrc, radioName) { /* Init */ const canvas = document.getElementById(canvasId); let frameTexture, circleDrawFramebuffer, frameTextureLinear; let buffersInitialized = false; let resDiv = 1; const gl = canvas.getContext('webgl', { preserveDrawingBuffer: false, antialias: false, alpha: true, premultipliedAlpha: true } ); /* Setup Possibilities */ let samples = 1; let renderbuffer = null; let resolveFramebuffer = null; /* Render Resolution */ const radios = document.querySelectorAll(`input[name="${radioName}"]`); radios.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { resDiv = event.target.value; stopRendering(); startRendering(); }); }); /* Shaders */ /* Circle Shader */ const circleShd = compileAndLinkShader(gl, circleVtxSrc, circleFragSrc); const aspect_ratioLocation = gl.getUniformLocation(circleShd, "aspect_ratio"); const offsetLocationCircle = gl.getUniformLocation(circleShd, "offset"); const sizeLocationCircle = gl.getUniformLocation(circleShd, "size"); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); /* Post Shader */ const postShd = compileAndLinkShader(gl, postVtxSrc, postFragSrc); const rcpFrameLocation = gl.getUniformLocation(postShd, "RcpFrame"); /* Simple Red Box */ const redShd = compileAndLinkShader(gl, redVtxSrc, redFragSrc); const transformLocationRed = gl.getUniformLocation(redShd, "transform"); const offsetLocationRed = gl.getUniformLocation(redShd, "offset"); const aspect_ratioLocationRed = gl.getUniformLocation(redShd, "aspect_ratio"); const thicknessLocation = gl.getUniformLocation(redShd, "thickness"); const pixelsizeLocation = gl.getUniformLocation(redShd, "pixelsize"); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT); gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); setupTextureBuffers(); const circleOffsetAnim = new Float32Array([ 0.0, 0.0 ]); let aspect_ratio = 0; let last_time = 0; let redrawActive = false; let animationFrameId; gl.enable(gl.BLEND); function setupTextureBuffers() { gl.deleteFramebuffer(resolveFramebuffer); resolveFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, resolveFramebuffer); frameTexture = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTexture, gl.NEAREST); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTexture, 0); gl.deleteFramebuffer(circleDrawFramebuffer); circleDrawFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); frameTextureLinear = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTextureLinear, gl.LINEAR); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTextureLinear, 0); buffersInitialized = true; } function redraw(time) { redrawActive = true; if (!buffersInitialized) { setupTextureBuffers(); } last_time = time; gl.viewport(0, 0, canvas.width / resDiv, canvas.height / resDiv); /* Setup PostProcess Framebuffer */ gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(circleShd); /* Draw Circle Animation */ gl.uniform1f(aspect_ratioLocation, aspect_ratio); var radius = 0.1; var speed = (time / 10000) % Math.PI * 2; circleOffsetAnim[0] = radius * Math.cos(speed) + 0.1; circleOffsetAnim[1] = radius * Math.sin(speed); gl.uniform2fv(offsetLocationCircle, circleOffsetAnim); gl.uniform1f(sizeLocationCircle, circleSize); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.useProgram(postShd); gl.uniform2f(rcpFrameLocation, 1.0 / (canvas.width / resDiv), 1.0 / (canvas.height / resDiv)); gl.disable(gl.SAMPLE_ALPHA_TO_COVERAGE); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); gl.bindTexture(gl.TEXTURE_2D, frameTextureLinear); gl.bindFramebuffer(gl.FRAMEBUFFER, resolveFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.viewport(0, 0, canvas.width, canvas.height); gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.bindTexture(gl.TEXTURE_2D, frameTexture); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Scaled image in the bottom left */ gl.uniform4f(transformLocation, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationPost, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(redShd); gl.uniform1f(aspect_ratioLocationRed, (1.0 / aspect_ratio) - 1.0); gl.uniform1f(thicknessLocation, 0.2); gl.uniform1f(pixelsizeLocation, (1.0 / canvas.width) * 50); gl.uniform4f(transformLocationRed, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationRed, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.uniform1f(thicknessLocation, 0.1); gl.uniform1f(pixelsizeLocation, 0.0); gl.uniform4f(transformLocationRed, 0.5, 0.5, 0.0, 0.0); gl.uniform2f(offsetLocationRed, -0.75, -0.75); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); redrawActive = false; } function onResize() { const dipRect = canvas.getBoundingClientRect(); const width = Math.round(devicePixelRatio * dipRect.right) - Math.round(devicePixelRatio * dipRect.left); const height = Math.round(devicePixelRatio * dipRect.bottom) - Math.round(devicePixelRatio * dipRect.top); if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; setupTextureBuffers(); aspect_ratio = 1.0 / (width / height); } } window.addEventListener('resize', onResize, true); onResize(); let isRendering = false; function renderLoop(time) { if (isRendering) { redraw(time); animationFrameId = requestAnimationFrame(renderLoop); } } function startRendering() { /* Start rendering, when canvas visible */ isRendering = true; renderLoop(last_time); } function stopRendering() { /* Stop another redraw being called */ isRendering = false; cancelAnimationFrame(animationFrameId); while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality this code is block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the important buffer to free up memory */ gl.deleteTexture(frameTexture); gl.deleteFramebuffer(circleDrawFramebuffer); gl.deleteRenderbuffer(renderbuffer); gl.deleteFramebuffer(resolveFramebuffer); buffersInitialized = false; } function handleIntersection(entries) { entries.forEach(entry => { if (entry.isIntersecting) { if (!isRendering) startRendering(); } else { stopRendering(); } }); } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


A bit of a weird result. It looks good if the circle wouldn’t move. Perfectly smooth edges. But the circle distorts as it moves. The axis-aligned top and bottom especially have a little nub that appears and disappears. And switching to lower resolutions, the circle even loses its round shape, [wobbling like Play Station 1 graphics](https://www.youtube.com/watch?v=x8TO-nrUtSI).

Per-pixel, FXAA considers only the 3x3 neighborhood, so it can’t possibly know that this area is part of a big shape. But it also doesn’t just “blur edges”, as often said. As explained in the [official whitepaper](https://developer.download.nvidia.com/assets/gamedev/files/sdk/11/FXAA_WhitePaper.pdf), it finds the edge’s direction and shifts the pixel’s coordinates to let the performance free bilinear filtering do the blending.

For our demo here, wrong tool for the job. Really, we didn’t do FXAA justice with our example. FXAA was created for another use case and has many settings and presets. It was created to anti-alias more complex scenes. Let’s give it a fair shot!

#### FXAA full demo [#](https://blog.frost.kiwi#fxaa-full-demo)

A scene from my favorite piece of software in existence: [NeoTokyo°](https://store.steampowered.com/app/244630/NEOTOKYO/). I created a bright area light in an NT° map and moved a bench to create an area of strong aliasing. The following demo uses the aliased output from [NeoTokyo°](https://store.steampowered.com/app/244630/NEOTOKYO/), calculates the required luminance channel and applies FXAA. All FXAA presets and settings at your finger tips.

This has fixed resolution and will only be at you device's native resolution, if your device has no dpi scaling and the browser is at 100% zoom.

`FXAA_QUALITY_PRESET` | |||
`FXAA_QUALITY_PRESET` | |||
`fxaaQualitySubpix` | |||
`fxaaQualitySubpix` | |||
`fxaaQualityEdgeThreshold` | |||
`fxaaQualityEdgeThreshold` | |||
`fxaaQualityEdgeThresholdMin` | |||
`fxaaQualityEdgeThresholdMin` | |||

## WebGL Vertex Shader

[FXAA-interactive.vs]`/* Our Vertex data for the Quad */ attribute vec2 vtx; varying vec2 uv; void main() { /* FXAA expects flipped, DirectX style UV coordinates */ uv = vtx * vec2(0.5, -0.5) + 0.5; gl_Position = vec4(vtx, 0.0, 1.0); }`

## WebGL Fragment Shader

[FXAA-interactive.fs]`precision highp float; varying vec2 uv; uniform sampler2D texture; uniform vec2 RcpFrame; uniform float u_fxaaQualitySubpix; uniform float u_fxaaQualityEdgeThreshold; uniform float u_fxaaQualityEdgeThresholdMin; /*============================================================================ FXAA QUALITY - PRESETS ============================================================================*/ /*============================================================================ FXAA QUALITY - MEDIUM DITHER PRESETS ============================================================================*/ #if (FXAA_QUALITY_PRESET == 10) #define FXAA_QUALITY_PS 3 #define FXAA_QUALITY_P0 1.5 #define FXAA_QUALITY_P1 3.0 #define FXAA_QUALITY_P2 12.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 11) #define FXAA_QUALITY_PS 4 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 3.0 #define FXAA_QUALITY_P3 12.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 12) #define FXAA_QUALITY_PS 5 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 4.0 #define FXAA_QUALITY_P4 12.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 13) #define FXAA_QUALITY_PS 6 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 4.0 #define FXAA_QUALITY_P5 12.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 14) #define FXAA_QUALITY_PS 7 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 4.0 #define FXAA_QUALITY_P6 12.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 15) #define FXAA_QUALITY_PS 8 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 2.0 #define FXAA_QUALITY_P6 4.0 #define FXAA_QUALITY_P7 12.0 #endif /*============================================================================ FXAA QUALITY - LOW DITHER PRESETS ============================================================================*/ #if (FXAA_QUALITY_PRESET == 20) #define FXAA_QUALITY_PS 3 #define FXAA_QUALITY_P0 1.5 #define FXAA_QUALITY_P1 2.0 #define FXAA_QUALITY_P2 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 21) #define FXAA_QUALITY_PS 4 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 22) #define FXAA_QUALITY_PS 5 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 23) #define FXAA_QUALITY_PS 6 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 24) #define FXAA_QUALITY_PS 7 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 3.0 #define FXAA_QUALITY_P6 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 25) #define FXAA_QUALITY_PS 8 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 2.0 #define FXAA_QUALITY_P6 4.0 #define FXAA_QUALITY_P7 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 26) #define FXAA_QUALITY_PS 9 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 2.0 #define FXAA_QUALITY_P6 2.0 #define FXAA_QUALITY_P7 4.0 #define FXAA_QUALITY_P8 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 27) #define FXAA_QUALITY_PS 10 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 2.0 #define FXAA_QUALITY_P6 2.0 #define FXAA_QUALITY_P7 2.0 #define FXAA_QUALITY_P8 4.0 #define FXAA_QUALITY_P9 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 28) #define FXAA_QUALITY_PS 11 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 2.0 #define FXAA_QUALITY_P6 2.0 #define FXAA_QUALITY_P7 2.0 #define FXAA_QUALITY_P8 2.0 #define FXAA_QUALITY_P9 4.0 #define FXAA_QUALITY_P10 8.0 #endif /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PRESET == 29) #define FXAA_QUALITY_PS 12 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.5 #define FXAA_QUALITY_P2 2.0 #define FXAA_QUALITY_P3 2.0 #define FXAA_QUALITY_P4 2.0 #define FXAA_QUALITY_P5 2.0 #define FXAA_QUALITY_P6 2.0 #define FXAA_QUALITY_P7 2.0 #define FXAA_QUALITY_P8 2.0 #define FXAA_QUALITY_P9 2.0 #define FXAA_QUALITY_P10 4.0 #define FXAA_QUALITY_P11 8.0 #endif /*============================================================================ FXAA QUALITY - EXTREME QUALITY ============================================================================*/ #if (FXAA_QUALITY_PRESET == 39) #define FXAA_QUALITY_PS 12 #define FXAA_QUALITY_P0 1.0 #define FXAA_QUALITY_P1 1.0 #define FXAA_QUALITY_P2 1.0 #define FXAA_QUALITY_P3 1.0 #define FXAA_QUALITY_P4 1.0 #define FXAA_QUALITY_P5 1.5 #define FXAA_QUALITY_P6 2.0 #define FXAA_QUALITY_P7 2.0 #define FXAA_QUALITY_P8 2.0 #define FXAA_QUALITY_P9 2.0 #define FXAA_QUALITY_P10 4.0 #define FXAA_QUALITY_P11 8.0 #endif /*============================================================================ GREEN AS LUMA OPTION SUPPORT FUNCTION ============================================================================*/ #if (FXAA_GREEN_AS_LUMA == 0) float FxaaLuma(vec4 rgba) { return rgba.w; } #else float FxaaLuma(vec4 rgba) { return rgba.y; } #endif /*============================================================================ FXAA3 QUALITY - PC ============================================================================*/ vec4 FxaaPixelShader( // // Use noperspective interpolation here (turn off perspective interpolation). // {xy} = center of pixel vec2 pos, // // Input color texture. // {rgb_} = color in linear or perceptual color space // if (FXAA_GREEN_AS_LUMA == 0) // {__a} = luma in perceptual color space (not linear) sampler2D tex, // // Only used on FXAA Quality. // This must be from a constant/uniform. // {x_} = 1.0/screenWidthInPixels // {_y} = 1.0/screenHeightInPixels vec2 fxaaQualityRcpFrame, // // Only used on FXAA Quality. // This used to be the FXAA_QUALITY_SUBPIX define. // It is here now to allow easier tuning. // Choose the amount of sub-pixel aliasing removal. // This can effect sharpness. // 1.00 - upper limit (softer) // 0.75 - default amount of filtering // 0.50 - lower limit (sharper, less sub-pixel aliasing removal) // 0.25 - almost off // 0.00 - completely off float fxaaQualitySubpix, // // Only used on FXAA Quality. // This used to be the FXAA_QUALITY_EDGE_THRESHOLD define. // It is here now to allow easier tuning. // The minimum amount of local contrast required to apply algorithm. // 0.333 - too little (faster) // 0.250 - low quality // 0.166 - default // 0.125 - high quality // 0.063 - overkill (slower) float fxaaQualityEdgeThreshold, // // Only used on FXAA Quality. // This used to be the FXAA_QUALITY_EDGE_THRESHOLD_MIN define. // It is here now to allow easier tuning. // Trims the algorithm from processing darks. // 0.0833 - upper limit (default, the start of visible unfiltered edges) // 0.0625 - high quality (faster) // 0.0312 - visible limit (slower) // Special notes when using FXAA_GREEN_AS_LUMA, // Likely want to set this to zero. // As colors that are mostly not-green // will appear very dark in the green channel! // Tune by looking at mostly non-green content, // then start at zero and increase until aliasing is a problem. float fxaaQualityEdgeThresholdMin ) { /*--------------------------------------------------------------------------*/ vec2 posM; posM.x = pos.x; posM.y = pos.y; vec4 rgbyM = texture2D(tex, posM); #if (FXAA_GREEN_AS_LUMA == 0) #define lumaM rgbyM.w #else #define lumaM rgbyM.y #endif float lumaS = FxaaLuma(texture2D(tex, posM + (vec2(ivec2( 0, 1)) * fxaaQualityRcpFrame.xy))); float lumaE = FxaaLuma(texture2D(tex, posM + (vec2(ivec2( 1, 0)) * fxaaQualityRcpFrame.xy))); float lumaN = FxaaLuma(texture2D(tex, posM + (vec2(ivec2( 0,-1)) * fxaaQualityRcpFrame.xy))); float lumaW = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(-1, 0)) * fxaaQualityRcpFrame.xy))); /*--------------------------------------------------------------------------*/ float maxSM = max(lumaS, lumaM); float minSM = min(lumaS, lumaM); float maxESM = max(lumaE, maxSM); float minESM = min(lumaE, minSM); float maxWN = max(lumaN, lumaW); float minWN = min(lumaN, lumaW); float rangeMax = max(maxWN, maxESM); float rangeMin = min(minWN, minESM); float rangeMaxScaled = rangeMax * fxaaQualityEdgeThreshold; float range = rangeMax - rangeMin; float rangeMaxClamped = max(fxaaQualityEdgeThresholdMin, rangeMaxScaled); bool earlyExit = range < rangeMaxClamped; /*--------------------------------------------------------------------------*/ if(earlyExit) return rgbyM; /*--------------------------------------------------------------------------*/ float lumaNW = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(-1,-1)) * fxaaQualityRcpFrame.xy))); float lumaSE = FxaaLuma(texture2D(tex, posM + (vec2(ivec2( 1, 1)) * fxaaQualityRcpFrame.xy))); float lumaNE = FxaaLuma(texture2D(tex, posM + (vec2(ivec2( 1,-1)) * fxaaQualityRcpFrame.xy))); float lumaSW = FxaaLuma(texture2D(tex, posM + (vec2(ivec2(-1, 1)) * fxaaQualityRcpFrame.xy))); /*--------------------------------------------------------------------------*/ float lumaNS = lumaN + lumaS; float lumaWE = lumaW + lumaE; float subpixRcpRange = 1.0/range; float subpixNSWE = lumaNS + lumaWE; float edgeHorz1 = (-2.0 * lumaM) + lumaNS; float edgeVert1 = (-2.0 * lumaM) + lumaWE; /*--------------------------------------------------------------------------*/ float lumaNESE = lumaNE + lumaSE; float lumaNWNE = lumaNW + lumaNE; float edgeHorz2 = (-2.0 * lumaE) + lumaNESE; float edgeVert2 = (-2.0 * lumaN) + lumaNWNE; /*--------------------------------------------------------------------------*/ float lumaNWSW = lumaNW + lumaSW; float lumaSWSE = lumaSW + lumaSE; float edgeHorz4 = (abs(edgeHorz1) * 2.0) + abs(edgeHorz2); float edgeVert4 = (abs(edgeVert1) * 2.0) + abs(edgeVert2); float edgeHorz3 = (-2.0 * lumaW) + lumaNWSW; float edgeVert3 = (-2.0 * lumaS) + lumaSWSE; float edgeHorz = abs(edgeHorz3) + edgeHorz4; float edgeVert = abs(edgeVert3) + edgeVert4; /*--------------------------------------------------------------------------*/ float subpixNWSWNESE = lumaNWSW + lumaNESE; float lengthSign = fxaaQualityRcpFrame.x; bool horzSpan = edgeHorz >= edgeVert; float subpixA = subpixNSWE * 2.0 + subpixNWSWNESE; /*--------------------------------------------------------------------------*/ if(!horzSpan) lumaN = lumaW; if(!horzSpan) lumaS = lumaE; if(horzSpan) lengthSign = fxaaQualityRcpFrame.y; float subpixB = (subpixA * (1.0/12.0)) - lumaM; /*--------------------------------------------------------------------------*/ float gradientN = lumaN - lumaM; float gradientS = lumaS - lumaM; float lumaNN = lumaN + lumaM; float lumaSS = lumaS + lumaM; bool pairN = abs(gradientN) >= abs(gradientS); float gradient = max(abs(gradientN), abs(gradientS)); if(pairN) lengthSign = -lengthSign; float subpixC = clamp(abs(subpixB) * subpixRcpRange, 0.0, 1.0); /*--------------------------------------------------------------------------*/ vec2 posB; posB.x = posM.x; posB.y = posM.y; vec2 offNP; offNP.x = (!horzSpan) ? 0.0 : fxaaQualityRcpFrame.x; offNP.y = ( horzSpan) ? 0.0 : fxaaQualityRcpFrame.y; if(!horzSpan) posB.x += lengthSign * 0.5; if( horzSpan) posB.y += lengthSign * 0.5; /*--------------------------------------------------------------------------*/ vec2 posN; posN.x = posB.x - offNP.x * FXAA_QUALITY_P0; posN.y = posB.y - offNP.y * FXAA_QUALITY_P0; vec2 posP; posP.x = posB.x + offNP.x * FXAA_QUALITY_P0; posP.y = posB.y + offNP.y * FXAA_QUALITY_P0; float subpixD = ((-2.0)*subpixC) + 3.0; float lumaEndN = FxaaLuma(texture2D(tex, posN)); float subpixE = subpixC * subpixC; float lumaEndP = FxaaLuma(texture2D(tex, posP)); /*--------------------------------------------------------------------------*/ if(!pairN) lumaNN = lumaSS; float gradientScaled = gradient * 1.0/4.0; float lumaMM = lumaM - lumaNN * 0.5; float subpixF = subpixD * subpixE; bool lumaMLTZero = lumaMM < 0.0; /*--------------------------------------------------------------------------*/ lumaEndN -= lumaNN * 0.5; lumaEndP -= lumaNN * 0.5; bool doneN = abs(lumaEndN) >= gradientScaled; bool doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P1; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P1; bool doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P1; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P1; /*--------------------------------------------------------------------------*/ if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P2; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P2; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P2; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P2; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 3) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P3; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P3; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P3; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P3; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 4) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P4; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P4; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P4; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P4; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 5) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P5; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P5; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P5; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P5; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 6) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P6; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P6; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P6; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P6; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 7) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P7; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P7; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P7; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P7; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 8) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P8; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P8; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P8; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P8; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 9) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P9; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P9; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P9; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P9; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 10) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P10; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P10; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P10; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P10; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 11) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P11; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P11; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P11; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P11; /*--------------------------------------------------------------------------*/ #if (FXAA_QUALITY_PS > 12) if(doneNP) { if(!doneN) lumaEndN = FxaaLuma(texture2D(tex, posN.xy)); if(!doneP) lumaEndP = FxaaLuma(texture2D(tex, posP.xy)); if(!doneN) lumaEndN = lumaEndN - lumaNN * 0.5; if(!doneP) lumaEndP = lumaEndP - lumaNN * 0.5; doneN = abs(lumaEndN) >= gradientScaled; doneP = abs(lumaEndP) >= gradientScaled; if(!doneN) posN.x -= offNP.x * FXAA_QUALITY_P12; if(!doneN) posN.y -= offNP.y * FXAA_QUALITY_P12; doneNP = (!doneN) || (!doneP); if(!doneP) posP.x += offNP.x * FXAA_QUALITY_P12; if(!doneP) posP.y += offNP.y * FXAA_QUALITY_P12; /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } #endif /*--------------------------------------------------------------------------*/ } /*--------------------------------------------------------------------------*/ float dstN = posM.x - posN.x; float dstP = posP.x - posM.x; if(!horzSpan) dstN = posM.y - posN.y; if(!horzSpan) dstP = posP.y - posM.y; /*--------------------------------------------------------------------------*/ bool goodSpanN = (lumaEndN < 0.0) != lumaMLTZero; float spanLength = (dstP + dstN); bool goodSpanP = (lumaEndP < 0.0) != lumaMLTZero; float spanLengthRcp = 1.0/spanLength; /*--------------------------------------------------------------------------*/ bool directionN = dstN < dstP; float dst = min(dstN, dstP); bool goodSpan = directionN ? goodSpanN : goodSpanP; float subpixG = subpixF * subpixF; float pixelOffset = (dst * (-spanLengthRcp)) + 0.5; float subpixH = subpixG * fxaaQualitySubpix; /*--------------------------------------------------------------------------*/ float pixelOffsetGood = goodSpan ? pixelOffset : 0.0; float pixelOffsetSubpix = max(pixelOffsetGood, subpixH); if(!horzSpan) posM.x += pixelOffsetSubpix * lengthSign; if( horzSpan) posM.y += pixelOffsetSubpix * lengthSign; return vec4(texture2D(tex, posM).xyz, lumaM); } void main(void) { #if (FXAA_LUMA) #if (FXAA_GREEN_AS_LUMA) gl_FragColor = vec4(texture2D(texture, uv).ggg, 1.0); #else gl_FragColor = vec4(texture2D(texture, uv).aaa, 1.0); #endif #elif (FXAA_ENABLE) gl_FragColor = FxaaPixelShader( uv, texture, RcpFrame, u_fxaaQualitySubpix, u_fxaaQualityEdgeThreshold, u_fxaaQualityEdgeThresholdMin); #else gl_FragColor = vec4(texture2D(texture, uv).rgb, 1.0); #endif }`

## WebGL Javascript

[FXAA-interactive.js]`"use strict"; async function loadFrame(gl, path) { const response = await fetch(path); const blob = await response.blob(); const bitmap = await createImageBitmap(blob, { colorSpaceConversion: 'none' }); const target = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, target); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, bitmap); bitmap.close(); return target; } async function loadAllFrames(gl, start, end) { const framePromises = []; const totalFrames = end - start + 1; let loadedFrames = 0; const loadingOverlay = document.getElementById('loading-overlay'); loadingOverlay.style.display = 'flex'; function updateLoadingProgress() { const percentage = Math.floor((loadedFrames / totalFrames) * 100); loadingOverlay.innerHTML = `Loading... ${percentage}%`; if (loadedFrames === totalFrames) loadingOverlay.style.display = 'none'; } for (let i = start; i <= end; i++) { const path = `frames/${i}.png`; const framePromise = loadFrame(gl, path).then(texture => { loadedFrames++; updateLoadingProgress(); return texture; }); framePromises.push(framePromise); } const textures = await Promise.all(framePromises); return textures; } function setupFXAAInteractive(canvasId, simpleVtxSrc, simpleFragSrc, vertexLumaSrc, lumaFragSrc, blitVtxSrc, blitFragSrc, redVtxSrc, redFragSrc) { /* Init */ const canvas = document.getElementById(canvasId); const gl = canvas.getContext('webgl', { preserveDrawingBuffer: false, antialias: false, alpha: false, premultipliedAlpha: false } ); let lumaBuffer, lumaTexture, blitBuffer, blitTexture; let enableFXAA = true; let enableRed = true; let showLuma = false; let greenLuma = false; let pause = false; let fxaaQualityPreset = 12; /* Shaders */ /* Passthrough Shader */ let fxaaShd; let rcpFrameLocation; let fxaaQualitySubpixLocation; let fxaaQualityEdgeThresholdLocation; let fxaaQualityEdgeThresholdMinLocation; function updateFXAAShader() { if (fxaaShd) { gl.deleteProgram(fxaaShd); } const prefix = ` #define FXAA_QUALITY_PRESET ${fxaaQualityPreset} #define FXAA_GREEN_AS_LUMA ${greenLuma ? 1 : 0} #define FXAA_ENABLE ${enableFXAA ? 1 : 0} #define FXAA_LUMA ${showLuma ? 1 : 0} `; fxaaShd = compileAndLinkShader(gl, simpleVtxSrc, simpleFragSrc, prefix); rcpFrameLocation = gl.getUniformLocation(fxaaShd, "RcpFrame"); fxaaQualitySubpixLocation = gl.getUniformLocation(fxaaShd, "u_fxaaQualitySubpix"); fxaaQualityEdgeThresholdLocation = gl.getUniformLocation(fxaaShd, "u_fxaaQualityEdgeThreshold"); fxaaQualityEdgeThresholdMinLocation = gl.getUniformLocation(fxaaShd, "u_fxaaQualityEdgeThresholdMin"); } updateFXAAShader(); const lumaShd = compileAndLinkShader(gl, vertexLumaSrc, lumaFragSrc); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); /* Simple Red Box */ const redShd = compileAndLinkShader(gl, redVtxSrc, redFragSrc); const transformLocationRed = gl.getUniformLocation(redShd, "transform"); const offsetLocationRed = gl.getUniformLocation(redShd, "offset"); const aspect_ratioLocationRed = gl.getUniformLocation(redShd, "aspect_ratio"); const thicknessLocation = gl.getUniformLocation(redShd, "thickness"); const pixelsizeLocation = gl.getUniformLocation(redShd, "pixelsize"); /* Load frames */ let framesLoaded = false; let textures = []; /* Vertex Buffer of a simple Quad with some colors */ const unitQuad = new Float32Array([ -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, ]); const trackedCoords = [ [357.250, 206.375], [356.602, 207.301], [356.309, 207.559], [354.832, 208.711], [353.121, 209.863], [350.578, 211.102], [347.594, 212.336], [343.457, 214.652], [338.086, 216.977], [332.803, 219.934], [327.791, 222.625], [324.259, 224.398], [319.233, 227.902], [315.627, 231.492], [315.381, 233.305], [314.672, 234.145], [314.616, 235.363], [315.028, 236.508], [316.072, 237.676], [317.366, 238.301], [317.657, 239.703], [319.354, 240.016], [320.018, 241.277], [321.091, 241.785], [321.726, 241.777], [321.824, 242.117], [322.334, 242.109], [322.082, 242.965], [322.100, 242.965] ]; function applyTrackingData(index, location) { const x = (trackedCoords[index][0] / canvas.width) * 2 - 1; const y = 1 - (trackedCoords[index][1] / canvas.height) * 2; gl.uniform2f(location, x, y); } function setupBuffers() { gl.deleteFramebuffer(lumaBuffer); lumaBuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, lumaBuffer); lumaTexture = setupTexture(gl, canvas.width, canvas.height, lumaTexture, gl.LINEAR); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, lumaTexture, 0); gl.deleteFramebuffer(blitBuffer); blitBuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, blitBuffer); blitTexture = setupTexture(gl, canvas.width, canvas.height, blitTexture, gl.NEAREST); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, blitTexture, 0); } const fxaaCheckbox = document.getElementById('fxaaCheck'); fxaaCheckbox.addEventListener('change', () => { enableFXAA = fxaaCheckbox.checked; updateFXAAShader(); redraw(); }); const redCheckbox = document.getElementById('redCheck'); redCheckbox.addEventListener('change', () => { enableRed = redCheckbox.checked; redraw(); }); const pauseCheckbox = document.getElementById('pauseCheck'); pauseCheckbox.addEventListener('change', () => { pause = !pauseCheckbox.checked; redraw(); }); const lumaCheckbox = document.getElementById('lumaCheck'); lumaCheckbox.addEventListener('change', () => { showLuma = lumaCheckbox.checked; updateFXAAShader(); redraw(); }); const greenCheckbox = document.getElementById('greenCheck'); greenCheckbox.addEventListener('change', () => { greenLuma = greenCheckbox.checked; updateFXAAShader(); redraw(); }); /* FXAA Parameters */ const fxaaQualityPresetSelect = document.getElementById('FXAA_QUALITY_PRESET'); fxaaQualityPresetSelect.addEventListener('change', function () { fxaaQualityPreset = parseInt(fxaaQualityPresetSelect.value); updateFXAAShader(); redraw(); }); let fxaaQualitySubpix = 0.75; let fxaaQualityEdgeThreshold = 0.166; let fxaaQualityEdgeThresholdMin = 0.0833; const fxaaQualitySubpixRange = document.getElementById('fxaaQualitySubpixRange'); const fxaaQualityEdgeThresholdRange = document.getElementById('fxaaQualityEdgeThresholdRange'); const fxaaQualityEdgeThresholdMinRange = document.getElementById('fxaaQualityEdgeThresholdMinRange'); fxaaQualitySubpixRange.addEventListener('input', function () { fxaaQualitySubpix = parseFloat(fxaaQualitySubpixRange.value); redraw(); }); fxaaQualityEdgeThresholdRange.addEventListener('input', function () { fxaaQualityEdgeThreshold = parseFloat(fxaaQualityEdgeThresholdRange.value); redraw(); }); fxaaQualityEdgeThresholdMinRange.addEventListener('input', function () { fxaaQualityEdgeThresholdMin = parseFloat(fxaaQualityEdgeThresholdMinRange.value); redraw(); }); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0); gl.enableVertexAttribArray(0); let last_time = 0; let redrawActive = false; canvas.width = 684; canvas.height = 480; gl.viewport(0, 0, 684, 480); const fps = 30; const frameDuration = 1000 / fps; const waitBetweenFramesMs = 1000; let frameIndex = 0; let lastFrameTime = 0; let forward = true; let delayActive = false; function redraw() { if (!isRendering || redrawActive || !framesLoaded) return; redrawActive = true; /* Setup PostProcess Framebuffer */ gl.bindFramebuffer(gl.FRAMEBUFFER, lumaBuffer); gl.disable(gl.BLEND); gl.bindTexture(gl.TEXTURE_2D, textures[frameIndex]); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(lumaShd); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw To Screen */ gl.bindFramebuffer(gl.FRAMEBUFFER, blitBuffer); gl.bindTexture(gl.TEXTURE_2D, lumaTexture); gl.useProgram(fxaaShd); gl.clear(gl.COLOR_BUFFER_BIT); /* FXAA Arguments */ gl.uniform2f(rcpFrameLocation, 1.0 / canvas.width, 1.0 / canvas.height); gl.uniform1f(fxaaQualitySubpixLocation, fxaaQualitySubpix); gl.uniform1f(fxaaQualityEdgeThresholdLocation, fxaaQualityEdgeThreshold); gl.uniform1f(fxaaQualityEdgeThresholdMinLocation, fxaaQualityEdgeThresholdMin); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.bindTexture(gl.TEXTURE_2D, blitTexture); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Scaled image in the bottom left */ gl.uniform4f(transformLocation, 0.25, 0.25, -0.75, -0.75); applyTrackingData(frameIndex, offsetLocationPost); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(redShd); gl.uniform1f(aspect_ratioLocationRed, canvas.width / canvas.height - 1.0); gl.uniform1f(thicknessLocation, 0.2); gl.uniform1f(pixelsizeLocation, (1.0 / canvas.width) * 50); gl.uniform4f(transformLocationRed, 0.25, 0.25, 0, 0); applyTrackingData(frameIndex, offsetLocationRed); if (enableRed) gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.uniform1f(thicknessLocation, 0.1); gl.uniform1f(pixelsizeLocation, 0.0); gl.uniform4f(transformLocationRed, 0.5, 0.5, 0.0, 0.0); gl.uniform2f(offsetLocationRed, -0.75, -0.75); if (enableRed) gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); redrawActive = false; } let isRendering = false; function renderLoop(time) { if (isRendering) { const elapsed = time - lastFrameTime; if (elapsed >= frameDuration) { lastFrameTime = time - (elapsed % frameDuration); redraw(); if (forward) { if (!pause) frameIndex++; if (frameIndex == 29) { frameIndex = 28; forward = false; if (!delayActive) { delayActive = true; setTimeout(() => { delayActive = false; if (isRendering) requestAnimationFrame(renderLoop); }, waitBetweenFramesMs); return; } } } else { if(!pause) frameIndex--; if (frameIndex < 0) { forward = true; frameIndex = 0; if (!delayActive) { delayActive = true; setTimeout(() => { delayActive = false; if (isRendering) requestAnimationFrame(renderLoop); }, waitBetweenFramesMs); return; } } } } if (!delayActive) { requestAnimationFrame(renderLoop); } } } async function handleIntersection(entries) { for (const entry of entries) { if (entry.isIntersecting) { if (!isRendering) { /* Start rendering, when canvas visible */ isRendering = true; /* Load all frames and await the result */ textures = await loadAllFrames(gl, 0, 28); setupBuffers(); framesLoaded = true; renderLoop(last_time); } } else { /* Stop another redraw being called */ isRendering = false; while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality, this code block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the textures to free up memory */ if (framesLoaded) { textures.forEach(texture => { gl.deleteTexture(texture); }); gl.deleteTexture(lumaTexture); gl.deleteFramebuffer(lumaBuffer); gl.deleteTexture(blitTexture); gl.deleteFramebuffer(blitBuffer); textures = []; framesLoaded = false; } } } } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


Just looking at the [full FXAA 3.11 source](https://github.com/FrostKiwi/treasurechest/blob/main/posts/analytical-anti-aliasing/shader/FXAA-3.11.glsl), you can see the passion in every line. Portable [across OpenGL and DirectX](https://github.com/FrostKiwi/treasurechest/blob/main/posts/analytical-anti-aliasing/shader/FXAA-3.11.glsl#L611), a [PC version](https://github.com/FrostKiwi/treasurechest/blob/main/posts/analytical-anti-aliasing/shader/FXAA-3.11.glsl#L716), a [XBOX 360](https://github.com/FrostKiwi/treasurechest/blob/main/posts/analytical-anti-aliasing/shader/FXAA-3.11.glsl#L1341) version, two finely optimized [PS3 versions](https://github.com/FrostKiwi/treasurechest/blob/main/posts/analytical-anti-aliasing/shader/FXAA-3.11.glsl#L1437) fighting for every GPU cycle, [including shader disassambly](https://github.com/FrostKiwi/treasurechest/blob/main/posts/analytical-anti-aliasing/shader/FXAA-3.11.glsl#L1450). Such level of professionalism and dedication, shared with the world in plain text.

The sharing and openness is why I'm in love with graphics programming.

It may be performance cheap, but only if you already have post-processing in place or do [deferred shading](https://en.wikipedia.org/wiki/Deferred_shading). Especially in mobile graphics, memory access is expensive, so saving the framebuffer to perform post processing is not always a given. If you need to setup render-to-texture in order to have FXAA, then the “F” in FXAA evaporates.

In this article we won’t jump into modern [temporal anti-aliasing](https://sugulee.wordpress.com/2021/06/21/temporal-anti-aliasingtaa-tutorial/), but before FXAA was even developed, [TAA was already experimented](https://x.com/NOTimothyLottes/status/1756732098402992584) with. In fact, FXAA was supposed to [get a new version 4](https://web.archive.org/web/20120120082725/http://timothylottes.blogspot.com/2011/12/fxaa-40-stills-and-features.html) and [incorporate temporal anti aliasing](https://web.archive.org/web/20120120070945/http://timothylottes.blogspot.com/2011/12/big-fxaa-update-soon.html) in addition [to the standard spatial one](https://web.archive.org/web/20120120072820/http://timothylottes.blogspot.com/2011/12/fxaa-40-will-have-new-spatial-only.html), but instead it evolved further and rebranded into [TXAA](https://web.archive.org/web/20210116205348/https://www.nvidia.com/en-gb/geforce/technologies/txaa/technology/).

## Analytical Anti Aliasing [#](https://blog.frost.kiwi#analytical-anti-aliasing)

Now we get to the good stuff. Analytical Anti-Aliasing approaches the problem backwards - it knows the shape you need and draws the pixel already Anti-Aliased to the screen. Whilst drawing the 2D or 3D shape you need, it fades the shape’s border by exactly one pixel.

## WebGL Vertex Shader

[circle-analytical.vs]`/* Our Vertex data for the Quad */ attribute vec2 vtx; attribute vec3 col; /* The coordinates that will be used to for our drawing operations */ varying vec2 uv; /* Color for the fragment shader */ varying vec3 color; /* Fragment shader needs to know the pixel size and since we mess with the quad to expand it by 1 pixel to not change the final pixel size, we need to give the fragment shader the corrected pixel size */ varying float pixelSizeAdjusted; /* Aspect ratio */ uniform float aspect_ratio; /* Position offset for the animation */ uniform vec2 offset; /* Size of the Unit Quad */ uniform float size; /* Pixel size in regards to the Quad */ uniform float pixelSize; void main() { /* Assign the verticies to be used as the distance field for drawing. This will be linearly interpolated before going to the fragment shader */ uv = vtx; /* Sending some nice color to the fragment shader */ color = col; vec2 vertex = vtx; /* correct for aspect ratio */ vertex.x *= aspect_ratio; /* Grow the Quad and thus the "canvas", that the circle is drawn on. The pixelSize is added for two reasons: 0.5px to get the original circle size again, as the AAA fading is set to fade the edge on the circle inside, preventing hard edges due to unrasterized pixels. And another 0.5px is to correct the "breathing room" added in the fragment shader, specifically for the MSAA sampling case, as hardware specific issues around MSAA sampling may or may not result in transparent pixels disappearing too soon. */ vertex *= size + pixelSize; /* Calculate the true pixel size, after we messed with the quad's size */ pixelSizeAdjusted = pixelSize / (size + pixelSize); /* Make the circle move in a circle, heh :] */ vertex += offset; /* Vertex Output */ gl_Position = vec4(vertex, 0.0, 1.0); }`

## WebGL Fragment Shader

[circle-analytical.fs]`precision mediump float; /* uv coordinates from the vertex shader */ varying vec2 uv; /* color from the vertex shader */ varying vec3 color; /* pixel size from the vertex shader, corrected for influence of size changes */ varying float pixelSizeAdjusted; void main(void) { /* Our signed distance field of a point */ float dist = length(uv); /* We add half a pixel of breathing room. This is only required for the MSAA case. Depending on Hardware implementation, rasterization, MSAA sample count and placement, one row of pixels may or may not disappear too soon, when the circle's edge is right up against the unit quad's border */ dist += pixelSizeAdjusted * 0.5; /* Fade out the pixels near the edge of the circle with exactly the size of one pixel, so we get pixel perfect Anti-Aliasing. */ float alpha = (1.0 - dist) / pixelSizeAdjusted; /* Clamped and scaled uv.y added to color simply to make the bottom of the circle white, so the contrast is high and you can see strong aliasing */ gl_FragColor = vec4(color + clamp( - uv.y * 0.4, 0.0, 1.0), alpha); }`

## WebGL Javascript

[circleAnalytical.js]`function setupAnalytical(canvasId, circleVtxSrc, circleFragSrc, blitVtxSrc, blitFragSrc, redVtxSrc, redFragSrc, radioName, radioSmoothSize) { /* Init */ const canvas = document.getElementById(canvasId); let circleDrawFramebuffer, frameTexture; let buffersInitialized = false; let resDiv = 1; let pixelSmoothSize = 1; const gl = canvas.getContext('webgl', { preserveDrawingBuffer: false, antialias: false, alpha: true } ); /* Render Resolution */ const radios = document.querySelectorAll(`input[name="${radioName}"]`); radios.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { resDiv = event.target.value; stopRendering(); startRendering(); }); }); /* Smooth Size */ const radiosSmooth = document.querySelectorAll(`input[name="${radioSmoothSize}"]`); radiosSmooth.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { pixelSmoothSize = event.target.value; stopRendering(); startRendering(); }); }); /* Shaders */ /* Circle Shader */ const circleShd = compileAndLinkShader(gl, circleVtxSrc, circleFragSrc); const aspect_ratioLocation = gl.getUniformLocation(circleShd, "aspect_ratio"); const offsetLocationCircle = gl.getUniformLocation(circleShd, "offset"); const pixelSizeCircle = gl.getUniformLocation(circleShd, "pixelSize"); const sizeLocationCircle = gl.getUniformLocation(circleShd, "size"); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); /* Simple Red Box */ const redShd = compileAndLinkShader(gl, redVtxSrc, redFragSrc); const transformLocationRed = gl.getUniformLocation(redShd, "transform"); const offsetLocationRed = gl.getUniformLocation(redShd, "offset"); const aspect_ratioLocationRed = gl.getUniformLocation(redShd, "aspect_ratio"); const thicknessLocation = gl.getUniformLocation(redShd, "thickness"); const pixelsizeLocation = gl.getUniformLocation(redShd, "pixelsize"); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT); gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); setupTextureBuffers(); const circleOffsetAnim = new Float32Array([ 0.0, 0.0 ]); let aspect_ratio = 0; let last_time = 0; let redrawActive = false; function setupTextureBuffers() { gl.deleteFramebuffer(circleDrawFramebuffer); circleDrawFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); frameTexture = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTexture, gl.NEAREST); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTexture, 0); buffersInitialized = true; } gl.enable(gl.BLEND); function redraw(time) { redrawActive = true; if (!buffersInitialized) { setupTextureBuffers(); } last_time = time; /* Setup PostProcess Framebuffer */ gl.viewport(0, 0, canvas.width / resDiv, canvas.height / resDiv); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(circleShd); /* Draw Circle Animation */ gl.uniform1f(pixelSizeCircle, (2.0 / (canvas.height / resDiv)) * pixelSmoothSize); gl.uniform1f(aspect_ratioLocation, aspect_ratio); var radius = 0.1; var speed = (time / 10000) % Math.PI * 2; circleOffsetAnim[0] = radius * Math.cos(speed) + 0.1; circleOffsetAnim[1] = radius * Math.sin(speed); gl.uniform2fv(offsetLocationCircle, circleOffsetAnim); gl.uniform1f(sizeLocationCircle, circleSize); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.viewport(0, 0, canvas.width, canvas.height); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Scaled image in the bottom left */ gl.uniform4f(transformLocation, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationPost, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(redShd); gl.uniform1f(aspect_ratioLocationRed, (1.0 / aspect_ratio) - 1.0); gl.uniform1f(thicknessLocation, 0.2); gl.uniform1f(pixelsizeLocation, (1.0 / canvas.width) * 50); gl.uniform4f(transformLocationRed, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationRed, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.uniform1f(thicknessLocation, 0.1); gl.uniform1f(pixelsizeLocation, 0.0); gl.uniform4f(transformLocationRed, 0.5, 0.5, 0.0, 0.0); gl.uniform2f(offsetLocationRed, -0.75, -0.75); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); redrawActive = false; } let isRendering = false; let animationFrameId; function onResize() { const dipRect = canvas.getBoundingClientRect(); const width = Math.round(devicePixelRatio * dipRect.right) - Math.round(devicePixelRatio * dipRect.left); const height = Math.round(devicePixelRatio * dipRect.bottom) - Math.round(devicePixelRatio * dipRect.top); if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; setupTextureBuffers(); aspect_ratio = 1.0 / (width / height); stopRendering(); startRendering(); } } window.addEventListener('resize', onResize, true); onResize(); function renderLoop(time) { if (isRendering) { redraw(time); animationFrameId = requestAnimationFrame(renderLoop); } } function startRendering() { /* Start rendering, when canvas visible */ isRendering = true; renderLoop(last_time); } function stopRendering() { /* Stop another redraw being called */ isRendering = false; cancelAnimationFrame(animationFrameId); while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality this code is block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the important buffer to free up memory */ gl.deleteTexture(frameTexture); gl.deleteFramebuffer(circleDrawFramebuffer); buffersInitialized = false; } function handleIntersection(entries) { entries.forEach(entry => { if (entry.isIntersecting) { if (!isRendering) startRendering(); } else { stopRendering(); } }); } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


Always smooth without artifacts and you can adjust the amount of filtering. Preserves shape even at low resolutions. No extra buffers or extra hardware requirements.

Even runs on basic WebGL 1.0 or OpenGLES 2.0, without any extensions.

With the above buttons, you can set the smoothing to be equal to one pixel. This gives a sharp result, but comes with the caveat that axis-aligned 90° sides may still be perseved as “flat” in specific combinations of screen resolution, size and circle position.

Filtering based on the diagonal pixel size of `√2 px = 1.4142...`

, ensures the “tip” of the circle in axis-aligned pixel rows and columns is always non-opaque. This removes the perception of flatness, but makes the shape ever so slightly more blurry.

Or in other words: as soon as the border has an opaque pixel, there is already a transparent pixel "in front" of it.

This style of Anti-Aliasing is [usually implemented](http://www.numb3r23.net/2015/08/17/using-fwidth-for-distance-based-anti-aliasing/) with 3 ingredients:

- Enabled
[Screen Space Derivative](https://gamedev.stackexchange.com/a/130933)extension or having a modern graphics context - Pixel-size calculated via
+`length`

+`dFdx`

or approximated with`dFdy`

`fwidth`

- Blending with
`smoothstep`


But if you look at the code box above, you will find [circle-analytical.fs](https://blog.frost.kiwi/shader/circle-analytical.fs) having **none** of those. And this is the secret sauce we will look at. Before we dive into the implementation, let’s clear the elephants in the room…

### What even *is* “Analytical”? [#](https://blog.frost.kiwi#what-even-is-%E2%80%9Canalytical%E2%80%9D%3F)

In graphics programming, *Analytical* refers to effects created by knowing the make-up of the intended shape beforehand and performing calculations against the mathematical definition of said shape. This term is used ** very** loosely across computer graphics, similar to super sampling referring to multiple things, depending on context.

A picture is worth a thousand words...

![Character soft-shadow from stretched spheres in The Last Of Us](../../assets/66aaa3c1f25d589e.jpg)

[Lighting Technology of "The Last Of Us"](http://miciwan.com/SIGGRAPH2013/Lighting%20Technology%20of%20The%20Last%20Of%20Us.pdf), Siggraph 2013 talk by

[Michał Iwanicki](http://miciwan.com/)

Very soft soft-shadows which include [contact-hardening](http://wscg.zcu.cz/WSCG2012/short/B37-full.pdf), implemented by algorithms like [percentage-closer soft shadows](https://developer.download.nvidia.com/shaderlibrary/docs/shadow_PCSS.pdf) are very computationally intense and require both high resolution shadow maps and/or very aggressive filtering to not produce shimmering during movement.

This is why [Naughty Dog](https://en.wikipedia.org/wiki/Naughty_Dog)’s [The Last of Us](https://en.wikipedia.org/wiki/The_Last_of_Us) relied on getting soft-shadows on the main character by calculating the shadow from a rigidly defined formula of a stretched sphere, multiple of which were arranged in the shape of the main character, shown in red. An improved implementation with shader code can be seen in this [Shadertoy demo](https://www.shadertoy.com/view/3stcD4) by [romainguy](https://www.shadertoy.com/user/romainguy), with the modern [capsule](https://en.wikipedia.org/wiki/Capsule_(geometry)), as opposed to a stretched sphere.

This is now an integral part of modern game engines, [like Unreal](http://dev.epicgames.com/documentation/en-us/unreal-engine/capsule-shadows-overview-in-unreal-engine). As opposed to [standard shadow mapping](https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping), we don’t render the scene from the perspective of the light with finite resolution. We evaluate the shadow *per-pixel* against the mathematical equation of the stretched sphere or capsule. This makes capsule shadows ** analytical**.

A video is worth a thousand words, 30 times a second.

[YouTube Video](https://www.youtube.com/watch?v=1J6aAHLCbWg)by

["Max Lebled's 2nd channel"](https://www.youtube.com/@MaxLebled_ALT)

Staying with the Last of Us, [The Last of Us Part II](https://en.wikipedia.org/wiki/The_Last_of_Us_Part_II) uses the same logic for blurry real-time reflections of the main character, where [Screen Space Reflections](https://lettier.github.io/3d-game-shaders-for-beginners/screen-space-reflection.html) aren’t defined. Other options like [raytracing against the scene](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@8.2/manual/Ray-Traced-Reflections.html), or using a [real-time cubemap](https://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study/#environment-cubemap) like in [GTA V](https://en.wikipedia.org/wiki/Grand_Theft_Auto_V) are either noisy and low resolution or high resolution, but low performance.

Here the reflection calculation is part of the material shader, rendering against the rigidly defined mathematical shape of the capsule *per-pixel*, multiple of which are arranged in the shape of the main character. This makes capsule reflections ** analytical**.

An online demo is worth at least a million...

...yeah the joke is getting old.

![](../../assets/dc35852948264a66.png)

[Shadertoy demo](https://www.shadertoy.com/view/4djSDy)for Analytical Ambient Occlusion by

[Inigo Quilez](https://iquilezles.org/)

[Ambient Occlusion](https://learnopengl.com/Advanced-Lighting/SSAO) is essential in modern rendering, bringing contact shadows and approximating global illumination. Another topic as deep as the ocean, with so many implementations. Usually implemented by some form of “raytrace a bunch of rays and blur the result”.

In this [Shadertoy demo](https://www.shadertoy.com/view/4djSDy), the floor is evaluated *per-pixel* against the rigidly defined mathematical description of the sphere to get a soft, non-noisy, non-flickering occlusion contribution from the hovering ball. This implementation is ** analytical**. Not just spheres, there are

[analytical approaches](https://research.nvidia.com/sites/default/files/pubs/2010-06_Ambient-Occlusion-Volumes/McGuire10AOV.pdf)also for complex geometry.

By extension, Unreal Engine has distance field approaches for [Soft Shadows](https://dev.epicgames.com/documentation/en-us/unreal-engine/distance-field-soft-shadows-in-unreal-engine) and [Ambient Occlusion](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-distance-field-ambient-occlusion-in-unreal-engine), though one may argue, that this type of signed distance field rendering doesn’t fit the description of *analytical*, considering the distance field is precalculated into a 3D texture.

### Implementation [#](https://blog.frost.kiwi#implementation)

Let’s dive into the sauce. We work with [signed distance fields](https://www.youtube.com/watch?v=62-pRVZuS5c), where for every point that we sample, we know the distance to the desired shape. This information may be baked into a texture as done for [SDF text rendering](https://github.com/Chlumsky/msdf-atlas-gen) or may be derived *per-pixel* from a mathematical formula for simpler shapes like [bezier curves or hearts](https://iquilezles.org/articles/distfunctions2d/).

Based on that distance we fade out the border of the shape. If we fade by the size of one pixel, we get perfectly smooth edges, without any strange side effects. The secret sauce is in the implementation and [under the sauce](https://www.youtube.com/watch?v=bRL8v6--bW4) is where the magic is. *How* does the shader know the size of pixel? *How* do we blend based on distance?

This approach gives motion-stable pixel-perfection, but doesn't work with traditional rasterization. Thefullshape requires a signed distance field.

`Pixel size method` | |||
`Pixel size method` | |||
`Blend method` | |||
`Blend method` | |||
`Smoothing` | |||
`Smoothing` | px | ||
`Radius adjust ` | |||
`Radius adjust ` | px | ||

## WebGL Vertex Shader

[circle-analytical.vs]`/* Our Vertex data for the Quad */ attribute vec2 vtx; attribute vec3 col; /* The coordinates that will be used to for our drawing operations */ varying vec2 uv; /* Color for the fragment shader */ varying vec3 color; /* Fragment shader needs to know the pixel size and since we mess with the quad to expand it by 1 pixel to not change the final pixel size, we need to give the fragment shader the corrected pixel size */ varying float pixelSizeAdjusted; /* Aspect ratio */ uniform float aspect_ratio; /* Position offset for the animation */ uniform vec2 offset; /* Size of the Unit Quad */ uniform float size; /* Pixel size in regards to the Quad */ uniform float pixelSize; void main() { /* Assign the verticies to be used as the distance field for drawing. This will be linearly interpolated before going to the fragment shader */ uv = vtx; /* Sending some nice color to the fragment shader */ color = col; vec2 vertex = vtx; /* correct for aspect ratio */ vertex.x *= aspect_ratio; /* Grow the Quad and thus the "canvas", that the circle is drawn on. The pixelSize is added for two reasons: 0.5px to get the original circle size again, as the AAA fading is set to fade the edge on the circle inside, preventing hard edges due to unrasterized pixels. And another 0.5px is to correct the "breathing room" added in the fragment shader, specifically for the MSAA sampling case, as hardware specific issues around MSAA sampling may or may not result in transparent pixels disappearing too soon. */ vertex *= size + pixelSize; /* Calculate the true pixel size, after we messed with the quad's size */ pixelSizeAdjusted = pixelSize / (size + pixelSize); /* Make the circle move in a circle, heh :] */ vertex += offset; /* Vertex Output */ gl_Position = vec4(vertex, 0.0, 1.0); }`

## WebGL Fragment Shader

[circle-analyticalCompare.fs]`#if defined(FWIDTH) || defined(DFD) #extension GL_OES_standard_derivatives : enable #endif precision mediump float; /* uv coordinates from the vertex shader */ varying vec2 uv; /* color from the vertex shader */ varying vec3 color; /* pixel size from the vertex shader, corrected for resizing */ varying float pixelSizeAdjusted; /* How many pixels to shrink */ uniform float shrinkAmount; /* How many pixels to smooth */ uniform float smoothingAmount; /* Step function with Linear Interpolation, instead of Hermite Interpolation */ float linearstep(float edge0, float edge1, float x) { return clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0); } /* Step function with Linear Interpolation, but no clamping */ float linearstepNoclamp(float edge0, float edge1, float x) { return (x - edge0) / (edge1 - edge0); } void main(void) { /* The basic signed distance field of a point */ float dist = length(uv); /* Pixel size method */ #if defined(SIMPLE) float pixelSize = pixelSizeAdjusted; #elif defined(DFD) float pixelSize = length(vec2(dFdx(dist), dFdy(dist))); #elif defined(FWIDTH) float pixelSize = fwidth(dist); #endif /* Radius Adjust */ dist += pixelSize * shrinkAmount; /* Blend method */ #if defined(DIVISION) float alpha = (1.0 - dist) / (pixelSize * smoothingAmount); #elif defined(SMOOTHSTEP) float alpha = smoothstep(1.0, 1.0 - pixelSize * smoothingAmount, dist); #elif defined(LINSTEP) float alpha = linearstep(1.0, 1.0 - pixelSize * smoothingAmount, dist); #elif defined(LINSTEP_NO_CLAMP) float alpha = linearstepNoclamp(1.0, 1.0 - pixelSize * smoothingAmount, dist); #endif /* Clamped and scaled uv.y added to color simply to make the bottom of the circle white, so the contrast is high and you can see strong aliasing */ gl_FragColor = vec4(color + clamp( - uv.y * 0.4, 0.0, 1.0), alpha); }`

## WebGL Javascript

[circleAnalyticalComparison.js]`function setupAnalyticalComparison(canvasId, circleVtxSrc, circleFragSrc, blitVtxSrc, blitFragSrc, redVtxSrc, redFragSrc, radioName) { /* Init */ const canvas = document.getElementById(canvasId); let circleDrawFramebuffer, frameTexture; let buffersInitialized = false; let resDiv = 1; let shrinkAmount = 1; let smoothingAmount = 1; let pixelSizeMethod = "SIMPLE"; let blendMethod = "DIVISION"; const gl = canvas.getContext('webgl', { preserveDrawingBuffer: false, antialias: false, alpha: true } ); let DerivativesExtension = gl.getExtension('OES_standard_derivatives'); /* Render Resolution */ const radios = document.querySelectorAll(`input[name="${radioName}"]`); radios.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { resDiv = event.target.value; stopRendering(); startRendering(); }); }); const pixelSizeMethodSwitch = document.getElementById('pixelSizeMethod'); pixelSizeMethodSwitch.addEventListener('change', function () { pixelSizeMethod = pixelSizeMethodSwitch.value; updateShader(); }); const blendMethodSwitch = document.getElementById('BLENDMETHOD'); blendMethodSwitch.addEventListener('change', function () { blendMethod = blendMethodSwitch.value; updateShader(); }); const SmoothingPxRange = document.getElementById('SmoothingPxRange'); const ShrinkAmountRange = document.getElementById('ShrinkAmountRange'); SmoothingPxRange.addEventListener('input', function () { smoothingAmount = SmoothingPxRange.value; }); ShrinkAmountRange.addEventListener('input', function () { shrinkAmount = -ShrinkAmountRange.value; }); /* Shaders */ /* Circle Shader */ let circleShd; let aspect_ratioLocation; let offsetLocationCircle; let shrinkAmountLocation; let smoothingAmountLocation; let pixelSizeCircle; let sizeLocationCircle; function updateShader() { if (circleShd) { gl.deleteProgram(circleShd); } const prefix = ` #define ${pixelSizeMethod} #define ${blendMethod} `; circleShd = compileAndLinkShader(gl, circleVtxSrc, circleFragSrc, prefix); aspect_ratioLocation = gl.getUniformLocation(circleShd, "aspect_ratio"); offsetLocationCircle = gl.getUniformLocation(circleShd, "offset"); shrinkAmountLocation = gl.getUniformLocation(circleShd, "shrinkAmount"); smoothingAmountLocation = gl.getUniformLocation(circleShd, "smoothingAmount"); pixelSizeCircle = gl.getUniformLocation(circleShd, "pixelSize"); sizeLocationCircle = gl.getUniformLocation(circleShd, "size"); } updateShader(); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); /* Simple Red Box */ const redShd = compileAndLinkShader(gl, redVtxSrc, redFragSrc); const transformLocationRed = gl.getUniformLocation(redShd, "transform"); const offsetLocationRed = gl.getUniformLocation(redShd, "offset"); const aspect_ratioLocationRed = gl.getUniformLocation(redShd, "aspect_ratio"); const thicknessLocation = gl.getUniformLocation(redShd, "thickness"); const pixelsizeLocation = gl.getUniformLocation(redShd, "pixelsize"); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT); gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); setupTextureBuffers(); const circleOffsetAnim = new Float32Array([ 0.0, 0.0 ]); let aspect_ratio = 0; let last_time = 0; let redrawActive = false; function setupTextureBuffers() { gl.deleteFramebuffer(circleDrawFramebuffer); circleDrawFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); frameTexture = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTexture, gl.NEAREST); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTexture, 0); buffersInitialized = true; } gl.enable(gl.BLEND); function redraw(time) { redrawActive = true; if (!buffersInitialized) { setupTextureBuffers(); } last_time = time; /* Setup PostProcess Framebuffer */ gl.viewport(0, 0, canvas.width / resDiv, canvas.height / resDiv); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(circleShd); /* Draw Circle Animation */ gl.uniform1f(pixelSizeCircle, (2.0 / (canvas.height / resDiv))); gl.uniform1f(aspect_ratioLocation, aspect_ratio); var radius = 0.1; var speed = (time / 10000) % Math.PI * 2; circleOffsetAnim[0] = radius * Math.cos(speed) + 0.1; circleOffsetAnim[1] = radius * Math.sin(speed); gl.uniform2fv(offsetLocationCircle, circleOffsetAnim); gl.uniform1f(sizeLocationCircle, circleSize); gl.uniform1f(shrinkAmountLocation, shrinkAmount); gl.uniform1f(smoothingAmountLocation, smoothingAmount); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.viewport(0, 0, canvas.width, canvas.height); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Scaled image in the bottom left */ gl.uniform4f(transformLocation, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationPost, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(redShd); gl.uniform1f(aspect_ratioLocationRed, (1.0 / aspect_ratio) - 1.0); gl.uniform1f(thicknessLocation, 0.2); gl.uniform1f(pixelsizeLocation, (1.0 / canvas.width) * 50); gl.uniform4f(transformLocationRed, 0.25, 0.25, -0.75, -0.75); gl.uniform2fv(offsetLocationRed, circleOffsetAnim); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); gl.uniform1f(thicknessLocation, 0.1); gl.uniform1f(pixelsizeLocation, 0.0); gl.uniform4f(transformLocationRed, 0.5, 0.5, 0.0, 0.0); gl.uniform2f(offsetLocationRed, -0.75, -0.75); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); redrawActive = false; } let isRendering = false; let animationFrameId; function onResize() { const dipRect = canvas.getBoundingClientRect(); const width = Math.round(devicePixelRatio * dipRect.right) - Math.round(devicePixelRatio * dipRect.left); const height = Math.round(devicePixelRatio * dipRect.bottom) - Math.round(devicePixelRatio * dipRect.top); if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; setupTextureBuffers(); aspect_ratio = 1.0 / (width / height); stopRendering(); startRendering(); } } window.addEventListener('resize', onResize, true); onResize(); function renderLoop(time) { if (isRendering) { redraw(time); animationFrameId = requestAnimationFrame(renderLoop); } } function startRendering() { /* Start rendering, when canvas visible */ isRendering = true; renderLoop(last_time); } function stopRendering() { /* Stop another redraw being called */ isRendering = false; cancelAnimationFrame(animationFrameId); while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality this code is block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the important buffer to free up memory */ gl.deleteTexture(frameTexture); gl.deleteFramebuffer(circleDrawFramebuffer); buffersInitialized = false; } function handleIntersection(entries) { entries.forEach(entry => { if (entry.isIntersecting) { if (!isRendering) startRendering(); } else { stopRendering(); } }); } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


#### How big is a pixel? [#](https://blog.frost.kiwi#how-big-is-a-pixel%3F)

Specifically, by how much do we fade the border? If we hardcode a static value, eg. fade at 95% of the circle’s radius, we may get a pleasing result for that circle size at that screen resolution, but too much smoothing when the circle is bigger or closer to the camera and aliasing if the circle becomes small.

![Too much edge fading relative to this circle size](../../assets/ebefbd31f7af19a1.png)

We need to know the size of a pixel. This is in part what [Screen Space derivatives](https://gamedev.stackexchange.com/a/130933) were created for. Shader functions like [ dFdx](https://docs.gl/sl4/dFdx),

[and](https://docs.gl/sl4/dFdy)

`dFdy`

[allow you to get the size of a screen pixel relative to some vector. In the above](https://docs.gl/sl4/fwidth)

`fwidth`

[circle-analyticalCompare.fs](https://blog.frost.kiwi/shader/circle-analyticalCompare.fs)we determine by how much the distance changes via two methods:

```
pixelSize = fwidth(dist);
/* or */
pixelSize = length(vec2(dFdx(dist), dFdy(dist)));
```


Relying on Screen Space derivatives has the benefit, that we get the pixel size delivered to us by the graphics pipeline. It properly respects any transformations we might throw at it, including 3D perspective.

The down side is that it is not supported by the WebGL 1 standard and has to be pulled in via the extension `GL_OES_standard_derivatives`

or requires the jump to WebGL 2.

Luckily I have never witnessed any device that supported WebGL 1, but not the Screen Space derivatives. Even the GMA based[Thinkpad X200 & T500]I hardware modded do.

##### Possibly painful

Generally, there are some nasty pitfalls when using Screen Space derivatives: how the calculation happens is up to the implementation. This led to the split into `dFdxFine()`

and `dFdxCoarse()`

in later OpenGL revisions. The default case can be set via [ GL_FRAGMENT_SHADER_DERIVATIVE_HINT](https://docs.gl/gl4/glHint), but the standard hates you:


[: The implementation]OpenGL Docschoose which calculation to perform based upon factors such as performance or the value of the APImay`GL_FRAGMENT_SHADER_DERIVATIVE_HINT`

hint.

Why do we have standards again? As a graphics programmer, anything with`hint`

has me traumatized.

Luckily, neither case concerns us, as the difference doesn’t show itself in the context of Anti-Aliasing. Performance technically [ dFdx](https://docs.gl/sl4/dFdx) and

[are free (or rather, their cost is already part of the rendering pipeline), though the pixel size calculation using](https://docs.gl/sl4/dFdy)

`dFdy`

`length()`

or `fwidth()`

is not. It is performed *per-pixel*.

This is why there exist two ways of doing this: getting the `length()`

of the vector that `dFdx`

and `dFdy`

make up, a step involving the historically performance expensive `sqrt()`

function or using `fwidth()`

, which is the approximation `abs(dFdx()) + abs(dFdy())`

of the above.

It depends on context, but on semi-modern hardware a call to`length()`

should be performance trivial though, even per-pixel.

To showcase the difference, the above `Radius adjust`

slider works off of the `Pixel size method`

and adjusts the SDF distance. If you go with `fwidth()`

and a strong radius shrink, you’ll see something weird.

![Rhombous warping at small shape sizes due to use of fwidth()](../../assets/47650354de7c4054.png)

`fwidth()`

The diagonals shrink more than they should, as the approximation using addition scales too much diagonally. We’ll talk about professional implementations further below in a moment, but using `fwidth()`

for AAA is what Unity extension “[Shapes](https://acegikmo.com/shapes/)” by [Freya Holmér](https://twitter.com/FreyaHolmer/) calls “[Fast Local Anti-Aliasing](https://acegikmo.com/shapes/docs#anti-aliasing)” with the following text:

Fast LAA has a slight bias in the diagonal directions, making circular shapes appear ever so slightly rhombous and have a slightly sharper curvature in the orthogonal directions, especially when small. Sometimes the edges in the diagonals are slightly fuzzy as well.


This effects our fading, which will fade more on diagonals. Luckily, we fade by the amount of one pixel and thus the difference is really only visible when flicking between the methods. What to choose depends on what you care more about: Performance or Accuracy? But what if I told you can have your cake and eat it too…

##### DIY

…Calculate it yourself! For the 2D case, this is trivial and easily abstracted away. We know the size our context is rendering at and how big our quad is that we draw on. Calculating the size of the pixel is thus done per-object, not per-pixel. This is what happens in the above [circleAnalyticalComparison.js](https://blog.frost.kiwi/circleAnalyticalComparison.js).

```
/* Calculate pixel size based on height.
Simple case: Assumes Square pixels and a square quad. */
gl.uniform1f(pixelSizeCircle, (2.0 / (canvas.height / resDiv)));
```


No WebGL 2, no extensions, works on ancient hardware.

The results are identical to the `dFdx`

+ `dFdy`

+ `length()`

case, with the benefit of fully skipping the per-pixel calculation. This does become more involved, once the quad is stretched and performance-painful when perspective is involved.

#### How do we blend? [#](https://blog.frost.kiwi#how-do-we-blend%3F)

Ok, now we have the amount we want to blend by. The next step is to perform the adjustment of opacity. If we are doing 2D, then Alpha blending is the way to go. Straight forward, will never betray you.

Another option is using MSAA + [Alpha to Coverage](https://bgolus.medium.com/anti-aliased-alpha-test-the-esoteric-alpha-to-coverage-8b177335ae4f), as is done in the MSAA demo above. There are pit falls with the latter, as discussed previously and more headaches to follow below. The reason you would need this is for depth-buffer writes for [correct blending in 3D scenes](https://bgolus.medium.com/rendering-a-sphere-on-a-quad-13c92025570c).

For the MSAA and AAA demos above, merely an API level switch. In both cases, the shaders are 100%[identical]!

Still the alpha itself has to be faded based on distance. Here is where a “step” function comes in. We can input a start, an end point and the function will fade between them. [Usually](http://www.numb3r23.net/2015/08/17/using-fwidth-for-distance-based-anti-aliasing/), this is where the graphics programmer’s favorite `smoothstep()`

comes in and where this blog post’s hot take begins:

##### Don’t use `smoothstep()`


`smoothstep()`

Its use is [often associated](http://www.numb3r23.net/2015/08/17/using-fwidth-for-distance-based-anti-aliasing/) with implementing anti-aliasing in `GLSL`

, but its use doesn’t make sense in this context. It performs a [hermite interpolation](https://en.wikipedia.org/wiki/Smoothstep), but we are dealing with a function applied across 2 pixels or just inside 1. There is no curve to be witnessed here.

To be precise, both sampling and blending witness the smoothstep curve in the sub-pixel make-up of the edge, but the difference is tiny and can be corrected using an adjusted smoothing amount.

Even though the slight performance difference doesn’t particularly matter on modern graphics cards, wasting cycles on performing the hermite interpolation doesn’t make sense to me. Let’s DIY it! The implementation of [ smoothstep()](https://en.wikipedia.org/wiki/Smoothstep) is up to the vendor, but for the

`float`

case it’s essentially just :```
float smoothstep(float edge0, float edge1, float x) {
float t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
return t * t * (3.0 - 2.0 * t);
}
...
float alpha = smoothstep(1.0, 1.0 - pixelSize * smoothingAmount, dist);
```


We can rip out the hermite interpolation and stick to the simple linear one. If you flick between the two in the above demo, you’ll see only a slight change, with pixel sized smoothing. At pixel size, the difference can easily be counter acted with an adjustment to the smoothing factor if you like one method over the other.

```
/* Step function with Linear Interpolation
instead of the Hermite Interpolation */
float linearstep(float edge0, float edge1, float x) {
return clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
}
...
float alpha = linearstep(1.0, 1.0 - pixelSize * smoothingAmount, dist);
```


But why even clamp? Alpha values below 0.0 or above 1.0 will be taken care of by the rendering pipeline during the blending step and thus no clamping is required. It *is* required when having multiple shapes on one quad, something I’ll go into below. But in the one shape per quad case, we can delete it.

```
/* Step function with Linear Interpolation, but no clamping */
float linearstepNoclamp(float edge0, float edge1, float x) {
return (x - edge0) / (edge1 - edge0);
}
...
float alpha = linearstepNoclamp(1.0, 1.0 - pixelSize * smoothingAmount, dist);
```


But wait a moment… When doing Anti-Aliasing we wish to affect the border of the shape, specifically distance 1.0, so most of this function cancels out! In fact, we **don’t** need a step function. The blending can be performed by a simple division.

`float alpha = (1.0 - dist) / (pixelSize * smoothingAmount);`


I have been using this simplified term in different places for years. Performance wise, the most expensive thing still remains: the per-pixel division. Modern cards should also have no issues optimizing the hermite interpolation’s multiplication and addition down to a few [Fused Multiply-Add](https://en.wikipedia.org/wiki/Multiply%E2%80%93accumulate_operation#Fused_multiply%E2%80%93add) instructions. Still, I prefer the simplicity.

##### What’s with the shrinking?

There is an ellusive implementation interaction with MSAA and the rasterizer. *Only* when using this with MSAA + Alpha to Coverage (regardless of sample count), there will be exactly one side of the quad with a missing 0.5 pixels, on **some** hardware. This is why there is this weird 0.5 px breathing room being added.

![Hard edge bug with MSAA on select hardware](../../assets/5a7f5871cd7a7c4b.png)

Our circle is drawn to the very edge of the quad, which works, but only as long the graphics card doesn’t surprise us with edge cases. Specifically modern NVIDIA cards seems to eat one side of the quad too soon, though I have never seen this occur with alpha blending. To combat this, we give our SDF 0.5px of breathing room:

```
/* We add half a pixel of breathing room. This is only required for the MSAA
case. Depending on Hardware implementation, rasterization, MSAA sample
count and placement, one row pixels may or may not disappear too soon,
when the circle's edge is right up against the unit quad's border */
dist += pixelSizeAdjusted * 0.5;
```


An edge case.

##### Drawing multiple?

You can draw multiple shapes in one Quad and both will be Anti-Aliased, though blending will start to get more involved. In that case both shapes will need to be evaluated per-pixel and their results will need to be clamped, weighted and summed, otherwise there won’t be Anti-Aliasing when they intersect.

![Aliasing free blending of multiple circle visualizations from mirrorball.frost.kiwi](../../assets/94547297139087e4.jpg)

From

[🔮 Mathematical Magic Mirrorball](https://mirrorball.frost.kiwi)

Here is what blending looks like in my WebApp [🔮 Mathematical Magic Mirrorball](https://mirrorball.frost.kiwi), a WebApp which pulls 360° panoramic projections from photos, videos and live-streams of mirror balls. There I have multiple visualizations and color overlays explaining resolution distribution of the projection. [The code](https://github.com/FrostKiwi/Mirrorball/blob/main/src/shd/crop.fs#L35) to keep all this anti-aliased is:

```
float factorGreen = area_toggle * clamp((area_f - lenCircle) * pxsize_rcp, 0.0, 1.0);
float factorRed = area_toggle * clamp((lenCircle - area_b) * pxsize_rcp, 0.0, 1.0) * smoothedAlpha;
float factorBlack = mask_toggle * (1.0 - smoothedAlpha);
vec3 finalColor = baseColor * (1.0 - factorGreen - factorRed - factorBlack) +
greenColor * factorGreen +
redColor * factorRed +
blackColor * factorBlack;
```


All this additional stuff … why not draw color overlays in an additional pass? The cost of drawing across that area again is an order of magnitude higher than just coloring the output in the shape we need as we go. Tinting in an Anti-Aliased fashion in one draw-call is the cleanest way to do this I think.

### 3D [#](https://blog.frost.kiwi#3d)

Everything we talked about extends to the 3D case as well. We won’t dig [into 3D shapes themselves](https://iquilezles.org/articles/distfunctions/) and will stick to a 2D rounded square in 3D perspective with a moving camera. I use this a lot when graphics programming to create a scene with a “ground floor” where my objects live on.

## WebGL Vertex Shader

[3DAnalytical.vs]`/* Our Vertex data for the Quad */ attribute vec2 vtx; attribute vec3 col; /* The coordinates that will be used to for our drawing operations */ varying vec2 uv; varying vec3 color; uniform mat4 perspective; void main() { /* Assign the verticies to be used as the distance field for drawing. This will be linearly interpolated before going to the fragment shader */ uv = vtx; /* Some nice color */ color = col; /* Make Circle smaller and correct aspect ratio */ vec4 pos = vec4(vtx, 0.0, 1.0); gl_Position = perspective * pos; }`

## WebGL Fragment Shader

[3DAnalytical.fs]`#extension GL_OES_standard_derivatives : enable precision mediump float; varying vec2 uv; varying vec3 color; float roundedBoxSDF(vec2 uv, float Size, float Radius) { return length(max(abs(uv) - Size + Radius, 0.0)) - Radius; } void main(void) { /* Pixel Size, but missing Perspective correction */ float dist = roundedBoxSDF(uv, 1.0, 0.4); /* Fade out near the edge of the circle */ float pixelSize = length(vec2(dFdx(dist), dFdy(dist))); float alpha = -dist / (pixelSize * 1.4142135623730950488016887242097); /* Clamped and scaled uv.y added to color simply to make the bottom of the circle white, so the contrast is high and you can see strong aliasing */ gl_FragColor = vec4(color + clamp( - uv.y * 0.4, 0.0, 1.0), alpha); }`

## WebGL Javascript

[3DAnalytical.js]`function setup3D(canvasId, circleVtxSrc, circleFragSrc, simpleColorFragSrc, blitVtxSrc, blitFragSrc, radioName, showQuadOpt) { /* Init */ const canvas = document.getElementById(canvasId); let circleDrawFramebuffer, frameTexture; let buffersInitialized = false; let showQuad = false; let resDiv = 1; const gl = canvas.getContext('webgl', { preserveDrawingBuffer: false, antialias: false, alpha: true } ); let DerivativesExtension = gl.getExtension('OES_standard_derivatives'); /* Render Resolution */ const radios = document.querySelectorAll(`input[name="${radioName}"]`); radios.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "1") radio.checked = true; radio.addEventListener('change', (event) => { resDiv = event.target.value; stopRendering(); startRendering(); }); }); /* Show Quad instead of circle choise */ const showQuadOption = document.querySelectorAll(`input[name="${showQuadOpt}"]`); showQuadOption.forEach(radio => { /* Force set to 1 to fix a reload bug in Firefox Android */ if (radio.value === "false") radio.checked = true; radio.addEventListener('change', (event) => { showQuad = (event.target.value === "true"); stopRendering(); startRendering(); }); }); /* Shaders */ /* Circle Shader */ const circleShd = compileAndLinkShader(gl, circleVtxSrc, circleFragSrc); const viewProjectionLocation = gl.getUniformLocation(circleShd, "perspective"); /* SimpleColor Shader */ const simpleColorShd = compileAndLinkShader(gl, circleVtxSrc, simpleColorFragSrc); const viewProjectionLocationSimple = gl.getUniformLocation(simpleColorShd, "perspective"); /* Blit Shader */ const blitShd = compileAndLinkShader(gl, blitVtxSrc, blitFragSrc); const transformLocation = gl.getUniformLocation(blitShd, "transform"); const offsetLocationPost = gl.getUniformLocation(blitShd, "offset"); const vertex_buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer); gl.bufferData(gl.ARRAY_BUFFER, unitQuad, gl.STATIC_DRAW); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 0); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 5 * Float32Array.BYTES_PER_ELEMENT, 2 * Float32Array.BYTES_PER_ELEMENT); gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); setupTextureBuffers(); let aspect_ratio = 0; let last_time = 0; let redrawActive = false; function setupTextureBuffers() { gl.deleteFramebuffer(circleDrawFramebuffer); circleDrawFramebuffer = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); frameTexture = setupTexture(gl, canvas.width / resDiv, canvas.height / resDiv, frameTexture, gl.NEAREST); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, frameTexture, 0); buffersInitialized = true; } let viewMatrix = Mat4.create(); let projectionMatrix = Mat4.create(); let eye = [1.5, 1.5, 1.5]; let target = [0, 0, 0]; let up = [0, 0, 1]; gl.enable(gl.BLEND); function redraw(time) { redrawActive = true; if (!buffersInitialized) { setupTextureBuffers(); } last_time = time; const radius = 5 + 4 * Math.sin(time / 2000); var speed = (time / 5000) % Math.PI * 2; eye[0] = radius * Math.cos(speed) + 0.1; eye[1] = radius * Math.sin(speed); Mat4.lookAt(viewMatrix, eye, target, up); let fov = 75 * Math.PI / 180; Mat4.perspectiveNO(projectionMatrix, fov, aspect_ratio, 1, Infinity); Mat4.multiply(projectionMatrix, projectionMatrix, viewMatrix); /* Setup PostProcess Framebuffer */ gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.viewport(0, 0, canvas.width / resDiv, canvas.height / resDiv); gl.bindFramebuffer(gl.FRAMEBUFFER, circleDrawFramebuffer); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(circleShd); gl.uniformMatrix4fv(viewProjectionLocation, false, projectionMatrix); /* Draw Circle Animation */ gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); if(showQuad){ gl.useProgram(simpleColorShd); gl.uniformMatrix4fv(viewProjectionLocationSimple, false, projectionMatrix); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); } gl.viewport(0, 0, canvas.width, canvas.height); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); gl.useProgram(blitShd); gl.bindFramebuffer(gl.FRAMEBUFFER, null); /* Simple Passthrough */ gl.uniform4f(transformLocation, 1.0, 1.0, 0.0, 0.0); gl.uniform2f(offsetLocationPost, 0.0, 0.0); gl.drawArrays(gl.TRIANGLE_FAN, 0, 4); /* Draw Red box for viewport illustration */ redrawActive = false; } let isRendering = false; let animationFrameId; function onResize() { const dipRect = canvas.getBoundingClientRect(); const width = Math.round(devicePixelRatio * dipRect.right) - Math.round(devicePixelRatio * dipRect.left); const height = Math.round(devicePixelRatio * dipRect.bottom) - Math.round(devicePixelRatio * dipRect.top); if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; setupTextureBuffers(); aspect_ratio = width / height; stopRendering(); startRendering(); } } window.addEventListener('resize', onResize, true); onResize(); function renderLoop(time) { if (isRendering) { redraw(time); animationFrameId = requestAnimationFrame(renderLoop); } } function startRendering() { /* Start rendering, when canvas visible */ isRendering = true; renderLoop(last_time); } function stopRendering() { /* Stop another redraw being called */ isRendering = false; cancelAnimationFrame(animationFrameId); while (redrawActive) { /* Spin on draw calls being processed. To simplify sync. In reality this code is block is never reached, but just in case, we have this here. */ } /* Force the rendering pipeline to sync with CPU before we mess with it */ gl.finish(); /* Delete the important buffer to free up memory */ gl.deleteTexture(frameTexture); gl.deleteFramebuffer(circleDrawFramebuffer); buffersInitialized = false; } function handleIntersection(entries) { entries.forEach(entry => { if (entry.isIntersecting) { if (!isRendering) startRendering(); } else { stopRendering(); } }); } /* Only render when the canvas is actually on screen */ let observer = new IntersectionObserver(handleIntersection); observer.observe(canvas); }`


With the 3D camera and resulting perspective matrix multiplication, we use the reliable screen space derivatives again to get the pixel size. But in reality, [we can still do without](https://web.archive.org/web/20150521050627/https://www.opengl.org/wiki/Compute_eye_space_from_window_space)! This would require us to multiply the inverse perspective matrix with the fragment coordinates * per pixel*. Performance-painful, yet possible.

### Unmentioned challenges [#](https://blog.frost.kiwi#unmentioned-challenges)

There is something I have not explained yet, a persistent misunderstanding I held until [Yakov Galka](https://stannum.io/) explained [the deetz to me on stackoverflow](https://stackoverflow.com/questions/73903568). Depending on how we setup the blending math, to perform the smoothing we may remove pixel alpha on the inside of the shape, add it to the outside or center it.

Adding or subtracting would mess with the shape every so slightly, especially at small sizes or under strong perspective. So centering is the way to go. Unfortunately, centering the fade on the border can put the edge outside our quad and lead to hard edges or clipping.

![Clipping of the border](../../assets/2f4c4cc6ab0154a0.png)

In 3D this is especially painful, as there is no amount of safety margin that would solve this, with the camera at oblique angles. Nvidia introduced the vendor specific extension [ NV_conservative_raster_dilate](https://registry.khronos.org/OpenGL/extensions/NV/NV_conservative_raster_dilate.txt) to always give you an extra pixel at the border. Unfortunately it’s not available in WebGL and specific to NVIDIA hardware.

![Border pixels not rasterized due to fading overshooting the quad](../../assets/f831a8f21dd0ccd9.png)

Source:

[Explanation](https://stackoverflow.com/questions/73903568)on Stack overflow by

[Yakov Galka](https://stannum.io/)

So we are forced to shrink the border in all cases. This leads to smooth edges even under strong perspective, but technically influences the shape. This is absolutely *not* visible in isolation, but may lead to mismatches or unexpected behavior, as even perspective has now an influence on the shape.

![Border pixels rasterized with shrunken border](../../assets/b4718249c6b2c8fc.png)

Source:

[Explanation](https://stackoverflow.com/questions/73903568)on Stack overflow by

[Yakov Galka](https://stannum.io/)

For the 2D case, we could implement a kind of [ NV_conservative_raster_dilate](https://registry.khronos.org/OpenGL/extensions/NV/NV_conservative_raster_dilate.txt) ourselves, by growing the quad in the vertex shader by half a pixel and shrinking the signed distance field by half a pixel in the fragment shader. And this

*is*exactly what’s happening in the 2D demos on this page!

This is really pedantic and just here for correctness. In most cases, you don't need to be so precise.

That is the reason the red box always lines up with the border, at all resolution switches and with all 2D demos on this page. Specifically in the vertex shader, the line responsible for this is:

```
/* Grow the Quad and thus the "canvas", that the circle is drawn on. The
pixelSize is added for two reasons: 0.5px to get the original circle size
again, as the AAA fading is set to fade the edge on the circle inside,
preventing hard edges due to unrasterized pixels. And another 0.5px is
to correct the "breathing room" added in the fragment shader,
specifically for the MSAA sampling case, as hardware specific issues
around MSAA sampling may or may not result in transparent pixels
disappearing too soon. */
vertex *= size + pixelSize;
```


Not messing up gamma and multiplied vs premultiplied alpha are important for all forms of AA, but are very context dependant. This blog post is about AAA specifically, thus we ignore these.

## What are the big boys doing? [#](https://blog.frost.kiwi#what-are-the-big-boys-doing%3F)

This rendering approach has found its way into many professional products. Let’s finish by looking at some of them.

Feature-wise the most complete implementation of this approach is in Unity extension [Shapes](https://acegikmo.com/shapes) by [Freya Holmér](https://twitter.com/FreyaHolmer/). There the SDFs are either anti-aliased by MSAA or are blended like in this blog post, though it’s referred to as “[Fast Local Anti-Aliasing](https://acegikmo.com/shapes/docs/#anti-aliasing)” for the `fwidth()`

case and “[Corrected Local Anti-Aliasing](https://acegikmo.com/shapes/docs/#anti-aliasing)” for the `length()`

case.

["Shapes"](https://acegikmo.com/shapes)by

[Freya Holmér](https://twitter.com/FreyaHolmer/)

With motion-blur, [shape-respecting color gradients](https://acegikmo.com/shapes/docs/#shapes-feature-table) and lines [below 1px being opacity faded](https://acegikmo.com/shapes/docs/#anti-aliasing) to prevent further aliasing, this is signed-distance field rendering and AAA by extension, implemented to its logical conclusion.

[Valve Software](https://www.valvesoftware.com/)’s implementation [#](https://blog.frost.kiwi#valve-software%E2%80%99s-implementation)

![Hud elements in Team Fortress 2](../../assets/d2d46e5af95aaa1b.png)

[Team Fortress 2](https://www.teamfortress.com/)

Valve introduced extensive use of signed distance field rendering to the [Source engine](https://en.wikipedia.org/wiki/Source_(game_engine)) during the development of the [Orange Box](https://en.wikipedia.org/wiki/The_Orange_Box). Most prominently in [Team Fortress 2](https://www.teamfortress.com/), where it was used to create smooth yet sharp UI elements on the HUD. It even received its own [Developer Commentary](https://wiki.teamfortress.com/wiki/Developer_commentary) entry.


Alden Kroll:Two-dimensional HUD elements present a particular art problem, because they have to look good and sharp no matter what resolution the user is running their game at. Given today’s availability of high resolution wide-screen displays, this can require a lot of texture memory and a lot of work anticipating different display resolutions. The problem for Team Fortress 2 was even more daunting because of our desire to include a lot of smooth curved elements in our HUD. We developed a new shader system for drawing ‘line art’ images. The system allows us to create images at a fixed resolution that produced smooth silhouettes even when scaled up to a very high resolution. This shader system also handles outlining and drop-shadows, and can be applied in the 3D space to world elements such as signs.

![64x64 Texture: Alpha blended, Alpha Tested and SDF rendering](../../assets/cd8d35a11f8423ee.png)

Paper:

[Improved Alpha-Tested Magnification for Vector Textures and Special Effect](https://steamcdn-a.akamaihd.net/apps/valve/2007/SIGGRAPH2007_AlphaTestedMagnification.pdf)

They also released [a paper](https://steamcdn-a.akamaihd.net/apps/valve/2007/SIGGRAPH2007_AlphaTestedMagnification.pdf) describing the specific implementation, including a showcase for use in the 3D game world, though I have never seen it used in the game world itself in Valve titles. Added as a mere footnote to the paper, was a way to improve rendering with sharp corners…

### The future of all things font? [#](https://blog.frost.kiwi#the-future-of-all-things-font%3F)

If you save a signed distance field into a texture and sample it with linear interpolation, you will get perfectly sharp characters at any size, but the limited resolution will result in clipped or rounded corners, depending on implementation math.

Picking up on that foot note and bringing the technique to its logical conclusion was the most thorough and well composed Master Thesis I ever read: “[Shape Decomposition for Multi-channel Distance Fields](https://github.com/Chlumsky/msdfgen/files/3050967/thesis.pdf)” by [Viktor Chlumský](https://github.com/Chlumsky), which included code for the [font-file to SDF conversion](https://github.com/Chlumsky/msdfgen) and a full [font atlas generator](https://github.com/Chlumsky/msdf-atlas-gen?tab=readme-ov-file).

Basically, use RGB and a median term to get perfectly sharp text at any size, including an Alpha channel with the classical SDF for effects like glows and drop shadows, all done on the GPU with no run-time baking or intense processing. If you dig around in video games, you will find SDF based font rendering from time to time!

![Multi-Channel SDF demo from msdf-atlas-gen](../../assets/8833af35c61bc8e5.png)

[msdf-atlas-gen](https://github.com/Chlumsky/msdf-atlas-gen?tab=readme-ov-file)

From experience I can tell you, that there are more implementation headaches. Chinese, Japanese, Korean characters require bigger textures to resolve their minute details. Bigger textures means you’ll often minimize during rendering, but minimizing may introduce artifacts on its own…

But considering the current state of browser font baking + rendering and the *pure insanity* of edge-cases covered, including [synthetic fallbacks for missing italic or bold variants](https://faultlore.com/blah/text-hates-you/) and baking 4 variants with 0.25px offsets to account for minute sampling issues, I think SDF text rendering has not been given enough serious consideration.

"[Text rendering hates you]" is a recommended read if you want to see how crushingly complex this topic gets.

You may be wondering, if we can get the [analytical solution for a bezier curve](https://www.shadertoy.com/view/MlKcDD), why bake into textures instead? We may know the solution for **one** segment, but to get the full shape we need to sum up all the contributions from all segments. This works, but performance tanks hard, as we solve *every* bezier curve segment **per pixel**.

This post is already long enough, but therearenew text rendering approaches going the analytical route, like[Slug].

## Clarity should not be a luxury [#](https://blog.frost.kiwi#clarity-should-not-be-a-luxury)

Modern video games often use TAA in combination with dynamic resolution scaling, a concoction guaranteed to result in blurriness. These AA algorithms come with post-process sharpening built-in to combat this, as is done in [FSR](https://gpuopen.com/fidelityfx-cas/) or [TAA](https://docs.unity3d.com/Packages/com.unity.postprocessing@3.4/manual/Anti-aliasing.html#temporal-anti-aliasing). Fixing blurring by sharpening, I find this a bit of graphics programming sin.

![TAA Sharpening in Warframe](../../assets/7d50371df6829189.png)

[Warframe](https://www.warframe.com/)

Whole communities rally around fixing this, like the reddit communities “[r/MotionClarity](https://www.reddit.com/r/MotionClarity/)” or the lovingly titled “[r/FuckTAA](https://www.reddit.com/r/FuckTAA)”, all with the understanding, that Anti-Aliasing should not come at the cost of clarity. FXAA creator Timothy Lottes mentioned, that this is [solvable to some degree with adjustments to filtering](https://x.com/NOTimothyLottes/status/1756733156877578611), though even the most modern titles suffer from this.

What we have not talked about are the newer machine learning approaches as done for instance with NVIDIA’s [ DLAA](https://en.wikipedia.org/wiki/Deep_learning_anti-aliasing), as that is really outside the scope of this post. Suffice to say Timothy Lottes is

[not a fan](https://x.com/NOTimothyLottes/status/1756746848402800785). As for AAA, it’s lovely being able to draw smooth yet sharp, motion-stable shapes of any size at native resolutions.

Please feel free to use these techniques in your projects.

## Addendum [#](https://blog.frost.kiwi#addendum)

Here are some extra comments from other graphics programmers, that came from discussions after this article was posted on [Hacker News](https://news.ycombinator.com/item?id=42191709), [Lobste.rs](https://lobste.rs/s/6e8zc3/aaa_analytical_anti_aliasing) and E-Mail.

### Google Maps [#](https://blog.frost.kiwi#google-maps)

[Google Maps](http://maps.google.com/) is using this method to draw street segments, as [mentioned](https://news.ycombinator.com/item?id=42197506) by user [aappleby](https://news.ycombinator.com/user?id=aappleby) on Hacker News.


[: Google Maps uses AAA on capsule shapes for all road segments - I wrote it ~10 years ago. :D]aappleby

Checking with a [WebGL debugger](https://spector.babylonjs.com/) it seems to be indeed the case. Sometimes there is no local rendering and a tile is fetched from memory or from the server, but sometimes the local drawing kicks-in an indeed, the shader code seems to indicate shape dependant blended alpha on the draw call that draws the streets.

## Google Maps Fragment Shader during streets draw call

Captured via [https://spector.babylonjs.com/](https://spector.babylonjs.com/)

It’s minified, so a bit hard to read. Comments added by me.

```
precision highp float;
varying vec4 s, u; /* s is color, u must be size and line width */
varying vec3 t;
const float B = 1.;
float L(float C) {
/* Never actually called ? */
const float D = 0.;
const float E = 1.;
const float F = .3;
const float G = .3;
const float H = 2.*D-2.*E+F+G;
const float I = 3.*E-3.*D-2.*F-G;
const float J = F;
const float K = D;
return clamp(((H*C+I)*C+J)*C+K, 0., 1.);
}
void main() {
vec2 C = vec2(t.x-clamp(t.x, 0., 1.), t.y);
float D, E, F, G, H, I, J;
D = C.x*C.x+C.y*C.y; /* Capsule Shape Calculation */
E = u.x; /* Should be the scale */
F = u.y; /* Should be the line width */
G = sqrt(D)*E; /* Distance to the capsule shape border */
H = clamp(G-F+1., 0., 1.);
I = clamp(G+F, 0., 1.);
if(B>1.) {
H = L(H);
I = L(I);
}
J = clamp(H-I, 0., 1.); /* Smoothing, based on the distance */
if(J == 0.)discard; /* Fragment discard when alpha fully zero */
gl_FragColor = s;
gl_FragColor.a *= J;
}
```


![Google maps rendering during streets draw call](../../assets/2b7f7f7d4ea45ee1.png)

![Google maps after rendering](../../assets/1f19b9197e8e1f20.png)

That's pretty damn fire!

### Limit’s of SDFs [#](https://blog.frost.kiwi#limit%E2%80%99s-of-sdfs)

Yakov Galka emphasized when this drawing style breaks down:


[: I think it’s worth mentioning that the SDF approach still samples the SDF at a particular point, which may cause aliasing if the SDF has high-frequency components. E.g. if you rasterize a circle smaller than a pixel, then the discussed approach won’t fully eliminate the aliasing.]Yakov Galka

There is a truly analytical method of rasterizing antialiased polygonal and bezier shapes:[Wavelet Rasterization by J. Manson and S. Schaefer].

Indeed a limit of this drawing style. I guess this is why “[Shapes](https://acegikmo.com/shapes/docs/#anti-aliasing)” by [Freya Holmér](https://twitter.com/FreyaHolmer/) limits lines to a minimum 1px size and performs alpha fading instead, a technique named [Line Thinness Fading](https://acegikmo.com/shapes/docs/#anti-aliasing) in “Shapes”. And this is part of the issues around minimization I mentioned in chapter “The future of all things font?”.

As for the demos on this page, you can radius adjust the circle to be below 1px in the [implementation comparison](https://blog.frost.kiwi#implementation) above. With ⅛ Resolution on a 1080p Screen and an shrunk radius, you can push the rendering below 1px and see how this code handles it. In this specific case, quite well.

### TAA [#](https://blog.frost.kiwi#taa)

In the comments below, GitHub user [presentfactory](https://github.com/presentfactory) mentioned me going too hard on TAA. Indeed, this blog post didn’t go into which problems TAA tries to solve, that other techniques cannot. In a [tweet thread](https://twitter.com/NOTimothyLottes/status/1859225171678159318), Timothy Lottes also mentioned TAA as the clear technological evolution, but also states that there *are* limits to motion clarity.


[: Also FXAA 4 (2-frame blender) and TXAA are radically different, no MLAA in TXAA (MSAA based instead). I dropped FXAA 4, because I believed the MSAA based TAA’s (like the one in The Order on PS4) had been a much better technical evolution (MLAA’s cannot handle sub-pixel geometry)]Timothy Lottes

So to be clear, I think it was a radical improvement for the ML-scaling-TAA’s compared to where say UE4’s first TAA ended up. BUT fully solving the ghosting/flicker/artifact problems in the frame-jitter TAA framework might not actually be possible …

TAA goes * deep* and the way jitter resolves things other techniques can’t, takes some time to grasp intuitively.

[Previously](https://blog.frost.kiwi/GLSL-noise-and-radial-gradient)I introduced my favorite GLSL one-liner for dithering, which can also help TAA resolve effects temporally. Sledgehammer games used it for shadow filtering.

TAA is some fascinating stuff! This post was too full to appreciate it properly. Here's a recommended[deep-dive talk]by "[Inside]" developer[Lasse Jon Fuglsang Pedersen]