import cv2
import numpy as np
import sys
import os
import subprocess

def crop_transparent_border(rgba_img):
    alpha = rgba_img[..., 3]
    ys, xs = np.where(alpha > 0)
    if xs.size == 0 or ys.size == 0:
        return rgba_img
    x1, x2 = xs.min(), xs.max() + 1
    y1, y2 = ys.min(), ys.max() + 1
    return rgba_img[y1:y2, x1:x2]

def add_watermark(input_video, watermark_png, temp_video, margin=10, wm_frac=0.15):
    # — load & ensure alpha
    wm = cv2.imread(watermark_png, cv2.IMREAD_UNCHANGED)
    if wm is None:
        raise FileNotFoundError(f"Can't load '{watermark_png}'")
    if wm.shape[2] == 3:
        wm = cv2.cvtColor(wm, cv2.COLOR_BGR2BGRA)

    # — crop
    wm = crop_transparent_border(wm)
    h0, w0 = wm.shape[:2]

    # — open video
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        raise FileNotFoundError(f"Can't open '{input_video}'")
    fps    = cap.get(cv2.CAP_PROP_FPS)
    W      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Video: {W}×{H} @ {fps:.2f}FPS")

    # — scale watermark to wm_frac of video width
    target_w = int(W * wm_frac)
    scale = target_w / w0
    if scale != 1.0:
        new_w = target_w
        new_h = int(h0 * scale)
        wm = cv2.resize(wm, (new_w, new_h), interpolation=cv2.INTER_AREA)
    wm_h, wm_w = wm.shape[:2]
    print(f"Watermark scaled to {wm_w}×{wm_h}")

    # — prepare writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, fps, (W, H))
    if not out.isOpened():
        raise RuntimeError(f"Can't write '{temp_video}'")

    wm_bgr   = wm[...,:3].astype(np.uint8)
    wm_alpha = (wm[...,3:] / 255.0).astype(np.float32)

    # — blend each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # bottom-right coords
        x2 = W  - margin
        x1 = x2 - wm_w
        y2 = H  - margin
        y1 = y2 - wm_h

        roi = frame[y1:y2, x1:x2]
        blended = (wm_alpha * wm_bgr + (1.0 - wm_alpha) * roi).astype(np.uint8)
        frame[y1:y2, x1:x2] = blended
        out.write(frame)

    cap.release()
    out.release()
    print("✓ Video (no audio) written to", temp_video)

def remux_audio(video_no_audio, original_video, final_output):
    # requires ffmpeg on your PATH
    cmd = [
        'ffmpeg', '-y',
        '-i',  video_no_audio,
        '-i',  original_video,
        '-c',  'copy',
        '-map', '0:v:0',
        '-map', '1:a:0',
        final_output
    ]
    print("…running ffmpeg to re-attach audio")
    subprocess.run(cmd, check=True)
    print("✓ Final video with audio at", final_output)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python watermark.py input.mp4 watermark.png output.mp4")
        sys.exit(1)

    inp, logo, out = sys.argv[1:]
    temp = ".__wm_temp__.mp4"

    add_watermark(inp, logo, temp,
                  margin=35,    # pixels from edges
                  wm_frac=0.205) # watermark width = 15% of video width

    remux_audio(temp, inp, out)
    os.remove(temp)
    print("All done!")
