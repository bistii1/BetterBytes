from sync import generate_lip_sync

def main():
    # Replace these with actual values
    input_video_url = "https://lfldehquopamazavycth.supabase.co/storage/v1/object/public/sync-public/david_demo_shortvid.mp4?t=2023-10-12T08%3A14%3A44.537Z"
    script_text = "Hello, nice to meet you!"
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Example voice ID

    # Run the function
    output_video_url = generate_lip_sync(voice_id, script_text, input_video_url)

    # Print the final output
    if output_video_url:
        print("Final Output Video URL:", output_video_url)
    else:
        print("Failed to generate lip-sync video.")

if __name__ == "__main__":
    main()
