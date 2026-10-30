# BettboxPlus signing policy

BettboxPlus is independently maintained. Windows artifacts in the first release are unsigned. No upstream certificate, SignPath organization, signing service, or certification claim applies to this fork.

Android release builds use a dedicated persistent BettboxPlus keystore. The private key is never committed. GitHub Actions receives `BETTBOXPLUS_KEYSTORE_BASE64`, `BETTBOXPLUS_STORE_PASSWORD`, `BETTBOXPLUS_KEY_ALIAS`, and `BETTBOXPLUS_KEY_PASSWORD` through repository Secrets. Missing values stop packaging; Gradle also refuses release builds without signing configuration. There is no debug-key fallback.

Back up the keystore and passwords securely before distributing an APK. Future updates must use this same key. A lost key prevents compatible updates to existing installations. Never recreate a key automatically in CI.

Checksums establish artifact integrity, not publisher certification. Build provenance accompanies each artifact.
