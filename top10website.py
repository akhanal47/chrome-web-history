import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt 
import itertools
from tkinter import messagebox
import tkinter as tk

root=tk.Tk()
root.withdraw()

url_count=dict()

#select the default path or the first profile path
def checkpath():
	global history_path
	global history_database
	history_path=os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
	i=1
	while True:
		if os.path.exists(history_path)==True:
			break
		history_path=os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Profile "+str(i)
		i=i+1
	history_database=os.path.join(history_path,'history')

def db_connection():
	global search_result
	conn=sqlite3.connect(history_database)
	cursor=conn.cursor()
	cursor.execute('SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url')
	search_result=cursor.fetchall()
	conn.close()

def url_formatter(url):
	try:
		url=url.split('//')
		second_split=url[1].split('/',1)
		domain=second_split[0].replace('www.','')
		return domain
	except IndexError:
		print ('error')

def plot(final_dict):
	figure=plt.gcf()
	figure.set_size_inches(11, 8)
	plt.bar(range(len(final_dict)),final_dict.values(),align='edge')
	plt.xticks(range(len(final_dict)),final_dict.keys())
	plt.gca().axes.yaxis.grid(True)
	plt.xticks(rotation=15)
	plt.savefig('top_10_visited_sites.jpeg',orientation='landscape',dpi=300, quality=100)
	plt.show()

messagebox.showinfo('Attention', 'Close Chrome Before Proceeding')

try:
	checkpath()
	db_connection()

	for url,count in search_result:
		url=url_formatter(url)
		if url in url_count:
			url_count[url] += 1
		else:
			url_count[url]= 1

	sorted_url=OrderedDict(sorted((url_count.items()), key=operator.itemgetter(1), reverse=True))

	final_dict=dict(itertools.islice(sorted_url.items(),10))

	plot(final_dict)
except Exception as e:
	messagebox.showerror('Error',e)






