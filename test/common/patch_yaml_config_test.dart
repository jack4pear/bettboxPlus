import 'package:bett_box/common/utils.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('patchYamlConfig', () {
    test('returns content without tabs unchanged', () {
      const content = 'proxies:\n  - name: a\n    short-id: 0123abcd\n';

      expect(identical(utils.patchYamlConfig(content), content), isTrue);
    });

    test('replaces tabs inside leading whitespace only', () {
      const content = 'proxies:\n\t- name: "a\tb"\n \t  server: x\n';

      expect(
        utils.patchYamlConfig(content),
        'proxies:\n  - name: "a\tb"\n     server: x\n',
      );
    });
  });

  group('patchValidateConfig', () {
    test('forces geodata-mode to false', () {
      expect(
        utils.patchValidateConfig('geodata-mode: true\nmode: rule\n'),
        'geodata-mode: false\nmode: rule\n',
      );
    });
  });
  test('import normalization preserves enhanced nested fields', () {
    const source =
        'proxy-groups:\n\t- name: Smart\n\t  smart-fallback:\n\t    enabled: true\n\t    cooldown: [1800, 3600, 7200]\n';
    final result = utils.patchValidateConfig(utils.patchYamlConfig(source));
    expect(
      result,
      contains(
        'smart-fallback:\n      enabled: true\n      cooldown: [1800, 3600, 7200]',
      ),
    );
  });
}
