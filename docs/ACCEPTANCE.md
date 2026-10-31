# 首版验收

2026-10-30：完成构建与自动检查。2026-10-31：维护者在当前 Codex 对话中确认“实机验收通过”，据此登记当前计划范围内的 Windows x64 与 Android ARM64 验收通过，并允许发布预发布版本。

实机结果由维护者确认，代理未独立复测；未提供设备型号、系统版本、逐项测试结果或设备日志。其他架构仍仅声明构建验证。

客户端构建提交：`acde77934d3087eecf1fb5dd2480d1d4250d4b4d`。内核锁定：`3803eebbdb4ac3e92d39b1104e1c5ae668c2b18f`。

[最终打包运行与全部产物](https://github.com/jack4pear/bettboxPlus/actions/runs/41058638604) 已成功。详细文件 SHA-256、签名证书指纹与内核追溯信息见 [ACCEPTANCE.json](ACCEPTANCE.json) 的 `build_verification`；顶层 Windows x64 与 Android ARM64 验收状态已按维护者确认更新为 `passed`。

| 检查 | 状态 | 证据 |
| --- | --- | --- |
| Windows x64 兼容版构建 | 通过 | Windows runner；便携包应用、核心、helper 均为 PE AMD64；核心嵌入 GOAMD64=v1 |
| Windows ARM64 构建 | 通过 | 原生 ARM64 Windows runner；固定 Flutter 提交初始化原生 SDK；内核运行 --version 输出完整锁定提交 |
| Android ARM64 / ARMv7 / x86_64 / 通用 APK 构建 | 全部通过 | 四种 APK 实际 ABI 与目标一致；使用同一专属持久签名证书 |
| 配置导入、保存、覆写与启动字段保留 | 自动测试通过 | Go YAML/脚本 JSON round trip；Flutter 文件保存与导入测试 |
| 非法参数向客户端返回内核错误 | 自动测试通过 | 非正整数、小数、非法字符串均保留 smart-fallback 错误 |
| 熔断、冷却、连续恢复、全部不可用 | 自动测试通过 | race tests；离线 SOCKS/HTTP 故障注入；覆盖优先级恢复及紧急恢复 |
| 更新检查 | 自动测试通过 | 定制 plus.N 预发布比较、草稿过滤、新仓库地址；不回到官方发行版 |
| 产物完整性与源码追溯 | 通过 | 六组归档下载摘要及内部校验和；APK 内 Go 构建信息指向客户端提交，版本含内核锁定提交 |
| Android 应用标识与 JNI | 编译产物核对通过 | APK manifest 包名 io.github.jack4pear.bettboxplus，JNI 导出名称匹配新命名空间 |
| Android 64 位内核页对齐 | 编译产物核对通过 | ARM64、x86_64 内核 ELF LOAD 对齐为 16 KB |
| Windows x64 启动、代理/TUN、停止、重启、订阅、节点切换 | 维护者确认通过 | 2026-10-31 用户报告；代理未独立复测 |
| Android ARM64 启动、VPN、停止、重启、订阅、节点切换 | 维护者确认通过 | 2026-10-31 用户报告；代理未独立复测 |
| 官方版安装共存、数据不覆盖 | 维护者确认验收通过；静态标识核对通过 | 包名、安装 GUID、服务、管道、程序名、数据路径独立；未提供逐项设备日志 |

19 项 Flutter 导入、保存、更新检查测试通过。Flutter 静态分析无问题，GitHub Actions 工作流经 actionlint 检查。

APK 中库文件可能经 Android Gradle 的符号剥离而与编译时原件哈希不同。记录同时保留编译原件和 APK 实际库的哈希；实际库的内核提交、Go 工具链、客户端 VCS 提交与目标 ABI 已核对。

设备验收记录需包含系统版本、设备/CPU、客户端提交、内核提交、测试日期、步骤、实际结果、错误或日志路径。Android 另记签名证书 SHA-256。自动检查不替代设备测试；实机通过结论仅依据维护者本次确认。

`ACCEPTANCE.json` 顶层已记录对应打包源码提交与维护者验收确认。后续补充设备型号、系统版本和日志时，应保留本次确认来源。发布工作流仍核对构建成功状态、源码一致性和验收记录。
