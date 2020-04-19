#!/usr/bin/env python3
import time
import os  
def f(file_path):
	time.sleep(120)
	command="rm -r "+file_path
	os.system(command)
