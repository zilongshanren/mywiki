---
tags: [渲染, shader, 创意编程, shader-art, code-golf]
date: 2026-04-19
sources: 2
---

# 280 字符 Tweet Shader 的思维方式

[[xor-shader-artist|Xor]] 在 twitter / X 上推广的 "**280 字符内的完整 shader**" 是一种极限 [[shader-code-golfing|code golf]] + [[creative-coding-process|creative coding]] 的融合体。它不是单纯的压缩游戏——它本身是一套**简化思维的训练**。

## 运行环境：Twigl 极简模式

[twigl.app](https://twigl.app) 是一个专为 tweet shader 设计的在线编辑器，"geekest 300" 模式下预设：

- `gl_FragColor` → `o`
- `gl_FragCoord` → `FC`（`FC.rgb` 包含 `xy + 0.5 + 1.0` 的第三维把一些 hack 变简洁）
- 分辨率 → `r`（`vec2`）
- 时间 → `t`（秒）
- 鼠标 → `m`、backbuffer → `b`
- `main()` 外层自动包装

省掉外壳后，280 字符就能塞下一个完整的 fragment shader。

## Xor 的三项代表作

### Galaxy in 197 chars

单层 fragment shader 画一个动画螺旋星系，靠 noise + 径向坐标旋转。

### Voxel DDA raytracer in 175 chars

把 Amanatides & Woo 的 3D DDA 算法塞进 175 字符，带边缘检测。这类"在限制内塞下一个真实算法"是 Xor 风格的标志。

### Phosphor in 258 chars（[[sources/xor-decoding-phosphor|技术拆解]]）

一个 shader 同时做：raymarch 循环 + glow 衰减 + 3D 场景旋转 + 相机位移 + 湍流流体 + 3D 圆环上的粒子分布。
全部代码复述如下，留意「for 循环的 `INIT; COND; LAST` 三段都被塞满了本该在循环体里做的事」：

```glsl
for (float i,z,d; i++<8e1; o += (cos(d/.1+vec4(0,2,4,0))+1.)/d*z) {
    vec3 p = z*normalize(FC.rgb*2.-r.xyy),
         a = normalize(cos(vec3(4,2,0)+t-d*8.));
    p.z += 5., a = a*dot(a,p)-cross(a,p);
    for (d=1.;d++<9.;) a += sin(a*d+t).yzx/d;
    z += d = .05*abs(length(p)-3.)+.04*abs(a.y);
}
o = tanh(o/1e4);
```

## 常见技巧

- **For 循环的每一段都要省出语句**：`INIT` 塞 `float i,z,d;`（一次三变量）；`LAST` 塞颜色累积。
- **逗号表达式多语句合并**：`p.z+=5., a=a*dot(a,p)-cross(a,p);`。
- **硬编码特殊角度**：如果要旋转 270°，`cos(t)=0, sin(t)=-1`，直接展开就省了 `sin/cos/mix`。
- **坐标构造省括号**：`.xyy` / `.yzx` 等 swizzle 比 `.y, .y, .x` 简洁一个字符。
- **tanh tonemap**：`tanh(o/K)` 一条指令解决 HDR 裁剪，见 [[hyperbolic-tangent-shader]]。
- **域折叠**：`abs(length(p)-3.)` 做一个空心球 SDF，比写两个球便宜。
- **湍流域形变**：`for(d=1;d<9;d++) a += sin(a*d+t).yzx/d` 是 Xor 的签名式湍流，见 [[turbulence-domain-warping]]。

## 为什么值得做

Xor 在 Codrops 的文章里列了四条动机：好奇与热情、学习与发现、挑战、社群。关键的一条**不是追求性能最优，而是追求"约束驱动的创造力"**——字符预算逼着你抛弃繁琐的抽象，回到最小可行 shader。多数情况下，压缩后的版本在 GPU 上其实也更快，因为省去了不必要的中间变量。

## 相关

- [[xor-shader-artist]]
- [[shader-code-golfing]]
- [[creative-coding-process]]
- [[density-field-volumetric]]
- [[turbulence-domain-warping]]
- [[hyperbolic-tangent-shader]]

## Sources

- [[sources/xor-modeling-the-world-in-280-chars]]
- [[sources/xor-decoding-phosphor]]
