import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg and ffprobe")
class VideoDeliveryTests(unittest.TestCase):
    def test_png_poster_exports_jpeg_without_changing_timeline(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            def ffmpeg(*args):
                subprocess.run(["ffmpeg", "-v", "error", *args], check=True, capture_output=True)

            ffmpeg("-f", "lavfi", "-i", "color=c=blue:s=320x180:r=30:d=1",
                   "-c:v", "libx264", str(work / "silent.mp4"))
            ffmpeg("-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                   str(work / "audio.wav"))
            ffmpeg("-f", "lavfi", "-i", "color=c=red:s=320x180", "-frames:v", "1",
                   str(work / "poster.png"))
            output = work / "cut/video.mp4"
            subprocess.run([
                sys.executable, str(ROOT / "plugins/rstack/skills/launch-video/scripts/deliver.py"),
                "--video", str(work / "silent.mp4"), "--audio", str(work / "audio.wav"),
                "--poster", str(work / "poster.png"), "--out", str(output),
            ], check=True, capture_output=True)
            probe = subprocess.check_output([
                "ffprobe", "-v", "error", "-show_streams", "-of", "json", str(output)])
            streams = json.loads(probe)["streams"]
            video = next(stream for stream in streams if stream["codec_type"] == "video")
            self.assertEqual((video["width"], video["height"]), (320, 180))
            self.assertEqual(video["r_frame_rate"], "30/1")
            self.assertEqual(int(video["nb_frames"]), 30)
            self.assertAlmostEqual(float(video["duration"]), 1, places=2)
            self.assertTrue(any(stream["codec_type"] == "audio" for stream in streams))
            poster = output.parent / "poster.jpg"
            self.assertTrue(poster.read_bytes().startswith(b"\xff\xd8\xff"))
            # The exported poster is the delivered red opening frame, not the original blue video.
            pixel = subprocess.check_output([
                "ffmpeg", "-v", "error", "-i", str(poster), "-vf", "scale=1:1",
                "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
            self.assertGreater(pixel[0], 200)
            self.assertLess(pixel[1], 40)
            self.assertLess(pixel[2], 40)


if __name__ == "__main__":
    unittest.main()
