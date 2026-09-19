#!/usr/bin/env python3
"""Generate casks only from published releases of the two allowlisted forks."""
import json
import re
import subprocess
import tempfile
from pathlib import Path

REPOSITORIES = {
    'zed': ('sasha-edit', 'SashaEdit', 'io.sasha00123.SashaEdit'),
    'warp': ('sasha-term', 'SashaTerm', 'io.sasha00123.SashaTerm'),
}

def render(repo, release, manifest):
    cask, app, bundle = REPOSITORIES[repo]
    version = manifest.get('version', '')
    tag = 'personal-v' + version
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
        raise ValueError('Invalid version')
    if release.get('draft') or release.get('prerelease') or release['tag_name'] != tag:
        raise ValueError('Only published stable personal releases are accepted')
    if any(manifest.get(k) != v for k, v in {'repository':f'sasha00123/{repo}', 'cask':cask, 'app_name':app, 'bundle_id':bundle, 'tag':tag}.items()):
        raise ValueError('Unexpected app identity')
    if not re.fullmatch(r'[0-9a-f]{40}', manifest.get('commit', '')):
        raise ValueError('Missing source commit')
    assets = manifest.get('assets', [])
    if len(assets) != 2 or {a['architecture'] for a in assets} != {'arm64', 'x86_64'}:
        raise ValueError('Both architectures are required')
    published = {a['name']:a for a in release['assets']}
    for asset in assets:
        name = f'{cask}-{version}-macos-{asset["architecture"]}.zip'
        if asset['asset'] != name or name not in published:
            raise ValueError('Release is missing expected binary')
        if not re.fullmatch(r'[0-9a-f]{64}', asset['sha256']):
            raise ValueError('Missing immutable SHA-256')
        # GitHub computes this digest when an asset is uploaded.
        if published[name].get('digest') != 'sha256:' + asset['sha256']:
            raise ValueError('Binary digest does not match GitHub asset')
    source = f'{cask}-{version}-source.tar.gz'
    if source not in published or manifest.get('source_asset') != source:
        raise ValueError('Missing corresponding source archive')
    hashes = {a['architecture']:a['sha256'] for a in assets}
    return f'''cask "{cask}" do
  arch arm: "arm64", intel: "x86_64"

  version "{version}"
  sha256 arm:   "{hashes['arm64']}",
         intel: "{hashes['x86_64']}"

  url "https://github.com/sasha00123/{repo}/releases/download/personal-v#{{version}}/{cask}-#{{version}}-macos-#{{arch}}.zip"
  name "{app}"
  desc "Unofficial personal build of {repo.title()}"
  homepage "https://github.com/sasha00123/{repo}"

  depends_on macos: ">= :ventura"

  app "{app}.app"

  caveats <<~EOS
    This personal build is ad-hoc signed, not Apple-notarized.
    Update via this tap. Upstream self-updating is disabled.
    Source and licenses: https://github.com/sasha00123/{repo}/releases/tag/personal-v#{{version}}
  EOS
end
'''

def main():
    root = Path(__file__).resolve().parent.parent
    casks = root / 'Casks'
    casks.mkdir(exist_ok=True)
    for repo, (cask, _, _) in REPOSITORIES.items():
        releases = json.loads(subprocess.check_output(['gh','api',f'repos/sasha00123/{repo}/releases?per_page=100'], text=True))
        eligible = [r for r in releases if not r['draft'] and not r['prerelease'] and re.fullmatch(r'personal-v[0-9]+\.[0-9]+\.[0-9]+',r['tag_name'])]
        if not eligible:
            print(f'{repo}: no published personal release yet')
            continue
        release = max(eligible,key=lambda r:tuple(map(int,r['tag_name'].removeprefix('personal-v').split('.'))))
        with tempfile.TemporaryDirectory() as temporary:
            subprocess.run(['gh','release','download',release['tag_name'],'--repo',f'sasha00123/{repo}','--pattern','homebrew.json','--dir',temporary],check=True)
            manifest = json.loads((Path(temporary)/'homebrew.json').read_text())
        content = render(repo, release, manifest)
        path = casks / f'{cask}.rb'
        if path.exists():
            old = re.search(r'version "([0-9.]+)"',path.read_text())
            if old and tuple(map(int,old[1].split('.'))) > tuple(map(int,manifest['version'].split('.'))):
                raise ValueError('Refusing version downgrade')
        path.write_text(content)
        subprocess.run(['ruby','-c',str(path)],check=True)
        print(f'{repo}: validated {release["tag_name"]}')

if __name__ == '__main__':
    main()
