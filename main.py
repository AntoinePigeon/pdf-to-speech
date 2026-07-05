import argparse
import time
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from pypdf import PdfReader


def extract_pdf_text(pdf_path):
    """Read a PDF and return all its text as one string."""
    reader = PdfReader(pdf_path)
    full_text = ""
    for index, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()
        except Exception as error:
            print(f"  Skipping page {index + 1}: could not read it ({error}).")
            continue
        if page_text:
            full_text += page_text + "\n"
    return full_text


def chunk_text(text, max_chars=3000):
    """Split text into a list of strings, each under max_chars."""
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        if len(" ".join(current_chunk)) + len(word) + 1 <= max_chars:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def synthesize_one_chunk(polly, text, voice, max_retries=3):
    """Synthesize one chunk, retrying on transient API errors."""
    for attempt in range(1, max_retries + 1):
        try:
            response = polly.synthesize_speech(
                Text=text,
                OutputFormat="mp3",
                VoiceId=voice,
                Engine="neural"
            )
            return response["AudioStream"].read()
        except (BotoCoreError, ClientError) as error:
            if attempt == max_retries:
                print(f"  Failed after {max_retries} attempts: {error}")
                raise
            wait = 2 ** (attempt - 1)   # 1s, then 2s, then 4s
            print(f"  Attempt {attempt} failed. Retrying in {wait}s...")
            time.sleep(wait)


def synthesize_chunks(chunks, output_path, voice="Joanna"):
    """Send each chunk to Polly and stitch the audio into one MP3."""
    polly = boto3.client("polly")
    with open(output_path, "wb") as audio_file:
        for index, chunk in enumerate(chunks):
            print(f"Synthesizing chunk {index + 1} of {len(chunks)}...")
            audio_bytes = synthesize_one_chunk(polly, chunk, voice)
            audio_file.write(audio_bytes)
    print(f"Done! Saved {output_path}")


def main():
    """Read command-line options and run the PDF-to-speech pipeline."""
    parser = argparse.ArgumentParser(
        description="Convert a PDF file into an MP3 using Amazon Polly."
    )
    parser.add_argument("--input", required=True, help="Path to the PDF file to read.")
    parser.add_argument("--output", default="output.mp3", help="Path for the MP3 (default: output.mp3).")
    parser.add_argument("--voice", default="Joanna", help="Polly voice to use (default: Joanna).")
    args = parser.parse_args()

    try:
        pdf_text = extract_pdf_text(args.input)
    except FileNotFoundError:
        print(f"Error: could not find the file '{args.input}'. Check the path and try again.")
        return

    text_chunks = chunk_text(pdf_text)
    if not text_chunks:
        print("No readable text found. Is it a scanned/image PDF?")
        return

    print(f"PDF split into {len(text_chunks)} chunk(s).")
    synthesize_chunks(text_chunks, args.output, args.voice)


if __name__ == "__main__":
    main()