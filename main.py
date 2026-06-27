import argparse
import time
import json
import os
from pathlib import Path

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()

# Import the Google GenAI SDK and yt-dlp
from google import genai
from google.genai import types
import yt_dlp

# --- Markdown Template ---
README_TEMPLATE = """# {title}

> **Source:** [Original Reel]({source_url}) | **Estimated Cost:** ~${cost} | **Added:** {date_added}

## 📝 Overview
{description}

---

## 🛒 Bill of Materials (BOM)

| Component | Est. Price | Link |
| :--- | :--- | :--- |
{bom_table}

---

## 🗓️ Proposed Timeline
* **Day 1:** Sourcing & Setup - Order parts and organize workspace.
* **Day 2:** Dry Assembly - Prototype the build without final adhesives or soldering.
* **Day 3:** Final Integration - Assemble, code, and test.

---

## 🛠️ Build Guide
*(AI generated steps will be populated here in V2)*
"""

# --- Processing Functions ---

def download_video(url: str) -> str:
    """Downloads the video natively using yt-dlp to a temporary file."""
    output_filename = "temp_video.mp4"
    print(f"📥 Downloading video from: {url}")
    
    # Configure yt-dlp to grab the best mp4 format quietly
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_filename
    except Exception as e:
        raise RuntimeError(f"Failed to download video: {e}")

def real_ai_extraction(video_path: str, url: str) -> dict:
    """Uploads a video to Gemini and extracts a structured BOM using the new SDK."""
    if "GEMINI_API_KEY" not in os.environ:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Check your .env file.")
    
    client = genai.Client()

    print(f"📤 Uploading video ({video_path}) to Gemini...")
    video_file = client.files.upload(file=video_path)
    
    while video_file.state.name == "PROCESSING":
        print("⏳ Waiting for Google's servers to process the video...")
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)
        
    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed on Google's end.")

    print("🧠 Analyzing video frames and extracting components...")
    
    prompt = """
    You are an expert hardware and software engineer. Watch this video of a DIY project.
    Extract the components being used and output the data STRICTLY as a JSON object with this exact schema:
    {
        "title": "A catchy title for the project",
        "cost": "Estimated total cost in USD (just the number, e.g., 45.00)",
        "description": "A 2-sentence overview of what is being built",
        "components": [
            {
                "name": "Specific component name",
                "price": "Estimated price in USD (just the number)",
                "link": "A generic search URL for the item (e.g., https://amazon.com/s?k=component+name)"
            }
        ]
    }
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[video_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    
    # Clean up Google's servers
    client.files.delete(name=video_file.name)

    extracted_data = json.loads(response.text)
    extracted_data["source_url"] = url
    extracted_data["date_added"] = time.strftime("%Y-%m-%d")
    
    return extracted_data

def generate_project_docs(data: dict):
    """Creates the directory and the README.md file based on the extracted data."""
    dir_name = data["title"].lower().replace(" ", "-")
    out_path = Path("vault") / dir_name

    print(f"📂 Creating project directory: {out_path}")
    out_path.mkdir(parents=True, exist_ok=True)

    bom_table = "\n".join(
        [f"| {c['name']} | ${c['price']} | [Buy/Source]({c['link']}) |" for c in data["components"]]
    )

    readme_content = README_TEMPLATE.format(
        title=data["title"],
        source_url=data["source_url"],
        cost=data["cost"],
        date_added=data["date_added"],
        description=data["description"],
        bom_table=bom_table
    )

    readme_path = out_path / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

# --- CLI Entrypoint ---

# --- CLI Entrypoint ---

def main():
    parser = argparse.ArgumentParser(description="Projectify: Turn Reels into Markdown Projects")
    parser.add_argument("--url", required=True, help="The original Reel URL")
    args = parser.parse_args()

    print(f"🚀 Starting Projectify pipeline...")
    temp_video_path = None

    try:
        # 1. Download
        temp_video_path = download_video(args.url)
        
        # 2. Extract
        project_data = real_ai_extraction(temp_video_path, args.url)
        
        # 3. Generate Docs
        generate_project_docs(project_data)
        
        print("✅ Success! Project successfully added to your vault.")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        
    finally:
        # 4. Clean up the local hard drive
        if temp_video_path and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
            print("🧹 Cleaned up temporary video file.")

if __name__ == "__main__":
    main()
