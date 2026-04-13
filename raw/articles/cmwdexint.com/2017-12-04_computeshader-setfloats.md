---
title: ComputeShader.SetFloats()
url: https://cmwdexint.com/2017/12/04/computeshader-setfloats/
author: Ming Wai Chan
published: '2017-12-04'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Originally I have in

**C#**

_floatArray = new float[2]; _floatArray[0] = 1f; _floatArray[1] = 0.5f;

**Compute Shader**

`float FloatArray[2];`

And use ComputeShader.SetFloats() to pass the values from C# to Compute Shader**.
**Reading the values in Compute Shader, I found that

**only FloatArray[0] has the value**. So FloatArray[1] will equals to 0.

Unity dev (Marton E.) replied me that:


This is expected behavior and user code should be modified to follow packing rules.


[HLSL specs]says:

“Arrays are not packed in HLSL by default. To avoid forcing the shader to take on ALU overhead for offset computations, every element in an array is stored in a four-component vector. Note that you can achieve packing for arrays (and incur the addressing calculations) by using casting.”

[Unity documentation]says:

“This function can be used to set float vector, float array or float vector array values. For example, float4 myArray[4] in the compute shader can be filled by passing 16 floats. See Compute Shaders for information on data layout rules and cross-platform compatibility.”Unity implementation doesn’t do casting suggested in HLSL documentation but just goes for unpacked storage (same as std140 GLSL directive) therefore calling SetFloats with a float[] argument should be aligned according to HLSL rules, i.e. float[] should be packed as every array item on 16 byte (float4) boundary.


So I should have in

**C#**

_floatArray = new float[4 * 4]; _floatArray[0] = 1f; _floatArray[4] = 0.5f; _floatArray[8] = 0.75f; _floatArray[12] = 1f;

**Compute Shader**

`float FloatArray[4];`

And read values in Compute Shader with

FloatArray[0], FloatArray[1], FloatArray[2], FloatArray[3] like usual.

——-

One more note for Mac Metal:

Metal does not enforce similar packing restriction but in order to maintain compatibility (along with GLCore) it was implemented the same way.


+1000 internet points for this post. I would of never figured this out from any documentation.

LikeLike

Thanks a lot! New to HLSL here, wondering why my code wasn’t working.

LikeLike