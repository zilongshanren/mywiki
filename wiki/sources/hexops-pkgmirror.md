---
tags: [source, zig, 包管理, 镜像, 构建系统]
date: 2026-04-19
sources: 1
---

# Announcing pkgmirror: self-host your own Zig mirror（Stephen Gutekanst）

[[stephen-gutekanst]] 2026 年 3 月发布的文章，宣布 [[zig-package-mirror|pkgmirror]]——一个用 Zig 写的开源自托管 Zig toolchain + 包镜像服务，Mach 自己挂在 `pkg.hexops.org`。

## 摘要

Zig 社区有一张[community mirror 列表](https://ziglang.org/download/community-mirrors/)，`setup-zig` / `anyzig` 等工具会轮询这张表拉 toolchain（minisig 保证官方签名）。pkgmirror 让任何人能跑一台自己的 Zig toolchain 镜像，并把能力扩展到包镜像和 CI artifact 镜像——核心作用是把 `build.zig.zon` 里对 GitHub tarball 的依赖换成一条"永远不会消失"的 URL，永久缓存在本地磁盘。Mach 自己因此把所有依赖 URL 从 GitHub 搬到 `pkg.hexops.org`。服务端单 binary ~9 MB、Zig 原生、支持 [[mach-nominated-zig-versions|Mach Nominated Zig]]、预热缓存所有 stable+nominated 版本的每个 OS/arch、内置 acme.sh 直接出 LetsEncrypt 证书无需反向代理。技术栈上靠 `karlseguin/http.zig` 和 `ianic/tls.zig`（TLS 1.3 server）。

## 关键要点

- "不是每个人都该跑 mirror"——作者明确责任面：跑 mirror 就得处理备份。
- pkgmirror 的存在有明显的反 GitHub 中心化立场，Mach 已迁到自托管 Forgejo `code.hexops.org`。
- 与现有方案比，这是市面上少见的非 Go 实现。

## 链接到的概念

- [[zig-package-mirror]]
- [[mach-engine]]
- [[mach-nominated-zig-versions]]
- [[stephen-gutekanst]]

## 原文

- 链接：<https://devlog.hexops.org/2026/announcing-pkgmirror/>
- 本地：`raw/articles/devlog.hexops.org/2026-03-26_announcing-pkgmirror-self-host-your-own-zig-mirror.md`
