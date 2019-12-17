setup:
	pip install --upgrade google-api-python-client
update:
	python mk_syllabus.py
	git add index.md
	git add ../full_syllabus/index.md
	git add ../objectives/index.md
	git commit -m"autoupdate"
	git push origin master

check-style:
	flake8 --show-source mk_syllabus.py get_syllabus2.py 
