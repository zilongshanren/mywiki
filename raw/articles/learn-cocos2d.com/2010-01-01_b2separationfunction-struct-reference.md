---
title: b2SeparationFunction Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_separation_function/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2SeparationFunction Struct Reference

[List of all members.](/)

## Public Types |
| enum | [Type](../../../box2d-api-reference/API/structb2_separation_function/#a8c1446894223e9b6c80dc4d7230141a4) { [e_points](../../../box2d-api-reference/API/structb2_separation_function/#a8c1446894223e9b6c80dc4d7230141a4af830d0c5486d2bc9f184845d749c6881),
[e_faceA](../../../box2d-api-reference/API/structb2_separation_function/#a8c1446894223e9b6c80dc4d7230141a4a2b20fea3586ba7dceadfcd76a4257a22),
[e_faceB](../../../box2d-api-reference/API/structb2_separation_function/#a8c1446894223e9b6c80dc4d7230141a4a3d70e056a292a2aaf38e8b56c276a713)
} |
## Public Member Functions |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [Initialize](../../../box2d-api-reference/API/structb2_separation_function/#a642ead4a34d5ffe5300877510a7b0dfd) (const [b2SimplexCache](../../../box2d-api-reference/API/structb2_simplex_cache/) *cache, const [b2DistanceProxy](../../../box2d-api-reference/API/structb2_distance_proxy/) *proxyA, const [b2Sweep](../../../box2d-api-reference/API/structb2_sweep/) &sweepA, const [b2DistanceProxy](../../../box2d-api-reference/API/structb2_distance_proxy/) *proxyB, const [b2Sweep](../../../box2d-api-reference/API/structb2_sweep/) &sweepB) |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [FindMinSeparation](../../../box2d-api-reference/API/structb2_separation_function/#a33a79217db8089b8927a4dfe47088f43) ([int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) *indexA, [int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) *indexB, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) t) const |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) | [Evaluate](../../../box2d-api-reference/API/structb2_separation_function/#a4464af744155a59217e3dafc83c2e7f3) ([int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) indexA, [int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) indexB, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) t) const |
## Public Attributes |
const [b2DistanceProxy](../../../box2d-api-reference/API/structb2_distance_proxy/) * | [m_proxyA](../../../box2d-api-reference/API/structb2_separation_function/#a5c03d798e97cd653aa7db390275bf9a7) |
const [b2DistanceProxy](../../../box2d-api-reference/API/structb2_distance_proxy/) * | [m_proxyB](../../../box2d-api-reference/API/structb2_separation_function/#a25fc938e03bf77ac276b17b24e52958f) |
[b2Sweep](../../../box2d-api-reference/API/structb2_sweep/) | [m_sweepA](../../../box2d-api-reference/API/structb2_separation_function/#a46b838a661baa40cde771b779c2ff341) |
[b2Sweep](../../../box2d-api-reference/API/structb2_sweep/) | [m_sweepB](../../../box2d-api-reference/API/structb2_separation_function/#a11ba433f6e524fb92390bd8b4dd376b6) |
[Type](../../../box2d-api-reference/API/structb2_separation_function/#a8c1446894223e9b6c80dc4d7230141a4) | [m_type](../../../box2d-api-reference/API/structb2_separation_function/#a51075eff2de404a1d82eee831fdfd4af) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_localPoint](../../../box2d-api-reference/API/structb2_separation_function/#ab77a17de0f5c708212090f599ec1795e) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_axis](../../../box2d-api-reference/API/structb2_separation_function/#a767b8fc4174d200ae8fb1d2bfba3407b) |


## Member Enumeration Documentation


## Member Function Documentation


## Member Data Documentation


The documentation for this struct was generated from the following file: