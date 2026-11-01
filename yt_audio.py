#!/usr/bin/env python3
"""Baixa áudio de um vídeo do YouTube para Downloads."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def validate_url(value):
    parsed = urlparse(value)
    host = (parsed.hostname or '').lower()
    if parsed.scheme not in ('http', 'https') or host not in (
        'youtube.com', 'www.youtube.com', 'm.youtube.com', 'music.youtube.com',
        'youtu.be', 'www.youtu.be',
    ) or parsed.username or parsed.password:
        raise argparse.ArgumentTypeError('Informe um link HTTP(S) do YouTube válido.')
    return value


def downloads_dir():
    if shutil.which('xdg-user-dir'):
        result = subprocess.run(['xdg-user-dir', 'DOWNLOAD'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            candidate = Path(result.stdout.strip())
            if candidate.is_absolute() and candidate != Path.home():
                return candidate
    return Path.home() / 'Downloads'


def options(destination, audio_format):
    return {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': str(destination / '%(title).160B [%(id)s].%(ext)s'),
        'windowsfilenames': True,
        'overwrites': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav' if audio_format == 'ambos' else audio_format,
            'preferredquality': '0',
        }],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', nargs='?', type=validate_url, help='Link do vídeo (use aspas).')
    parser.add_argument('-f', '--formato', choices=['mp3', 'wav', 'ambos'], help='Formato de saída.')
    parser.add_argument('-o', '--destino', type=Path, help='Pasta alternativa a Downloads.')
    args = parser.parse_args(argv)
    try:
        if args.url is None:
            if not sys.stdin.isatty():
                parser.error('Informe o link do vídeo.')
            args.url = validate_url(input('Link do YouTube: ').strip())
        if args.formato is None:
            args.formato = input('Formato [mp3/wav/ambos] (mp3): ').strip().lower() or 'mp3' if sys.stdin.isatty() else 'mp3'
            if args.formato not in ('mp3', 'wav', 'ambos'):
                parser.error('Escolha mp3, wav ou ambos.')
        for program in ('ffmpeg', 'ffprobe'):
            if not shutil.which(program):
                raise RuntimeError('FFmpeg ausente. No Ubuntu: sudo apt install ffmpeg')
        try:
            import yt_dlp
        except ImportError as exc:
            raise RuntimeError('Instale as dependências com: bash instalar.sh') from exc
        destination = (args.destino or downloads_dir()).expanduser().resolve()
        destination.mkdir(parents=True, exist_ok=True)
        print(f'Destino: {destination}', flush=True)
        downloaded = []
        config = options(destination, args.formato)
        config['post_hooks'] = [lambda filename: downloaded.append(Path(filename))]
        with yt_dlp.YoutubeDL(config) as downloader:
            downloader.download([args.url])
        if not downloaded:
            raise RuntimeError('Nenhum arquivo de áudio foi produzido.')
        for source in downloaded:
            print(f'Salvo: {source}')
            if args.formato == 'ambos':
                target = source.with_suffix('.mp3')
                if target.exists():
                    print(f'Já existe, preservado: {target}')
                    continue
                try:
                    subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error',
                                    '-n', '-i', str(source), '-vn', '-codec:a', 'libmp3lame',
                                    '-q:a', '0', str(target)], check=True)
                except (subprocess.CalledProcessError, KeyboardInterrupt):
                    target.unlink(missing_ok=True)
                    raise
                print(f'Salvo: {target}')
        return 0
    except KeyboardInterrupt:
        print('\nCancelado. Execute novamente para retomar o download.', file=sys.stderr)
        return 130
    except Exception as exc:
        print(f'Erro: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
