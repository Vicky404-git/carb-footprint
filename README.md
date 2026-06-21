# 🌱 carb-trak

A fast, containerized desktop application for tracking daily carbon footprints. Built for privacy, speed, and faceless deployment.

## Features
- **Frutiger Aero UI**: A clean, nostalgic interface with fully adjustable background blur.
- **Local-First Architecture**: Saves all logs completely offline using local database transactions—no data ever leaves your device.
- **Auto-Browser Binding**: Spawns an internal routine that triggers your default system browser instantly upon launch.

## Quick Start (Pre-compiled Binary)
1. Head to the **Releases** section on GitHub.
2. Download the compiled native binary for your platform.
3. Grant execution permissions and run it:
```bash
   chmod +x carb-trak
   ./carb-trak```

## Development 
If you prefer running the raw environment locally using uv:
```bash
uv run pytest test_app.py -v
uv run python app.py```

```
