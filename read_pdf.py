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