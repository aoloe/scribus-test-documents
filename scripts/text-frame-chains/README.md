# Text frame chaining

Create a Scribus document:

- With a longer text (the Odyssey, about 350 A5 pages).
- It first creates the document with a single page and the whole text, loaded from the text file in this folder.
- It then creates one page after the other, adding a full page text frame that is then linked to the text frame in the previous page.
- At the time of writing this is very slow (up to half an hour).

An alternative test:

- Create a new A5 document.
- Fill its first page with a text frame.
- Load the content of `odyssey.txt` into the frame.
- Create 400 more empty pages.
- Use "Multiple duplicate by page" to duplicate the first text frame into the following pages.
- At the time of writing this is very slow (up to half an hour).
