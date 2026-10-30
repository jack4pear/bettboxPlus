# BettboxPlus 安装说明

从 `jack4pear/bettboxPlus` 的预发布页下载；核对 `SHA256SUMS.txt`。

## Windows

首版提供 x64 兼容版（GOAMD64=v1）和 ARM64 安装程序。兼容版指 CPU 指令集，不承诺 Windows 7。实际最低系统版本还受 Flutter、插件及 Go 工具链限制，未经验收的系统不作支持声明。Windows 首版不签名。

应用目录名为 BettboxPlus，服务为 `BettboxPlusHelperService`，管道为 `BettboxPlus.Helper`。安装 GUID 独立，程序与数据均不复用官方版。Windows 常规数据由 path_provider 放入 `%APPDATA%\io.github.jack4pear\BettboxPlus`；便携包使用包内 `portable`。实际路径可在客户端打开数据目录核对。

首次启动导入普通配置，确认能启动和切换节点，再测试系统代理或 TUN。停止其他客户端的代理/TUN 后测试。本项目不保证两个客户端同时接管系统网络。

## Android

包名为 `io.github.jack4pear.bettboxplus`，可与官方版共存。提供 ARM64、ARMv7、x86_64、通用 APK。各 ABI 包使用相同的持久密钥，可按系统正常覆盖更新；它们都不能覆盖官方包名。

Android 最低 API 26。系统一次只允许一个 VPN 服务。导入配置后授权 VPN，测试启动、停止、重启与节点切换。不要把仅构建验证的 ABI 当成实机通过。

## Smart Fallback

导入 `examples/smart-fallback.yaml`，先把 SOCKS 端点改成真实节点。示例默认 `enabled: false`。在配置编辑器中设为 `true`，或通过现有脚本覆写 `proxy-groups` 中的 `smart-fallback` 对象。不增加专门的设置开关。

使用 `use` 时，provider 必须启用周期健康检查且 `lazy: false`，组同样设 `lazy: false`。provider 与组的 URL、expected-status 和检查周期必须匹配，周期大于超时。详见内核文档。

客户端保留增强字段及内核校验错误。非法数值、未知字段或不满足检查条件时，应显示 `smart-fallback` 错误。全部节点不可用时，内核状态为 `SMART-FALLBACK-UNAVAILABLE`，新连接报 `smart-fallback: no eligible healthy proxy`。可在代理组状态和日志中核对。

关闭增强功能后使用普通 fallback 行为。重载或重启清空熔断状态。使用官方内核前删除新增字段。

更新检查仅指向 `jack4pear/bettboxPlus`。首版使用 pre 通道，安装包文件名与更新后缀匹配；不会下载官方发行版。
