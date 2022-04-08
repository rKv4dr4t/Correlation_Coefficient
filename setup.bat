@echo off
title Setup
pip install -r requirements.txt %*
echo REQUIREMENTS INSTALLED
timeout /t 5
exit