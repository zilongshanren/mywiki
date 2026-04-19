---
title: ShaderGraph 2
url: https://acko.net/blog/shadergraph-2/
author: Steven Wittens
published: '2015-09-27'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![ShaderGraph 2](../../assets/6f65d6816819da2f.png)

# ShaderGraph 2

## Functional GLSL

For MathBox 1, I already needed to generate GL shaders programmatically. So I built ShaderGraph. You gave it snippets of GLSL code, each with a function inside. It would connect them for you, matching up the inputs and outputs. It supported directed graphs of calls with splits and joins, which were compiled down into a single shader. To help build up the graph progressively, it came with a simple chainable factory API.

It worked despite being several steps short of being a real compiler and having gaps in its functionality. It also committed the cardinal sin of regex code parsing, and hence accepted only a small subset of GLSL. All in all it was a bit of a happy mess, weaving vertex and fragment shaders together in a very ad-hoc fashion. Each snippet could only appear once in a shader, as it was still just a dumb code concatenator. I needed a proper way to compose shaders.

*Select a node to view its code*

## Instanced Data Flow

Enter [ShaderGraph 2](https://github.com/unconed/shadergraph). It's a total rewrite using Chris Dickinson's bona fide `glsl-parser`

. It still parses snippets and connects them into a directed graph to be compiled. But a snippet is now a full GLSL program whose `main()`

function can have open inputs and outputs. What's more, it now also *links* code in the proper sense of the word: linking up module entry points as callbacks.

Basically, snippets can now have inputs and outputs that are themselves functions. These connections don't obey the typical data flow of a directed graph and instead are for function calls. A callback connection provides a path along which calls are made and values are returned.

Snippets can be instanced multiple times, including their uniforms, attributes and varyings (if requested). Uniforms are bound to Three.js-style registers as you build the graph incrementally. So it's a module system, sort of, which enables functional shader building. Using callbacks as micro-interfaces feels very natural in practice, especially with bound parameters. You can decorate existing functions, e.g. turning a texture sampler into a convolution filter.

```
// Build shader graph
var shader = shadergraph.shader();
shader
.callback()
.pipe('sampleColor')
.fan()
.pipe('sepiaColor')
.next()
.pipe('invertColor')
.join()
.pipe('combineColors')
.join()
.pipe('convolveColor');
```


## GLSL Composer

If you know GLSL, you can write ShaderGraph snippets: there is no extra syntax, you just add inputs and outputs to your `main()`

function. You can use `in/out/inout`

qualifiers or return a value. If there's no main function, the last defined function is exported.

`vec3 callback(vec3 arg1, vec3 arg2);`


To create a *callback input* in a snippet, you declare a function prototype in GLSL without a body. The function name and signature is used to create the outlet.

To create a *callback output*, you use the factory API. You can `.require()`

a snippet directly, or bundle up a subgraph with `.callback().….join()`

. In the latter case, the function signature includes all unconnected inputs and outputs inside. Outlets are auto-matched by name, type and order, with the semantics from v1 cleaned up.

Building basic pipes is easy: `.pipe(…).pipe(…).…`

, passing in a snippet or factory. For forked graphs, you can `.fan()`

(1-to-N) or `.split()`

(N-to-N), use `.next()`

to begin a new branch, and then `.join()`

at the end. There's a few other operations, nothing crazy.

```
var v = shadergraph.shader();
// Graphs generated elsewhere
v.pipe(vertexColor(color, mask));
v.require(vertexPosition(position, material, map, 2, stpq));
v.pipe('line.position', uniforms, defs);
v.pipe('project.position', uniforms);
```


By connecting pairs you create a functional data flow that compiles down to vanilla GLSL. It's not functional programming *in* GLSL, it just enables useful run-time assembly patterns, letting the snippets do the heavy lifting the old fashioned way.

As GPUs are massively parallel pure function applicators, the resulting mega-shaders are a great fit.

`$ cat *.glsl | magic`


The process still comes down to concatenating the code in a clever way, with global symbols namespaced to be unique. Function bodies are generated to call snippets in the right order, and the callbacks are linked. In the trivial case it links a callback by `#define`

ing the two symbols to be the same. It can also impedance match compatible signatures like `void main(in float, out vec2)`

and `vec2 main(float)`

by inserting an intermediate call.

```
precision highp float;
precision highp int;
uniform mat4 modelMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat3 normalMatrix;
uniform vec3 cameraPosition;
#define _sn_191_getPosition _pg_103_
#define _sn_190_getPosition _pg_102_
#define _sn_189_getSample _pg_100_
#define _pg_99_ _sn_185_warpVertex
#define _pg_103_ _sn_190_getMeshPosition
#define _pg_100_ _sn_188_getTransitionSDFMask
#define _pg_101_ _sn_189_maskLevel
vec2 _sn_180_truncateVec(vec4 v) { return v.xy; }
uniform vec2 _sn_181_dataResolution;
uniform vec2 _sn_181_dataPointer;
vec2 _sn_181_map2DData(vec2 xy) {
return fract((xy + _sn_181_dataPointer) * _sn_181_dataResolution);
}
uniform sampler2D _sn_182_dataTexture;
vec4 _sn_182_sample2D(vec2 uv) {
return texture2D(_sn_182_dataTexture, uv);
}
vec4 _sn_183_swizzle(vec4 xyzw) {
return vec4(xyzw.x, xyzw.w, 0.0, 0.0);
}
uniform float _sn_184_polarBend;
uniform float _sn_184_polarFocus;
uniform float _sn_184_polarAspect;
uniform float _sn_184_polarHelix;
uniform mat4 _sn_184_viewMatrix;
vec4 _sn_184_getPolarPosition(vec4 position, inout vec4 stpq) {
if (_sn_184_polarBend > 0.0) {
if (_sn_184_polarBend < 0.001) {
vec2 pb = position.xy * _sn_184_polarBend;
float ppbbx = pb.x * pb.x;
return _sn_184_viewMatrix * vec4(
position.x * (1.0 - _sn_184_polarBend + (pb.y * _sn_184_polarAspect)),
position.y * (1.0 - .5 * ppbbx) - (.5 * ppbbx) * _sn_184_polarFocus / _sn_184_polarAspect,
position.z + position.x * _sn_184_polarHelix * _sn_184_polarBend,
1.0
);
}
else {
vec2 xy = position.xy * vec2(_sn_184_polarBend, _sn_184_polarAspect);
float radius = _sn_184_polarFocus + xy.y;
return _sn_184_viewMatrix * vec4(
sin(xy.x) * radius,
(cos(xy.x) * radius - _sn_184_polarFocus) / _sn_184_polarAspect,
position.z + position.x * _sn_184_polarHelix * _sn_184_polarBend,
1.0
);
}
}
else {
return _sn_184_viewMatrix * vec4(position.xyz, 1.0);
}
}
uniform float _sn_185_time;
uniform float _sn_185_intensity;
vec4 _sn_185_warpVertex(vec4 xyzw, inout vec4 stpq) {
xyzw += 0.2 * _sn_185_intensity * (sin(xyzw.yzwx * 1.91 + _sn_185_time + sin(xyzw.wxyz * 1.74 + _sn_185_time)));
xyzw += 0.1 * _sn_185_intensity * (sin(xyzw.yzwx * 4.03 + _sn_185_time + sin(xyzw.wxyz * 2.74 + _sn_185_time)));
xyzw += 0.05 * _sn_185_intensity * (sin(xyzw.yzwx * 8.39 + _sn_185_time + sin(xyzw.wxyz * 4.18 + _sn_185_time)));
xyzw += 0.025 * _sn_185_intensity * (sin(xyzw.yzwx * 15.1 + _sn_185_time + sin(xyzw.wxyz * 9.18 + _sn_185_time)));
return xyzw;
}
vec4 _sn_186_getViewPosition(vec4 position, inout vec4 stpq) {
return (viewMatrix * vec4(position.xyz, 1.0));
}
vec3 _sn_187_getRootPosition(vec4 position, in vec4 stpq) {
return position.xyz;
}
vec3 _pg_102_(vec4 _io_510_v, in vec4 _io_519_stpq) {
vec2 _io_509_return;
vec2 _io_511_return;
vec4 _io_513_return;
vec4 _io_515_return;
vec4 _io_517_return;
vec4 _io_520_stpq;
vec4 _io_527_return;
vec4 _io_528_stpq;
vec4 _io_529_return;
vec4 _io_532_stpq;
vec3 _io_533_return;
_io_509_return = _sn_180_truncateVec(_io_510_v);
_io_511_return = _sn_181_map2DData(_io_509_return);
_io_513_return = _sn_182_sample2D(_io_511_return);
_io_515_return = _sn_183_swizzle(_io_513_return);
_io_520_stpq = _io_519_stpq;
_io_517_return = _sn_184_getPolarPosition(_io_515_return, _io_520_stpq);
_io_528_stpq = _io_520_stpq;
_io_527_return = _pg_99_(_io_517_return, _io_528_stpq);
_io_532_stpq = _io_528_stpq;
_io_529_return = _sn_186_getViewPosition(_io_527_return, _io_532_stpq);
_io_533_return = _sn_187_getRootPosition(_io_529_return, _io_532_stpq);
return _io_533_return;
}
uniform vec4 _sn_190_geometryResolution;
#ifdef POSITION_STPQ
varying vec4 vSTPQ;
#endif
#ifdef POSITION_U
varying float vU;
#endif
#ifdef POSITION_UV
varying vec2 vUV;
#endif
#ifdef POSITION_UVW
varying vec3 vUVW;
#endif
#ifdef POSITION_UVWO
varying vec4 vUVWO;
#endif
vec3 _sn_190_getMeshPosition(vec4 xyzw, float canonical) {
vec4 stpq = xyzw * _sn_190_geometryResolution;
vec3 xyz = _sn_190_getPosition(xyzw, stpq);
#ifdef POSITION_MAP
if (canonical > 0.5) {
#ifdef POSITION_STPQ
vSTPQ = stpq;
#endif
#ifdef POSITION_U
vU = stpq.x;
#endif
#ifdef POSITION_UV
vUV = stpq.xy;
#endif
#ifdef POSITION_UVW
vUVW = stpq.xyz;
#endif
#ifdef POSITION_UVWO
vUVWO = stpq;
#endif
}
#endif
return xyz;
}
uniform float _sn_188_transitionEnter;
uniform float _sn_188_transitionExit;
uniform vec4 _sn_188_transitionScale;
uniform vec4 _sn_188_transitionBias;
uniform float _sn_188_transitionSkew;
uniform float _sn_188_transitionActive;
float _sn_188_getTransitionSDFMask(vec4 stpq) {
if (_sn_188_transitionActive < 0.5) return 1.0;
float enter = _sn_188_transitionEnter;
float exit = _sn_188_transitionExit;
float skew = _sn_188_transitionSkew;
vec4 scale = _sn_188_transitionScale;
vec4 bias = _sn_188_transitionBias;
float factor = 1.0 + skew;
float offset = dot(vec4(1.0), stpq * scale + bias);
vec2 d = vec2(enter, exit) * factor + vec2(-offset, offset - skew);
if (exit == 1.0) return d.x;
if (enter == 1.0) return d.y;
return min(d.x, d.y);
}
uniform float _sn_191_worldUnit;
uniform float _sn_191_lineWidth;
uniform float _sn_191_lineDepth;
uniform float _sn_191_focusDepth;
uniform vec4 _sn_191_geometryClip;
attribute vec2 line;
attribute vec4 position4;
#ifdef LINE_PROXIMITY
uniform float _sn_191_lineProximity;
varying float vClipProximity;
#endif
#ifdef LINE_STROKE
varying float vClipStrokeWidth;
varying float vClipStrokeIndex;
varying vec3 vClipStrokeEven;
varying vec3 vClipStrokeOdd;
varying vec3 vClipStrokePosition;
#endif
#ifdef LINE_CLIP
uniform float _sn_191_clipRange;
uniform vec2 _sn_191_clipStyle;
uniform float _sn_191_clipSpace;
attribute vec2 strip;
varying vec2 vClipEnds;
void _sn_191_clipEnds(vec4 xyzw, vec3 center, vec3 pos) {
vec4 xyzwE = vec4(strip.y, xyzw.yzw);
vec3 end = _sn_191_getPosition(xyzwE, 0.0);
vec4 xyzwS = vec4(strip.x, xyzw.yzw);
vec3 start = _sn_191_getPosition(xyzwS, 0.0);
vec3 diff = end - start;
float l = length(diff) * _sn_191_clipSpace;
float arrowSize = 1.25 * _sn_191_clipRange * _sn_191_lineWidth * _sn_191_worldUnit;
vClipEnds = vec2(1.0);
if (_sn_191_clipStyle.y > 0.0) {
float depth = _sn_191_focusDepth;
if (_sn_191_lineDepth < 1.0) {
float z = max(0.00001, -end.z);
depth = mix(z, _sn_191_focusDepth, _sn_191_lineDepth);
}
float size = arrowSize * depth;
float mini = clamp(1.0 - l / size * .333, 0.0, 1.0);
float scale = 1.0 - mini * mini * mini;
float invrange = 1.0 / (size * scale);
diff = normalize(end - center);
float d = dot(end - pos, diff);
vClipEnds.x = d * invrange - 1.0;
}
if (_sn_191_clipStyle.x > 0.0) {
float depth = _sn_191_focusDepth;
if (_sn_191_lineDepth < 1.0) {
float z = max(0.00001, -start.z);
depth = mix(z, _sn_191_focusDepth, _sn_191_lineDepth);
}
float size = arrowSize * depth;
float mini = clamp(1.0 - l / size * .333, 0.0, 1.0);
float scale = 1.0 - mini * mini * mini;
float invrange = 1.0 / (size * scale);
diff = normalize(center - start);
float d = dot(pos - start, diff);
vClipEnds.y = d * invrange - 1.0;
}
}
#endif
const float _sn_191_epsilon = 1e-5;
void _sn_191_fixCenter(vec3 left, inout vec3 center, vec3 right) {
if (center.z >= 0.0) {
if (left.z < 0.0) {
float d = (center.z - _sn_191_epsilon) / (center.z - left.z);
center = mix(center, left, d);
}
else if (right.z < 0.0) {
float d = (center.z - _sn_191_epsilon) / (center.z - right.z);
center = mix(center, right, d);
}
}
}
void _sn_191_getLineGeometry(vec4 xyzw, float edge, out vec3 left, out vec3 center, out vec3 right) {
vec4 delta = vec4(1.0, 0.0, 0.0, 0.0);
center = _sn_191_getPosition(xyzw, 1.0);
left = (edge > -0.5) ? _sn_191_getPosition(xyzw - delta, 0.0) : center;
right = (edge < 0.5) ? _sn_191_getPosition(xyzw + delta, 0.0) : center;
}
vec3 _sn_191_getLineJoin(float edge, bool odd, vec3 left, vec3 center, vec3 right, float width) {
vec2 join = vec2(1.0, 0.0);
_sn_191_fixCenter(left, center, right);
vec4 a = vec4(left.xy, right.xy);
vec4 b = a / vec4(left.zz, right.zz);
vec2 l = b.xy;
vec2 r = b.zw;
vec2 c = center.xy / center.z;
vec4 d = vec4(l, c) - vec4(c, r);
float l1 = dot(d.xy, d.xy);
float l2 = dot(d.zw, d.zw);
if (l1 + l2 > 0.0) {
if (edge > 0.5 || l2 == 0.0) {
vec2 nl = normalize(d.xy);
vec2 tl = vec2(nl.y, -nl.x);
#ifdef LINE_PROXIMITY
vClipProximity = 1.0;
#endif
#ifdef LINE_STROKE
vClipStrokeEven = vClipStrokeOdd = normalize(left - center);
#endif
join = tl;
}
else if (edge < -0.5 || l1 == 0.0) {
vec2 nr = normalize(d.zw);
vec2 tr = vec2(nr.y, -nr.x);
#ifdef LINE_PROXIMITY
vClipProximity = 1.0;
#endif
#ifdef LINE_STROKE
vClipStrokeEven = vClipStrokeOdd = normalize(center - right);
#endif
join = tr;
}
else {
float lmin2 = min(l1, l2) / (width * width);
#ifdef LINE_PROXIMITY
float lr = l1 / l2;
float rl = l2 / l1;
float ratio = max(lr, rl);
float thresh = _sn_191_lineProximity + 1.0;
vClipProximity = (ratio > thresh * thresh) ? 1.0 : 0.0;
#endif
vec2 nl = normalize(d.xy);
vec2 nr = normalize(d.zw);
vec2 tl = vec2(nl.y, -nl.x);
vec2 tr = vec2(nr.y, -nr.x);
#ifdef LINE_PROXIMITY
vec2 tc = normalize(mix(tl, tr, l1/(l1+l2)));
#else
vec2 tc = normalize(tl + tr);
#endif
float cosA = dot(nl, tc);
float sinA = max(0.1, abs(dot(tl, tc)));
float factor = cosA / sinA;
float scale = sqrt(1.0 + min(lmin2, factor * factor));
#ifdef LINE_STROKE
vec3 stroke1 = normalize(left - center);
vec3 stroke2 = normalize(center - right);
if (odd) {
vClipStrokeEven = stroke1;
vClipStrokeOdd = stroke2;
}
else {
vClipStrokeEven = stroke2;
vClipStrokeOdd = stroke1;
}
#endif
join = tc * scale;
}
return vec3(join, 0.0);
}
else {
return vec3(0.0);
}
}
vec3 _sn_191_getLinePosition() {
vec3 left, center, right, join;
float edge = line.x;
float offset = line.y;
vec4 p = min(_sn_191_geometryClip, position4);
edge += max(0.0, position4.x - _sn_191_geometryClip.x);
_sn_191_getLineGeometry(p, edge, left, center, right);
#ifdef LINE_STROKE
vClipStrokePosition = center;
vClipStrokeIndex = p.x;
bool odd = mod(p.x, 2.0) >= 1.0;
#else
bool odd = true;
#endif
float width = _sn_191_lineWidth * 0.5;
float depth = _sn_191_focusDepth;
if (_sn_191_lineDepth < 1.0) {
float z = max(0.00001, -center.z);
depth = mix(z, _sn_191_focusDepth, _sn_191_lineDepth);
}
width *= depth;
width *= _sn_191_worldUnit;
join = _sn_191_getLineJoin(edge, odd, left, center, right, width);
#ifdef LINE_STROKE
vClipStrokeWidth = width;
#endif
vec3 pos = center + join * offset * width;
#ifdef LINE_CLIP
_sn_191_clipEnds(p, center, pos);
#endif
return pos;
}
uniform vec4 _sn_189_geometryResolution;
uniform vec4 _sn_189_geometryClip;
varying float vMask;
void _sn_189_maskLevel() {
vec4 p = min(_sn_189_geometryClip, position4);
vMask = _sn_189_getSample(p * _sn_189_geometryResolution);
}
uniform float _sn_192_styleZBias;
uniform float _sn_192_styleZIndex;
void _sn_192_setPosition(vec3 position) {
vec4 pos = projectionMatrix * vec4(position, 1.0);
float bias = (1.0 - _sn_192_styleZBias / 32768.0);
pos.z *= bias;
if (_sn_192_styleZIndex > 0.0) {
float z = pos.z / pos.w;
pos.z = ((z + 1.0) / (_sn_192_styleZIndex + 1.0) - 1.0) * pos.w;
}
gl_Position = pos;
}
void main() {
vec3 _io_546_return;
_io_546_return = _sn_191_getLinePosition();
_sn_192_setPosition(_io_546_return);
_pg_101_();
}
```


It still does guarded regex manipulation of code too, but those manipulations are now derived from a proper syntax tree. GLSL doesn't have strings and its scope is simple, so this is unusually safe. I'm sure you can still trip it up somehow, but it's worth it for speed. I'm seeing assembly times of ~10-30ms cold, 2-4ms warm, but it depends entirely on the particular shaders.

The assembly process is now properly recursive. Unassembled shaders can be used in factory form, standing in for snippets. Completed graphs form stand-alone programs with no open inputs or outputs. The result can be turned straight into a Three.js `ShaderMaterial`

, but there is no strict Three dependency. It's just a dictionary with code and a list of uniforms, attributes and varyings. Unlike before, building a combined vertex/fragment program is now merely syntactic sugar for a pair of separate graphs.

As it's run-time, you can slot in user-defined or code-generated GLSL just the same. Shaders are fetched by name or passed as inline code, mixed freely as needed. You supply the dictionary or lookup method. You could bundle your GLSL into JS with a build step or include embedded `<script>`

tags.

*This is the fragment shader that implements the partial differential equation for this ripple effect ( getFramesSample). It samples from a volumetric N×N×2 array, feeding back into itself.*

## Paging Dr. Hickey

ShaderGraph 2 drives the entirety of MathBox 2. Its shaders are specialized for particular types and dimensions, generating procedural data, clipping geometry, resampling transformed data on the fly, …. The composibility comes out naturally. To do so, I pass a partially built `factory`

by interested parties. This way I build graphs for position, color, normal, mask and more. These are injected as callbacks into a final shader. Shader factories enable ad-hoc contracts, sandwiched between the inner and outer retained layers of Three.js and MathBox, but disappearing entirely in the end result.

Of course, all of this is meta-programming of GLSL, done through a stateful JS lasagna and a ghetto compiler, instead of an idiomatic language. I know this, it's an inner platform effect bathing luxuriously in Turing tar like a rhino in mud. I didn't really see a way around it, given the constraints at play.

While the factory API is designed for making graphs on the spot and then tossing them, you could keep graphs around. There's a full data model underneath. You can always skip the factory entirely.

Plenty of caveats of course. There is no built-in preprocessor, so you can't `#define`

or `#ifdef`

uniforms or attributes and have it make sense. But then the point of ShaderGraph is to formalize exactly that sort of ad-hoc fiddling. Preprocessor directives will just pass through. `glsl-parser`

has gaps too, and it is also exceedingly picky with reserved variable names, so watch out for that.

I did sometimes feel the need for more powerful metaprogramming, but you can work around it. It is easy to dynamically make GLSL one-liner snippets and feed them in. String manipulation of code is always still an option, you just don't need to do it at the macro-level anymore.

ShaderGraph 2 has been in active use now for months, it does the job I need it to very well. In a perfect world, this would be solved at the GPU driver level. Until SPIR-V or WebVulkan gets here, imma stick to my regexes. Don't try this at home, kids.

*For docs and more, see the Git repository.*

[MathBox² - PowerPoint Must Die](https://acko.net/blog/mathbox2/)[A DOM for Robots - Modelling Live Data](https://acko.net/blog/a-dom-for-robots/)[Yak Shading - Data Driven Geometry](https://acko.net/blog/yak-shading/)*ShaderGraph 2 - Functional GLSL*