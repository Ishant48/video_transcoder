import os
import sys
import subprocess


# Detect if the input video file is HDR by using ffprobe to analyze the video stream.
def detect_hdr(input_file):
    try:
        # Using ffprobe command to probe the input file
        cmd = ['ffprobe', '-show_streams', '-select_streams', 'v:0', '-of', 'default=noprint_wrappers=1:nokey=1', '-v', 'error', input_file]
        output = subprocess.check_output(cmd).decode().strip()
        # Checking HDR indicators in the output
        return 'color_range=pc' in output or 'color_space=bt2020' in output
    except subprocess.CalledProcessError as e:
        print(f"Error detecting HDR: {e}")
        return False

# Transcode the input video to specified resolution and add an overlay(circle).
def transcode_video(input_file, output_prefix, resolution, is_hdr=False):
    width, height = resolution
    # Get the original file extension
    _, ext = os.path.splitext(input_file)
    output_file = f"{output_prefix}_{height}p{ext}"

    try:
        circle_radius = int(height * 0.07) if is_hdr else int(height * 0.05)
        font_color = 'green' if is_hdr else 'white'
        x_position = width - circle_radius
        y_position = circle_radius if is_hdr else height - circle_radius

        cmd = [
            'ffmpeg', '-i', input_file, '-vf',
            f'scale={width}:{height},drawtext=text=◯:fontcolor={font_color}:fontsize={circle_radius * 2}:x={x_position - circle_radius}:y={y_position - circle_radius}',
            '-c:v', 'libx265', '-preset', 'fast', '-crf', '28', '-y', output_file
        ]
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error transcoding video: {e}")

    return output_file

# In this transcoded video file convereted into DASH format using mp4fragment and mp4dash.
def package_dash(input_file, output_dir):
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Get the original file extension
        _, ext = os.path.splitext(input_file)
        # Fragment the input file
        fragmented_file = os.path.join(output_dir, f'fragmented{ext}')
        cmd_fragment = ['mp4fragment', '--fragment-duration', '7000', input_file, fragmented_file]
        subprocess.run(cmd_fragment, check=True)
         # Set up the output directory for DASH
        mpd_output_dir = os.path.join(output_dir, 'dash_output')
        mpdOut = mpd_output_dir
        mpd_file = os.path.join(mpdOut, 'output.mpd')

        # Inpuit file for mp4dash command
        fragIn = fragmented_file
        # Construct the mp4dash command
        cmd_mp4dash = ['mp4dash', '--output-dir', mpdOut, '--mpd-name', 'output.mpd', fragIn]
        print(f"Running mp4dash command: {cmd_mp4dash}")
        subprocess.run(cmd_mp4dash, check=True,shell=True)

    except subprocess.CalledProcessError as e:
        print(f"Error in DASH packaging: {e}")
    except Exception as ex:
        print(f"Unexpected error occurred: {ex}")


# Main function to handle the overall process: detecting HDR, transcoding, and packaging.
def main(input_file):
    resolutions = [(640, 360), (854, 480), (1280, 720), (1920, 1080)]
    output_dir = "output_videos"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' does not exist.")
        sys.exit(1)
    # Detect if the video is HDR
    is_hdr = detect_hdr(input_file)
    # Define the output prefix based on HDR status
    output_prefix = f"{output_dir}/output_hdr" if is_hdr else f"{output_dir}/output_sdr"

    if is_hdr:
        # For HDR videos, create both HDR and SDR variants
        for width, height in resolutions:
            output_file = transcode_video(input_file, output_prefix, (width, height), is_hdr=is_hdr)
            package_dash(output_file, f"{output_dir}/dash_hdr_{height}p", 'video_hdr.mpd')

        for width, height in resolutions:
            output_file_sdr = transcode_video(input_file, f"{output_dir}/output_sdr", (width, height), is_hdr=False)
            package_dash(output_file_sdr, f"{output_dir}/dash_sdr_{height}p")
    else:
        # For SDR videos, create only one variant
        for width, height in resolutions:
            output_file = transcode_video(input_file, output_prefix, (width, height), is_hdr=is_hdr)
            package_dash(output_file, f"{output_dir}/dash_sdr_{height}p")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcode.py <path_to_video_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    main(input_file)
