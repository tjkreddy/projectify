
# 🛠️ Projectify

Turn passive doom-scrolling into an actionable engineering backlog. 

Projectify is an automated CLI pipeline that ingests short-form DIY videos (Instagram Reels, TikToks, YouTube Shorts), uses Google's Gemini 2.5 Flash Multimodal AI to extract a Bill of Materials (BOM), and generates a structured, Obsidian-ready Markdown document.

## 🚀 Features
* **Automated Ingestion:** Downloads videos natively via `yt-dlp`.
* **AI Vision Parsing:** Uses Gemini to identify electronic components, hardware, and materials from video frames.
* **Structured Output:** Automatically generates YAML-frontmatter heavy `.md` files perfect for PKM vaults like Obsidian or Notion.

## ⚙️ Setup & Installation

**1. Clone the repository:**

```bash
git clone https://github.com/tjkreddy/projectify.git
cd projectify

```

**2. Create a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate

```

**3. Install dependencies:**

```bash
pip install -r requirements.txt

```

**4. Environment Variables:**

Create a `.env` file in the root directory and add your Google Gemini API Key:

```env
GEMINI_API_KEY="your_api_key_here"

```

## 💻 Usage

Pass any valid video URL to the CLI:

```bash
python main.py --url="https://instagram.com/reel/YOUR_LINK"

```

The script will download the video, process it, generate a new project folder in the `vault/` directory, and clean up the temporary video files.

```

### Step 3: Save and Push
Save it (`Ctrl + O`, `Enter`, `Ctrl + X`), then push the fix:

```bash
git add README.md
git commit -m "fix: force empty lines for github markdown parser"
git push origin master

```

