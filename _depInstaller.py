import os

pips = ["selenium", "colored", "pytube", "yt-dlp"]

for pip in pips:
  os.system("pip install " + pip)  # Installs all the dependencies
