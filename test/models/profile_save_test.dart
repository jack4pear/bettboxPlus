import 'dart:convert';
import 'dart:io';

import 'package:bett_box/common/common.dart';
import 'package:bett_box/models/models.dart';
// ignore: depend_on_referenced_packages
import 'package:path_provider_platform_interface/path_provider_platform_interface.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late Directory home;

  setUpAll(() async {
    home = await Directory.systemTemp.createTemp('bettboxplus_profiles_');
    PathProviderPlatform.instance = _ProfilePaths(home.path);
  });

  tearDownAll(() => home.delete(recursive: true));

  test('an unchanged update leaves the profile file untouched', () async {
    const profile = Profile(id: 'p', autoUpdateDuration: Duration(hours: 1));
    final file = File(await appPath.getProfilePath(profile.id));
    final first = utf8.encode('proxies: []\n');
    final second = utf8.encode('proxies: []\nrules: []\n');

    await profile.saveFile(first, validate: false);
    final stamp = DateTime(2020);
    await file.setLastModified(stamp);

    await profile.saveFile(first, validate: false);
    expect(await file.lastModified(), stamp);

    await profile.saveFile(second, validate: false);
    expect(await file.lastModified(), isNot(stamp));
    expect(await file.readAsString(), 'proxies: []\nrules: []\n');
  });
  test('saved subscription preserves Smart Fallback settings', () async {
    const profile = Profile(
      id: 'smart-profile',
      autoUpdateDuration: Duration(hours: 1),
    );
    final source = File('examples/smart-fallback.yaml').readAsBytesSync();
    await profile.saveFile(source, validate: false);
    final saved = await File(
      await appPath.getProfilePath(profile.id),
    ).readAsString();
    expect(saved, utf8.decode(source));
    expect(saved, contains('smart-fallback:'));
    expect(saved, contains('cooldown: [1800, 3600, 7200]'));
  });
}

class _ProfilePaths extends PathProviderPlatform {
  _ProfilePaths(this.path);
  final String path;
  @override
  Future<String?> getApplicationSupportPath() async => path;
  @override
  Future<String?> getTemporaryPath() async => path;
  @override
  Future<String?> getDownloadsPath() async => path;
}
