---
tags: [pc-porting, gpu-drivers, qa, compatibility, testing]
date: 2026-04-19
sources: 2
---

# PC 发行的显卡驱动兼容地狱

[[joost-van-dongen]] 在 PS3 / Wii 上发行 *De Blob* 和 *Swords & Soldiers* 之后，把 *Swords & Soldiers* 移到 PC + Mac + Steam，得出一条逆直觉结论：**PC 发行比主机发行难**。主机认证（TRC / TCR / Lotcheck）虽然有几百条测试项，**但要求都合理、且目标硬件 uniform**——所有 PS3 本质一样，测一台等于测所有。PC 发行则在一个「硬件 × 驱动 × OS × 用户设置」的笛卡尔积里挨坑。

**典型坑位**（全部来自 *Swords & Soldiers* / *De Blob* / *Proun* 真实现场）：

1. **Non-Power-of-Two texture 检测不可靠**。为了省空间（600×512 不想补到 1024×512），Proun 用 NPOT。想根据硬件能力切 HD / SD 档位，查 OpenGL 扩展——但**部分显卡没有该扩展却能正常跑 NPOT**。最后 van Dongen 放弃自动检测，改成「让所有人选 HD，坏了就提示切 SD」。
2. **Max vertex index 上限**。某些老 Intel 板载显卡不能画 > 65536 顶点的单个 mesh。Proun 的解决方案是**不解决**——作为 hobby project，重写 mesh 切分不值得。Reg 在评论里补充：DirectX SDK 的 *CardCaps.xls* 明确列出了这些芯片（Intel 915/910、945、G33/G31、Q35）的 `MaxVertexIndex = 65534`，查一查就知道。
3. **Shader 能力说谎**。*De Blob* 遇到某些显卡声称支持 shader 2.0、实际加载 shader 时拒绝。能力查询本身是骗子，没法信。
4. **`glTexSubImage2D` 的未解之谜**。*Swords & Soldiers* 用动态字形系统（运行时只加载用到的字，支持中日韩）。这个系统是**在全部显卡 QA 完成之后**加的，没有复测——导致 \~1% 用户完全看不到文本。Day-1 补丁绕开 `glTexSubImage2D`，绕开后好了，但**根因始终没查清**。评论里 Mike 猜测和纹理格式（A8 vs RGBA/ARGB）有关——Joost 确认他们就是 IA8。
5. **双显示器刷新率不一致**把某 DirectX 自研引擎的全屏模式卡成 juddering；拔一台就好、窗口模式没事。

**延伸到发行实践**（*Awesomenauts* 工作室层面的 QA 流程）：
- **老 GPU 当毒药测试机**：故意找一台最烂的 netbook，老 GPU 能暴露的问题多过新 GPU。
- **发前 Steam 开 beta / closed beta**，让玩家的野外硬件先踩坑。
- **发后靠快速补丁兜底**：build 系统调好后可以做到当日热修。
- **给报 bug 的用户寄定制 build**：带更多日志、甚至带多个备选修复方案让玩家自测，玩家通常很配合。
- **QA 公司**（有大量硬件做兼容性测试）作为预算选项。

这篇 2010 年的文章对今天的适用性：具体的 API bug（glTexSubImage2D、NPOT 扩展）过时，但**「PC 笛卡尔积 >> 主机 uniform 硬件」+「QA 流程应该用老 GPU / beta / 患者协作」** 的方法论依然成立——2025 年 Steam 玩家的硬件分布比 2010 年更散（集显 + 独显 + AMD/NVIDIA/Intel + Windows/Mac/Linux/Proton），结论只会更强。

## 相关

- [[joost-van-dongen]]

## Sources
- [[sources/joostdevblog-pc-dev-horror]]
- [[sources/joostdevblog-proun-patch-v108]] —— Proun v108 补丁：ATI X1xxx SM3.0 说谎触发 DOF 崩溃；Intel GMA 3xxx 上 `IDirect3D9` 与 `IDirect3DDevice9` 对 vertex shader 能力答案互斥；另带一个 6 年埋下的 `cross(dir,[0,1,0])` 退化 bug，被 Cubed 用户赛道当模糊测试触发
