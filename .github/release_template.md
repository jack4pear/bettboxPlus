BettboxPlus 首个定制预发布版本。

基于 Bettbox 1.19.7，接入 MihomoPlus Smart Fallback，功能默认关闭，通过 YAML 或现有脚本覆写启用。

内核锁定：`3803eebbdb4ac3e92d39b1104e1c5ae668c2b18f`。桥接补丁、客户端提交和工具链见各目标 `BUILD-INFO-*.json`、`build-lock.json`。文件校验见 `SHA256SUMS.txt`。

包含 Windows x64 兼容版、ARM64；Android ARM64、ARMv7、x86_64 和通用 APK。Windows 首版不签名；Android 使用本定制版持久密钥。请阅读附件 `INSTALL.md`。

Windows x64 与 Android ARM64 的实机验收证据见 `ACCEPTANCE.json`。其他架构仅构建验证。可与官方版安装及数据共存；不保证同时接管系统代理或 VPN。

保留 Bettbox、Mihomo 及其他上游许可证和致谢。本定制版不继承上游签名认证声明。
