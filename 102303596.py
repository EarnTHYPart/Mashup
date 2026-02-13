import sys
import os
from pytubefix import Search
from moviepy.editor import AudioFileClip, concatenate_audioclips

def create_mashup(singer, n, duration, output_file):
    # Check if N > 10
    if n <= 10:
        print("Error: Number of videos (N) must be greater than 10.") # [cite: 25]
        return
    if duration <= 20:
        print("Error: Duration must be greater than 20 seconds.")
        return

    try: 
        print(f"Searching for {n} videos of {singer}...")
        search = Search(singer)
        videos = search.videos[:n]
        
        clips = []
        temp_audio_files = []
        for i, v in enumerate(videos): 
            print(f"Downloading & Processing {i+1}/{n}...")
            # Download audio
            st = v.streams.get_audio_only()
            temp = st.download(filename=f"temp_{i}.mp4")
            
            # Cut first Y seconds
            audio_clip = AudioFileClip(temp)
            clip = audio_clip.subclip(0, duration)
            
            # Write subclip to temp audio file to avoid file locking
            temp_audio = f"temp_audio_{i}.mp3"
            clip.write_audiofile(temp_audio, verbose=False, logger=None)
            clips.append(AudioFileClip(temp_audio))
            temp_audio_files.append(temp_audio)
            
            # Close and remove temp files
            audio_clip.close()
            clip.close()
            os.remove(temp)

        if clips:
            print("Merging into one file...")
            final = concatenate_audioclips(clips)
            final.write_audiofile(output_file)
            
            # Close clips and remove temp audio files
            for c in clips: 
                c.close()
            final.close()
            for temp_file in temp_audio_files:
                os.remove(temp_file)
            print(f"Mashup Done! File saved as: {output_file}")
            
    except Exception as e: 
        print(f"An error occurred: {e}") # 

if __name__ == "__main__": 
    # Command line usage check [cite: 21, 22, 24]
    if len(sys.argv) != 5: 
        print("Usage: python 102303724.py <SingerName> <N> <Y> <OutputName>") # [cite: 22]
    else: 
        create_mashup(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])