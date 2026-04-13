---
title: 云风的 BLOG
url: https://blog.codingnow.com/2021/05/
published: '2021-05-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### ANSI escape code 及 Lua 封装

这两天想给一个想法做个简单的原型，因为涉及人机交互，需要在屏幕上绘制一些简单的交互元素。当然，现在有很多工具可供利用。过去遇到这种事情，我会尝试用已有的各种开源游戏引擎（我尤其推荐 [PICO-8](https://www.lexaloffle.com/pico-8.php)），或是直接在浏览器中用 css/javascript 写等等。

最近几年我玩了大量 RogueLike ，想尝试一下在 console 下用 ascii 字符来拼凑画面。这很有趣，能让我回忆起小时候 Apple ][ 上花掉的大把时光。同时我想用 Lua 来做开发，却不想引入 [ncurses](https://en.wikipedia.org/wiki/Ncurses) 这样的第三方库。最好能用几分钟就可以从零搭建起开发环境。

最好的选择当然是用 [ANSI escape code](https://en.wikipedia.org/wiki/ANSI_escape_code) 通过标准输出在 console 界面上作画了。

需要用到的是 CSI (Control Sequence Introducer) sequences ，也就是向标准输出写入一个 ESC(\x1b)[ 再跟上参数加可以命令字母。它可以用来控制光标的位置，这样就不限于在终端下一行行顺序输出文字。

最常用的是 CSI n ; m H 移动光标到决定位置；CSI n J 清屏；CSI n (A/B/C/D) 移动光标；CSI s 保存当前位置；CSI u 恢复保存的位置。

直接输出控制字符用起来会非常繁琐。当然是最个简单的封装了。我花了十几分钟做了个基本可用的东西：

-- cursor.lua local C = {} local write = io.write function C.clear() write "\x1b[2J" end local function drawline(line) write("\x1b[s", line, "\x1b[u\x1b[B") return drawline end local function move_cursor(match) return "\x1b[" .. #match .. "C" end local function trans_draw(cache, key) if key == "%" then key = "%%" end local pat = "[" .. key .. "+]" local function trans_drawline(line) line = line:gsub(pat, move_cursor) drawline(line) return trans_drawline end cache[key] = trans_drawline return trans_drawline end local drawline = setmetatable( { [true] = drawline }, { __index = trans_draw, __mode = "v" } ) function C.draw(y,x,trans) write("\x1b[",y,";",x,"H") return drawline[trans or true] end return C

这里就提供了两个 api ，一个是 cursor.clear() 清屏；另一个是 cursor.draw(行,列,可选的透明字符) 用来绘制一组 ascii 字符。

核心在于这个 draw 函数，它可以把光标移动到指定位置后，绘制多行文字。这里支持透明字符（通常是空格），用户可以指定透明字符，在绘制过程中跳过那些位置，避免覆盖背景。

例如，下面的代码可以在一个方框内绘制一张笑脸。注意，这里的方框是在最后绘制的，但不会遮挡前面已经绘制好的笑脸图案。

local c = require "cursor" c.clear() c.draw(3,4) " XXXXXXX" "X X" "X X" "X X" "X X" " XXXXXXX" c.draw(5,6) "^ ^" " < " " _ " c.draw(1,1, " ") "+-------------+" "| |" "| |" "| |" "| |" "| |" "| |" "| |" "| |" "+-------------+"

接下来的问题是，怎样让画面动起来？我用 coroutine 实现了一个非常简单的框架。

local c = require "cursor" local function run(main) local term = {} local co = coroutine.create(function() main() return term end) while true do c.clear() local ok, err = coroutine.resume(co) if not ok then error(err) end if err == term then break end os.execute "sleep 0.1" end end

这样，用 run 执行一个函数，这个函数中每画一帧就调用 coroutine.yield() 即可。

怎样和键盘交互？

标准的做法是读 stdin 。在 Lua 里可以用 io.read(1) 。但是标准输入有两个问题：

- 即使我们用 io.stdin:setvbuf "none" 把标准输入的缓冲关掉，在终端下依然需要按回车才能读到输入。这是因为终端默认是经典模式
[canonical mode](https://www.gnu.org/software/libc/manual/html_node/Canonical-or-Not.html)，这个模式下，终端只有在用户按下回车后，才会把整行的输入发给应用程序（这样，终端才能正确处理诸如退格，方向键等输入）。 - stdin 没有标准 API 设置为非阻塞模式，阻塞模式下，如果没有输入，程序就会挂起等待输入。

我想了一下，通过写[一个简单的 C 程序](https://gist.github.com/cloudwu/96ec4d6636d65b7974b633e01d97a1f9)把这两个问题一并解决。

这个程序会先将终端设置为 None canonical mode ，这样每次按键都会直接进入 stdin 。然后它把获得的输入写到 stdout （同时把回车转换为 0xff ）；另外，它创建一个线程，每隔 0.1 秒把 \n 写入标准输出。

接下来，我们可以通过管道把这个程序的输出重定向给 Lua 脚本。这样，Lua 中就能每隔 0.1 秒拿到一行字符串，这个字符串就是过去 0.1 秒的键盘输入（其中回车是 0xff）。

由于 Windows 不是 posix 系统，所以设置 None canonical mode 和开线程都需要为 Windows 单独实现。

最后，前面那个 run 函数就可以把 sleep 改成 io.read "l" 。

local function run(main) local term = {} local co = coroutine.create(function() main() return term end) while true do local keys = io.read "l" c.clear() local ok, err = coroutine.resume(co, key) if not ok then error(err) end if err == term then break end end end

有了这么一段小程序，就可以用 Lua 愉快的开发跨平台的 Rogue Like 游戏了 :D