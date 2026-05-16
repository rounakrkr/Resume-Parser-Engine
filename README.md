# 🚀 Automated Resume Parser Engine (ETL Pipeline)

A robust, pure-Python data extraction pipeline that converts unstructured PDF resumes into structured JSON formats and tabular CSV databases. Designed to handle varying industry resume formats using spatial text analysis and smart keyword anchoring.

## ✨ Key Features
- **Spatial Text Sorting:** Utilizes PyMuPDF (`fitz`) to sort PDF text blocks by Y-axis coordinates, preventing data jumbling commonly found in multi-column or Canva-style resumes.
- **Smart Fallback Logic:** Dynamically searches for flexible section headers (e.g., automatically pivoting to "Experience" or "Employment History" if "Projects" is absent).
- **Ghost-Spacing Fix:** Handles dummy/redacted PDF artifacts where characters are artificially spaced out (e.g., `A L I C E`).
- **Batch Processing:** Scans an entire directory of PDFs and processes them sequentially in seconds.
- **Dual Output Generation:** Exports a developer-friendly JSON file and an HR-ready CSV database simultaneously.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Core Library:** PyMuPDF (`fitz`)
- **Text Processing:** Regular Expressions (`re`), JSON, CSV

## 📁 Repository Structure

```text
/Resume-Parser-Engine
  ├── /resumes                 # Directory for input PDFs (Ignored in Git)
  ├── main.py                  # Core parsing engine
  ├── requirements.txt         # Dependencies
  ├── .gitignore               # Ignored files
  └── README.md                # Documentation
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Resume-Parser-Engine.git
cd Resume-Parser-Engine
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare the Data
Create a folder named `resumes` in the root directory and place your `.pdf` resumes inside it.

### 4. Run the Engine
Execute the main script to start the batch processing:
```bash
python main.py
```

### 5. Check Outputs
The script will automatically generate two files in your root directory:
- `all_parsed_resumes.json`: Full structural breakdown of every candidate.
- `candidates_database.csv`: A flattened, easy-to-read Excel/CSV sheet.

## 🧠 Core Extraction Architecture
1. **Coordinate Mapping:** Extracts text blocks along with their spatial coordinates.
2. **Reconstruction:** Recombines sorted words into paragraphs based on Y-axis progression.
3. **Regex Targeting:** Identifies robust patterns for Emails and Phone Numbers.
4. **Anchor Extraction:** Scans standard industry headings (`SKILLS`, `PROJECTS`, `WORK EXPERIENCE`) to isolate key profile data.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
