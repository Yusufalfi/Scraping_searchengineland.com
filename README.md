# Search Engine Land Content Scraper

A Python-based web scraper that collects articles from **Search Engine Land** published from **January 1, 2024 onward**. The scraper reads the website sitemap, extracts article content, and exports the results into structured Microsoft Word (`.docx`) documents.

The project focuses on structured content extraction, date-based filtering, resumable progress tracking, and document generation.

## 📋 Project Overview

### Target

- **Website:** [Search Engine Land](https://searchengineland.com/)
- **Sitemap:** [Search Engine Land Sitemap](https://searchengineland.com/sitemap_index.xml)
- **Date filter:** Articles published on or after `2024-01-01`
- **Output:** Structured `.docx` documents
- **Content:** Article paragraphs, headings, bullet lists, and images

### Problem Statement

Collecting and formatting a large number of articles manually can be repetitive and time-consuming. Website pages may also contain unrelated elements such as advertisements, sidebars, author information, and other widgets.

This project automates the process of:

1. Reading sitemap files.
2. Filtering articles by publication date.
3. Downloading article pages.
4. Extracting the relevant article content.
5. Removing unwanted page elements.
6. Generating structured Word documents.
7. Saving progress so interrupted runs can continue.

## 🛠️ Key Features

### 1. Sitemap-Based Crawling

- Reads `sitemap_index.xml`.
- Iterates through related sub-sitemaps.
- Processes article URLs based on the configured date threshold.

### 2. Date Filtering

- Selects articles published on or after `2024-01-01`.
- Helps avoid processing articles outside the target date range.

### 3. Article Content Extraction

Uses `BeautifulSoup4` and `lxml` to extract relevant content from the page structure, including:

- Paragraphs
- Headings
- Bullet lists
- Images

The parser targets known page structures such as:

- `#articleContent`
- `.body-content`
- `p.wp-block-paragraph`
- `figure.wp-block-image`

It also excludes unwanted elements such as:

- Advertisements
- Sidebars
- Topic labels
- Author biography sections
- Other unrelated widgets

> **Note:** Website HTML structures can change over time. Extraction rules may need to be updated when the website layout changes.

### 4. HTTP Request Handling

Uses `cloudscraper` for HTTP requests and to attempt access to pages that may include anti-bot protections.

> **Limitation:** This tool does not guarantee that every Cloudflare protection or challenge can be bypassed. Access depends on the website's security configuration and current conditions.

### 5. Resumable Progress Tracking

- Stores processing progress in local JSON files.
- Allows the scraper to continue after an interruption.
- Reduces the need to repeat completed work.

### 6. Word Document Generation

Uses `python-docx` to generate structured Word documents containing the extracted article content.

## 🧰 Tech Stack

- **Programming Language:** Python 3.10+
- **HTTP Client:** `cloudscraper`
- **HTML Parser:** `BeautifulSoup4`
- **Parser Backend:** `lxml`
- **Document Export:** `python-docx`
- **Progress Tracking:** JSON

## 📁 Project Structure

```text
├── config.py          # Configuration & constants
├── fetcher.py         # Cloudscraper & HTTP retry logic
├── sitemap_parser.py  # Sitemap Index & XML caching logic
├── doc_builder.py     # Word (.docx) export helper
├── main.py            # Main application orchestrator
├── .gitignore         # Git ignore rules
└── README.md          # Documentation
```

> Update this structure if your actual repository contains additional files or folders.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Yusufalfi/Scraping_searchengineland.com.git
cd searchengineland
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
cloudscraper>=1.2.60
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-docx>=0.8.11
```

### 4. Run the Scraper

```bash
python scraper.py
```

Generated Word documents will be saved in the configured output directory, such as:

```text
word_outputs/
```

## 📄 Output

The scraper is designed to generate Word documents containing structured article content, including:

- Article title
- Article body text
- Headings
- Bullet lists
- Images, where supported by the extraction logic

The exact output structure depends on the implementation in `doc_builder.py`.

## ⚠️ Limitations and Responsible Use

- Use the scraper only where access and collection are permitted.
- Respect the website's terms of service, robots directives, and applicable laws.
- Avoid excessive request rates that could affect website availability.
- Website layouts and anti-bot protections may change.
- Extraction accuracy depends on the HTML structure of each page.
- The current project should be tested against representative articles before large-scale execution.

## 🔮 Possible Improvements

- Add configurable request delays and retry limits.
- Add structured logging for successful and failed URLs.
- Add a command-line option for the start date.
- Add a command-line option for the output directory.
- Add automated tests for HTML extraction.
- Add support for additional export formats such as PDF.
- Add a summary report containing processed, skipped, and failed URLs.

## 📌 Disclaimer

This project is intended for learning, research, and authorized data collection. Users are responsible for ensuring that their use of the scraper complies with the target website's policies and applicable regulations.
