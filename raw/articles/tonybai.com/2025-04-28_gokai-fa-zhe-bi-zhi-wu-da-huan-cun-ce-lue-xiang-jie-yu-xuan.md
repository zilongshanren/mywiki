---
title: Go开发者必知：五大缓存策略详解与选型指南
url: https://tonybai.com/2025/04/28/five-cache-strategies/
published: '2025-04-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go开发者必知：五大缓存策略详解与选型指南

![](../../assets/9abbd5d3c1a15bd6.png)


[本文永久链接](https://tonybai.com/2025/04/28/five-cache-strategies) – https://tonybai.com/2025/04/28/five-cache-strategies

大家好，我是Tony Bai。

在构建高性能、高可用的后端服务时，缓存几乎是绕不开的话题。无论是为了加速数据访问，还是为了减轻数据库等主数据源的压力，缓存都扮演着至关重要的角色。对于我们 Go 开发者来说，选择并正确地实施缓存策略，是提升应用性能的关键技能之一。

目前业界主流的缓存策略有多种，每种都有其独特的适用场景和优缺点。今天，我们就来探讨其中五种最常见也是最核心的缓存策略：Cache-Aside、Read-Through、Write-Through、Write-Behind (Write-Back) 和Write-Around，并结合Go语言的特点和示例（使用内存缓存和SQLite），帮助大家在实际项目中做出明智的选择。

## 0. 准备工作：示例代码环境与结构

为了清晰地演示这些策略，本文的示例代码采用了模块化的结构，将共享的模型、缓存接口、数据库接口以及每种策略的实现分别放在不同的包中。我们将使用Go语言，配合一个简单的**内存缓存**（带 TTL 功能）和一个 **SQLite 数据库**作为持久化存储。

示例项目的结构如下：

```
$tree -F ./go-cache-strategy
./go-cache-strategy
├── go.mod
├── go.sum
├── internal/
│ ├── cache/
│ │ └── cache.go
│ ├── database/
│ │ └── database.go
│ └── models/
│ └── models.go
├── main.go
└── strategy/
├── cacheaside/
│ └── cacheaside.go
├── readthrough/
│ └── readthrough.go
├── writearound/
│ └── writearound.go
├── writebehind/
│ └── writebehind.go
└── writethrough/
└── writethrough.go
```


其中核心组件包括：

- internal/models: 定义共享数据结构 (如 User, LogEntry)。
- internal/cache: 定义 Cache 接口及 InMemoryCache 实现。
- internal/database: 定义 Database 接口及 SQLite DB 实现。
- strategy/xxx: 每个子目录包含一种缓存策略的核心实现逻辑。

**注意：** 文中仅展示各策略的核心实现代码片段。**完整的、可运行的示例项目代码在Github上，大家可以通过文末链接访问。**

接下来，我们将详细介绍五种缓存策略及其Go实现片段。

## 1. Cache-Aside (旁路缓存/懒加载Lazy Loading)

![](../../assets/116fefd7fd716605.png)


这是最常用、也最经典的缓存策略。**核心思想是：应用程序自己负责维护缓存。**

**工作流程：**

- 应用需要读取数据时，
**先**检查缓存中是否存在。 **缓存命中 (Hit):**如果存在，直接从缓存返回数据。**缓存未命中 (Miss):**如果不存在，应用从主数据源（如数据库）读取数据。- 读取成功后，应用将数据
**写入缓存**（设置合理的过期时间）。 - 最后，应用将数据返回给调用方。

**Go示例 (核心实现 – strategy/cacheaside/cacheaside.go):**

```
package cacheaside
import (
"context"
"fmt"
"log"
"time"
"cachestrategysdemo/internal/cache"
"cachestrategysdemo/internal/database"
"cachestrategysdemo/internal/models"
)
const userCacheKeyPrefix = "user:" // Example prefix
// GetUser retrieves user info using Cache-Aside strategy.
func GetUser(ctx context.Context, userID string, db database.Database, memCache cache.Cache, ttl time.Duration) (*models.User, error) {
cacheKey := userCacheKeyPrefix + userID
// 1. Check cache first
if cachedVal, found := memCache.Get(cacheKey); found {
if user, ok := cachedVal.(*models.User); ok {
log.Println("[Cache-Aside] Cache Hit for user:", userID)
return user, nil
}
memCache.Delete(cacheKey) // Remove bad data
}
// 2. Cache Miss
log.Println("[Cache-Aside] Cache Miss for user:", userID)
// 3. Fetch from Database
user, err := db.GetUser(ctx, userID)
if err != nil {
return nil, fmt.Errorf("failed to get user from DB: %w", err)
}
if user == nil {
return nil, nil // Not found
}
// 4. Store data into cache
memCache.Set(cacheKey, user, ttl)
log.Println("[Cache-Aside] User stored in cache:", userID)
// 5. Return data
return user, nil
}
```


**优点:**

* 实现相对简单直观。

* 对读密集型应用效果好，缓存命中时速度快。

* 缓存挂掉不影响应用读取主数据源（只是性能下降）。

**缺点:**

* 首次请求（冷启动）或缓存过期后，会有一次缓存未命中，延迟较高。

* 存在数据不一致的风险：需要额外的缓存失效策略。

* 应用代码与缓存逻辑耦合。

**使用场景:** 读多写少，能容忍短暂数据不一致的场景。

### 2. Read-Through (穿透读缓存)

![](../../assets/24e078694fd440c4.png)


**核心思想：应用程序将缓存视为主要数据源，只与缓存交互。缓存内部负责在未命中时从主数据源加载数据。**

**工作流程：**

- 应用向缓存请求数据。
- 缓存检查数据是否存在。
**缓存命中:**直接返回数据。**缓存未命中:**缓存**自己**负责从主数据源加载数据。- 加载成功后，缓存将数据存入自身，并返回给应用。

**Go 示例 (模拟实现 – strategy/readthrough/readthrough.go):**

Read-Through 通常依赖缓存库自身特性。这里我们通过封装 Cache 接口模拟其行为。

```
package readthrough
import (
"context"
"fmt"
"log"
"time"
"cachestrategysdemo/internal/cache"
"cachestrategysdemo/internal/database"
)
// LoaderFunc defines the function signature for loading data on cache miss.
type LoaderFunc func(ctx context.Context, key string) (interface{}, error)
// Cache wraps a cache instance to provide Read-Through logic.
type Cache struct {
cache cache.Cache // Use the cache interface
loaderFunc LoaderFunc
ttl time.Duration
}
// New creates a new ReadThrough cache wrapper.
func New(cache cache.Cache, loaderFunc LoaderFunc, ttl time.Duration) *Cache {
return &Cache{cache: cache, loaderFunc: loaderFunc, ttl: ttl}
}
// Get retrieves data, using the loader on cache miss.
func (rtc *Cache) Get(ctx context.Context, key string) (interface{}, error) {
// 1 & 2: Check cache
if cachedVal, found := rtc.cache.Get(key); found {
log.Println("[Read-Through] Cache Hit for:", key)
return cachedVal, nil
}
// 4: Cache Miss - Cache calls loader
log.Println("[Read-Through] Cache Miss for:", key)
loadedVal, err := rtc.loaderFunc(ctx, key) // Loader fetches from DB
if err != nil {
return nil, fmt.Errorf("loader function failed for key %s: %w", key, err)
}
if loadedVal == nil {
return nil, nil // Not found from loader
}
// 5: Store loaded data into cache & return
rtc.cache.Set(key, loadedVal, rtc.ttl)
log.Println("[Read-Through] Loaded and stored in cache:", key)
return loadedVal, nil
}
// Example UserLoader function (needs access to DB instance and key prefix)
func NewUserLoader(db database.Database, keyPrefix string) LoaderFunc {
return func(ctx context.Context, cacheKey string) (interface{}, error) {
userID := cacheKey[len(keyPrefix):] // Extract ID
// log.Println("[Read-Through Loader] Loading user from DB:", userID)
return db.GetUser(ctx, userID)
}
}
```


**优点:**

* 应用代码逻辑更简洁，将数据加载逻辑从应用中解耦出来。

* 代码更易于维护和测试（可以单独测试 Loader）。

**缺点:**

* 强依赖缓存库或服务是否提供此功能，或需要自行封装。

* 首次请求延迟仍然存在。

* 数据不一致问题依然存在。

**使用场景:** 读密集型，希望简化应用代码，使用的缓存系统支持此特性或愿意自行封装。

### 3. Write-Through (穿透写缓存)

![](../../assets/7262ac9490f6255d.png)


**核心思想：数据一致性优先！应用程序更新数据时，同时写入缓存和主数据源，并且两者都成功后才算操作完成。**

**工作流程：**

- 应用发起写请求（新增或更新）。
- 应用
**先**将数据写入主数据源（或缓存，顺序可选）。 - 如果第一步成功，应用
**再**将数据写入另一个存储（缓存或主数据源）。 - 第二步写入成功（或至少尝试写入）后，操作完成，向调用方返回成功。
**通常以主数据源写入成功为准**，缓存写入失败一般只记录日志。

**Go 示例 (核心实现 – strategy/writethrough/writethrough.go):**

```
package writethrough
import (
"context"
"fmt"
"log"
"time"
"cachestrategysdemo/internal/cache"
"cachestrategysdemo/internal/database"
"cachestrategysdemo/internal/models"
)
const userCacheKeyPrefix = "user:" // Example prefix
// UpdateUser updates user info using Write-Through strategy.
func UpdateUser(ctx context.Context, user *models.User, db database.Database, memCache cache.Cache, ttl time.Duration) error {
cacheKey := userCacheKeyPrefix + user.ID
// Decision: Write to DB first for stronger consistency guarantee.
log.Println("[Write-Through] Writing to database first for user:", user.ID)
err := db.UpdateUser(ctx, user)
if err != nil {
// DB write failed, do not proceed to cache write
return fmt.Errorf("failed to write to database: %w", err)
}
log.Println("[Write-Through] Successfully wrote to database for user:", user.ID)
// Now write to cache (best effort after successful DB write).
log.Println("[Write-Through] Writing to cache for user:", user.ID)
memCache.Set(cacheKey, user, ttl)
// If strict consistency cache+db is needed, distributed transaction is required (complex).
// For simplicity, assume cache write is best-effort. Log potential errors.
return nil
}
```


**优点:**

* 数据一致性相对较高。

* 读取时（若命中）能获取较新数据。

**缺点:**

* 写入延迟较高。

* 实现需考虑失败处理（特别是DB成功后缓存失败的情况）。

* 缓存可能成为写入瓶颈。

**使用场景:** 对数据一致性要求较高，可接受一定的写延迟。

### 4. Write-Behind / Write-Back (回写 / 后写缓存)

![](../../assets/acd3370874a75070.png)


**核心思想：写入性能优先！应用程序只将数据写入缓存，缓存立即返回成功。缓存随后异步地、批量地将数据写入主数据源。**

**工作流程：**

- 应用发起写请求。
- 应用将数据写入缓存。
**缓存立即**向应用返回成功。- 缓存将此写操作放入一个队列或缓冲区。
- 一个
**独立的后台任务**在稍后将队列中的数据**批量**写入主数据源。

**Go 示例 (核心实现 – strategy/writebehind/writebehind.go):**

```
package writebehind
import (
"context"
"fmt"
"log"
"sync"
"time"
"cachestrategysdemo/internal/cache"
"cachestrategysdemo/internal/database"
"cachestrategysdemo/internal/models"
)
// Config holds configuration for the Write-Behind strategy.
type Config struct {
Cache cache.Cache
DB database.Database
KeyPrefix string
TTL time.Duration
QueueSize int
BatchSize int
Interval time.Duration
}
// Strategy holds the state for the Write-Behind implementation.
type Strategy struct {
// ... (fields: cache, db, updateQueue, wg, stopOnce, cancelCtx/Func, dbWriteMutex, config fields) ...
// Fields defined in the full code example provided previously
cache cache.Cache
db database.Database
updateQueue chan *models.User
wg sync.WaitGroup
stopOnce sync.Once
cancelCtx context.Context
cancelFunc context.CancelFunc
dbWriteMutex sync.Mutex // Simple lock for batch DB writes
keyPrefix string
ttl time.Duration
batchSize int
interval time.Duration
}
// New creates and starts a new Write-Behind strategy instance.
// (Implementation details in full code example - initializes struct, starts worker)
func New(cfg Config) *Strategy {
// ... (Initialization code as provided previously) ...
// For brevity, showing only the function signature here.
// It sets defaults, creates the context/channel, and starts the worker goroutine.
// Returns the *Strategy instance.
// ... Full implementation in GitHub Repo ...
panic("Full implementation required from GitHub Repo") // Placeholder
}
// UpdateUser queues a user update using Write-Behind strategy.
func (s *Strategy) UpdateUser(ctx context.Context, user *models.User) error {
cacheKey := s.keyPrefix + user.ID
s.cache.Set(cacheKey, user, s.ttl) // Write to cache immediately
// Add to async queue
select {
case s.updateQueue <- user:
return nil // Return success to the client immediately
default:
// Queue is full! Handle backpressure.
log.Printf("[Write-Behind] Error: Update queue is full. Dropping update for user: %s\n", user.ID)
return fmt.Errorf("update queue overflow for user %s", user.ID)
}
}
// dbWriterWorker processes the queue (Implementation details in full code example)
func (s *Strategy) dbWriterWorker() {
// ... (Worker loop logic: select on queue, ticker, context cancellation) ...
// ... (Calls flushBatchToDB) ...
// ... Full implementation in GitHub Repo ...
}
// flushBatchToDB writes a batch to the database (Implementation details in full code example)
func (s *Strategy) flushBatchToDB(ctx context.Context, batch []*models.User) {
// ... (Handles batch write logic using s.db.BulkUpdateUsers) ...
// ... Full implementation in GitHub Repo ...
}
// Stop gracefully shuts down the Write-Behind worker.
// (Implementation details in full code example - signals context, waits for WaitGroup)
func (s *Strategy) Stop() {
// ... (Stop logic using stopOnce, cancelFunc, wg.Wait) ...
// ... Full implementation in GitHub Repo ...
}
```


**优点:**

* 写入性能极高。

* 降低主数据源压力。

**缺点:**

* **数据丢失风险。**

* **最终一致性。**

* 实现复杂度高。

**使用场景:** 对写性能要求极高，写操作非常频繁，能容忍数据丢失风险和最终一致性。

### 5. Write-Around (绕写缓存)

![](../../assets/8f26f21a41c38588.png)


**核心思想：写操作直接绕过缓存，只写入主数据源。读操作时才将数据写入缓存（通常结合 Cache-Aside）。**

**工作流程：**

**写路径:**应用发起写请求，直接将数据写入主数据源。**读路径 (通常是Cache-Aside):**应用需要读取数据时，先检查缓存。如果未命中，则从主数据源读取，然后将数据存入缓存，最后返回。

**Go 示例 (核心实现 – strategy/writearound/writearound.go):**

```
package writearound
import (
"context"
"fmt"
"log"
"time"
"cachestrategysdemo/internal/cache"
"cachestrategysdemo/internal/database"
"cachestrategysdemo/internal/models"
)
const logCacheKeyPrefix = "log:" // Example prefix for logs
// WriteLog writes log entry directly to DB, bypassing cache.
func WriteLog(ctx context.Context, entry *models.LogEntry, db database.Database) error {
// 1. Write directly to DB
log.Printf("[Write-Around Write] Writing log directly to DB (ID: %s)\n", entry.ID)
err := db.InsertLogEntry(ctx, entry) // Use the appropriate DB method
if err != nil {
return fmt.Errorf("failed to write log to DB: %w", err)
}
return nil
}
// GetLog retrieves log entry, using Cache-Aside for reading.
func GetLog(ctx context.Context, logID string, db database.Database, memCache cache.Cache, ttl time.Duration) (*models.LogEntry, error) {
cacheKey := logCacheKeyPrefix + logID
// 1. Check cache (Cache-Aside read path)
if cachedVal, found := memCache.Get(cacheKey); found {
if entry, ok := cachedVal.(*models.LogEntry); ok {
log.Println("[Write-Around Read] Cache Hit for log:", logID)
return entry, nil
}
memCache.Delete(cacheKey)
}
// 2. Cache Miss
log.Println("[Write-Around Read] Cache Miss for log:", logID)
// 3. Fetch from Database
entry, err := db.GetLogByID(ctx, logID) // Use the appropriate DB method
if err != nil { return nil, fmt.Errorf("failed to get log from DB: %w", err) }
if entry == nil { return nil, nil /* Not found */ }
// 4. Store data into cache
memCache.Set(cacheKey, entry, ttl)
log.Println("[Write-Around Read] Log stored in cache:", logID)
// 5. Return data
return entry, nil
}
```


**优点:**

* 避免缓存污染。

* 写性能好。

**缺点:**

* 首次读取延迟高。

* 可能存在数据不一致（读路径上的 Cache-Aside 固有）。

**使用场景:** 写密集型，且写入的数据不太可能在短期内被频繁读取的场景。

## 总结与选型

![](../../assets/bcf48113ef2d3e7f.png)


**没有银弹！** 选择哪种缓存策略，最终取决于你的具体业务场景对**性能、数据一致性、可靠性和实现复杂度**的权衡。

**本文涉及的完整可运行示例代码已托管至GitHub，你可以通过 这个链接访问。**

希望这篇详解能帮助你在 Go 项目中更自信地选择和使用缓存策略。**你最常用哪种缓存策略？在 Go 中实现时遇到过哪些坑？欢迎在评论区分享交流！**

## >注：本文代码由AI生成，可编译运行，但仅用于演示和辅助文章理解，切勿用于生产！

**原「Gopher部落」已重装升级为「Go & AI 精进营」知识星球，快来加入星球，开启你的技术跃迁之旅吧！**

我们致力于打造一个高品质的 **Go 语言深度学习** 与 **AI 应用探索** 平台。在这里，你将获得：

**体系化 Go 核心进阶内容:**深入「Go原理课」、「Go进阶课」、「Go避坑课」等独家深度专栏，夯实你的 Go 内功。**前沿 Go+AI 实战赋能:**紧跟时代步伐，学习「Go+AI应用实战」、「Agent开发实战课」，掌握 AI 时代新技能。**星主 Tony Bai 亲自答疑:**遇到难题？星主第一时间为你深度解析，扫清学习障碍。**高活跃 Gopher 交流圈:**与众多优秀 Gopher 分享心得、讨论技术，碰撞思想火花。**独家资源与内容首发:**技术文章、课程更新、精选资源，第一时间触达。

衷心希望「Go & AI 精进营」能成为你学习、进步、交流的港湾。让我们在此相聚，享受技术精进的快乐！欢迎你的加入！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论