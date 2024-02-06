with open("SECRETS.txt","r") as f:
    string = f.read()
def parse(smth):
    return (i for i in smth.strip().split("\n"))
  

key, sender, password, email = parse(string)

import urllib
def unquote(str):
    return urllib.parse.unquote(str).replace("\\u0026","&")

import os, sys, pytube, requests, re, json, pytube

from pydub import AudioSegment

import time

from termcolor import colored

import smtplib, ssl, datetime
import OpenAI from openai
openai = new OpenAI()
openai.API_KEY = key


channel = "https://www.youtube.com/@dakang"


html = requests.get(channel + "/streams").text
html = html[html.find("v="):]

url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()

#url="https://www.youtube.com/watch?v=7DKv5H5Frt0"

with open("latest.txt","r") as f:
    latestvid = f.read()
      
if latestvid != url: #do this stuff if the latest video is new
    #youtube (extract audio)
    print(colored("Making ","cyan")+colored("You","red")+"Tube"+colored(" object","cyan"))
    yt = pytube.YouTube(url) #pytube!
    
    print(colored("RUNNING ON: "+yt.title+"\n","blue"))
        
    response = requests.get(url).text

    response = response[response.find('"itag":249'):]
    response = response[response.find("https://"):]
    response = response[:response.find("\"")]

    audiourl = unquote(response)

    print(colored(audiourl,"green")) #just get the urls
    
    print(colored("\nDownloading sound [audio.mp3]","cyan"))
        
    start = time.time()
    yt.streams.get_by_itag(249).download(filename="audio.mp3") #more pytube! #for some reason downloading this matters a lot
    end = time.time()
    print(colored("Time to download: "+str(end-start),"magenta"))
    
    print(colored("Downloading transcript","cyan"))
    transcript = ""

    try:
        transcriptlist = yt.captions['zh'].xml_captions.split(">") #this should probably not be hardcoded - fix at some point
    
        for row in transcriptlist:
            temp = row[row.find(">"):]
            temp = row[:row.find("<")]
            temp = temp.replace("\n", " ").strip() + " "
    
            transcript += temp
            
        transcript = transcript.replace("  "," ")
    except: #download didn't work for whatever reason [likely no transcript]
        start = 0
        end = 0
        for i in range(4):
            start = time.time()
            audio_file = open("num"+str(i)+".mp3","rb")
            print(colored("Transcribing: "+str(i+1),"cyan"))
            text = openai.Audio.transcribe("whisper-1", audio_file).text
            transcript += text
            print(colored("Done with "+str(i+1),"cyan"))
            end = time.time()
            print(colored(f"Time to transcribe {str(i+1)}: {str(end-start)}","magenta"))
            print(colored(f"{(len(text)/(end-start)):.2f} words per second"))
        print()
            
        #print(colored(transcript,"green"))
            
    print(colored(transcript,"green"))
    
    print(colored("Logging in","cyan"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender,password)
        print(colored("Sending","cyan"))
        msg = "Subject:  Transcription of "+yt.title+" "+datetime.datetime.now().strftime("%m/%d/%y")+"\n\nTranscript for "+yt.title+"\n\n"+transcript
        server.sendmail(sender,email,msg.encode())
        
        
    with open("latest.txt","w") as f:
        f.write(url)
    print(url)
else:
    print(colored("Today's video already transcribed!","green"))
