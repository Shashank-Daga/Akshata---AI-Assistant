import os
from datetime import datetime, timedelta

# Folders to track for recent file activity
TRACKED_FOLDERS = [
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    "D:/College"  # Add more folders here as needed
]


def get_recent_files(within_hours=24, max_results=10):
    now = datetime.now()
    cutoff = now - timedelta(hours=within_hours)
    recent_files = []

    for folder in TRACKED_FOLDERS:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if mtime >= cutoff:
                        recent_files.append((filepath, mtime))
                except Exception:
                    continue

    if not recent_files:
        return f"No files modified in the last {within_hours} hours."

    # Sort by actual datetime object (mtime)
    recent_files.sort(key=lambda x: x[1], reverse=True)

    return "\n".join(
        [f"{os.path.basename(path)} - Modified: {mtime.strftime('%Y-%m-%d %H:%M')}"
         for path, mtime in recent_files[:max_results]]
    )


# Example usage
if __name__ == "__main__":
    print(get_recent_files(within_hours=24))
