from math import isclose
import os
from typing import Boolean, Dict, List

import fitz


class HighlightExtractor:
    """Actually pull the images of highlights out of the given PDF."""

    def __init__(
        self, image_dir: str, pdf_path: str, padding: int = 7, get_content: bool = False
    ):
        """Initalize the HighlightExtractor.

        Args:
            pdf_path (str): The path to the PDF to extract highlights from
            padding (int): Padding to add around the highlight to ensure we
                           get all of the text that is highlighted
        """
        super().__init__()
        self.get_content = get_content
        self.image_dir = image_dir
        self.padding = padding
        self.pdf_path = pdf_path

    def is_highlight(self, drawing: Dict) -> Boolean:
        """Determine if the given drawing is a highlight.

        Args:
            drawing (dict): The drawing to check

        Return:
            True if we consider it a highlight, False otherwise
        """
        raise NotImplementedError("Subclasses must implement this method")

    def parse_content(self, filename: str) -> str:
        # TODO: Original CV formula struggles with overlapping highlights,
        # need to adjust. Placeholder for now.
        return "Content not parsed."

    def process_drawing(self, page: fitz.Page, drawing: Dict) -> Dict:
        """Process the given drawing on the given page.

        Args:
            page (fitz.Page): The page the drawing is from
            drawing (dict): The drawing to process

        Return:
            dict containing the page number, corners, and rect for the drawing
        """
        tl_x = drawing["rect"].tl.x
        tl_y = drawing["rect"].tl.y
        br_x = drawing["rect"].br.x
        br_y = drawing["rect"].br.y
        # Calculate new rect: Need to add space around to ensure all text is
        # fully captured
        new_rect = fitz.Rect(
            fitz.Point(tl_x - self.padding, tl_y - self.padding),
            fitz.Point(br_x + self.padding, br_y + self.padding),
        )
        highlight = page.get_pixmap(clip=new_rect)
        highlight = {
            "pageNumber": page.number,
            "topLeft": (tl_x, tl_y),
            "bottomRight": (br_x, br_y),
            "rect": highlight,
        }
        image_filename = [
            os.path.basename(self.pdf_path).split(".")[0],
            page.number,
            highlight["topLeft"][0],
            highlight["bottomRight"][1],
            ".png",
        ]
        filename = os.path.join(self.image_dir, "_".join(image_filename))
        highlight["rect"].save(filename)
        if self.get_content:
            highlight["content"] = self.parse_content(filename)
        return highlight

    def process_page(self, page: fitz.Page) -> List[Dict]:
        """Process an individual page from the PDF.

        Args:
            page (fitz.Page): The page to process the annotations out of

        Return:
            pass
        """
        annotations = []
        drawings = page.get_drawings()
        if len(drawings):
            for drawing in drawings:
                if self.is_highlight(drawing):
                    annotations.append(self.process_drawing(page, drawing))
        return annotations

    def extract(self) -> List[Dict]:
        """Extract annotations from the PDF document.

        Return:
            list of dict annotations
        """
        annotations = []
        with fitz.open(self.pdf_path) as doc:
            if doc.has_annots():
                for page in doc.pages():
                    annotations.extend(self.process_page(page))
        return annotations


class KoboElipsaHighlightExtractor(HighlightExtractor):
    """A highlight extractor specifically for the Kobo Elipsa e-reader."""

    def __init__(self, pdf_path: str, padding: int = 7):
        """Initialize the KoboElipsaHighlightExtractor."""
        super().__init__(pdf_path, padding)

    def is_highlight(self, drawing: Dict) -> bool:
        """Determine if the given drawing is a Kobo Elipsa highlight.

        Args:
            drawing (dict): The drawing to check

        Return:
            True if it is a highlight, False otherwise
        """
        return isclose(drawing["opacity"], 0.5)
