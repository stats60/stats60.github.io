run:
	bundle exec jekyll serve
html:
	pandoc -s full_syllabus/index.md -o full_syllabus.html
