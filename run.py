import subprocess

db_delete = True
db_init = True
db_load_data = True
streamlit_run = True

if db_delete:
    subprocess.call(["rm", "-r", "./data"])

if db_init:
    subprocess.call(['sh', './sh/db_init.sh'])

if db_load_data:
    subprocess.call(['sh', './sh/db_load_data.sh'])

if streamlit_run:
    subprocess.call(["streamlit", "run", "Welcome.py"])