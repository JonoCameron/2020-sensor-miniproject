import sys
import subprocess

filename = open('data.json', 'w')

# filename.truncate()  # mode 'w' truncates file

sys.stdout = filename

print('Hello')

print('Testing')



filename.close()

# reattach stdout to console
sys.stdout = sys.__stdout__
