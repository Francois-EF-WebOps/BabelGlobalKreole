"""Safety tests for the explicitly gated TikTok inbox CLI."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "tiktok_inbox_publish.py"


def run_cli(*args, env_updates=None):
    env = {key: value for key, value in os.environ.items() if key not in {
        "TIKTOK_ACCESS_TOKEN", "PUBLISHING_ENABLED", "TIKTOK_INBOX_UPLOAD_ENABLED",
        "TIKTOK_VERIFIED_VIDEO_HOSTS"
    }}
    env.update(env_updates or {})
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT, env=env, text=True, capture_output=True, check=False
    )


def test_missing_token_blocks_before_network():
    result = run_cli("--video-url", "https://media.example.test/video.mp4")
    assert result.returncode == 2
    assert "TIKTOK_ACCESS_TOKEN" in result.stderr


def test_explicit_upload_gates_are_required():
    result = run_cli(
        "--video-url", "https://media.example.test/video.mp4",
        env_updates={"TIKTOK_ACCESS_TOKEN": "test-only-token"}
    )
    assert result.returncode == 1
    assert "PUBLISHING_ENABLED" in result.stderr


def test_unverified_host_is_blocked_before_network():
    result = run_cli(
        "--video-url", "https://media.example.test/video.mp4",
        env_updates={
            "TIKTOK_ACCESS_TOKEN": "test-only-token",
            "PUBLISHING_ENABLED": "true",
            "TIKTOK_INBOX_UPLOAD_ENABLED": "true",
            "TIKTOK_VERIFIED_VIDEO_HOSTS": "verified.example.test",
        }
    )
    assert result.returncode == 1
    assert "not in TIKTOK_VERIFIED_VIDEO_HOSTS" in result.stderr
