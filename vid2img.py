import os
import argparse
from pathlib import Path
import cv2
from joblib import Parallel, delayed


class Vid2Img:

    def __init__(self, path, outdir, interval):
        self.path = path
        self.outdir = outdir
        self.interval = interval
        self.cores = os.cpu_count()
        self.make_outdir()
        self.read_vid()

    def make_outdir(self):
        if not self.outdir:
            self.outdir = Path(self.path.stem)
        if not self.outdir.exists():
            self.outdir.mkdir(exist_ok=True, parents=True)

    def read_vid(self):
        vid = cv2.VideoCapture(str(self.path))
        self.cnt = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    def save_frames(self, parallel):
        if parallel:
            self.set_positions()
            proc = [delayed(self.save_block)(self.get_block(core)) for core in range(self.cores)]
            Parallel(n_jobs=self.cores, backend='threading', verbose=1)(proc)
        else:
            vid = cv2.VideoCapture(str(self.path))
            self.save_block(vid)

    def set_positions(self):
        self.one_block = self.cnt // (self.cores-1)
        self.positions = list(range(0, self.cnt, self.one_block))

    def get_block(self, i):
        vid = cv2.VideoCapture(str(self.path))
        start = self.positions[i]
        vid.set(cv2.CAP_PROP_POS_FRAMES, start)
        return vid

    def save_block(self, vid):
        for idx in range(self.one_block):
            frame_cnt = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_cnt % self.interval == 0:
                ret, frame = vid.read()
                if ret:
                    cv2.imwrite(f"{Path(self.outdir)/str(frame_cnt)}.png", frame)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path,
                        help="Path to the input video.")
    parser.add_argument("-o", "--outdir", type=Path,
                        help="Directory to save the frames.")
    parser.add_argument("-i", "--interval", type=int, default=60,
                        help="Interval between the frames to save.")
    parser.add_argument("-e", "--extention", type=str, default="png",
                        help="Extension to save frames as.")
    parser.add_argument("-p", "--parallel", default=False, action='store_true',
                        help="Run the extraction in parallel.")
    args = parser.parse_args()

    vi = Vid2Img(args.path, args.outdir, args.interval)
    vi.save_frames(args.parallel)
