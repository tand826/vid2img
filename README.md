# vid2img
Extract frames from a video. Keep it simple stupid.

# Requirements
```bash: Requirements
pip install -r requirements.txt
```

# Usage
```bash: Usage
python vid2img.py [-h] [-o OUTDIR] [-i INTERVAL] [-e EXTENTION] [-p] path
```

# Be careful
- If the code run in parallel, memory loads vid-size * cpu_cores of data because the threads cannot share cv2.VideoCapture object.