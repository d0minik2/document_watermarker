#! /usr/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # if the package is called with arguments

        from watermarker import watermark_document_images

        watermark_document_images(*sys.argv[1:])
        print("Watermarked document images.")
