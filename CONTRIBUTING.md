# Contributing to Projectify

First off, thank you for considering contributing to Projectify! It's people like you that make open-source tools great.

## 🛠️ Local Development Setup

To set up the project locally for development:

**1. Fork and clone the repository:**

```bash
git clone [https://github.com/YOUR_USERNAME/projectify.git](https://github.com/YOUR_USERNAME/projectify.git)
cd projectify
2. Create an isolated virtual environment:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install the dependencies:

Bash
pip install -r requirements.txt
4. Set up your environment variables:

Create a .env file and add your Google Gemini API key:

Code snippet
GEMINI_API_KEY="your_api_key_here"
🐛 Found a Bug?
Ensure the bug was not already reported by searching on GitHub under Issues.

If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.  

✨ Adding a Feature  
Open a new Issue to discuss the feature before putting in the work. This ensures your time isn't wasted on a feature that might not align with the project's roadmap.  

Once approved, branch off of master, write your code, and submit a Pull Request (PR).

🔀 Pull Request Process
Ensure your code strictly adheres to standard Python PEP 8 formatting.

Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations, and container parameters.

Your PR will be reviewed by maintainers. Please be open to feedback and iteration!

⚖️ License
By contributing, you agree that your contributions will be licensed under the project's GPLv3 License.
