# Xplur

### Project Setup:
1. git clone 
2. cd xplur
3. git status
4. now, outside the project dir. create the pythonenv. 
	- cd ..
5. python3 -m venv envxplur
6. source envxplur/bin/activate
7. cd xplur
8. pip install -r requirements.txt
9. set environment

10. Run migrations 
	- flask db init-db
	- flask db migrate
	- flask db upgrade

11. Run Flask
	- flask run
