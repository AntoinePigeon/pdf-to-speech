# PDF to Speech

A command-line tool that converts PDF documents into spoken-word MP3 audio using [Amazon Polly](https://aws.amazon.com/polly/).

Point it at a PDF, and it extracts the text, splits it into Polly-sized pieces, synthesizes natural-sounding neural speech, and stitches everything into a single MP3 you can play or share.

---

## Features

- **PDF text extraction** using `pypdf`, with unreadable or image-only pages skipped gracefully.
- **Smart chunking** that splits long text into pieces under Amazon Polly's per-request character limit, without ever cutting a word in half.
- **Neural text-to-speech** via Amazon Polly for natural, human-sounding audio.
- **Audio stitching** that joins all chunks into one continuous MP3.
- **Configurable CLI** built with `argparse`: choose your input file, output path, and voice.
- **Automatic retries** with exponential backoff, so a brief network hiccup doesn't crash a whole run.
- **Friendly error handling** for missing files and PDFs with no readable text.
- **Unit tests** covering the chunking logic with `pytest`.

---

## Prerequisites

Before you begin, you'll need:

- **Python 3.8 or newer**
- **An AWS account** ([free tier available](https://aws.amazon.com/polly/pricing/); Amazon Polly includes a monthly free character allowance for new accounts)
- **AWS credentials configured locally** (see [AWS Setup](#aws-setup) below)

---

## Installation

Clone the repository and set up an isolated environment:

```bash
git clone https://github.com/AntoinePigeon/pdf-to-speech.git
cd pdf-to-speech

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## AWS Setup

This tool talks to Amazon Polly, so it needs AWS credentials. Credentials are stored **outside** the project folder (in `~/.aws/`), so no secrets ever end up in your code or on GitHub.

1. In the AWS console, create an **IAM user** with the `AmazonPollyFullAccess` permission.
2. Generate an **access key** for that user.
3. Save your credentials to `~/.aws/credentials`:

   ```ini
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY_ID
   aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
   ```

4. Set your region in `~/.aws/config`:

   ```ini
   [default]
   region = us-east-1
   ```

`boto3` reads these files automatically. **Never commit your credentials or share your secret access key.**

---

## Usage

Convert a PDF using the default voice (Joanna) and output file (`output.mp3`):

```bash
python main.py --input sample.pdf
```

Specify an output file and a different voice:

```bash
python main.py --input report.pdf --output report.mp3 --voice Matthew
```

See all available options:

```bash
python main.py --help
```

### Options

| Flag        | Required | Default        | Description                          |
|-------------|----------|----------------|--------------------------------------|
| `--input`   | Yes      | —              | Path to the PDF file to convert.     |
| `--output`  | No       | `output.mp3`   | Path for the generated MP3.          |
| `--voice`   | No       | `Joanna`       | The Amazon Polly voice to use.       |

### Playing the audio

On macOS:

```bash
afplay output.mp3
```

Or simply double-click the MP3 file in your file browser.

---

## Running the tests

The chunking logic is covered by a `pytest` suite:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

---

## How it works

The program runs a simple pipeline:

1. **Extract** — `pypdf` reads the PDF page by page and collects the text.
2. **Chunk** — the text is split into pieces under Polly's 3,000-character request limit, breaking only on spaces so words stay intact.
3. **Synthesize** — each chunk is sent to Amazon Polly, which returns an audio stream. Failed requests are retried with exponential backoff.
4. **Stitch** — the audio bytes from every chunk are written to the same file, in order, producing one continuous MP3.

---

## Project structure

```
pdf-to-speech/
├── main.py              # The CLI and the full pipeline
├── test_chunking.py     # Pytest suite for the chunking logic
├── requirements.txt     # Project dependencies
├── .gitignore           # Files Git should ignore (venv, secrets, output)
└── README.md            # You are here
```

---

## Roadmap

Possible improvements for future versions:

- **Sentence-aware chunking** for smoother pauses between audio segments.
- **OCR support** to handle scanned (image-based) PDFs.
- **Smarter retries** that fail fast on permanent errors (like an invalid voice) instead of retrying them.
- **Voice discovery** via a `--list-voices` flag using Polly's `describe_voices`.
- **A progress bar** for long documents.

---

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.
