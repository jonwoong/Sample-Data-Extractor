# Author: Jonathan Woong

#!/usr/bin/python

##### IMPORT STUFF #####

import Tkinter as tk
from Tkinter import *
import subprocess
import time

##### DATA STRUCTURES #####

fields = ['Project Name', 'Website URL', 'Table Attribute', 'Attribute Value', 'Number of Columns']
entries = []

##### METHODS #####

def generateForm(root,fields): # adapted from python-course.eu
	for field in fields:
		row = Frame(root) # create frame for row
		label = Label(row, text=field, anchor='w') # create label in row
		row.pack(side=TOP, fill=X, padx=5, pady=5) # initialize row
		label.pack(side=LEFT) # initialize label
		entry = Entry(row) # create entry field
		entry.pack(side=RIGHT, expand=YES, fill=X) # initialize entry field
		entries.append((field,entry)) # store user choice
	return entries

def generateSpider(): # generates a Scrapy spider using user inputs
	spiderTemplate = open("spider.py", "r") # open template
	contents = spiderTemplate.readlines() # read contents of template
	spiderTemplate.close() # close template

	projectName = entries[0][1].get() # get project name as string
	url = entries[1][1].get() # get url as string
	attribtue = entries[2][1].get() # get attribute as string
	value = entries[3][1].get() # get attribtue value as string
	numberOfColumns = int(entries[4][1].get()) # get number of columns as int

	# substitute user values for placeholders
	contents = [line.replace('$VALUE', value) for line in [line.replace('$URL', url) for line in [line.replace('$ATTRIBUTE', attribtue) for line in [line.replace('$NAME', projectName) for line in contents]]]]

	# fill in column headers
	for x in range(numberOfColumns):
		contents.insert(x+3, "\t_" + str(x) + " = scrapy.Field()\n")

	# fill in data extraction code
	for z in range(numberOfColumns):
		contents.insert(z+12+numberOfColumns, "\t\t\titem['_" + str(z) + "'] = row.xpath('td[" + str(z + 1) + "]/text()').extract()\n")

	spiderFile = open(projectName + "-spider.py", "w+") # create new tailored spider file
	contents = "".join(contents) # join contents into single string
	spiderFile.write(contents) # write to new spider file
	spiderFile.close() # close new spider file

def runScrapy(): # execute shell commands
	projectName = entries[0][1].get()
	projectSpiderName = projectName + "-spider.py"
	startProject = "scrapy startproject " + projectName # create new scrapy project
	moveSpider = "mv " + projectSpiderName + " " + projectName + "/" + projectName + "/spiders/" + projectSpiderName # install our custom spider
	runSpider = "scrapy runspider " + projectName + "/" + projectName + "/spiders/" + projectSpiderName + " -o data.csv -t csv" # run the spider
	subprocess.Popen(startProject.split(),stdout=subprocess.PIPE) # run in shell
	time.sleep(2) # wait for scrapy to build
	subprocess.Popen(moveSpider.split(),stdout=subprocess.PIPE) # run in shell
	subprocess.Popen(runSpider.split(),stdout=subprocess.PIPE) # run in shell

def cleanUp(): # clear gui fields
	projectName = entries[0][1].get() # get project name as string

	# remove first row (placeholder column headers)
	with open("data.csv","r") as dataFile: 
		with open(projectName + ".csv", "w") as outputFile:
			dataFile.next() # remove first row 
			for line in dataFile:
				outputFile.write(line)

	cleanup = "rm -r " + projectName + " && rm data.csv" # cleanup Scrapy files
	subprocess.Popen(cleanup.split(),stdout=subprocess.PIPE)

def scrape(): # high level function execution
	generateSpider() # generate custom spider
	runScrapy() # run scrapy
	time.sleep(1) # wait for runScrapy to finish
	cleanUp() # remove unnecessary files
 
##### MAIN ROUTINE #####
if __name__ == '__main__':
	root = tk.Tk() # root of gui
	root.title("Web Table Scraper") # set window title
	entries = generateForm(root, fields) # generate form gui
	scrapeButton = tk.Button(root,text="Scrape",command=scrape) # scrape button, calls scrape() when clicked
	scrapeButton.pack(side=RIGHT, padx=5, pady=5) # initialize scrape button
	root.mainloop() # run tkinter
