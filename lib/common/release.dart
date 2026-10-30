final _clientVersion = RegExp(
  r'^v?(\d+)\.(\d+)\.(\d+)(?:-plus\.(\d+))?(?:\+\d+)?$',
);

List<int>? _parts(String version) {
  final match = _clientVersion.firstMatch(version);
  if (match == null) return null;
  return [
    for (var i = 1; i <= 3; i++) int.parse(match.group(i)!),
    match.group(4) == null ? 1 : 0,
    int.parse(match.group(4) ?? '0'),
  ];
}

int? compareBettboxPlusVersions(String a, String b) {
  final left = _parts(a);
  final right = _parts(b);
  if (left == null || right == null) return null;
  for (var i = 0; i < left.length; i++) {
    final result = left[i].compareTo(right[i]);
    if (result != 0) return result;
  }
  return 0;
}

Map<String, dynamic>? selectBettboxPlusUpdate(
  List<dynamic> releases,
  String currentVersion, {
  required bool includePrerelease,
}) {
  Map<String, dynamic>? selected;
  var newest = currentVersion;
  for (final release in releases) {
    if (release is! Map ||
        release['draft'] == true ||
        (!includePrerelease && release['prerelease'] == true))
      continue;
    final tag = release['tag_name'];
    if (tag is! String || (compareBettboxPlusVersions(tag, newest) ?? -1) <= 0)
      continue;
    newest = tag;
    selected = {
      'tag_name': tag,
      'html_url': 'https://github.com/jack4pear/bettboxPlus/releases/tag/$tag',
      'body': release['body'] is String ? release['body'] : '',
    };
  }
  return selected;
}
