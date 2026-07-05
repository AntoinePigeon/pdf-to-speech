from pypdf import PdfReader

# 1. Open the PDF and hand it to a "reader" object.
reader = PdfReader("sample.pdf")

# 2. Prepare an empty string to collect text from every page.
full_text = ""

# 3. Loop through each page in the PDF.
for page in reader.pages:
    # extract_text() pulls the text out of one page as a string.
    page_text = page.extract_text()

    # Some pages have no extractable text (blank pages, images).
    # This "if" skips those so they don't break anything.
    if page_text:
        full_text += page_text + "\n"

# 4. Show a preview so we can confirm it worked.
print("Total characters extracted:", len(full_text))
print("---- First 300 characters ----")
print(full_text[:300])
print("\n")


def chunk_text(text, max_chars=3000):
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


test = "word " * 1000   # makes a string of 1000 "word "s, about 5000 chars
result = chunk_text(test)

print("Number of chunks:", len(result))
for i, chunk in enumerate(result):
    print(f"Chunk {i} length: {len(chunk)}")