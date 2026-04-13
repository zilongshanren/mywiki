---
title: A brief postscript on moment-based order-independent transparency
url: http://momentsingraphics.de/MissingTMBOITCode.html
published: '2018-08-23'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# A brief postscript on moment-based order-independent transparency

Back in May, we published [moment-based order-independent transparency](http://momentsingraphics.de/I3D2018.html) (MBOIT) at the [Symposium on Interactive 3D Graphics and Games 2018](http://i3dsymposium.github.io/2018/). This brief post follows up on two things; a similar but independent work and some missing code.

## Moment transparency

At [High-Performance Graphics 2018](https://www.highperformancegraphics.org/2018/) there is a paper by [Brian Sharpe](https://briansharpe.wordpress.com/) from Weta Digital titled [Moment Transparency](https://dl.acm.org/citation.cfm?id=3231585). Brian submitted this work to HPG shortly before our i3D paper was made available, so it is a concurrent and independent work but pursuing the same basic idea: Moments serve to represent optical depth enabling truly order-independent transparency with nothing but two additive rendering passes. Both techniques have variants with four power moments that are virtually identical.

Nonetheless, there are differences. Our work features six different choices of moments, can use rasterizer ordered views to store them in half the memory and offers shadows for transparent shadow casters. Moment transparency proposes to render moments at a lower resolution, utilizes non-linear quantization and features a mode with an additional pass that is meant to get more out of four moments.

Brian has done exellent work and it is good to see that others are picking up [moment-based methods](http://momentsingraphics.de/DissertationAnnouncement.html). If you are interested in using [MBOIT](http://momentsingraphics.de/I3D2018.html), you should also read Brian's [Moment Transparency](https://dl.acm.org/citation.cfm?id=3231585) and vice versa. Hopefully, this post will avoid some confusion about the two techniques.

## Missing code

Brian noticed that the code that we published is a little incomplete. We published shader code only, so the code to set up the various constant buffers is missing. In most cases, the constants are easy enough to get right but if you want to use MBOIT with trigonometric moments, you need to set an entry called `float4 wrapping_zone_parameters`

and that is more complicated. The four values all arise from the wrapping zone angle (usually \(\frac{\pi}{10}\)) but are pre-computed to save some work in the shader. This computation is performed by the following C++ code:

```
#include <cmath>
/*! Circle constant.*/
#ifndef M_PI
#define M_PI 3.14159265358979323f
#endif
/*! This utility function turns an angle from 0 to 2*pi into a parameter that
grows monotonically as function of the input. It is designed to be
efficiently computable from a point on the unit circle and must match the
function in TrigonometricMomentMath.hlsli.
\param pOutMaxParameter Set to the maximal possible output value.*/
float circleToParameter(float angle, float* pOutMaxParameter = nullptr) {
float x = std::cos(angle);
float y = std::sin(angle);
float result = std::abs(y) - std::abs(x);
result = (x<0.0f) ? (2.0f - result) : result;
result = (y<0.0f) ? (6.0f - result) : result;
result += (angle >= 2.0f * M_PI) ? 8.0f : 0.0f;
if (pOutMaxParameter) {
(*pOutMaxParameter) = 7.0f;
}
return result;
}
/*! Given an angle in radians providing the size of the wrapping zone, this
function computes all constants required by the shader.*/
void computeWrappingZoneParameters(float p_out_wrapping_zone_parameters[4],float new_wrapping_zone_angle = 0.1f * M_PI) {
p_out_wrapping_zone_parameters[0] = new_wrapping_zone_angle;
p_out_wrapping_zone_parameters[1] = M_PI - 0.5f * new_wrapping_zone_angle;
if (new_wrapping_zone_angle <= 0.0f) {
p_out_wrapping_zone_parameters[2] = 0.0f;
p_out_wrapping_zone_parameters[3] = 0.0f;
}
else {
float zone_end_parameter;
float zone_begin_parameter = circleToParameter(2.0f * M_PI - new_wrapping_zone_angle, &zone_end_parameter);
p_out_wrapping_zone_parameters[2] = 1.0f / (zone_end_parameter - zone_begin_parameter);
p_out_wrapping_zone_parameters[3] = 1.0f - zone_end_parameter * p_out_wrapping_zone_parameters[2];
}
}
```


Like all code that comes with MBOIT, the code above is made available under [CC0](https://creativecommons.org/publicdomain/zero/1.0/).