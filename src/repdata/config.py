from pathlib import Path

# Default location to save synced files
GSYNC_DPATH = Path("/tmp/gsync")


def get_sync_dir() -> Path:
    GSYNC_DPATH.mkdir(parents=True, exist_ok=True)
    return GSYNC_DPATH
