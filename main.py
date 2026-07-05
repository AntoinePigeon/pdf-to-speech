import argparse
import boto3
from pypdf import PdfReader


def extract_pdf_text(pdf_path):
    """Read a PDF and return all its text as one string."""
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
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


def synthesize_chunks(chunks, output_path, voice="Joanna"):
    """Send each chunk to Polly and stitch the audio into one MP3."""
    polly = boto3.client("polly")
    with open(output_path, "wb") as audio_file:
        for index, chunk in enumerate(chunks):
            print(f"Synthesizing chunk {index + 1} of {len(chunks)}...")
            response = polly.synthesize_speech(
                Text=chunk,
                OutputFormat="mp3",
                VoiceId=voice,
                Engine="neural"
            )
            audio_bytes = response["AudioStream"].read()
            audio_file.write(audio_bytes)
    print(f"Done! Saved {output_path}")


def main():
    """Read command-line options and run the PDF-to-speech pipeline."""
    parser = argparse.ArgumentParser(
        description="Convert a PDF file into an MP3 using Amazon Polly."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the PDF file to read."
    )
    parser.add_argument(
        "--output",
        default="output.mp3",
        help="Path for the MP3 to create (default: output.mp3)."
    )
    parser.add_argument(
        "--voice",
        default="Joanna",
        help="Polly voice to use (default: Joanna)."
    )
    args = parser.parse_args()

    pdf_text = extract_pdf_text(args.input)
    text_chunks = chunk_text(pdf_text)
    print(f"PDF split into {len(text_chunks)} chunk(s).")
    synthesize_chunks(text_chunks, args.output, args.voice)


if __name__ == "__main__":
    main()