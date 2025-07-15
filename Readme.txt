# Logic Tag Writer

**Logic Tag Writer** is a multithreaded semantic tagging tool designed for large-scale text file processing. It uses SHA256 hashing for deduplication, OpenAI GPT integration for context-aware tagging, and threaded I/O for high-throughput analysis. Developed for use in threat intelligence pipelines, knowledge base classification, and AI model training prep.

This tool scans directories, hashes text files, and generates `.tag.txt` metadata files based on the file’s content and structure. Each tag file includes semantically rich context and is saved alongside the original source.

---

## Features

- Multithreaded directory traversal and file processing
- SHA256-based file fingerprinting and cache deduplication
- Automatic `.tag.txt` file creation alongside source files
- Caching and manifest tracking to prevent reprocessing
- Modular design for easy adaptation to other LLMs or prompt engines

---

## File Overview

| File                     | Description                                       |
|--------------------------|---------------------------------------------------|
| `logic_tag_writer.py`    | Main script for scanning, tagging, and caching    |
| `run_tagging_engine.ps1` | PowerShell runner for CLI execution and automation |
| `tagging_manifest.csv`   | (Optional) Example of processed files + hashes     |
| `requirements.txt`       | Python dependencies for this module               |

---

## Usage

### Option 1: Run via PowerShell

```powershell
.\run_tagging_engine.ps1 -TargetDirectory "C:\Path\To\TextFiles"
