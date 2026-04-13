---
title: 透视软件供应链安全：SBOM标准解读与Go项目生成指南
url: https://tonybai.com/2025/05/22/go-sbom-practice/
published: '2025-05-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 透视软件供应链安全：SBOM标准解读与Go项目生成指南

![](../../assets/b3eb3d30ff07d88a.png)


[本文永久链接](https://tonybai.com/2025/05/22/go-sbom-practice) – https://tonybai.com/2025/05/22/go-sbom-practice

大家好，我是Tony Bai。

近年来，软件供应链安全事件频发，从 SolarWinds 到 Log4Shell，每一次都给业界敲响了警钟。在这样的背景下，软件物料清单 (SBOM, Software Bill of Materials) 的重要性日益凸显。无论是甲方爸爸的硬性要求（尤其是在2B软件交付和白盒交付场景），还是我们自身对软件透明度和安全性的追求，SBOM 都已成为现代软件开发不可或缺的一环。

那么，SBOM 究竟是什么？它为何如此重要？市面上有哪些主流的 SBOM 标准？我们又该如何为自己的 Go 项目（当然，也适用于 Java、JS 等其他语言项目）生成和使用 SBOM 呢？

今天，我们就来一起深入探讨这些问题，为你揭开 SBOM 的神秘面纱。

![](../../assets/32b03e4c457f472e.gif)


## SBOM：你的软件“配料表”，为何如此重要？

想象一下，我们购买食品时会关注配料表，了解其成分、产地和营养信息。SBOM 之于软件，就如同食品的配料表。它是一份正式的、结构化的清单，详细列出了构成某个软件产品的所有组件及其依赖关系。

**SBOM 的核心价值在于提升软件供应链的透明度和可管理性，从而增强安全性：**

**透明度与可追溯性：**清晰展示软件由哪些“零件”（开源库、第三方组件、内部模块等）组装而成，包括直接依赖和传递依赖，让软件的构成不再是“黑盒”。**高效的漏洞管理：**当某个组件爆出新的安全漏洞时，通过 SBOM 可以快速定位所有受影响的软件产品，及时采取修复或缓解措施，大大缩短应急响应时间。**许可证合规性审计：**准确识别所有组件的开源许可证类型，确保符合合规要求，避免潜在的法律风险。**供应链风险评估：**了解组件的来源、版本、维护状态等信息，有助于评估整个软件供应链的潜在风险。**提升软件质量与可信度：**向客户和合作伙伴提供 SBOM，能够证明你对软件安全和质量的重视，建立信任。

可以说，SBOM 是构筑现代软件供应链安全防线的基石。

## SBOM 标准巡礼：SPDX、CycloneDX、SWID 与 DSDX

要让 SBOM 真正发挥作用，统一的标准至关重要。目前，业界存在多个 SBOM 标准，各有侧重。我们重点关注几个主流和新兴的规范：

![](../BlogImages/2025/go-sbom-practice-2.png)


**1. SPDX (Software Package Data Exchange):**

**定位与特点：**由**Linux Foundation**主导，是国际公认的[SBOM 开放标准 (ISO/IEC 5962:2021)](https://www.iso.org/standard/81870.html)。SPDX 最初更侧重于**许可证合规性**，但其规范已发展得非常全面，能够详细描述软件包、文件、代码片段及其之间的关系。**核心数据字段：**包含包信息（名称、版本、供应商、下载位置、校验和）、文件信息（名称、类型、许可证、校验和）、许可证信息（SPDX许可证列表中的标准标识符、自定义许可证）、以及组件之间的关系（依赖、包含、生成等）。**格式：**支持多种格式，如 Tag-Value、JSON、YAML、RDF/XML 等。**适用场景：**许可证合规审计、知识产权管理、软件溯源、大型复杂项目的详细清单管理、漏洞管理等。**由于其全面性和国际标准化地位，SPDX 是本次我们实战演练的重点。**

**2. CycloneDX:**

**定位与特点：**由**OWASP（开放式Web应用程序安全项目）**社区驱动，更侧重于**安全用例和运营需求**。它设计轻量、易于自动化生成和消费，非常适合在 CI/CD 流程中集成。**核心数据字段：**关注组件（名称、版本、供应商、PURL、CPE）、依赖关系图谱、已知漏洞信息（或指向漏洞数据库的链接如 VEX）、服务信息、许可证信息等。**格式：**主要支持 JSON 和 XML。**适用场景：**漏洞管理、安全审计、软件成分分析 (SCA)、CI/CD 集成等。

**3. SWID (Software Identification) Tags:**

**定位与特点：**由**ISO/IEC 19770-2:2015**标准定义，主要用于**软件资产管理 (SAM)**和安全。SWID 标签提供了识别已安装软件、追踪其生命周期（安装、更新、卸载）的方法。**核心价值：**虽然 SWID 本身不直接提供完整的依赖关系图谱，但它可以作为 SBOM 中组件身份识别的重要依据，并能与其他 SBOM 格式结合使用。**适用场景：**软件资产管理、安全配置管理、补丁管理。

**4. DSDX (Digital Supply-chain Data Exchange):**

**定位与特点：**这是由**中国信息通信研究院（CAICT）**牵头，联合国内多家单位共同研究制定的**数字供应链数据交换标准**。它旨在规范数字供应链中各类数据的描述、交换和共享，SBOM 是其关注的重要数据类型之一。**核心价值：**DSDX 致力于构建符合中国国情和产业发展需求的数字供应链标准体系，推动国内软件供应链的透明化和安全保障。**适用场景：**国内企业间的软件供应链数据交换、合规性要求等。目前 DSDX 仍在发展和推广阶段，值得国内开发者关注。

**标准之间的关系与选择：**

这些标准并非完全孤立。例如，SPDX 和 CycloneDX 都被广泛用于生成 SBOM，并且都符合美国 NTIA《软件物料清单的最小元素》的要求。SWID 标签可以增强 SBOM 中组件的识别能力。DSDX 则可能在未来成为国内数字供应链数据交换的重要规范。

**在实际操作中，SPDX 和 CycloneDX 是目前最主流的 SBOM 格式选择。** 许多工具都支持生成这两种格式，它们之间也可以进行一定程度的转换。本次，我们将以 **SPDX** 为例进行后续的实战演示。

## Go 项目 SPDX SBOM 生成实战：利器 anchore/syft 登场

理论说了不少，我们来动手实践一下。市面上有许多优秀的 SBOM 生成工具，今天我们选用一款广受欢迎的开源工具：**anchore/syft**。

syft 是一个功能强大的 CLI 工具和 Go 库，可以从容器镜像和文件系统中生成 SBOM。它支持多种 SBOM 格式（包括我们今天重点关注的 SPDX 和另一种主流格式 CycloneDX），并且对多种编程语言和包管理器有良好的支持。

### 安装 syft

你可以从其 GitHub Release 页面下载预编译的二进制文件，或者使用 Go 工具安装：

```
$go install github.com/anchore/syft/cmd/syft@latest
```


确保你的 \$GOPATH/bin 或 \$GOBIN 在你的 PATH 环境变量中。

### 实战：为知名 Go Web 框架 gin-gonic/gin 生成 SPDX JSON SBOM

让我们以一个真实的、大家熟知的 Go 开源项目 `gin-gonic/gin`

为例。首先，你需要将项目克隆到本地：

```
$git clone https://github.com/gin-gonic/gin.git
$cd gin
```


然后，在 gin 项目的根目录下，运行 syft 命令生成 SPDX JSON 格式([spdx 2.3规范](https://spdx.github.io/spdx-spec/v2.3/))的 SBOM：

```
$syft . -o spdx-json=gin-sbom.spdx.json
✔ Indexed file system .
✔ Cataloged contents cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8
├── ✔ Packages [48 packages]
├── ✔ Executables [0 executables]
├── ✔ File digests [4 files]
└── ✔ File metadata [4 locations]
[0000] WARN no explicit name and version provided for directory source, deriving artifact ID from the given path (which is not id
... ...
```


这里的“.”代表当前目录。syft会自动识别 Go 项目的 go.mod 文件来解析依赖，并将结果输出到 gin-sbom.spdx.json 文件中。

注：截至目前，

[spdx的最新规范版本为3.0.1]。

生成的 gin-sbom.spdx.json 文件内容片段示例：

```
{
"spdxVersion": "SPDX-2.3",
"dataLicense": "CC0-1.0",
"SPDXID": "SPDXRef-DOCUMENT",
"name": ".",
"documentNamespace": "https://anchore.com/syft/dir/453d49c6-8063-46f1-9d7e-61dd7e789f6d",
"creationInfo": {
"licenseListVersion": "3.25",
"creators": [
"Organization: Anchore, Inc",
"Tool: syft-[not provided]"
],
"created": "2025-05-17T22:45:19Z"
},
"packages": [
{
"name": "actions/cache",
"SPDXID": "SPDXRef-Package-github-action-actions-cache-422933d2a61f8d51",
"versionInfo": "v4",
"supplier": "Organization: GitHub",
"originator": "Organization: GitHub",
"downloadLocation": "NOASSERTION",
"filesAnalyzed": false,
"sourceInfo": "acquired package info from GitHub Actions workflow file or composite action file: /.github/workflows/gin.yml",
"licenseConcluded": "NOASSERTION",
"licenseDeclared": "NOASSERTION",
"copyrightText": "NOASSERTION",
"externalRefs": [
{
"referenceCategory": "SECURITY",
"referenceType": "cpe23Type",
"referenceLocator": "cpe:2.3:a:actions\\/cache:actions\\/cache:v4:*:*:*:*:*:*:*"
},
{
"referenceCategory": "PACKAGE-MANAGER",
"referenceType": "purl",
"referenceLocator": "pkg:github/actions/cache@v4"
}
]
},
... ...
```


SPDX JSON 格式详细记录了文档信息、包信息（包括名称、版本、SPDXID、许可证、PURL等）以及它们之间的依赖关系。

### syft输出定制

如果你觉得syft默认输出到json文件中的信息不全，你可以对syft的行为做一些配置，可以使用syft配置文件，也可以使用环境变量。

syft默认的配置文件位置有如下几个(优先级从高到低)：

```
.syft.yaml
.syft/config.yaml
~/.syft.yaml
<XDG_CONFIG_HOME>/syft/config.yaml
```


如果你不知道配置文件的格式，可以执行syft config查看当前配置：

```
$syft config
log:
# suppress all logging output (env: SYFT_LOG_QUIET)
quiet: false
# increase verbosity (-v = info, -vv = debug) (env: SYFT_LOG_VERBOSITY)
verbosity: 0
# explicitly set the logging level (available: [error warn info debug trace]) (env: SYFT_LOG_LEVEL)
level: 'warn'
# file path to write logs to (env: SYFT_LOG_FILE)
file: ''
dev:
# capture resource profiling data (available: [cpu, mem]) (env: SYFT_DEV_PROFILE)
profile: ''
# the configuration file(s) used to load application configuration (env: SYFT_CONFIG)
config: ''
# the output format(s) of the SBOM report (options: syft-table, syft-text, syft-json, spdx-json, ...)
# to specify multiple output files in differing formats, use a list:
# output:
# - "syft-json=<syft-json-output-file>"
# - "spdx-json=<spdx-json-output-file>" (env: SYFT_OUTPUT)
output:
- 'syft-table'
# file to write the default report output to (default is STDOUT) (env: SYFT_LEGACYFILE)
legacyFile: ''
format:
# default value for all formats that support the "pretty" option (default is unset) (env: SYFT_FORMAT_PRETTY)
pretty:
template:
# path to the template file to use when rendering the output with the template output format.
# Note that all template paths are based on the current syft-json schema (env: SYFT_FORMAT_TEMPLATE_PATH)
path: ''
# if true, uses the go structs for the syft-json format for templating.
# if false, uses the syft-json output for templating (which follows the syft JSON schema exactly).
#
# Note: long term support for this option is not guaranteed (it may change or break at any time) (env: SYFT_FORMAT_TEMPLATE_LEGACY)
legacy: false
json:
# transform any syft-json output to conform to an approximation of the v11.0.1 schema. This includes:
# - using the package metadata type names from before v12 of the JSON schema (changed in https://github.com/anchore/syft/pull/1983)
#
# Note: this will still include package types and fields that were added at or after json schema v12. This means
# that output might not strictly be json schema v11 compliant, however, for consumers that require time to port
# over to the final syft 1.0 json output this option can be used to ease the transition.
#
# Note: long term support for this option is not guaranteed (it may change or break at any time) (env: SYFT_FORMAT_JSON_LEGACY)
legacy: false
# include space indentation and newlines
# note: inherits default value from 'format.pretty' or 'false' if parent is unset (env: SYFT_FORMAT_JSON_PRETTY)
pretty:
spdx-json:
# include space indentation and newlines
# note: inherits default value from 'format.pretty' or 'false' if parent is unset (env: SYFT_FORMAT_SPDX_JSON_PRETTY)
pretty:
cyclonedx-json:
# include space indentation and newlines
# note: inherits default value from 'format.pretty' or 'false' if parent is unset (env: SYFT_FORMAT_CYCLONEDX_JSON_PRETTY)
pretty:
cyclonedx-xml:
# include space indentation and newlines
# note: inherits default value from 'format.pretty' or 'false' if parent is unset (env: SYFT_FORMAT_CYCLONEDX_XML_PRETTY)
pretty:
# whether to check for an application update on start up or not (env: SYFT_CHECK_FOR_APP_UPDATE)
check-for-app-update: true
# enable one or more package catalogers (env: SYFT_CATALOGERS)
catalogers: []
# set the base set of catalogers to use (defaults to 'image' or 'directory' depending on the scan source) (env: SYFT_DEFAULT_CATALOGERS)
default-catalogers: []
# add, remove, and filter the catalogers to be used (env: SYFT_SELECT_CATALOGERS)
select-catalogers: []
package:
# search within archives that do not contain a file index to search against (tar, tar.gz, tar.bz2, etc)
# note: enabling this may result in a performance impact since all discovered compressed tars will be decompressed
# note: for now this only applies to the java package cataloger (env: SYFT_PACKAGE_SEARCH_UNINDEXED_ARCHIVES)
search-unindexed-archives: false
# search within archives that do contain a file index to search against (zip)
# note: for now this only applies to the java package cataloger (env: SYFT_PACKAGE_SEARCH_INDEXED_ARCHIVES)
search-indexed-archives: true
# allows users to exclude synthetic binary packages from the sbom
# these packages are removed if an overlap with a non-synthetic package is found (env: SYFT_PACKAGE_EXCLUDE_BINARY_OVERLAP_BY_OWNERSHIP)
exclude-binary-overlap-by-ownership: true
license:
# include the content of licenses in the SBOM for a given syft scan; valid values are: [all unknown none] (env: SYFT_LICENSE_CONTENT)
content: 'none'
# deprecated: please use 'license-content' instead (env: SYFT_LICENSE_INCLUDE_UNKNOWN_LICENSE_CONTENT)
include-unknown-license-content:
# adjust the percent as a fraction of the total text, in normalized words, that
# matches any valid license for the given inputs, expressed as a percentage across all of the licenses matched. (env: SYFT_LICENSE_COVERAGE)
coverage: 75
# deprecated: please use 'coverage' instead (env: SYFT_LICENSE_LICENSE_COVERAGE)
license-coverage:
file:
metadata:
# select which files should be captured by the file-metadata cataloger and included in the SBOM.
# Options include:
# - "all": capture all files from the search space
# - "owned-by-package": capture only files owned by packages
# - "none", "": do not capture any files (env: SYFT_FILE_METADATA_SELECTION)
selection: 'owned-by-package'
# the file digest algorithms to use when cataloging files (options: "md5", "sha1", "sha224", "sha256", "sha384", "sha512") (env: SYFT_FILE_METADATA_DIGESTS)
digests:
- 'sha1'
- 'sha256'
content:
# skip searching a file entirely if it is above the given size (default = 1MB; unit = bytes) (env: SYFT_FILE_CONTENT_SKIP_FILES_ABOVE_SIZE)
skip-files-above-size: 256000
# file globs for the cataloger to match on (env: SYFT_FILE_CONTENT_GLOBS)
globs: []
executable:
# file globs for the cataloger to match on (env: SYFT_FILE_EXECUTABLE_GLOBS)
globs: []
# selection of layers to catalog, options=[squashed all-layers deep-squashed] (env: SYFT_SCOPE)
scope: 'squashed'
# number of cataloger workers to run in parallel
# by default, when set to 0: this will be based on runtime.NumCPU * 4, if set to less than 0 it will be unbounded (env: SYFT_PARALLELISM)
parallelism: 0
relationships:
# include package-to-file relationships that indicate which files are owned by which packages (env: SYFT_RELATIONSHIPS_PACKAGE_FILE_OWNERSHIP)
package-file-ownership: true
# include package-to-package relationships that indicate one package is owned by another due to files claimed to be owned by one package are also evidence of another package's existence (env: SYFT_RELATIONSHIPS_PACKAGE_FILE_OWNERSHIP_OVERLAP)
package-file-ownership-overlap: true
compliance:
# action to take when a package is missing a name (env: SYFT_COMPLIANCE_MISSING_NAME)
missing-name: 'drop'
# action to take when a package is missing a version (env: SYFT_COMPLIANCE_MISSING_VERSION)
missing-version: 'stub'
# Enable data enrichment operations, which can utilize services such as Maven Central and NPM.
# By default all enrichment is disabled, use: all to enable everything.
# Available options are: all, golang, java, javascript (env: SYFT_ENRICH)
enrich: []
dotnet:
# only keep dep.json packages which an executable on disk is found. The package is also included if a DLL is found for any child package, even if the package itself does not have a DLL. (env: SYFT_DOTNET_DEP_PACKAGES_MUST_HAVE_DLL)
dep-packages-must-have-dll: false
# only keep dep.json packages which have a runtime/resource DLL claimed in the deps.json targets section (but not necessarily found on disk). The package is also included if any child package claims a DLL, even if the package itself does not claim a DLL. (env: SYFT_DOTNET_DEP_PACKAGES_MUST_CLAIM_DLL)
dep-packages-must-claim-dll: true
# treat DLL claims or on-disk evidence for child packages as DLL claims or on-disk evidence for any parent package (env: SYFT_DOTNET_PROPAGATE_DLL_CLAIMS_TO_PARENTS)
propagate-dll-claims-to-parents: true
# show all packages from the deps.json if bundling tooling is present as a dependency (e.g. ILRepack) (env: SYFT_DOTNET_RELAX_DLL_CLAIMS_WHEN_BUNDLING_DETECTED)
relax-dll-claims-when-bundling-detected: true
golang:
# search for go package licences in the GOPATH of the system running Syft, note that this is outside the
# container filesystem and potentially outside the root of a local directory scan (env: SYFT_GOLANG_SEARCH_LOCAL_MOD_CACHE_LICENSES)
search-local-mod-cache-licenses:
# specify an explicit go mod cache directory, if unset this defaults to $GOPATH/pkg/mod or $HOME/go/pkg/mod (env: SYFT_GOLANG_LOCAL_MOD_CACHE_DIR)
local-mod-cache-dir: '~/Go/pkg/mod'
# search for go package licences in the vendor folder on the system running Syft, note that this is outside the
# container filesystem and potentially outside the root of a local directory scan (env: SYFT_GOLANG_SEARCH_LOCAL_VENDOR_LICENSES)
search-local-vendor-licenses:
# specify an explicit go vendor directory, if unset this defaults to ./vendor (env: SYFT_GOLANG_LOCAL_VENDOR_DIR)
local-vendor-dir: ''
# search for go package licences by retrieving the package from a network proxy (env: SYFT_GOLANG_SEARCH_REMOTE_LICENSES)
search-remote-licenses:
# remote proxy to use when retrieving go packages from the network,
# if unset this defaults to $GOPROXY followed by https://proxy.golang.org (env: SYFT_GOLANG_PROXY)
proxy: 'https://goproxy.cn,direct'
# specifies packages which should not be fetched by proxy
# if unset this defaults to $GONOPROXY (env: SYFT_GOLANG_NO_PROXY)
no-proxy: 'gomod.io,10.170.133.199'
main-module-version:
# look for LD flags that appear to be setting a version (e.g. -X main.version=1.0.0) (env: SYFT_GOLANG_MAIN_MODULE_VERSION_FROM_LD_FLAGS)
from-ld-flags: true
# search for semver-like strings in the binary contents (env: SYFT_GOLANG_MAIN_MODULE_VERSION_FROM_CONTENTS)
from-contents: false
# use the build settings (e.g. vcs.version & vcs.time) to craft a v0 pseudo version
# (e.g. v0.0.0-20220308212642-53e6d0aaf6fb) when a more accurate version cannot be found otherwise (env: SYFT_GOLANG_MAIN_MODULE_VERSION_FROM_BUILD_SETTINGS)
from-build-settings: true
java:
# enables Syft to use the network to fetch version and license information for packages when
# a parent or imported pom file is not found in the local maven repository.
# the pom files are downloaded from the remote Maven repository at 'maven-url' (env: SYFT_JAVA_USE_NETWORK)
use-network:
# use the local Maven repository to retrieve pom files. When Maven is installed and was previously used
# for building the software that is being scanned, then most pom files will be available in this
# repository on the local file system. this greatly speeds up scans. when all pom files are available
# in the local repository, then 'use-network' is not needed.
# TIP: If you want to download all required pom files to the local repository without running a full
# build, run 'mvn help:effective-pom' before performing the scan with syft. (env: SYFT_JAVA_USE_MAVEN_LOCAL_REPOSITORY)
use-maven-local-repository:
# override the default location of the local Maven repository.
# the default is the subdirectory '.m2/repository' in your home directory (env: SYFT_JAVA_MAVEN_LOCAL_REPOSITORY_DIR)
maven-local-repository-dir: '~/.m2/repository'
# maven repository to use, defaults to Maven central (env: SYFT_JAVA_MAVEN_URL)
maven-url: 'https://repo1.maven.org/maven2'
# depth to recursively resolve parent POMs, no limit if <= 0 (env: SYFT_JAVA_MAX_PARENT_RECURSIVE_DEPTH)
max-parent-recursive-depth: 0
# resolve transient dependencies such as those defined in a dependency's POM on Maven central (env: SYFT_JAVA_RESOLVE_TRANSITIVE_DEPENDENCIES)
resolve-transitive-dependencies: false
javascript:
# enables Syft to use the network to fill in more detailed license information (env: SYFT_JAVASCRIPT_SEARCH_REMOTE_LICENSES)
search-remote-licenses:
# base NPM url to use (env: SYFT_JAVASCRIPT_NPM_BASE_URL)
npm-base-url: ''
# include development-scoped dependencies (env: SYFT_JAVASCRIPT_INCLUDE_DEV_DEPENDENCIES)
include-dev-dependencies:
linux-kernel:
# whether to catalog linux kernel modules found within lib/modules/** directories (env: SYFT_LINUX_KERNEL_CATALOG_MODULES)
catalog-modules: true
nix:
# enumerate all files owned by packages found within Nix store paths (env: SYFT_NIX_CAPTURE_OWNED_FILES)
capture-owned-files: false
python:
# when running across entries in requirements.txt that do not specify a specific version
# (e.g. "sqlalchemy >= 1.0.0, <= 2.0.0, != 3.0.0, <= 3.0.0"), attempt to guess what the version could
# be based on the version requirements specified (e.g. "1.0.0"). When enabled the lowest expressible version
# when given an arbitrary constraint will be used (even if that version may not be available/published). (env: SYFT_PYTHON_GUESS_UNPINNED_REQUIREMENTS)
guess-unpinned-requirements: false
registry:
# skip TLS verification when communicating with the registry (env: SYFT_REGISTRY_INSECURE_SKIP_TLS_VERIFY)
insecure-skip-tls-verify: false
# use http instead of https when connecting to the registry (env: SYFT_REGISTRY_INSECURE_USE_HTTP)
insecure-use-http: false
# Authentication credentials for specific registries. Each entry describes authentication for a specific authority:
# - authority: the registry authority URL the URL to the registry (e.g. "docker.io", "localhost:5000", etc.) (env: SYFT_REGISTRY_AUTH_AUTHORITY)
# username: a username if using basic credentials (env: SYFT_REGISTRY_AUTH_USERNAME)
# password: a corresponding password (env: SYFT_REGISTRY_AUTH_PASSWORD)
# token: a token if using token-based authentication, mutually exclusive with username/password (env: SYFT_REGISTRY_AUTH_TOKEN)
# tls-cert: filepath to the client certificate used for TLS authentication to the registry (env: SYFT_REGISTRY_AUTH_TLS_CERT)
# tls-key: filepath to the client key used for TLS authentication to the registry (env: SYFT_REGISTRY_AUTH_TLS_KEY)
auth: []
# filepath to a CA certificate (or directory containing *.crt, *.cert, *.pem) used to generate the client certificate (env: SYFT_REGISTRY_CA_CERT)
ca-cert: ''
# specify the source behavior to use (e.g. docker, registry, oci-dir, ...) (env: SYFT_FROM)
from: []
# an optional platform specifier for container image sources (e.g. 'linux/arm64', 'linux/arm64/v8', 'arm64', 'linux') (env: SYFT_PLATFORM)
platform: ''
source:
# set the name of the target being analyzed (env: SYFT_SOURCE_NAME)
name: ''
# set the version of the target being analyzed (env: SYFT_SOURCE_VERSION)
version: ''
# base directory for scanning, no links will be followed above this directory, and all paths will be reported relative to this directory (env: SYFT_SOURCE_BASE_PATH)
base-path: ''
file:
# the file digest algorithms to use on the scanned file (options: "md5", "sha1", "sha224", "sha256", "sha384", "sha512") (env: SYFT_SOURCE_FILE_DIGESTS)
digests:
- 'SHA-256'
image:
# allows users to specify which image source should be used to generate the sbom
# valid values are: registry, docker, podman (env: SYFT_SOURCE_IMAGE_DEFAULT_PULL_SOURCE)
default-pull-source: ''
# (env: SYFT_SOURCE_IMAGE_MAX_LAYER_SIZE)
max-layer-size: ''
# exclude paths from being scanned using a glob expression (env: SYFT_EXCLUDE)
exclude: []
unknowns:
# remove unknown errors on files with discovered packages (env: SYFT_UNKNOWNS_REMOVE_WHEN_PACKAGES_DEFINED)
remove-when-packages-defined: true
# include executables without any identified packages (env: SYFT_UNKNOWNS_EXECUTABLES_WITHOUT_PACKAGES)
executables-without-packages: true
# include archives which were not expanded and searched (env: SYFT_UNKNOWNS_UNEXPANDED_ARCHIVES)
unexpanded-archives: true
cache:
# root directory to cache any downloaded content; empty string will use an in-memory cache (env: SYFT_CACHE_DIR)
dir: '~/Library/Caches/syft'
# time to live for cached data; setting this to 0 will disable caching entirely (env: SYFT_CACHE_TTL)
ttl: '7d'
# show catalogers that have been de-selected (env: SYFT_SHOW_HIDDEN)
show-hidden: false
attest:
# the key to use for the attestation (env: SYFT_ATTEST_KEY)
key: ''
# password to decrypt to given private key
# additionally responds to COSIGN_PASSWORD env var (env: SYFT_ATTEST_PASSWORD)
password: ''
```


也可将输出的当前配置保存为上面配置文件中的任何一个，然后做配置定制。

此外，我们看到对于每个重要的配置，都会有一个环境变量对应，比如：

```
SYFT_FORMAT_SPDX_JSON_PRETTY - spdx json格式美化
SYFT_GOLANG_SEARCH_LOCAL_MOD_CACHE_LICENSES - 在本地go module cache查找license信息
SYFT_GOLANG_SEARCH_REMOTE_LICENSES - 通过GOPROXY查找go module的license信息
```


如果你对license信息比较看重，我们可以基于上述环境变量配置再重新生成一次gin的SBOM：

```
$export SYFT_FORMAT_SPDX_JSON_PRETTY=true
$export SYFT_GOLANG_SEARCH_LOCAL_MOD_CACHE_LICENSES=true
$export SYFT_GOLANG_SEARCH_REMOTE_LICENSES=true
$syft . -o spdx-json=gin-sbom.spdx.json
```


### 关于 Java 和 JavaScript 项目

syft 同样能够为 Java (如 Maven, Gradle) 和 JavaScript (如 npm, yarn) 等项目生成 SPDX 或其他格式的 SBOM。其基本使用方式与 Go 项目类似，通常只需将扫描路径指向你的 Java 或 JavaScript 项目根目录即可。syft 会自动识别对应的包管理文件（如 pom.xml, package-lock.json）并解析依赖。更详细的用法和特定语言的注意事项，推荐查阅 anchore/syft 的官方文档。

## 让 SPDX SBOM 清单“说话”：将 Go 项目的 SPDX JSON 转换为 Excel

生成的 SPDX JSON 文件虽然结构清晰，便于机器处理，但对于需要提交给甲方或公司安全合规团队进行人工审计的场景，Excel 格式往往更受欢迎。

我们可以使用 Linux Foundation 维护的官方[SPDX online Tools](https://tools.spdx.org/app/convert/) 来实现这个转换。

通过浏览器打开https://tools.spdx.org/app/convert/，选择将spdx json转换为xlsx格式，并上传gin-sbom.spdx.json文件，点击Convert：

![](../BlogImages/2025/go-sbom-practice-3.png)


转换成功后，下载生成的excel文件，该文件的内容如下截图：

![](../BlogImages/2025/go-sbom-practice-4.png)


转换后的 Excel 文档通常会包含多个工作表，例如：Document Information, Package Information, Per File Information (如果分析到文件级别), Relationships, Licensing Information 等。 通过这样的表格，团队成员可以更方便地进行许可证审计、版本检查和依赖关系梳理。

当然SPDX 社区和第三方也都提供了一些工具来帮助完成此类转换，有gui的，也有命令行，大家可以自己的需求使用不同的转换工具。

## SBOM 的更广阔图景与 Go 开发者的行动

生成 SBOM 只是第一步。它的真正价值在于融入到整个软件开发生命周期中：

**CI/CD 集成：**在构建过程中自动生成 SBOM，并进行漏洞扫描（例如与 Trivy、Grype 等工具结合）和许可证策略检查。**VEX (Vulnerability Exploitability eXchange)：**结合 VEX 文档，可以更准确地判断 SBOM 中列出的漏洞在当前产品中是否真正可被利用，减少误报。**持续监控：**定期重新生成 SBOM 并分析，以应对新出现的漏洞和组件更新。

对于我们 Gopher 而言，掌握 SBOM（特别是 SPDX 这样被广泛认可的标准）的生成和使用，不仅是满足日益增长的合规要求，更是提升自身软件质量、安全意识和专业素养的体现。Go 语言的静态编译特性和完善的模块系统 (go.mod)，使得像 syft 这样的工具能够相对容易和准确地分析依赖关系，生成高质量的 SBOM。

## 小结

软件供应链安全是一项系统工程，而 SBOM 则是其中不可或缺的一块拼图。它为我们提供了一双“透视眼”，让我们能够清晰地了解软件的“前世今生”，从容应对潜在的风险。

无论是选择 SPDX、CycloneDX，还是 SWID 或 DSDX，理解并实践 SBOM 的核心理念至关重要。利用 syft 这样的工具，为你的 Go 项目（以及其他语言项目）生成并维护一份符合 SPDX 标准的 SBOM，都应该成为我们开发实践中的一项基本功。

现在，就动手为你的项目构建一份清晰的“软件家谱”吧！

**聊一聊，也帮个忙：**

**在你的工作中，是否已经开始被要求提供 SBOM？你主要关注 SBOM 的哪些方面（安全、合规、还是其他）？你通常使用哪种 SBOM 标准？****除了 syft，你还知道或使用过哪些优秀的 SBOM 生成或分析工具？特别是针对 SPDX 格式的。****你认为在 Go 社区，我们还可以做些什么来进一步推动 SBOM（尤其是 SPDX 标准）的普及和应用？**

欢迎在**评论区**留下你的经验、思考和问题。如果你觉得这篇文章对你有帮助，也请**转发给你身边的开发者朋友们**，让更多人了解和重视 SBOM！

**想与我进行更深入的 Go 语言、软件供应链安全与 AI 技术交流吗？** 欢迎加入我的**“Go & AI 精进营”知识星球**。

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


我们星球见！

商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论