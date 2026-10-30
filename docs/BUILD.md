# 开发与构建

默认目录 `~/codes/bettboxPlus`。遵循 `~/WSL_QUICK_REFERENCE.md`，本项目明确使用 `codes`。跨 Windows/WSL 复制文件时先压缩。

## 锁定与源码

`build-lock.json` 记录客户端/内核提交、Flutter、Rust、Java、NDK 和 MetaCubeX Go 下载 SHA-256。MetaCubeX Go 1.26.10 是本内核需要的定制工具链，普通 Go 不可替代。`scripts/setup-toolchain.py` 校验归档、解压并检查版本。若上游可变下载地址的内容改变，摘要检查将失败，不自动接受更新。

`core/Clash.Meta` 是 MihomoPlus 指定提交的源码快照，加 `patches/bettbox-bridge.patch`。补丁保留 Bettbox 的 Android VPN、回调、流量统计及监听器改动。复现方式：在空目录检出锁定提交，然后 `git apply patches/bettbox-bridge.patch`。`core/kernel-files.json` 对最终源码逐文件锁定，`python scripts/verify-source.py` 在各平台构建前校验。Git 保留上游完整客户端历史。

Python 使用 uv 或既有运行时，Go/Rust 由 mise 管理。Flutter 固定为 3.47.7，Git 提交亦在锁文件。Windows 使用 Windows runner，Android 使用 Ubuntu runner。

## 验证

```sh
python scripts/verify-source.py
python scripts/setup-toolchain.py
mise link go@1.26.10-bettboxplus "$PWD/.toolchain/go"
export GOTOOLCHAIN=local
(cd core && mise exec go@1.26.10-bettboxplus -- go test -tags with_gvisor -timeout 5m ./...)
(cd core/Clash.Meta && CGO_ENABLED=1 mise exec go@1.26.10-bettboxplus -- go test -race -timeout 5m ./adapter ./adapter/outboundgroup ./adapter/provider ./tunnel)
flutter pub get
dart run build_runner build
flutter test test/common/patch_yaml_config_test.dart test/models/profile_save_test.dart test/common/qr_import_test.dart
```

内核故障注入：在 `core/Clash.Meta` 中编译 `dist/mihomo-smart-linux-amd64` 后运行 `python scripts/smoke-smart-fallback.py`。测试仅使用本地 SOCKS/HTTP 故障服务器，覆盖熔断、冷却、连续恢复、全部不可用与紧急恢复。

## 打包

手动运行 GitHub Actions `Package BettboxPlus`。六个目标：Windows x64 兼容版、Windows ARM64、Android ARM64、ARMv7、x86_64、通用 APK。所有内核从桥接源码编译，with_gvisor；ARMv7 额外 with_low_memory、GOARM=7。Android NDK 28.2.13676358，API 26 编译；64 位库采用 16 KB 页对齐链接选项。

Android 使用四个 `BETTBOXPLUS_*` 仓库 Secrets，详见签名政策。预检与 Gradle 双重阻止缺失密钥的 release 构建。Windows 的 helper 校验构建内核 SHA-256。产物附各目标 BUILD-INFO 与校验和，内核版本字符串含完整锁定提交，Windows 内核可运行 `BettboxPlusCore.exe --version`。

## 发布

只在验收后手动运行 `Publish accepted prerelease`，输入成功的打包 run ID 与匹配客户端版本的 tag。`docs/ACCEPTANCE.json` 必须记录该打包提交、Windows x64 和 Android ARM64 的通过结果及证据。发布校验拒绝未验收、构建失败、源码不匹配或缺少目标的运行，只发布 prerelease。

更新内核必须明确修改锁定提交、重新合入桥接补丁、重建文件摘要，并完整重跑验收。没有定时跟踪最新内核的工作流。
