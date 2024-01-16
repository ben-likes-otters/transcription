import requests, os

url = "https://raw.githubusercontent.com/ben-likes-otters/transcription/main/ev2prode.py"

try:
    code = requests.get(url).content.decode()

    with open("updated.py","w") as f:
        f.write(code)
except:
    print("NOT UPDATED")
    
os.system("python3 updated.py")

