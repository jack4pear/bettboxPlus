# 首版验收

当前尚未完成实机验收。以 CI 运行结果和下表的证据为准，不将构建成功写作设备通过。

| 检查 | 状态 | 证据 |
| --- | --- | --- |
| Windows x64 兼容版构建 | 待运行 | GitHub Actions |
| Windows ARM64 构建 | 待运行 | GitHub Actions |
| Android ARM64 / ARMv7 / x86_64 / 通用构建 | 待运行 | GitHub Actions |
| 配置导入、保存、覆写与启动字段保留 | 本地通过 | Go 桥接测试；16 项 Flutter 导入/保存测试 |
| 非法参数显示内核错误 | 本地通过 | bridge validation tests |
| 熔断、冷却、连续恢复、全部不可用 | 本地通过 | race tests + offline fault injection，覆盖全部不可用及紧急恢复 |
| Windows x64 启动、代理/TUN、停止、重启、订阅、节点切换 | 待设备验收 | 不以构建替代 |
| Android ARM64 启动、VPN、停止、重启、订阅、节点切换 | 待设备验收 | 不以构建替代 |
| 官方版共存、数据不覆盖、更新不回官方版 | 静态核对，待设备验收 | 独立标识 + 安装与更新检查 |

设备记录需包含系统版本、设备/CPU、客户端提交、内核提交、测试日期、步骤、实际结果、错误或日志路径。Android 另记签名证书 SHA-256。其他架构只声明构建验证范围。

验收完成后更新 `ACCEPTANCE.json` 的 `source_commit`、`windows_x64`、`android_arm64`。证据可为本仓库记录或可访问的 CI/设备日志链接。未通过前禁止正式发布预发布版本。

本地 Flutter 静态分析无问题；另有 3 项更新检查测试通过，覆盖定制预发布版本比较、草稿过滤及仓库地址。
