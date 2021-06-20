

run: 
	./main.py

test:
	# One line each line of Makefile recipe is run in separate shell.
	#export PYTHONPATH=$$PYTHONPATH:baseball; pytest -v
	pytest -v

clean:
	rm -r __pycache__
	rm -r baseball/*.pyc

