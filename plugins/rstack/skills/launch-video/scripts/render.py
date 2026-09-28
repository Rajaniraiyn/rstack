#!/usr/bin/env python3
"""Render a time-driven HTML page to stills, a contact sheet, or an H.264 video.

The page must define `window.render(t)` (a pure function of time in seconds)
and `window.ready` (a promise that resolves once fonts and images have
loaded). Chrome runs headless and is driven over the DevTools protocol with a
small stdlib WebSocket client, so there are no Python dependencies. Video and
contact sheets are encoded by ffmpeg.

Examples:
  python render.py stills page.html 0.5 2.0 4.2 --size 1080x1920 --out stills
  python render.py sheet page.html 0.5 2 4 6 8 10 --cols 3 --out sheet.jpg
  python render.py video page.html --duration 22.5 --fps 30 --out video-only.mp4
  python render.py video page.html --query "?p=tg" --size 1080x1920 --out tg.mp4
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import platform
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------- tools


def find_chrome() -> str:
    env = os.environ.get("CHROME")
    if env:
        return env
    candidates = {
        "Darwin": [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ],
        "Windows": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ],
    }.get(platform.system(), [])
    for path in candidates:
        if Path(path).exists():
            return path
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("Chrome/Chromium not found. Install it or set CHROME=/path/to/chrome.")


def find_ffmpeg() -> str:
    found = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if found:
        return found
    sys.exit(
        "ffmpeg not found. Install it (brew install ffmpeg, apt install ffmpeg, winget install ffmpeg), "
        "or set FFMPEG=/path/to/ffmpeg (for example the binary from the npm package ffmpeg-static)."
    )


# ---------------------------------------------------------------- websocket


class WebSocket:
    """Minimal RFC 6455 client: text frames, client masking, fragmentation."""

    def __init__(self, url: str):
        assert url.startswith("ws://"), url
        hostport, _, path = url[5:].partition("/")
        host, _, port = hostport.partition(":")
        self.sock = socket.create_connection((host, int(port or 80)))
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("WebSocket handshake failed")
            response += chunk
        if b" 101 " not in response.split(b"\r\n", 1)[0]:
            raise ConnectionError(response.decode(errors="replace"))
        self.buffer = response.split(b"\r\n\r\n", 1)[1]

    def _read(self, n: int) -> bytes:
        while len(self.buffer) < n:
            chunk = self.sock.recv(max(65536, n - len(self.buffer)))
            if not chunk:
                raise ConnectionError("WebSocket closed")
            self.buffer += chunk
        data, self.buffer = self.buffer[:n], self.buffer[n:]
        return data

    def send(self, text: str) -> None:
        payload = text.encode()
        header = bytearray([0x81])
        n = len(payload)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)

    def recv(self) -> str:
        message = b""
        while True:
            b1, b2 = self._read(2)
            opcode, n = b1 & 0x0F, b2 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            mask = self._read(4) if b2 & 0x80 else None
            data = self._read(n)
            if mask:
                data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
            if opcode == 0x8:
                raise ConnectionError("WebSocket closed by browser")
            if opcode == 0x9:  # ping -> pong
                continue
            message += data
            if b1 & 0x80:
                return message.decode()


class Browser:
    def __init__(self, width: int, height: int):
        self.profile = tempfile.mkdtemp(prefix="render-chrome-")
        args = [
            find_chrome(), "--headless=new", "--remote-debugging-port=0", f"--user-data-dir={self.profile}",
            "--hide-scrollbars", "--mute-audio", "--no-first-run", "--no-default-browser-check",
            "--allow-file-access-from-files", "--font-render-hinting=none", "--force-device-scale-factor=1",
            f"--window-size={width},{height}", "about:blank",
        ]
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        port_file = Path(self.profile) / "DevToolsActivePort"
        for _ in range(200):
            if port_file.exists() and port_file.read_text().strip():
                break
            time.sleep(0.05)
        else:
            raise RuntimeError("Chrome did not start (no DevToolsActivePort)")
        port = port_file.read_text().split()[0]
        for _ in range(100):
            try:
                targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list"))
                page = next(t for t in targets if t.get("type") == "page")
                break
            except (OSError, StopIteration):
                time.sleep(0.05)
        self.ws = WebSocket(page["webSocketDebuggerUrl"])
        self.next_id = 0
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=1, mobile=False)

    def call(self, method: str, **params):
        self.next_id += 1
        self.ws.send(json.dumps({"id": self.next_id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.next_id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def evaluate(self, expression: str, await_promise: bool = False):
        result = self.call("Runtime.evaluate", expression=expression, awaitPromise=await_promise, returnByValue=True)
        if "exceptionDetails" in result:
            raise RuntimeError(f"Page error in `{expression[:60]}`: {result['exceptionDetails'].get('exception', {}).get('description', result['exceptionDetails'])}")
        return result.get("result", {}).get("value")

    def open(self, url: str) -> None:
        self.call("Page.enable")
        self.call("Page.navigate", url=url)
        for _ in range(400):
            if self.evaluate("document.readyState") == "complete":
                break
            time.sleep(0.05)
        if not self.evaluate("typeof window.render === 'function'"):
            raise RuntimeError("The page must define window.render(t)")
        self.evaluate("Promise.resolve(window.ready)", await_promise=True)

    def frame(self, t: float, quality: int = 95) -> bytes:
        self.evaluate(f"window.render({t!r})")
        self.evaluate("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))", await_promise=True)
        shot = self.call("Page.captureScreenshot", format="jpeg", quality=quality)
        return base64.b64decode(shot["data"])

    def close(self) -> None:
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


# ---------------------------------------------------------------- commands


def page_url(page: str, query: str) -> str:
    return Path(page).resolve().as_uri() + (query or "")


def cmd_stills(args, browser):
    out = Path(args.out or "stills")
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for t in args.times:
        path = out / f"t{t:06.2f}.jpg"
        path.write_bytes(browser.frame(t))
        paths.append(path)
        print(path)
    return paths


def cmd_sheet(args, browser):
    tmp = Path(tempfile.mkdtemp(prefix="sheet-"))
    frames = []
    for i, t in enumerate(args.times):
        path = tmp / f"f{i:03d}.jpg"
        path.write_bytes(browser.frame(t))
        frames.append(path)
    cols = args.cols
    rows = -(-len(frames) // cols)
    thumb = args.thumb
    ffmpeg = find_ffmpeg()
    subprocess.run([
        ffmpeg, "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "f%03d.jpg"),
        "-vf", f"scale={thumb}:-1,tile={cols}x{rows}:padding=4:color=black", "-frames:v", "1", args.out or "sheet.jpg",
    ], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(args.out or "sheet.jpg")


def cmd_video(args, browser):
    ffmpeg = find_ffmpeg()
    out = args.out or "video-only.mp4"
    frames = round(args.duration * args.fps)
    enc = subprocess.Popen([
        ffmpeg, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(args.fps), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(args.crf), "-preset", "slow", out,
    ], stdin=subprocess.PIPE)
    start = time.time()
    for f in range(frames):
        enc.stdin.write(browser.frame(f / args.fps))
        if f % max(1, args.fps * 2) == 0:
            done = (f + 1) / frames
            eta = (time.time() - start) / done * (1 - done)
            print(f"\rframe {f + 1}/{frames}  eta {eta:4.0f}s", end="", file=sys.stderr, flush=True)
    enc.stdin.close()
    if enc.wait() != 0:
        sys.exit("ffmpeg failed while encoding")
    print(f"\n{out}", file=sys.stderr)
    print(out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["stills", "sheet", "video"])
    p.add_argument("page", help="HTML file defining window.render(t) and window.ready")
    p.add_argument("times", nargs="*", type=float, help="times in seconds (stills, sheet)")
    p.add_argument("--size", default="1920x1080", help="WIDTHxHEIGHT (default 1920x1080)")
    p.add_argument("--query", default="", help='appended to the file URL, e.g. "?p=wa"')
    p.add_argument("--out")
    p.add_argument("--duration", type=float, default=20.0)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--crf", type=int, default=15, help="intermediate quality; the deliver step re-encodes")
    p.add_argument("--cols", type=int, default=4)
    p.add_argument("--thumb", type=int, default=480, help="thumbnail width in a contact sheet")
    args = p.parse_args()
    if args.mode != "video" and not args.times:
        p.error("give one or more times in seconds")
    width, height = (int(v) for v in args.size.lower().split("x"))
    browser = Browser(width, height)
    try:
        browser.open(page_url(args.page, args.query))
        {"stills": cmd_stills, "sheet": cmd_sheet, "video": cmd_video}[args.mode](args, browser)
    finally:
        browser.close()


if __name__ == "__main__":
    main()
