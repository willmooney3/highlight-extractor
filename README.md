# highlight-extractor
A quick script to extract the highlights I make on PDF files using a Kobo
Elipsa.

# Description
The Kobo Elipsa allows you to export highlights made in documents, as long as
those highlights are *not* made using the stylus that comes included with the
eReader. Given that reading and highlighting PDFs was the entire point of me
buying the thing, I decided to make sure my freehand highlights could be
extracted from all of the papers I read with some Python.

# Usage
 1. Connect your Elipsa to your computer
 1. Copy the mounted drive into a folder
 1. Plop this script in the new folder
 1. Create a virtualenv and install the requirements
 1. Run the script with `python highlight_extractor.py`

# Output
This will create an `annotations` directory, with sub-directories for each file
that a highlight is detected in. Each file directory is then divided by page,
with those files containing PNG clips of the highlights. There is an
`index.html` file that contains the document titles followed by all of the
embedded image highlights.

# Future Plans
 1. Clean up code
 1. Add tests
 1. Add cli
 1. Package
 1. Put on pypi
 1. Stitch clips together
 1. OCR to make highlights indexable/searchable
 1. Add GUI
