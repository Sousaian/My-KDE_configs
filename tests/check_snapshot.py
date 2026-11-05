"""Verificações estáticas offline; nunca importa ou executa configurações."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ('.bashrc', '.zshrc', 'kdeglobals', 'kwinrc',
         'plasma-org.kde.plasma.desktop-appletsrc', 'kitty/kitty.conf',
         'kitty/theme.conf', 'kitty/userprefs.conf')


def require(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)


data = {name: (ROOT / name).read_text() for name in FILES}
privacy_pattern = re.compile(
    r'/home/|/Users/|-----BEGIN .*PRIVATE KEY|'
    r'(?im:^\s*(?:password|passwd|token|api[_-]?key|secret)\s*=\s*\S+)|'
    r'\bsk-[A-Za-z0-9_-]+|\bghp_[A-Za-z0-9]+|\bAIza[A-Za-z0-9_-]+')
privacy_count = sum(len(privacy_pattern.findall(content)) for content in data.values())
excluded_keys = ('XwaylandEisNoPromptApps', 'pinnedModel', '[Wallet]',
                 'Latitude=', 'Longitude=', 'latitude=', 'longitude=', 'Image=',
                 'placeInfo=', 'placeDisplayName=')
excluded_count = sum(content.count(key) for content in data.values() for key in excluded_keys)
require(privacy_count == 0 and excluded_count == 0,
        f'privacidade: {privacy_count} padrões; {excluded_count} chaves omitidas encontradas')
print(f'PASS: 8 snapshots; privacidade: {privacy_count} padrões; {excluded_count} chaves omitidas encontradas')

count = 0
for name in ('kdeglobals', 'kwinrc', 'plasma-org.kde.plasma.desktop-appletsrc'):
    section = False
    for number, line in enumerate(data[name].splitlines(), 1):
        line = line.strip()
        if not line or line.startswith(('#', ';')):
            continue
        if line.startswith('['):
            require(bool(re.fullmatch(r'(\[[^\[\]]*\])+', line)),
                    f'{name}:{number}: grupo inválido')
            section = True
        else:
            require(section and '=' in line, f'{name}:{number}: entrada inválida')
            if line.startswith('tiles='):
                tiles = json.loads(line.partition('=')[2])
                require(isinstance(tiles, dict) and isinstance(tiles.get('tiles'), list),
                        f'{name}:{number}: tiles inválido')
                count += 1
require(count > 0, 'nenhum JSON tiles encontrado')
print(f'PASS: estrutura KConfig básica; {count} JSON tiles')

visited = set()
def check_include(path, stack=()):
    require(path not in stack, 'ciclo de includes Kitty')
    require(path.is_file() and path.is_relative_to(ROOT / 'kitty'), 'include Kitty fora do snapshot')
    visited.add(path)
    for line in path.read_text().splitlines():
        if line.strip().startswith('include '):
            check_include((path.parent / line.strip().split(None, 1)[1]).resolve(), stack + (path,))
check_include(ROOT / 'kitty/kitty.conf')
require(len(visited) == 3, 'includes Kitty esperados')
print('PASS: 3 arquivos Kitty resolvidos sem executar Kitty')

zsh = data['.zshrc']
sources = [line for line in zsh.splitlines() if 'source ' in line and not line.lstrip().startswith('#')]
require(len(sources) == 5 and all(re.fullmatch(r'\[\[ -r (.+) \]\] && source \1', line)
                                                for line in sources), 'sources Zsh sem guarda -r')
require('[[ -o interactive && -x ~/.config/fastfetch/random-logo.sh ]] && ~/.config/fastfetch/random-logo.sh' in zsh,
        'guarda fastfetch ausente')
print('PASS: 5 sources Zsh com -r; fastfetch interativo com -x')

scratch = Path(os.environ['TMPDIR']) if 'TMPDIR' in os.environ else Path.home() / '.cache/My-KDE_configs/tests'
scratch.mkdir(mode=0o700, parents=True, exist_ok=True)
commands = [('bash', '--noprofile', '--norc', '-n', '.bashrc'), ('zsh', '-f', '-n', '.zshrc')]
with tempfile.TemporaryDirectory(prefix='kde-static-', dir=scratch) as home:
    for shell, *args in commands:
        executable = shutil.which(shell)
        require(executable is not None, shell + ' ausente (não instalar automaticamente)')
        result = subprocess.run([executable, *args], cwd=ROOT,
                                env={'HOME': home, 'PATH': '/usr/bin:/bin', 'TMPDIR': str(scratch)},
                                capture_output=True, text=True, timeout=10)
        require(result.returncode == 0, shell + ': ' + result.stderr)
        print('PASS: ' + ' '.join([shell, *args]) + ' (somente sintaxe; ambiente isolado)')
print('PASS: nenhuma configuração aplicada; revisão manual ainda necessária')
