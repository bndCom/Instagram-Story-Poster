import pickle
import os
import shutil
import time
import argparse
from instagrapi import Client
from datetime import datetime, date

BASE = os.path.dirname(os.path.abspath(__file__))

PKL_PATH = os.path.join(BASE, "../client.pkl")
QUEUE_FOLDER = os.path.join(BASE, "../queue")
ARCHIVE_FOLDER = os.path.join(BASE, "../archive")
RUN_LOG = os.path.join(BASE, "../.lastrun")

# posting story with ready-to-use picture
def post_story(close=True):
    
    # load session information
    with open(PKL_PATH, "rb") as f:
        cl = pickle.load(f)
    # finding images to be posted
    if not os.path.exists(QUEUE_FOLDER):
        print("[!] Error, Queue folder doesn't exist")
        exit(-1)
    files = sorted(os.listdir(QUEUE_FOLDER))
    first_file = files[0].split('-')[0]
    # get stories to be posted together
    for file in files:
        if file.split('-')[0] == first_file:
            path = os.path.join(QUEUE_FOLDER, file)
            if close:
                extra_data = {
                    "audience": "besties"
                }
                cl.photo_upload_to_story(path, extra_data=extra_data)
            else:
                cl.photo_upload_to_story(path)
            # archive stories
            if not os.path.exists(ARCHIVE_FOLDER):
                try:
                    os.makedirs(ARCHIVE_FOLDER, exist_ok=False)
                except OSError as e:
                    print("[!] Error while creating directory")
                    exit(-1)
            shutil.move(path, ARCHIVE_FOLDER)
            # save posting time
            with open(RUN_LOG, 'w') as f:
                f.write(str(int(time.time())))
              
    return 0

if __name__ == '__main__':
    # getting commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-nc", "--no-close", action="store_true", help="Post the story for public")
    args = parser.parse_args()
    # if log file doesn't exist, create one with old timestamp
    if not os.path.exists(RUN_LOG):
        with open(RUN_LOG, "w") as f:
            f.write(str(int(time.time()) - 86400))
    # check last post
    with open(RUN_LOG, 'r') as f:
        try:
            ts = datetime.fromtimestamp(int(f.read()))
        except (TypeError, ValueError) as e:
            # to do
            print(f"Error reading the last post date: {e}")
            with open(RUN_LOG, 'w') as f:
                f.write(str(int(time.time())))
                print(f"Last post date modified to: {datetime.fromtimestamp(int(time.time()))}")
                exit(-1)

    if ts.date() == date.today(): # already posted
        print("Already posted today. Exit...")
        exit(0) 
    # if log file doesn't exist, post directly

    if os.path.exists(PKL_PATH):
        try:
            post_story(not args.no_close)
            print("[+] Story posted!")
            exit(0)
        except (EOFError, pickle.UnpicklingError) as e:
            print(f"Error loading pickle file: {e}. Recreating the file...")
    
    # saving login data
    cl = Client()
    cl.login(os.environ["USER"], os.environ["PASS"])
    with open(PKL_PATH, "wb") as f:
        pickle.dump(cl, f)
        print("Logged-in successfully!")
