# s4challenge
prereq:
  sudo pip3 install virtualenv
  pip install flask

Run:
  Run program with s4app.py script

setup:
virtualenv flask_app
cd flask_app
bin		lib		pyvenv.cfg	s4app.py	templates
source bin/activate
pip install flask

html files should be placed in templates directory
python s4app.py

