# Author: Jonathan Woong

#!/usr/bin/python

##### IMPORT STUFF #####

import Tkinter as tk
from Tkinter import *
import subprocess
import time

##### DATA STRUCTURES #####

userInput = {} # dictionary to store user input values
root = tk.Tk() # root of gui
root.title("Web Table Scraper")

##### METHODS #####

def getFields(): # stores user gui input into dictionary
	userInput['project'] = projectNameEntry.get() # get project name
	userInput['columns'] = columnField.get() # get number of columns
	userInput['url']  = urlEntry.get() # get url
	userInput['tableAttribute']  = tableAttributeEntry.get() # get table attribute
	userInput['tableAttributeValue'] = tableAttributeValueEntry.get() # get value of table attribute

def generateSpider(): # generates a Scrapy spider using user inputs
	with open(userInput['project'] + ".py", "w") as newSpiderFile: # creates new file
		newSpiderFile.write("import scrapy\n") 
		newSpiderFile.write("from scrapy import log\n")
		newSpiderFile.write("class tableItem(scrapy.Item):\n") # set Scrapy iterable
		for x in range(int(userInput['columns'])):
			newSpiderFile.write("\t_" + str(x) + " = scrapy.Field()\n")
		newSpiderFile.write("class itemSpider(scrapy.Spider):\n") # define spider class
		newSpiderFile.write("\tname = '" + userInput['project'] + "'\n")
		newSpiderFile.write("\tstart_urls = ['" + userInput['url'] + "']\n")
		newSpiderFile.write("\tdef parse(self, response):\n")
		newSpiderFile.write("\t\titem = tableItem()\n")
		newSpiderFile.write("\t\trows = response.xpath('//table[@" + userInput['tableAttribute'] + "\"=" + userInput['tableAttributeValue'] + "\"]/tr')\n") # identify table to scrape
		newSpiderFile.write("\t\tfor row in rows[1:]:\n")
		for x in range(int(userInput['columns'])):
			newSpiderFile.write("\t\t\titem['_" + str(x) + "'] = row.xpath('td[" + str(x + 1) + "]/text()').extract()\n") # scrape table rows based on attribute
		newSpiderFile.write("\t\t\tyield item")

def runScrapy(): # execute shell commands
	startProject = "scrapy startproject " + userInput['project'] # create new scrapy project
	moveSpider = "mv ./" + userInput['project'] + ".py ./" + userInput['project'] + "/" + userInput['project'] + "/spiders/" + userInput['project'] + "_spider.py" # install our custom spider
	runSpider = "scrapy runspider " + userInput['project'] + "/" + userInput['project'] + "/spiders/" + userInput['project'] + "_spider.py -o data.csv -t csv" # run the spider
	subprocess.Popen(startProject.split(),stdout=subprocess.PIPE)
	time.sleep(2) # wait for scrapy to build
	subprocess.Popen(moveSpider.split(),stdout=subprocess.PIPE)
	subprocess.Popen(runSpider.split(),stdout=subprocess.PIPE)

def cleanUp(): # clear gui fields
	cleanup = "rm -r " + userInput['project'] + " && rm " + userInput['project'] + ".py" # cleanup Scrapy files
	subprocess.Popen(cleanup.split(),stdout=subprocess.PIPE)
	projectNameEntry.delete(0,END) # clear project name
	columnField.set('1') # reset number of columns
	urlEntry.delete(0,END) # clear url
	tableAttributeEntry.delete(0,END) # clear table attribute
	tableAttributeValueEntry.delete(0,END) # clear attribute value

def scrape(): # high level function execution
	getFields() # get gui fields
	generateSpider() # generate custom spider
	runScrapy() # run scrapy
	time.sleep(1) # wait for runScrapy to finish
	cleanUp() # remove unnecessary files

##### GUI STUFF #####

projectNameLabel = tk.Label(root,text="Project Name: ").grid(row=0,column=0) # project name label
urlLabel = tk.Label(root,text="URL: ").grid(row=1,column=0) # url label
tableAttributeLabel = tk.Label(root,text="table attribute: ").grid(row=2,column=0) # table attribute label
tableAttributeValueLabel = tk.Label(root,text="table attribute value: ").grid(row=3,column=0) # attribute value label
columnLabel = tk.Label(root,text="Number of columns: ").grid(row=4,column=0) # column label

columnField = StringVar(root) # instantiate column field
columnField.set('1') # default value
columnMenu = OptionMenu(root,columnField,'1','2','3','4','5','6','7','8').grid(row=4,column=1) # drop down menu values

projectNameEntry = Entry(root) # instantiate project name
projectNameEntry.grid(row=0,column=1)
urlEntry = Entry(root) # instantiate url
urlEntry.grid(row=1,column=1)
tableAttributeEntry = Entry(root) # instantiate table attribute
tableAttributeEntry.grid(row=2,column=1)
tableAttributeValueEntry = Entry(root) # instantiate attribute value
tableAttributeValueEntry.grid(row=3,column=1)

scrapeButton = tk.Button(root,text="Scrape",command=scrape).grid(row=5,column=1) # scrape button, calls scrape() when clicked
 
root.mainloop() # run tkinter
