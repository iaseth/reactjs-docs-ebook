
default: epub


epub: clean
	@python generate_ebook.py

download:
	@python download_index.py
	@python download_htmls.py

clean:
	@rm -rf data/ebookbase/OEBPS/content.opf
	@rm -rf data/ebookbase/OEBPS/toc.ncx
	@rm -rf data/ebookbase/OEBPS/text/*.html
