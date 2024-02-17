from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_transcript(video_id):
    try:
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Initialize the text formatter
        formatter = TextFormatter()
        # Format the transcript into plain text
        text_transcript = formatter.format_transcript(transcript)
        
        # Return the formatted transcript
        return text_transcript
    except Exception as e:
        return str(e)

# Example usage
video_id = 'GwaPwLrqwis?si=teCd_a0POkLPL77H' # Replace 'YOUR_VIDEO_ID_HERE' with the actual video ID
transcript = extract_transcript(video_id)
print(transcript)