# Video Edition Functions

This project provides a Python script to add a watermark to a video. It uses OpenCV for video processing and requires FFmpeg for audio remuxing.

## Features

- Adds a watermark to the bottom-right corner of a video.
- Automatically scales the watermark to a fraction of the video width.
- Retains the original audio by remuxing it into the output video.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- FFmpeg (must be available in your system's PATH)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/video-edition-functions.git
   cd video-edition-functions
   ```
2. Install the required Python packages:
   ```sh
   pip install opencv-python numpy
   ```
3. Ensure FFmpeg is installed and available in your system's PATH. You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html).
4. Make sure to have the `ffmpeg-python` package installed:
   ```sh
   pip install ffmpeg-python
   ```

## Usage
1. Run the script with the following command:

    ```sh
    python watermark.py input.mp4 watermark.png output.mp4
    ```
   Replace `input.mp4` with the path to your input video, `watermark.png` with the path to your watermark image, and `output.mp4` with the desired output video file name.
2. The script will process the video, add the watermark, and save the output video with the original audio.
3. The watermark will be scaled to 10% of the video width and positioned at the bottom-right corner.
4. The output video will be saved in the same directory as the input video.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

