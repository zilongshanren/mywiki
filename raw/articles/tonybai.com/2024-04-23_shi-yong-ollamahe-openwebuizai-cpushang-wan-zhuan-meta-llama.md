---
title: 使用Ollama和OpenWebUI在CPU上玩转Meta Llama3-8B
url: https://tonybai.com/2024/04/23/playing-with-meta-llama3-8b-on-cpu-using-ollama-and-openwebui/
published: '2024-04-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Ollama和OpenWebUI在CPU上玩转Meta Llama3-8B

![](../../assets/389122591bcef806.png)


[本文永久链接](https://tonybai.com/2024/04/23/playing-with-meta-llama3-8b-on-cpu-using-ollama-and-openwebui) – https://tonybai.com/2024/04/23/playing-with-meta-llama3-8b-on-cpu-using-ollama-and-openwebui

2024年4月18日，[meta开源了Llama 3大模型](https://ai.meta.com/blog/meta-llama-3/)，虽然只有[8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B)和[70B](https://huggingface.co/meta-llama/Meta-Llama-3-70B)两个版本，但Llama 3表现出来的强大能力还是让AI大模型界为之震撼了一番，本人亲测Llama3-70B版本的推理能力十分接近于[OpenAI的GPT-4](https://openai.com/research/gpt-4)，何况还有一个400B的超大模型还在路上，据说再过几个月能发布。

Github上人气巨火的本地大模型部署和运行工具项目[Ollama](https://github.com/ollama/ollama)也在[第一时间宣布了对Llama3的支持](https://ollama.com/blog/llama3)：

![](../../assets/af0aae0c92b535e6.png)


近期除了[学习Rust](https://tonybai.com/2024/04/22/gopher-rust-first-lesson-all-about-rust/)，还有就在研究如何将LLM应用于产品中。以前走微调的路径行不通，最近的RAG(Retrieval-Augmented Generation)和Agent路径则让我看到一丝曙光。不过实施这两个路径的前提是一个强大的LLM，而开源的meta Llama系列LLM则是不二之选。

在这篇文章中，我就先来体验一下如何基于Ollama安装和运行Meta Llama3-8B大模型，并通过兼容Ollama API的[OpenWebUI](https://github.com/open-webui/open-webui)建立对大模型的Web图形化访问方式。

## 1. 安装Ollama

Ollama是一个由Go实现的、可以**在本地丝滑地安装和运行各种开源大模型的工具**，支持目前国内外很多主流的开源大模型，比如Llama、[Mistral](https://mistral.ai/)、[Gemma](https://ai.google.dev/gemma)、[DBRX](https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm)、[Qwen](https://github.com/QwenLM/Qwen)、[phi](https://huggingface.co/microsoft/phi-2)、[vicuna](https://lmsys.org/blog/2023-03-30-vicuna/)、[yi](https://github.com/01-ai/Yi)、[falcon](https://huggingface.co/blog/falcon)等。其支持的全量模型列表可以在[Ollama library](https://ollama.com/library)查看。

Ollama的安装采用了“curl | sh”，我们可以一键将其下载并安装到本地：

```
$curl -fsSL https://ollama.com/install.sh | sh
>>> Downloading ollama...
######################################################################## 100.0%
>>> Installing ollama to /usr/local/bin...
>>> Creating ollama user...
>>> Adding ollama user to video group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
>>> Enabling and starting ollama service...
Created symlink from /etc/systemd/system/default.target.wants/ollama.service to /etc/systemd/system/ollama.service.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
WARNING: No NVIDIA/AMD GPU detected. Ollama will run in CPU-only mode.
```


我们看到Ollama下载后启动了一个ollama systemd service，这个服务就是Ollama的核心API服务，它常驻内存。通过systemctl可以确认一下该服务的运行状态：

```
$systemctl status ollama
● ollama.service - Ollama Service
Loaded: loaded (/etc/systemd/system/ollama.service; enabled; vendor preset: disabled)
Active: active (running) since 一 2024-04-22 17:51:18 CST; 11h ago
Main PID: 9576 (ollama)
Tasks: 22
Memory: 463.5M
CGroup: /system.slice/ollama.service
└─9576 /usr/local/bin/ollama serve
```


另外我对Ollama的systemd unit文件做了一些改动，我修改了一下Environment的值，增加了”OLLAMA_HOST=0.0.0.0″，这样便于后续在容器中运行的OpenWebUI可以访问到Ollama API服务：

```
# cat /etc/systemd/system/ollama.service
[Unit]
Description=Ollama Service
After=network-online.target
[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/root/.cargo/bin:/usr/local/cmake/bin:/usr/local/bin:.:/root/.bin/go1.21.4/bin:/root/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin" "OLLAMA_HOST=0.0.0.0"
[Install]
WantedBy=default.target
```


修改后执行下面命令使之生效：

```
$systemctl daemon-reload
$systemctl restart ollama
```


## 2. 下载和运行大模型

Ollama支持一键下载和运行模型。我手里有一个16/32G的云虚机，但没有GPU，因此这里我使用的是[Llama3-8B指令微调后的用于chat/diaglogue的模型](https://ollama.com/library/llama3)，我们只需要通过下面命令便可以快速下载并运行该模型(4bit量化的)：

```
$ollama run llama3
pulling manifest
pulling 00e1317cbf74... 0% ▕ ▏ 0 B/4.7 GB
pulling 00e1317cbf74... 7% ▕█ ▏ 331 MB/4.7 GB 34 MB/s 2m3s^C
pulling manifest
pulling manifest
pulling manifest
pulling manifest
pulling 00e1317cbf74... 61% ▕█████████ ▏ 2.8 GB/4.7 GB 21 MB/s 1m23s^C
... ...
```


下载和执行成功后，该命令行便会等待你的问题输入，我们随便输入一个关于Go的问题，下面是输出结果：

```
$ollama run llama3
>>> could you tell me something about golang language?
Go!
Here are some interesting facts and features about the Go programming language:
**What is Go?**
Go, also known as Golang, is a statically typed, compiled, and designed to be concurrent and garbage-collected language. It
was developed by Google in 2009.
**Key Features:**
1. **Concurrency**: Go has built-in concurrency support through goroutines (lightweight threads) and channels (communication
mechanisms). This makes it easy to write concurrent programs.
2. **Garbage Collection**: Go has a automatic garbage collector, which frees developers from worrying about memory
management.
3. **Static Typing**: Go is statically typed, meaning that the type system checks the types of variables at compile time,
preventing type-related errors at runtime.
4. **Simple Syntax**: Go's syntax is designed to be simple and easy to read. It has a minimalistic approach to programming
language design.
... ...
```


推理速度大约在5~6个token吧，尚可接受，但这个过程是相当耗CPU：

![](../../assets/6baca07fea346377.png)


除了通过命令行方式与Ollama API服务交互之外，我们还可以用Ollama的restful API：

```
$curl http://localhost:11434/api/generate -d '{
> "model": "llama3",
> "prompt":"Why is the sky blue?"
> }'
{"model":"llama3","created_at":"2024-04-22T07:02:36.394785618Z","response":"The","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:36.564938841Z","response":" color","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:36.745215652Z","response":" of","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:36.926111842Z","response":" the","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:37.107460031Z","response":" sky","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:37.287201658Z","response":" can","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:37.468517901Z","response":" vary","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:37.649011829Z","response":" depending","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:37.789353456Z","response":" on","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:37.969236546Z","response":" the","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:38.15172159Z","response":" time","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:38.333323271Z","response":" of","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:38.514564929Z","response":" day","done":false}
{"model":"llama3","created_at":"2024-04-22T07:02:38.693824676Z","response":",","done":false}
... ...
```


不过我日常使用大模型最为广泛的方式还是通过Web UI进行交互。目前有很多支持Ollama API的Web & Desktop项目，这里我们选取[Open WebUI](https://github.com/open-webui/open-webui)，它的前身就是Ollama WebUI。

## 3. 安装和使用Open WebUI与大模型交互

最快体验Open WebUI的方式当然是使用容器安装，不过官方镜像站点ghcr.io/open-webui/open-webui:main下载太慢，我找了一个位于Docker Hub上的个人mirror镜像，下面是在本地安装Open WebUI的命令：

```
$docker run -d -p 13000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://host.docker.internal:11434 --name open-webui --restart always dyrnq/open-webui:main
```


容器启动后，我们在host上访问13000端口即可打开Open WebUI页面：

![](../../assets/aeb4179822aaba66.png)


首个注册的用户，将会被Open WebUI认为是admin用户！注册登录后，我们就可以进入首页：

![](../../assets/0280ebe5a5221d2c.png)


选择model后，我们便可以输入问题，并与Ollama部署的Llama3模型对话了：

![](../../assets/d4d66c8c04d32993.png)


注：如果Open WebUI运行不正常，可以通过查看openwebui的容器日志来辅助诊断问题。


Open WebUI的功能还有很多，大家可以自行慢慢挖掘:)。

## 4. 小结

在本文中，我介绍了Meta开源的Llama 3大模型以及Ollama和OpenWebUI的使用。Llama 3是一个强大的AI大模型，实测接近于OpenAI的GPT-4，并且还有一个更强大的400B模型即将发布。Ollama是一个用于本地部署和运行大模型的工具，支持多个国内外开源模型，包括Llama在内。我详细介绍了如何安装和运行Ollama，并使用Ollama下载和运行Llama3-8B模型。展示了通过命令行和REST API与Ollama进行交互，以及模型的推理速度和CPU消耗。此外，我还提到了OpenWebUI，一种兼容Ollama API的Web图形化访问方式。通过Ollama和OpenWebUI，大家可以方便地在CPU上使用Meta Llama3-8B大模型进行推理任务，并获得满意的结果。

后续，我将进一步研究如何将Llama3应用于产品中，并探索RAG（Retrieval-Augmented Generation）和Agent技术的潜力。这两种路径可以为基于Llama3的大模型应用开发带来新的可能性。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

非常期待老师的后续关于 AI 应用的实战教程！例如：怎样为本地系统提供 HTTP 服务接口；怎样使用自己的资料让 Llama3 模型继续学习，打造私有知识 AI 助手，……

我也在学习和研究中，后续多多分享就是了，但不保证能完全解决你的问题:)

Awesome guide


I have made a similar guide for fine-tuning Llama 3 for specific use cases using ChatGPT. Check it out LLaMa 3 400B