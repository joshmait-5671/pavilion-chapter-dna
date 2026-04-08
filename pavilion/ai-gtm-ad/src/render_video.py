"""Capture HTML animation frame-by-frame and stitch into MP4 with ffmpeg."""

import os
import shutil
import subprocess
import tempfile

from playwright.sync_api import sync_playwright


# Path to local ffmpeg binary
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "..", "bin", "ffmpeg")


def capture_frames(html_path: str, output_dir: str, fps: int = 30, duration: int = 30, width: int = 1080, height: int = 1080):
    """Open HTML in headless Chromium, step through animation frame by frame, capture PNGs.

    Args:
        html_path: Absolute path to the injected HTML file
        output_dir: Directory to save frame PNGs
        fps: Frames per second
        duration: Total duration in seconds
        width: Viewport width
        height: Viewport height
    """
    total_frames = fps * duration

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page(viewport={"width": width, "height": height})

        # Load the HTML file
        file_url = f"file://{html_path}"
        page.goto(file_url, wait_until="networkidle")

        # Pause all animations at time 0
        page.evaluate("""() => {
            document.getAnimations().forEach(a => {
                a.pause();
                a.currentTime = 0;
            });
        }""")

        print(f"Capturing {total_frames} frames at {fps}fps...")

        for frame_num in range(total_frames):
            # Set animation time for this frame
            frame_time_ms = (frame_num / fps) * 1000
            page.evaluate(f"""() => {{
                document.getAnimations().forEach(a => {{
                    a.currentTime = {frame_time_ms};
                }});
            }}""")

            # Capture screenshot (clip to viewport for safety)
            frame_path = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
            page.screenshot(path=frame_path, clip={"x": 0, "y": 0, "width": width, "height": height})

            # Progress indicator every 5 seconds of video
            if frame_num % (fps * 5) == 0:
                seconds = frame_num // fps
                print(f"  {seconds}s / {duration}s captured")

        print(f"  {duration}s / {duration}s captured — done")
        browser.close()


def stitch_to_mp4(frames_dir: str, output_path: str, fps: int = 30):
    """Use ffmpeg to stitch PNG frames into an MP4.

    Args:
        frames_dir: Directory containing frame_NNNN.png files
        output_path: Where to write the MP4
        fps: Frames per second
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Use local ffmpeg binary
    ffmpeg = FFMPEG_PATH if os.path.exists(FFMPEG_PATH) else "ffmpeg"

    cmd = [
        ffmpeg, "-y",  # overwrite output
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",  # high quality
        output_path,
    ]

    print(f"Stitching MP4: {output_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}")
        raise RuntimeError("ffmpeg failed to create MP4")

    # File size info
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"MP4 created: {output_path} ({size_mb:.1f} MB)")


def render(html_path: str, output_mp4: str, fps: int = 30, duration: int = 30):
    """Full render pipeline: capture frames + stitch to MP4.

    Args:
        html_path: Absolute path to the injected HTML file
        output_mp4: Where to save the final MP4
        fps: Frames per second
        duration: Total video duration in seconds
    """
    # Create temp directory for frames
    frames_dir = tempfile.mkdtemp(prefix="chapter_pulse_frames_")

    try:
        capture_frames(html_path, frames_dir, fps, duration)
        stitch_to_mp4(frames_dir, output_mp4, fps)

    finally:
        # Clean up temp frames
        shutil.rmtree(frames_dir, ignore_errors=True)
        print("Temp frames cleaned up.")
