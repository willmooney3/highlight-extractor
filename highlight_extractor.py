from glob import iglob
import pathlib

import fitz


PADDING = 7


annotations = {}
for pdf in iglob("*.pdf"):
    with fitz.open(pdf) as doc:
        if doc.has_annots():
            pathlib.Path(f"annotations/{pdf}").mkdir(parents=True, exist_ok=True)
            annotations[pdf] = []
            for page in doc.pages():
                if len(page.get_drawings()):
                    for drawing in page.get_drawings():
                        # Try to skip over any drawings that aren't Kobo highlights
                        if drawing['opacity'] > 0.5:
                            continue
                        pathlib.Path(f"annotations/{pdf}/{page.number}").mkdir(parents=True, exist_ok=True)
                        tl_x = drawing['rect'].tl.x
                        tl_y = drawing['rect'].tl.y
                        br_x = drawing['rect'].br.x
                        br_y = drawing['rect'].br.y
                        annotations[pdf].append({
                            "page": page.number,
                            "topLeft": (tl_x, tl_y),
                            "bottomRight": (br_x, br_y),
                        })
                        # Calculate new rect: Need to add space around to ensure all text is fully
                        # captured
                        new_rect = fitz.Rect(
                            fitz.Point(tl_x - PADDING, tl_y - PADDING),
                            fitz.Point(br_x + PADDING, br_y + PADDING)
                        )
                        highlight = page.get_pixmap(clip=new_rect)
                        highlight.save(f"annotations/{pdf}/{page.number}/{tl_x}_{tl_y}_{br_x}_{br_y}.png")
if annotations:
    with open("annotations/index.html", "w") as annotation_index:
        annotation_index.write("<!doctype html>\n<html>\n<head>Annotation Index</head><body>\n")
        annotation_index.write("<ul>\n")
        for doc, annots in annotations.items():
            annotation_index.write(f"<li>{doc}</li>\n<ul>\n")
            current_page = -1
            for highlight in annots:
                if current_page < 0:
                    annotation_index.write(f"<li>{highlight['page']}</li><ul>")
                    current_page = highlight['page']
                elif highlight['page'] != current_page:
                    annotation_index.write(f"</ul>\n<li>{highlight['page']}</li>\n<ul>\n")
                    current_page = highlight['page']
                annotation_index.write(f"<li><img src=\"{doc}/{highlight['page']}/{highlight['topLeft'][0]}_{highlight['topLeft'][1]}_{highlight['bottomRight'][0]}_{highlight['bottomRight'][1]}.png\"></li>\n")
            annotation_index.write("</ul>\n")
            annotation_index.write("</ul>\n")
        annotation_index.write("</ul>\n")
        annotation_index.write("</body></html>")
