# mission-pinball-docker
Example Mission Pinball Framework game (demo_man) with Dockerfile that should work across MPF games.

All you need from this repo if you want this on your own game is the `Dockerfile`. 

Please note that there may be other issues with dependencies that this project doesn't account for (e.g. P3-ROC vs. FAST)
or if you're doing weird stuff with your code that doesn't follow current MPF best practices.

Currently built to support the latest supported versions of the underlying components:
- Ubuntu v22.04 LTS
- Python v3.11 (latest version supported by MPF v0.57)
- MPF v0.57