import scribus
import re
from pathlib import Path

# If MAX_PAGES is not 0, the script terminates when reaching the number of pages
MAX_PAGES = 0
PAGE_SIZE = scribus.PAPER_A5_MM
SHOW_PROGRESS = True

# Constants missing in scribus.*
MARGIN_TOP    = 0
MARGIN_LEFT   = 1
MARGIN_RIGHT  = 2
MARGIN_BOTTOM = 3
PAGE_WIDTH    = 0
PAGE_HEIGHT   = 1

def pickFont():
    """Try to pick a vaguely sensible font and return the font name"""
    fonts = scribus.getFontNames()
    preferences = ["Liberation Sans Regular", "Utopia Regular", "Luxi Serif Regular", "Nimbus Roman No9 L Regular", "Bitstream Vera Serif Regular", "Courier Regular" ]
    for pref in preferences:
        if pref in fonts:
            return pref
    raise Exception("Could not find any suitable font.")


def main():
    # Grab all our settings etc, retaining defaults.
    try:    # We need to make sure we turn redrawing back on at the end
        scribus.messagebarText("Loading text...")
        with Path(__file__).with_name('odyssey.txt').open('r') as f:
            full_text = f.read()
        # replace single newlines by spaces
        full_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', full_text)
        full_text_length = len(full_text)

        if SHOW_PROGRESS:
            scribus.progressTotal(full_text_length)
        scribus.messagebarText("Setting up document...")

        # create the document
        # size, margins, orientation, firstPageNumber, unit, pagesType, firstPageOrder, numPages
        if not scribus.newDocument(PAGE_SIZE, (10, 10, 10, 10), scribus.PORTRAIT, 1, scribus.UNIT_MILLIMETERS, scribus.PAGE_2, 1, 1) :
            raise Exception("Could not create the document")

        scribus.setRedraw(False)

        margins = scribus.getPageMargins()
        frame = {
            'x': margins[MARGIN_LEFT],
            'y': margins[MARGIN_RIGHT],
            'w': scribus.PAGE_SIZE[PAGE_WIDTH]  - margins[MARGIN_LEFT] - margins[MARGIN_RIGHT],
            'h': scribus.PAGE_SIZE[PAGE_HEIGHT] - margins[MARGIN_TOP]  - margins[MARGIN_BOTTOM]
        }

        # Create the first frame.
        text_frame = scribus.createText(frame['x'], frame['y'], frame['w'], frame['h'])
        scribus.setTextAlignment(scribus.ALIGN_BLOCK, text_frame)
        scribus.setFont(pickFont(), text_frame)

        page_number = 1

        # fill the initial frame with the full input text
        scribus.setText(full_text, text_frame)

        if SHOW_PROGRESS:
            scribus.progressSet(full_text_length - scribus.getTextLength(text_frame))

        # Create pages with one frame and link it, until the whole text fits
        while scribus.textOverflows(text_frame):
            scribus.messagebarText(f"Created and filled page {page_number}")
            page_number += 1
            prev_text_frame = text_frame
            scribus.newPage(-1)
            text_frame = scribus.createText(frame['x'], frame['y'], frame['w'], frame['h'])
            scribus.linkTextFrames(prev_text_frame, text_frame)
            if SHOW_PROGRESS:
                scribus.progressSet( full_text_length - scribus.getTextLength(text_frame) )

            if MAX_PAGES > 0 and page_number == MAX_PAGES:
                break

        scribus.messagebarText("Done")
    except Exception as e:
        scribus.messageBox('hey', 'failed' + e)
    finally:
        # Turn redraw back on and do other
        # cleanups, even if something goes horribly wrong.
        scribus.setRedraw(True)
        if SHOW_PROGRESS:
            scribus.progressReset()
        scribus.messagebarText("Ready")

if __name__ == '__main__':
    main()
