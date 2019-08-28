# vid2img
Extract frames from a video. Keep it simple stupid.

# Extentions
- Worked
	+ mp4, 3gp, avi, flv, m4v, mov, mpeg, vob, mpg, mts, wmv
- NOT Worked
	+ webm, mkvm

# Requirements
```
pip install -r requirements.txt
```

# Usage
- usage
```
python vid2img.py [-h] [-o OUTDIR] [-i INTERVAL] [-e EXTENTION] [-p] path
```

- default
```
python vid2img.py path -o extracted -i 60 -e png
```

# Be careful
- If the code run in parallel, memory loads vid-size * cpu_cores of data because the threads cannot share cv2.VideoCapture object.
