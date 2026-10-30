import 'package:bett_box/common/release.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('custom prerelease ordering ignores build metadata', () {
    expect(
      compareBettboxPlusVersions('v1.19.7-plus.2', '1.19.7-plus.1+2026103001'),
      greaterThan(0),
    );
    expect(
      compareBettboxPlusVersions('v1.19.7-plus.1', '1.19.7-plus.1+2026103001'),
      0,
    );
    expect(
      compareBettboxPlusVersions('v1.19.7', '1.19.7-plus.9'),
      greaterThan(0),
    );
    expect(compareBettboxPlusVersions('latest', '1.19.7-plus.1'), isNull);
  });
  test('pre channel chooses newest nondraft release from the fork', () {
    final selected = selectBettboxPlusUpdate(
      [
        {'tag_name': 'v1.19.7-plus.2', 'prerelease': true, 'body': 'two'},
        {'tag_name': 'v1.19.7-plus.12', 'prerelease': true},
        {'tag_name': 'v9.0.0-plus.1', 'prerelease': true, 'draft': true},
        {'tag_name': 'unrelated'},
      ],
      '1.19.7-plus.1',
      includePrerelease: true,
    );
    expect(selected?['tag_name'], 'v1.19.7-plus.12');
    expect(
      selected?['html_url'],
      startsWith('https://github.com/jack4pear/bettboxPlus/releases/tag/'),
    );
  });
  test('stable channel excludes prereleases and older versions', () {
    expect(
      selectBettboxPlusUpdate(
        [
          {'tag_name': 'v1.20.0-plus.1', 'prerelease': true},
          {'tag_name': 'v1.19.6'},
        ],
        '1.19.7',
        includePrerelease: false,
      ),
      isNull,
    );
  });
}
