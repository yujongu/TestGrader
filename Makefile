.PHONY: grade detail

grade:
	python grader.py

detail:
	python grader_detail.py $(PROB)
