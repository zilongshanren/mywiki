---
tags: [rendering, shader, unity, post-processing, tutorial]
date: 2026-04-14
sources: 2
---

# Unity Image Effect 基础（Built-in 管线）

Unity built-in 管线时代最常见的自定义后处理写法：一个继承自 `MonoBehaviour` 的脚本挂在相机上，通过 `OnRenderImage(RenderTexture src, RenderTexture dest)` 拦截相机的输出，用 `Graphics.Blit(src, dest, material)` 把源纹理经过一个自定义材质贴到目标纹理。材质背后是一支 ShaderLab 着色器，`_MainTex` 会被运行时自动赋值为相机渲染结果。这种写法常被叫做 *image effect shader*。

## 骨架解剖

典型的 image effect shader 文件由几块固定结构组成：

- **Shader 名字**：顶层 `Shader "Custom/..."`，决定在材质选择器菜单里的位置；写成 `Hidden/xxx` 时不会出现在菜单里。
- **Properties 块**：外部可调参数的声明，格式 `_Name ("Label", Type) = default`。这部分只是 Unity 编辑器侧的 UI 绑定，`_MainTex` 在 image effect 里会被相机输出覆盖掉。
- **SubShader**：包含一个或多个 Pass。全屏后处理用的固定三件套是 `Cull Off ZWrite Off ZTest Always`，让全屏四边形不受深度和剔除影响。
- **CGPROGRAM / HLSL 段**：真正喂给 GPU 的代码。Properties 里声明的变量必须在这里**同名再声明一次**才能被 GPU 读到，这是新手最容易踩的坑——Properties 块只跟 Unity 编辑器通信，HLSL 代码并不会自动看见它们。
- **appdata / v2f 结构体**：从顶点着色器到 [[fragment-shader]] 的输入输出约定，全屏后处理一般只需要 position + uv。
- **vert / frag**：顶点着色器只做裁剪空间变换和 UV 透传，片元着色器做真正的颜色运算。最简单的「反色」后处理就是 `col = tex2D(_MainTex, i.uv); return 1 - col;`。

## 挂接脚本

对应的 MonoBehaviour 是十行代码的模板，标 `[ExecuteInEditMode]` 就能在编辑器实时预览：

```csharp
[ExecuteInEditMode]
public class CustomImageEffect : MonoBehaviour {
    public Material material;
    void OnRenderImage(RenderTexture src, RenderTexture dest) {
        Graphics.Blit(src, dest, material);
    }
}
```

材质引用的就是上面那支 shader。多个 image effect 可以按组件顺序叠在同一个相机上，`Graphics.Blit` 会依次把上一阶段的 dest 当作下一阶段的 src。这种链式 blit 是 built-in 管线时代「Bloom/Vignette/Color Grading」这类全屏后处理的底层机制。

## 为什么现代管线用另一套

URP 和 HDRP 放弃了 `OnRenderImage` 回调，原因包括移动端上连续 blit 开销太大、不支持自定义 render target 的插入点、和 render graph 不兼容。URP 下等价的写法是实现一个 `ScriptableRendererFeature`（例如 [[blit-render-feature]]），把同样的全屏材质挂到自定义的 pass 上，这样可以精确控制它在哪一帧阶段执行、是否写入某张临时 RT。迁移一个 built-in image effect 到 URP 的主要工作是：把 MonoBehaviour 拆成 Feature + Pass，把 shader 的 HLSL 头文件换成 URP 的，`UNITY_MATRIX_MVP` 换成 `UnityObjectToClipPos`，顶点结构里加 `UNITY_VERTEX_INPUT_INSTANCE_ID`。

理解 image effect 的骨架对任何 shader 初学者都是一个好的切入点，因为它把顶点着色器折叠成几乎什么都不做的透传，让学习者专注在片元着色器的颜色运算上，不必先啃顶点变换、光照、材质系统那一整套。[[harry-alisavakis]] 在他 2017 年的 *My take on shaders* 系列第一篇用这个结构教完整套管线，后续的 [[night-time-tint-shader]] 就是在这个骨架上改一行 fragment 代码得到的。

## 相关

- [[fragment-shader]]
- [[shaderlab-hlsl-basics]]
- [[blit-render-feature]]
- [[scriptable-render-pipeline]]
- [[night-time-tint-shader]]
- [[bluk-2d-fog-sprite-shader]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-image-effects-intro]]
- [[sources/halisavakis-night-time-shader]]
