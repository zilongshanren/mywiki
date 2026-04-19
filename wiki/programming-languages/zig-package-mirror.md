---
tags: [zig, 包管理, 构建系统, 镜像, 软件供应链]
date: 2026-04-19
sources: 1
---

# pkgmirror：自托管 Zig 工具链与包镜像

`pkgmirror` 是 [[stephen-gutekanst]] 用 Zig 写的、开源自托管的 Zig 工具链 + 包镜像服务，[[mach-engine|Mach]] 自己用它挂在 `pkg.hexops.org`。单 binary、~9 MB、除了 libc 和可选的 acme.sh 没有运行时依赖——整体上属于"小即是好"的 Zig 风基础设施。

## 解决什么

Zig 社区一直靠一张[社区镜像列表](https://ziglang.org/download/community-mirrors/)给 ziglang.org 分流，`setup-zig`、`anyzig` 这些工具会轮询这张表挑一个能连上的镜像拉 toolchain，minisig 签名保证拿到的还是官方 binary。但这张表的数量和稳定性有限，pkgmirror 让任何人都可以自己架一个 Zig toolchain mirror 并贡献回去。

更重要的是包层面的镜像。如果你写 `build.zig.zon` 时直接指向 GitHub tarball，长期来看这个 URL 可能因为仓库被删除、被 archive、或者 GitHub 本身变糟糕（作者最近就把 Mach 迁到自托管 Forgejo `code.hexops.org`）而失效。pkgmirror 的做法是：**把 tarball 缓存到你自己的磁盘上永久保留**，给你一条 URL 稳定且归你管的 `build.zig.zon` 依赖源。CI artifact 也可以这样镜像。

## 功能点

- Zig toolchain mirroring：从 ziglang.org 反向代理 + 本地缓存。
- 可选的包镜像：支持 GitHub、Codeberg、任意 Git hosting。
- 可选的 artifact 镜像：把 CI 产物（预编译二进制）同样缓存为稳定 URL。
- [[mach-nominated-zig-versions|Nominated Zig 支持]]——针对 Mach 提名版本做专门匹配。
- Proactive cache warming：自动预取所有 stable + nominated Zig 版本的每个 OS/arch 变体，避免首次访问打穿。
- 内置 LetsEncrypt via acme.sh，server 本身能直接处理 TLS，不用再套反向代理（靠 `karlseguin/http.zig` 和 `ianic/tls.zig` 两个 Zig 生态库）。

## 定位的潜台词

"written in Zig, unlike the myriad of other Go-based solutions out there"——作者不掩饰这是一种生态宣言。更深层的一层主张是反 GitHub 中心化：Mach 把 `build.zig.zon` 里的依赖 URL 全部指到 `pkg.hexops.org`，把镜像的物理位置、备份、更新节奏都拿回自己手里。作者强调不是每个人都该跑 Zig mirror——有人靠你时你得处理备份——但至少 Zig 社区里有组织的项目能用 pkgmirror 摆脱对 third-party 的隐式依赖。

## 相关

- [[mach-engine]]
- [[mach-nominated-zig-versions]]
- [[stephen-gutekanst]]

## Sources

- [[sources/hexops-pkgmirror]]
