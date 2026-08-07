import os
import sys
import questionary
from rich.console import Console
from rich.panel import Panel
import yt_dlp

console = Console()

VIDEO_FORMATS = {
    "Best Available (4K/8K)": "bestvideo+bestaudio/best",
    "1080p MP4": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "720p MP4": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
    "480p MP4": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
    "Worst (Smallest Size)": "worstvideo+worstaudio/worst",
}

AUDIO_FORMATS = {
    "MP3 (192kbps)": {"codec": "mp3", "quality": "192"},
    "MP3 (320kbps)": {"codec": "mp3", "quality": "320"},
    "AAC (m4a)": {"codec": "aac", "quality": "192"},
    "FLAC (Lossless)": {"codec": "flac", "quality": "0"},
    "Opus (Best Efficiency)": {"codec": "opus", "quality": "192"},
}


class YTDownloader:
    def __init__(self):
        self.url = ""
        self.mode = ""
        self.format_key = ""
        self.target = ""
        self.output_dir = "./downloads"
        self.playlist_range = None

    def gather_inputs(self):
        console.print(Panel("YouTube Downloader", style="bold cyan"))

        self.url = questionary.text(
            "Paste YouTube URL (video or playlist):",
            validate=lambda t: "youtube.com" in t or "youtu.be" in t or "Invalid YouTube URL"
        ).ask()
        if not self.url:
            sys.exit(0)

        self.mode = questionary.select(
            "Download type:",
            choices=["Video", "Audio Only"]
        ).ask()

        if self.mode == "Video":
            self.format_key = questionary.select(
                "Select video quality:",
                choices=list(VIDEO_FORMATS.keys())
            ).ask()
        else:
            self.format_key = questionary.select(
                "Select audio format:",
                choices=list(AUDIO_FORMATS.keys())
            ).ask()

        is_playlist = "playlist" in self.url.lower() or "list=" in self.url
        if is_playlist:
            self.target = questionary.select(
                "Playlist detected. Download scope:",
                choices=["Full Playlist", "Specific Range", "Single Video from Playlist"]
            ).ask()

            if self.target == "Specific Range":
                self.playlist_range = questionary.text(
                    "Enter range (e.g., 1-10, 5,8,12-20):"
                ).ask()
            elif self.target == "Single Video from Playlist":
                idx = questionary.text("Enter video index number in playlist:").ask()
                self.playlist_range = str(idx)
        else:
            self.target = "Single Video"

        self.output_dir = questionary.path(
            "Save location:",
            default="./downloads",
            only_directories=True
        ).ask()

    def build_opts(self):
        opts = {
            'outtmpl': f'{self.output_dir}/%(playlist_index)s - %(title)s.%(ext)s',
            'ignoreerrors': True,
            'download_archive': f'{self.output_dir}/.archive.txt',
            'writethumbnail': True,
            'embedthumbnail': True,
            'addmetadata': True,
            'concurrent_fragment_downloads': 4,
            'progress_hooks': [self._progress_hook],
        }

        if self.mode == "Video":
            opts['format'] = VIDEO_FORMATS[self.format_key]
            opts['merge_output_format'] = 'mp4'
        else:
            audio_cfg = AUDIO_FORMATS[self.format_key]
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_cfg['codec'],
                'preferredquality': audio_cfg['quality'],
            }]

        if self.playlist_range:
            opts['playlist_items'] = self.playlist_range
        elif self.target == "Single Video" and "list=" in self.url:
            opts['noplaylist'] = True

        return opts

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            pct = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            filename = os.path.basename(d.get('filename', ''))[:40]
            console.print(
                f"\r{filename:<40} | {pct:>6} | {speed:>10} | ETA: {eta}",
                end="", highlight=False
            )
        elif d['status'] == 'finished':
            console.print(f"\nFinished: {os.path.basename(d['filename'])[:50]}")

    def download(self):
        opts = self.build_opts()

        console.print(Panel(
            f"[bold]Mode:[/] {self.mode}\n"
            f"[bold]Quality:[/] {self.format_key}\n"
            f"[bold]Target:[/] {self.target}\n"
            f"[bold]Saving to:[/] {self.output_dir}",
            title="Download Summary", border_style="green"
        ))

        confirm = questionary.confirm("Start download?").ask()
        if not confirm:
            console.print("[yellow]Cancelled.[/]")
            return

        os.makedirs(self.output_dir, exist_ok=True)

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self.url])
            console.print("\n[bold green]All downloads completed successfully![/]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user.[/]")
        except Exception as e:
            console.print(f"\n[bold red]Error: {e}[/]")


if __name__ == "__main__":
    downloader = YTDownloader()
    downloader.gather_inputs()
    downloader.download()