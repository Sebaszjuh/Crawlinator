import tkinter as tk
from tkinter import *
import os
from pathlib import Path
from inspect import getmembers, isfunction, ismethod, isclass
import ast
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import importlib
import multiprocessing

def findCrawlers():
    listbox.delete('0', 'end')
    default_path = "crawlinator/spiders"
    files = [fl for fl in os.listdir(default_path) if fl.endswith('.py')]

    for file in files:
        listbox.insert(END, file)

    return files

def runCrawler(crawlerName):
    className = getClassName(crawlerName)

    p = multiprocessing.Process(target=runCrawlerScript, args=(crawlerName, className))
    p.start()

    btnStop = tk.Button(frame, text="Stop crawler " + className, padx="10", pady="10", fg="black", bg="#f8f8f8",
                        command=lambda: stopCrawler(p, btnStop))
    btnStop.pack()

def runCrawlerScript(crawlerName, className):
    import_from("crawlinator.spiders." + crawlerName[:-3], className)
    process = CrawlerProcess(get_project_settings())
    process.crawl(crawlerName[:-3])
    process.start()

def stopCrawler(process, btnStop):
    process.terminate()
    btnStop.pack_forget()
'''
dynamically import stuff with variables
'''
def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

'''
Used to get the class name of a python file. We need this in order to generate the code to run the crawler.
'''
def getClassName(crawlerName):
    default_path = "crawlinator/spiders"
    filename = default_path + "/" + crawlerName
    print(filename)
    with open(filename) as file:
        node = ast.parse(file.read())
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    for class_ in classes:
        return class_.name


if __name__ == "__main__":
    root = tk.Tk()

    canvas = tk.Canvas(root, height=500, width=300, bg='#ffffff')
    canvas.pack()

    frame = tk.Frame(root, bg="#FFC0CB")
    frame.place(relwidth=1, relheight=1)

    listbox = Listbox(frame)
    listbox.pack()

    findCrawlers()

    btnAddLogin = tk.Button(frame, text="Refresh Crawlers", padx="10", pady="10", fg="black", bg="#f8f8f8",
                            command=findCrawlers)
    btnAddLogin.pack()

    btnCrawl = tk.Button(frame, text="Crawl", padx="10", pady="10", fg="black", bg="#f8f8f8",
                         command=lambda: runCrawler(listbox.get(listbox.curselection())))
    btnCrawl.pack()

    label = Label(frame, text="Running crawlers:", bg="#FFC0CB")
    label.pack()

    root.mainloop()