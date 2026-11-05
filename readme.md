# My-KDE_configs

Autor: Ian Alves Sousa.

Snapshot público revisado e sanitizado de configurações pessoais do Arch Linux.
Não representa backup completo ou 100% fiel do ambiente.
Clonar ou executar testes estáticos deste repositório não altera configurações reais.
Não existe instalador, build ou aplicação automática.

## Ambiente de referência

Versões confirmadas via Pacman em 5 de novembro de 2026:

| Componente | Versão |
| --- | --- |
| plasma-workspace | 6.8.2-1 |
| kwin | 6.8.2-1 |
| kitty | 0.49.2-1 |
| zsh | 5.9.2-1 |

KDE: Breeze Dark; ícones Tela-circle-dracula-dark.
Kitty: CaskaydiaCove Nerd Font Mono; tema escuro com includes locais.
KWin: 3 desktops virtuais. Monitores, IDs, screenMapping, geometrias,
painéis e layouts são específicos da máquina de origem, não portáveis.
Os snapshots preservam esses layouts; copiar não garante reprodução visual.

## Arquivos

Origem no ambiente de referência → arquivo no repositório → destino manual:

| Origem / destino | Snapshot |
| --- | --- |
| `~/.bashrc` | `.bashrc` |
| `~/.zshrc` | `.zshrc` |
| `~/.config/kdeglobals` | `kdeglobals` |
| `~/.config/kwinrc` | `kwinrc` |
| `~/.config/plasma-org.kde.plasma.desktop-appletsrc` | `plasma-org.kde.plasma.desktop-appletsrc` |
| `~/.config/kitty/kitty.conf` | `kitty/kitty.conf` |
| `~/.config/kitty/theme.conf` | `kitty/theme.conf` |
| `~/.config/kitty/userprefs.conf` | `kitty/userprefs.conf` |

Sanitização prévia: wallpapers pessoais, geolocalização do weather, pinnedModel
KDE, grupo Wallet com preferências pessoais e exceção XwaylandEisNoPromptApps
omitidos. IDs locais remanescentes exigem revisão manual antes de publicação.

## Dependências e recursos externos

Para usar cada configuração → aplicativo correspondente: Bash, Zsh, KDE Plasma/KWin
ou Kitty. Instalação de aplicativos é etapa separada, por decisão do usuário;
este repositório não instala pacotes.

Zsh preserva Oh My Zsh (plugins git e sudo), Powerlevel10k,
zsh-autosuggestions e zsh-syntax-highlighting. Sources são condicionados à
leitura dos arquivos. `~/.p10k.zsh` é opcional e não incluído.
O script pessoal `~/.config/fastfetch/random-logo.sh` não é versionado;
executa somente em shell interativo quando executável, sendo pulado se ausente.

Aliases dependem de eza, code, Flatpak/Spotify e utilitários correspondentes.
O handler de comandos ausentes depende de Pacman e sua base de arquivos.
A função `in` usa Pacman e yay ou paru para AUR; aliases de manutenção podem
instalar, atualizar ou remover pacotes quando invocados. Testes não os invocam.
Bash preserva referência opcional ao caminho pessoal `.console-ninja/.bin`.

Widgets externos observados:
- `a2n.earbud.plasmoid`
- `com.github.tilorenz.compact_pager`
- `org.kde.olib.thermalmonitor`

Widgets, fontes, ícones, temas externos, wallpapers e seus dados não são
incluídos nem instalados. Ausências podem mudar aparência e funcionalidade.
Nenhuma licença nova é atribuída a esses recursos.

## Testes offline, sem aplicação

Na raiz do repositório, com Python 3.9+ (`Path.is_relative_to` exige 3.9), Bash e Zsh já disponíveis:

```sh
python3 tests/check_snapshot.py
# Para selecionar diretório temporário existente ou criar um privado:
TMPDIR="$HOME/.cache/My-KDE_configs/tests" python3 tests/check_snapshot.py
```

Usa biblioteca padrão, ambiente vazio para parsers de shell, HOME descartável
no `TMPDIR` fornecido ou, sem essa variável, em `~/.cache/My-KDE_configs/tests`.
Diretório criado quando necessário com modo `0700`; análise estática. Não executa conteúdo dos dotfiles,
Kitty, aliases, helpers, Plasma ou DBus. Não acessa rede nem instala dependências.
Verifica sintaxe, estrutura KConfig básica, JSON de tiles, includes Kitty,
guardas opcionais e padrões selecionados de privacidade.
Não substitui revisão manual nem comprova comportamento visual ou ausência de segredos.

## Backup manual antes de qualquer restauração

Nada nesta seção é executado automaticamente. Escolha arquivos e preserve os
originais antes de sobrescrever. Exemplo opcional para preservar os oito caminhos
existentes, fora do repositório, com diretório privado e estrutura verificável:

```sh
umask 077
backup="$HOME/.local/state/My-KDE_configs/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup"
for rel in .bashrc .zshrc .config/kdeglobals .config/kwinrc .config/plasma-org.kde.plasma.desktop-appletsrc .config/kitty/kitty.conf .config/kitty/theme.conf .config/kitty/userprefs.conf; do
    if [ -f "$HOME/$rel" ]; then
        mkdir -p "$backup/$(dirname "$rel")"
        cp -a "$HOME/$rel" "$backup/$rel"
        chmod 600 "$backup/$rel"
    else
        printf 'Ausente, não copiado: %s\n' "$rel"
    fi
done
printf 'Backup para conferir: %s\n' "$backup"
```

Confira cada arquivo copiado antes de continuar. Arquivos ausentes não são
recriados pelo backup. `cp -a` preserva conteúdo e metadados; `chmod` restringe
permissões das cópias. Backup contém dados pessoais: não adicionar ao Git.

## Instalação / restauração escolhida manualmente

Leia e compare os arquivos. Prefira copiar somente arquivos escolhidos, um por
vez, depois do backup. Exemplo de instalação de um único arquivo, na raiz do repo:

```sh
cp -i .zshrc "$HOME/.zshrc"
```

Esse comando, somente se executado e confirmado quando solicitado, altera a
configuração real. Não aplique todos os snapshots por padrão. Para reverter
esse exemplo, confira primeiro o conteúdo no diretório de backup escolhido:

```sh
cp -i "$backup/.zshrc" "$HOME/.zshrc"
```

Use os caminhos explícitos da tabela para outros arquivos escolhidos e seus
backups correspondentes. Não copie diretórios inteiros sobre HOME.
`cp -i` pede confirmação de sobrescrita, mas backup e cópia não constituem
transação contra Plasma regravando arquivos.
Plasma pode sobrescrever configurações durante sessão ativa; planeje cópia com
sessão encerrada. Logout/login somente se usuário decidir. Nenhum reinício de
Plasma/KWin é automatizado ou necessário para testar este repositório.
