---
tags: [资源管线, 工具链, collada, dcc, 游戏引擎]
date: 2026-04-19
sources: 1
---

# 资源交换格式的三条路线（Supnik 的 COLLADA 抉择）

任何跨 DCC（Maya / 3ds Max / Blender / AC3D / Modo）供工作流的游戏引擎都会面对同一个问题：**如何把艺术家在第三方建模器里创建的几何 + 引擎专属注解，稳定地搬进引擎的私有运行时格式**？[[ben-supnik|Supnik]] 在 2011 年为 X-Plane 盘点了三条路线，指出的权衡今天仍适用。

## 背景：X-Plane 的特殊难度

X-Plane 是一个**开放平台**，美术资产来自全世界第三方开发者——没法约束大家都用同一款 DCC。引擎又需要「billboard 属性、硬表面参数、动画标记」这类引擎特有元数据从 DCC 侧就能录入并携带到运行时。

## 路线 A：为每个 DCC 单独写 exporter

X-Plane 当时走的路：Blender、AC3D、3ds Max、Maya 各一套独立 exporter，由不同人维护。**短期见效最快**，因为每个 exporter 可以针对该 DCC 的原生数据结构最优建模。

失败点是**扩展性线性恶化**——每个引擎新增一个建模特性（比如新一类硬表面属性），就要在 N 个 exporter 里并行实现。Supnik 本人维护的 AC3D exporter 都跟不上自己引擎的进度，别人的 exporter 更不可能全齐。最终结果是**格式支持度对不齐**，美术要凭 exporter 版本号选能用的特性子集。

## 路线 B：自造简单中间格式 + 后处理工具

让每个 DCC exporter 只负责**把数据原样倒出来**成一个简单文本流，真正的优化 / 编码 / 打包由一个离线工具（用引擎自带库）做第二步。

X-Plane 的 DSF scenery 格式就是这套思路：DSF 是复杂位打包二进制，但有 `DSF2Text` 工具转换简单文本 → 最终二进制。

优点：
- DCC exporter 变简单 → 维护成本 × N 变小；
- 格式复杂度集中在一份离线工具里 → 新特性只改一处；
- 文本中间表示对脚本语言友好（Python、Perl 处理 pipeline 的人不用链引擎 C++ 库）。

代价：**还是要为每个 DCC 写一个 exporter**，只是 exporter 变薄了；另需维护中间格式本身的规格。

## 路线 C：采用现成交换格式（COLLADA / 今天的 glTF）

理论上的理想：每个 DCC 已经有人写好 COLLADA exporter，引擎只要写一个 `COLLADA → 引擎格式` 转换器，就白嫖了所有 DCC 的 exporter 工作。

**现实的折扣**：

- COLLADA 是**极度通用**的 rich format，每家 DCC 导出的子集不一样——「3ds Max 的 COLLADA」「Maya 的 COLLADA」「Blender 的 COLLADA」实际是三套方言；
- 引擎侧要为每套方言写兼容层，工作量没有归零；
- 真正棘手的问题——**引擎特有元数据怎么塞进 DCC 的 UI 并幸存到 COLLADA 里**——并没有被格式本身解决。COLLADA 允许 `<extra>` 节点，但 DCC 是否把你的自定义属性识别成可填字段、是否在导出时保留 `<extra>`，取决于每个 DCC 的 COLLADA 实现。

Supnik 在文末给出了他当时倾向的判断（也是评论区一位同行的亲身经验）：**即便要处理 N 种方言，仍然比写 N 个 full-featured 原生 exporter 便宜**，因为 DCC 方言之间的公共部分已经被 COLLADA 规格化了——剩下的差异是 patch，不是从零造。这等价于「每个 DCC 都实现了同一个 API 的变体，我们为那个 API 的公共面只写一次」。

## 何时选哪条

- **封闭引擎 + 少量内部 DCC**（例如只用 Maya）：路线 A 最便宜，维护成本可控；
- **专有资产编码复杂、运行时对格式挑剔**（X-Plane 的 DSF 为例）：路线 B 把复杂度收敛到一处工具，DCC exporter 不背锅；
- **开放平台 + 多家 DCC**（X-Plane 自身的处境、今天的 glTF 生态）：路线 C 收益最大，即使每家 DCC 有方言也比维护 N 个 full exporter 省；
- **现代现实**：2020 年后 [glTF 2.0](https://www.khronos.org/gltf/) 事实上替代了 COLLADA 成为游戏资产通用交换格式——原因正是它**更窄、更具 opinion**，把 COLLADA 的通用性换成了「所有 DCC 都导一样的子集」的确定性。Supnik 框架里的「方言离散度」这个变量被显著压下了。

## 相关
- [[game-resource-pack-format]] —— 运行时侧的打包格式决策
- [[playcanvas-cloud-asset-pipeline]] —— 在线服务的资源管线对照
- [[decoupled-tool-engine-json-rpc]] —— 工具链与引擎的解耦通讯
- [[ben-supnik]]
- [[blender-euler-extrinsic-xyz-export]] —— 另一条跨坐标系 exporter 陷阱（同作者同 X-Plane 视角）
- [[art-asset-version-control-gap]] —— 资产管线的另一层：版本控制

## Sources

- [[sources/supnik-is-collada-a-win]]
