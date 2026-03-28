import os
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

commands = [
    "git init",
    "git add .",
    'git commit -m "Initial commit for ML E-Commerce Recommendation Engine"',
    "git branch -M main",
    "git remote add origin https://github.com/yugrajmangate-dev/ML_project.git",
    "git push -u origin main"
]

for cmd in commands:
    run_command(cmd)
