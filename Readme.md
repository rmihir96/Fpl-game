Welcome to MCU/DCU FPL 2023. Here are some instructions to get started with running this script. 

1. Need Python 3.X installed on your system. Follow this tutorial - https://www.digitalocean.com/community/tutorials/install-python-windows-10
2. Create a virtual environment by following these steps:
a. In the FPL directory run these commands

python3.8 -m venv env

source env/bin/activate

This would allow you to activate the virtual env.

3. Install some libraries! Run the following command in your virtual env terminal

pip install pandas

pip install thefuzz

pip install  python-Levenshtein

Note: If theres some library missing - always run "pip install <library name>" 

4. How to run the script?! Write this command on your terminal and hit enter!
   
python3 fpl.py

NOTE: Make sure you have the Fpl.xlsx file in the same location. 

ENJOY!!!
