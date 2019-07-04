import re

from scrollable import ScrollFrame

try:
	import json
except ImportError:
	import simplejson as json

# Imports
import tweepy
import tkinter as tk
from tkinter import font


# Save the credentials into a json file
def save_credentials(access_keys):
	with open("twitter_credentials.json", "w") as file:
		json.dump(access_keys, file)


# Load the credential from json file
def load_credentials():
	with open("twitter_credentials.json", "r") as file:
		return json.load(file)


def clear():
	for widget in scrollable.viewPort.winfo_children():
		widget.destroy()


def clicked():
	clear()
	name = str(entry.get()).strip().title()
	if "@" in name:
		name = name.replace('@', '')

	statuses = tweepy.Cursor(api.user_timeline, id=name, tweet_mode="extended").items(100)

	for status in statuses:
		if "@" in status.full_text:
			continue

		tweet = status.full_text
		char_list = [tweet[j] for j in range(len(tweet)) if ord(tweet[j]) in range(65536)]
		tweet = ''
		for j in char_list:
			tweet = tweet + j

		clean_tweet = re.sub(r"http\S+", "[IMAGE]", tweet)
		# clean_tweet = p.clean(tweet)

		# if not clean_tweet:
		# clean_tweet = "IMAGE ONLY"

		# Create a container for our whole tweet thing
		container = tk.Frame(scrollable.viewPort, bg='#8fddff')
		container.pack(fill='x')

		# Container for the username and date containers
		username_container = tk.Frame(container)
		username_container.pack(side='left')
		username_container.config(highlightbackground='#8fddff')
		username_container.config(highlightthickness="1")
		# Username container
		user = tk.Label(username_container, bg='#879bbf', fg='#383734', font=font_b, width=15, height=3, wraplength=150, anchor='s', justify='left',
						text="->@" + name + ":")
		user.pack(side='top', fill='both')

		# Date container
		date = tk.Label(username_container, bg='#879bbf', fg='#383734', font=font_i_10, width=15, height=3, wraplength=150, anchor='n', justify='left',
						text=status.created_at.strftime("%d/%m/%Y | %H:%M"))
		date.pack(side='bottom', fill='both')

		# Tweet container
		tw = tk.Label(container, bg='#c9ddff', fg='#383734', width=88, height=6, font=font_n, wraplength=660, justify='left', text=clean_tweet, anchor='w')
		tw.pack(fill='both', expand=True, pady=1)


ACCESS_KEYS = load_credentials()

# SETUP VARS
TITLE = 'TweetTooth :)'
HEIGHT = 600
WIDTH = 1100
FONT_FAMILY = 'Calibri'

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(ACCESS_KEYS['CONSUMER_KEY'], ACCESS_KEYS['CONSUMER_SECRET'])
auth.set_access_token(ACCESS_KEYS['ACCESS_TOKEN'], ACCESS_KEYS['ACCESS_SECRET'])

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

root = tk.Tk()
root.title(TITLE)
root.geometry(f'{WIDTH}x{HEIGHT}')
root.resizable(False, False)
font_b = font.Font(family=FONT_FAMILY, size=13, weight='bold')
font_n = font.Font(family=FONT_FAMILY, size=12)
font_i = font.Font(family=FONT_FAMILY, size=12, slant='italic')

font_i_10 = font.Font(family='Calibri', size=10, slant='italic')

frame = tk.Frame(root, bg='#1fbcff', width=100)
frame.place(relwidth=0.2, relheight=1)

frame.config(highlightbackground='#8fddff')
frame.config(highlightthickness="1")

frame2 = tk.Frame(root, bg='#8fddff')
frame2.place(relx=0.2, relwidth=0.8, relheight=1)

scrollable = ScrollFrame(frame2)
scrollable.pack(side="top", fill="both", expand=True)

entry = tk.Entry(frame, text='Type in a @twitter name', font=font_n, bg='#c9ddff')
entry.focus()
entry.insert(0, "@User here")
entry.pack(fill='x', pady=5)

button = tk.Button(frame, text='Search', command=clicked, font=font_n)
button.pack(fill='x')

random = tk.Button(frame, text='Random Tweet', font=font_n)
random.pack(fill='x')

clearbutton = tk.Button(frame, text='Clear Tweets', command=clear, font=font_n)
clearbutton.pack(side='bottom', fill='x')

scrollable.update()
root.mainloop()
