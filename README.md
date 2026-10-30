# BettboxPlus

[Bettbox](https://github.com/appshubcc/Bettbox) 的独立定制版，保留 Go 桥接层，接入 [MihomoPlus](https://github.com/jack4pear/mihomoPlus) 的 Smart Fallback。首版支持 Windows、Android，不新增设置界面。

- 客户端基线：Bettbox `1fb8806fdf8275a3694cda31eec7ed2062330aee`。
- 定制版：`1.19.7-plus.1+2026103001`。
- 内核：MihomoPlus `Meta`，锁定 `3803eebbdb4ac3e92d39b1104e1c5ae668c2b18f`。
- 内核以固定源码加 Bettbox 桥接补丁构建，不下载普通 Mihomo Release 内核，不自动追踪分支。
- Smart Fallback 默认关闭；通过 YAML 或脚本覆写配置启用。

Windows 首版不签名。本定制版不继承上游的签名、证书或审计认证声明。Android 使用本项目独立的持久签名密钥，缺失时禁止 release 构建。

## 使用与构建

- [安装说明](docs/INSTALL.md)
- [默认关闭的配置示例](examples/smart-fallback.yaml)
- [内核配置与行为](core/Clash.Meta/docs/SMART-FALLBACK.md)
- [开发与构建](docs/BUILD.md)
- [验收记录](docs/ACCEPTANCE.md)
- [签名政策](SIGNING-POLICY.md)

发布只经手动触发，并在六个目标构建完成、Windows x64 与 Android ARM64 实机验收通过后创建预发布。构建成功不代表实机通过；当前状态以验收记录为准。

## 许可证与致谢

保留上游 Git 历史及 [GPL-3.0 许可证](LICENSE)。感谢 Bettbox、FlClash、Mihomo、MihomoPlus、Zashboard、ClashMetaForAndroid、Sparkle、SFA、HUSI、v2rayN、Bett-rules 及所有上游贡献者。其他组件许可证仍随源码保留。本项目与上游官方发行版独立维护。
