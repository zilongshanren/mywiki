---
tags: [productivity, workflow, build-server, source-control, bitsquid]
date: 2026-04-19
sources: 1
---

# Now-Principle 与其他四条：Bitsquid 的程序员生产力清单

[[niklas-frykholm]] 2012 年初写的一篇短文给出五条日常纪律。看似 meta，实则都有明确的成本收益推理。

## 1. Now-principle：五分钟以内的事立刻做

把小事推迟并不省力——你要写进 TODO、排优先级、事后重建脑内状态，光这些开销就比直接干完多。"拖延看似懒，其实比立刻做更累。" 这条和 GTD 的 two-minute rule 同源，但 Niklas 把门槛拉到 5 分钟——对工程师场景更合理，因为重建上下文才是最贵的部分。

## 2. 修病根不是修症状

用户跑来报 "Error when compiling unit"：最差的做法是口头解答；好一点是改 error message 让它自己把线索说清楚（"unit 'bed' 的两个节点重名为 'pillow'"）；**最好是改工具让这类错误根本构造不出来**。类似地：能被 assert 发现的 bug 就加 assert；被问过一次的用法就写进文档。这不仅是质量习惯，也是工作的意义——不是在堵漏洞，而是在把系统变得更好。这条的工程表达是 [[warnings-as-errors-strategy|把 warning 升格为 error]]，也和 [[zero-tolerance]] 的「每天把复杂度增量按到零」一脉相承。

## 3. 编译/加载间隙不要切换 context

程序员一天里有无数个小停顿——编译、console 重启、关卡加载、客户端连接。反直觉的是：**刷一下邮件、读两段文章、看进度条**并不解压，反而破坏专注态，比停一次真正的大休息要累得多。Niklas 的做法是开一个**独立的文本编辑器**（不会被 IDE 卡住），在间隙里做相关但轻的事：补文档、review 刚写的代码、规划下一步实现、写测试脚本。保持在"同一个问题"里，心流不断。当然更根本的还是把停顿消灭——让编译更快、支持热 reload、写脚本一键 setup 多台 PS3 网络测试。

## 4. 版本控制用得比你想象的还多

不仅仅是源码。配置文件、第三方库（zlib、LuaJIT、stb_vorbis）、API sample code，全都 check in。好处是：跨机同步；第三方库本地魔改时明确看得到 diff；上游更新可以三路合并；sample code 可以随时回滚 pristine 状态，也能抽 patch 当 bug report 发回给厂商。分布式 VCS 之后建仓几乎无成本，不用再纠结「这个目录值不值得一个 repo」。

## 5. 监控构建

持续构建所有可执行（引擎、工具、导出器）× 所有配置（debug/dev/release）× 所有平台，出问题第一时间知道。**关键不是功能齐全而是它存在**——哪怕一个跑完构建发 Skype 消息的脚本也算 build server。同样的思路延伸到内容：写个脚本加载所有关卡、spawn 所有 unit。报告渠道选团队已经在用的——他们用 Skype 沟通就用 Skype，邮件/IRC 也行——别为了"正规"而引入第二条通讯通道。

## 为什么值得一并记下

这五条里没有什么惊人发现。价值在于它们被一个成熟引擎团队的人、用成本收益的语言明确写出来——"postpone 比 do it 更累"、"构建监控存在比完美重要"、"被你解释过一次的东西写进文档"——每一条都对应一类常见的偷懒借口。它们是 [[strategic-programming|strategic programming]] 在日常纪律层面的落地。

## 相关

- [[zero-tolerance]]
- [[strategic-programming]]
- [[warnings-as-errors-strategy]]
- [[automated-test-philosophy]]

## Sources

- [[sources/bitsquid-5-tips-programmer-productivity]]
