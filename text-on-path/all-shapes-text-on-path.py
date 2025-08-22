"""Attach a sample text to each possible type of shape.

This script is used to check for the direction of the nodes in the paths generated from the default Scribus shapes.
It is usually run with all-shapes-as-path.sla open.

(c) MIT ale rimoldi"""

try:
    import scribus
except ImportError as ex:
    print('\nThis script must be run from inside Scribus\n')
    raise ex

def attatch_text_to_all_paths():
    """
    There is a text frame called Text in the document.
    For each shape, we make a duplicate of it, convert the shape to path, delete the shape, attach the text to the path.
    """

    # create a text box in empty cell in the 4th row, 4th column
    textFrame = scribus.createText(426.46, 420.94, 128.82, 126.98)
    scribus.insertText('Start. This is some text to be used for testing the "Text on path" feature. End.', 0, textFrame)
    

    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        for item in scribus.getPageItems():
            print(item)
            # for each bezier item, attach a duplicate of the text frame
            if item[1] == 7:
                duplicateText = scribus.duplicateObject(textFrame)
                x, y = scribus.getPosition(item[0])
                bezierItem = scribus.createPathText(x, y, duplicateText, item[0])

    scribus.deleteObject(textFrame)
    scribus.gotoPage(1)


def main():
    if not scribus.haveDoc():
        scribus.messageBox('Export Error', 'You need an open document.', icon=scribus.ICON_CRITICAL)
        return

    attatch_text_to_all_paths()

if __name__ == "__main__":
    main()

