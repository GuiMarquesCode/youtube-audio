# YouTube Audio CLI

Baixe o áudio de um vídeo do YouTube em **MP3**, **WAV** ou nos dois formatos diretamente na sua pasta **Downloads**, pelo terminal Linux.

Usa [yt-dlp](https://github.com/yt-dlp/yt-dlp) para download e [FFmpeg](https://ffmpeg.org/) para conversão. Não precisa de servidor ou serviço em segundo plano.

## Recursos

- Modo interativo e argumentos de linha de comando.
- Detecta a pasta Downloads configurada no Linux, inclusive nomes traduzidos.
- Permite escolher outra pasta.
- Baixa somente o vídeo informado, mesmo se o link incluir uma playlist.
- Preserva arquivos finais existentes e permite retomar downloads parciais.
- Usa o título e o ID do vídeo no nome do arquivo.
- No modo `ambos`, baixa uma vez e produz WAV e MP3.

## Requisitos

Linux, Bash, Python 3.10 ou superior, suporte a `venv`, FFmpeg, ffprobe e internet.

Para suporte completo ao YouTube, instale também um runtime JavaScript compatível, como **Deno**, seguindo a [documentação oficial de EJS do yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/EJS). O extra `yt-dlp[default]` inclui o componente EJS, mas não instala o runtime. Deno é detectado automaticamente quando está no PATH.

## Instalação no Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-venv ffmpeg
```

Dentro da pasta deste projeto:

```bash
bash instalar.sh
```

O instalador cria `.venv` e instala as dependências Python nesse ambiente. Não altera o Python do sistema.

## Uso

Modo interativo — cole o link e escolha o formato:

```bash
./youtube-audio
```

Download direto de MP3:

```bash
./youtube-audio 'https://www.youtube.com/watch?v=ID_DO_VIDEO' -f mp3
```

Download de WAV:

```bash
./youtube-audio 'https://youtu.be/ID_DO_VIDEO' -f wav
```

Os dois formatos:

```bash
./youtube-audio 'https://youtu.be/ID_DO_VIDEO' -f ambos
```

Escolher outra pasta:

```bash
./youtube-audio 'https://youtu.be/ID_DO_VIDEO' -f mp3 -o "$HOME/Música/Meus áudios"
```

Ajuda:

```bash
./youtube-audio --help
```

Use aspas ao redor do link para proteger caracteres como `&`. No modo interativo, Enter no formato usa MP3. Fora de um terminal interativo, omitir `-f` também usa MP3.

## Qualidade e arquivos

O programa solicita o melhor áudio disponível na fonte. MP3 usa qualidade variável alta (`q=0`). WAV ocupa mais espaço e não recupera qualidade perdida na compressão original.

Os arquivos seguem o padrão `Título [ID].mp3` ou `Título [ID].wav`. No modo `ambos`, o WAV é a origem da conversão para MP3. Arquivos finais existentes são preservados. Se o download for interrompido, execute o mesmo comando para tentar retomar; arquivos parciais podem permanecer em Downloads.

## Atualizar

O YouTube muda com frequência. Para atualizar a dependência:

```bash
.venv/bin/python -m pip install --upgrade -r requirements.txt
```

## Solução de problemas

| Problema | Solução |
| --- | --- |
| FFmpeg ausente | Execute `sudo apt install ffmpeg`. |
| Falha ao criar `.venv` | Instale `python3-venv` e repita `bash instalar.sh`. |
| Desafio JavaScript / EJS | Instale um runtime conforme a documentação oficial vinculada acima. |
| Vídeo exige login ou está bloqueado | Confira o acesso no navegador e atualize yt-dlp. O CLI não importa cookies automaticamente. |
| Arquivo já existe | Ele é preservado. Mova ou remova o arquivo específico para baixar novamente. |
| Sem permissão na pasta | Escolha uma pasta gravável com `-o`. |

Vídeos privados, restritos, transmissões ao vivo e mudanças da plataforma podem impedir o download. O erro retornado pelo yt-dlp é exibido no terminal.

## Desenvolvimento

```text
.
├── yt_audio.py
├── youtube-audio
├── instalar.sh
├── requirements.txt
├── tests/test_cli.py
├── .gitignore
└── README.md
```

Testes unitários, sem rede nem dependências externas:

```bash
python3 -m unittest discover -s tests -v
```

Para testar o fluxo completo, instale os requisitos e execute com um vídeo seu ou autorizado:

```bash
./youtube-audio 'LINK_DO_VIDEO' -f ambos
```

## Publicação no GitHub

Crie um repositório vazio no GitHub e execute nesta pasta, substituindo a URL:

```bash
git init
git add .
git commit -m "Adiciona CLI de download de áudio"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

O `.gitignore` exclui o ambiente virtual e os caches Python. Escolha uma licença antes de distribuir o projeto como software de código aberto.

Use a ferramenta com conteúdos que você tem autorização para baixar.
# youtube-audio
