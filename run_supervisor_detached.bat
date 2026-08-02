@echo off
cd /d "C:\Users\ASUS\Claude\Projects\AutoDock"
start "MD Supervisor" /min "C:\Users\ASUS\miniforge3\envs\md\python.exe" -u md_supervisor_reps.py >> md\reps_supervisor_stdout.log 2>&1
