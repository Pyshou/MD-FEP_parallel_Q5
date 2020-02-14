#!/bin/bash
# This script calls pandoc to generate markdown and word documents
# automatically. The created documents will need some minor editing.
#pandoc -f latex -t docx pymemdyn-manual.tex -o pymemdyn-manual.docx
#pandoc -f latex -t markdown pymemdyn-manual.tex -o pymemdyn-manual.md
pandoc -f markdown pymemdyn-manual.md -o pymemdyn-manual.pdf
