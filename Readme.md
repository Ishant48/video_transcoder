# Video Transcoding and DASH Packaging

This project involves video transcoding and Dynamic Adaptive Streaming over HTTP (DASH) packaging using FFmpeg and Bento4 tools. The script detects if the input video is HDR or SDR, transcodes it to multiple resolutions, and packages the output files into DASH format.

## Prerequisites

Before running the script, ensure you have the following tools installed on your system:

- **Python 3.12.3**
- **FFmpeg** (place the binaries in the `FFMPEG` folder)
- **Bento4** (`mp4fragment` and `mp4dash` binaries in the `BENTO4` folder)


## Folder Structure

- `FFMPEG`: For installation purpose.
- `BENTO4`: For installation purpose.
- `input.mp4`: Sample input file with SDR quality for testing.

## Installation and Setup

### Windows

1. **Installtion of FFmpeg:**
   - Place this folder in C Drive

2. **Installtion of Bento4:**
   - Place this folder in C Drive

3. **Update System Path:**
   - Add the `FFMPEG` and `BENTO4` folders to your system PATH environment variable.
   - Go to `Control Panel > System and Security > System > Advanced system settings`.
   - Click on `Environment Variables`, find the `Path` variable, and add the path of bin folder to the `FFMPEG` and `BENTO4` folders.

### Linux

1. **Update System Path:**
   - Open your `.bashrc` or `.profile` file and add the following lines:
     ```sh
     export PATH=$PATH:/path/to/FFMPEG
     export PATH=$PATH:/path/to/BENTO4
     ```
   - Source the file to update the PATH:
     ```sh
     source ~/.bashrc
     ```

## Running the Script

1. Place the `input.mp4` file in the same directory as the script.

2. Open a terminal or command prompt and navigate to the script's directory.

3. Run the script:
   ```sh
   python transcode.py input.mp4
