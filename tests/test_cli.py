import argparse
import unittest
from pathlib import Path
from unittest.mock import patch
import yt_audio


class CliTests(unittest.TestCase):
    def test_rejects_external_or_disguised_hosts(self):
        for url in ('file:///etc/passwd', 'https://youtube.com.evil.org/x',
                    'https://youtube.com@evil.org/x', 'https://evil.org/x'):
            with self.subTest(url=url), self.assertRaises(argparse.ArgumentTypeError):
                yt_audio.validate_url(url)

    def test_accepts_video_and_short_links(self):
        for url in ('https://www.youtube.com/watch?v=abc&list=xyz', 'https://youtu.be/abc'):
            self.assertEqual(yt_audio.validate_url(url), url)

    def test_both_uses_wav_as_source_not_mp3(self):
        config = yt_audio.options(Path('/tmp/Downloads com espaços'), 'ambos')
        self.assertEqual(config['postprocessors'][0]['preferredcodec'], 'wav')
        self.assertTrue(config['noplaylist'])
        self.assertFalse(config['overwrites'])

    def test_disabled_download_directory_falls_back(self):
        with patch('yt_audio.shutil.which', return_value=None):
            self.assertEqual(yt_audio.downloads_dir(), Path.home() / 'Downloads')

    def test_missing_ffmpeg_returns_actionable_failure(self):
        with patch('yt_audio.shutil.which', return_value=None):
            self.assertEqual(yt_audio.main(['https://youtu.be/abc', '-f', 'mp3']), 1)


if __name__ == '__main__':
    unittest.main()
