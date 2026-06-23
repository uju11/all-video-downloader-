import yt_dlp
import os

def download_video(url, output_directory='downloads'):
    """
    Downloads a video from the provided URL.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Configuration options for yt-dlp
    ydl_opts = {
        # Save file as: downloads/Title_of_video.extension
        'outtmpl': f'{output_directory}/%(title)s.%(ext)s',
        
        # 'best' gets the best single file with both video and audio.
        # Alternatively, 'bestvideo+bestaudio/best' gets the absolute highest quality 
        # but requires FFmpeg installed on your system to merge them.
        'format': 'best', 
        
        # Prevents downloading entire playlists if you only want the single video
        'noplaylist': True,
        
        # Print progress to the console
        'quiet': False, 
    }

    try:
        print(f"\nAnalyzing link: {url}s")
        print("Please wait, download starting soon...\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print("\n✅ Download completed successfully!")
        print(f"Check the '{output_directory}' folder for your video.")
        
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Failed to download the video. It might be private or unsupported.")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("--- Python Video Downloader ---")
    video_link = input("Enter the video URL: ").strip()
    
    if video_link:
        download_video(video_link)
    else:
        print("No URL provided. Exiting.")