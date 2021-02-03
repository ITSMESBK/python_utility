# =========================================================================================
# !/usr/bin/env python3
# Filename: config.py
# Description:All the configuration related data will be stored and access by constants here
# Author: Bharathkumar Sivakumar <BHARATH SBK @ITSMESBK>
# Python Environment - Python3
# Usage: Get Path and other Additional data here 
# ===========================================================================================

#PACKAGES
import json
import os

NATIVE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

credintials_json_file = open(NATIVE_DIR_PATH + "/" +"credentials.json",)
credintials_json_data = json.load(credintials_json_file)

# DATASET AND OTHER PATHS 

CUSTOM_FILE_PATH_01 = credintials_json_data['file_path']['bs_pl_txt']

