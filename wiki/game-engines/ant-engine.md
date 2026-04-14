---
tags: [游戏引擎, 自研引擎, 移动游戏, lua, 开源]
date: 2026-04-14
sources: 2
---

# Ant Engine（蚂蚁引擎）

Ant Engine 是 [[cloudwu|云风]] 及其小团队自 2017 年底开始研发的自研移动端 3D 游戏引擎，2024 年 1 月正式以开源模式公开源代码（仓库 `ejoy/ant`）。它是一个基于 Lua 构建的、以 ECS 为核心架构、专注于 iOS / Android / Windows 的轻量级引擎，配套一款作为技术验证的异星工厂 Like 游戏 *Red Frontier* / *VastStars*。2024 年 5 月，阿里关停了 Ant Engine 作为公司项目的立项，云风离开阿里，但引擎本身以开源形式由原团队在业余时间继续维护。

## 为什么还要做一个新引擎

云风在 2024 年 1 月的开源公告中给出了清晰的论点：拥有 Unreal/Unity 的源码并不能解决问题，因为**长期维护的网络游戏与商业引擎假设的"多产原型"场景本质不同**。商业引擎擅长快速搭建原型，但在一个产品进入长期运营后，团队需要的是更单一、更易于裁剪、维护成本不会随着版本累积而膨胀的引擎。国内大厂（王者荣耀、原神）几乎都对 Unity 做了深度魔改，印证了这个判断——但没有人真正彻底解决资源打包更新、移动平台功耗、Lua 集成这几类痛点。云风的思路是：与其在 Unity 上打无止境的补丁，不如**从零开始、直接面对这些痛点**。

这套论证和他对 [[interface-vs-implementation|接口胜于实现]]、[[modular-design|模块化]]、[[cognitive-load|降低认知负担]] 的长期偏好是一致的——他不信任"all-in-one"的巨型框架，而更愿意把引擎设计成可裁剪、可扩展的积木组合。

## 技术定位

- **语言混合**：Lua 搭上层结构（ECS、调度、资源），C 做性能热点（渲染核心、ltask 调度器）；这延续了云风在 [[lua-design-philosophy|Lua 设计哲学]] 与 [[c-interface-oop|C 模块化]] 上的一贯立场。
- **Lua ECS**：数据存在 C 内存中，Lua 层通过 ECS 访问。在首版 *Red Frontier* 性能不达标时，正是靠把核心渲染系统从 Lua 改写为 C，把帧率拉高了一个数量级以上。
- **任务调度**：底层基于 [[ltask-scheduler|ltask]]，面向客户端低延迟调度，与 [[cloudwu|skynet]] 服务端高吞吐调度属于对立但同源的一对设计。
- **虚拟文件系统**：基于 [[game-engine-vfs|VFS]] 提供资源打包、热更新与编辑器动态修改；云风在 2024 年 2 月对这套 VFS 的"不变快照"假设提出了重构思路。
- **移动优先**：为手机节能而做出的架构取舍，详见 [[mobile-energy-optimization]]。区别于 Unity 的一个关键点：Ant 强调开发工作**随时在真实移动设备上运行**，以便交互手感不失真。
- **资源打包与热更**：借鉴自云风十余年的 MMO 运营经验，专门为"小代价更新美术 / 策划资产"这一场景优化。
- **可裁剪 / 可扩展**：不用的特性可以去掉，渲染管线可改写，甚至可作为非游戏应用的 UI 后端。云风援引腾讯 QQ 集成 Unreal 带来几十 MB 体积的反例，声称 Ant 本身只需链接约 1 MB 二进制。

## 为什么选开源

云风把游戏引擎类比为操作系统那样的"基础设施"——越基础越适合开源，因为：

1. 基础设施质量由少数领域专家决定，靠堆人数没用，而高质量专家只能由有影响力的开源项目吸引到。
2. 开源项目的良性竞争会不断提升质量，远胜闭源项目。
3. 一旦用户和开发者投入，项目像滚雪球一样壮大，护城河不在技术秘密而在**主导权**。

他把 [[cloudwu|skynet]] 作为正面案例反复引用：一个人维护十余年的 Lua/C actor 框架，因为开源而收获了 10K+ Star、100+ 外部 contributor，许多 bug 甚至在云风自己遇到之前就被外部用户发现、修复。skynet 反哺本公司招聘和技术品牌的案例，是 Ant 选择开源的直接动力。

## 一款引擎，一个用来养它的游戏

Ant Engine 和它的第一款试炼游戏 *Red Frontier*（异星工厂 Like）被云风视为"共同生长"的一对：游戏作为引擎功能完备性与性能的真实负载，引擎作为游戏的加速器。2024 年 4 月，他报告说在 iPhone 上复杂场景下已能做到每帧小于 10ms，耗电比玩微信刷抖音还少——这是六年自研最有说服力的一个技术脚注。但他同时坦承，游戏性（gameplay）方面还远未打磨好，且手机并不是理想的独立游戏平台。2024 年 5 月他离开阿里时，已计划将后续开发重心转向 Windows + Steam 平台的独立游戏。

## 相关

- [[cloudwu]]
- [[game-engine]]
- [[game-engine-vfs]]
- [[ltask-scheduler]]
- [[mobile-energy-optimization]]
- [[async-offline-culling]]
- [[unity-vs-unreal]]
- [[engine-evolution]]
- [[lua-design-philosophy]]

## Sources

- [[sources/cloudwu-ant-engine-open-source]]
- [[sources/cloudwu-ant-engine-mobile-optimization]]
