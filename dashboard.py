import tkinter as tk
from tkinter import *
import os
import ast
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import importlib
import multiprocessing
import hashlib
from crawlinator.spiders import tor


def findCrawlers():
    listbox.delete('0', 'end')
    default_path = "crawlinator/spiders"
    files = [fl for fl in os.listdir(default_path) if fl.endswith('.py') and not fl == "__init__.py"]

    for file in files:
        listbox.insert(END, file)

    return files


def runCrawler(crawlerName):
    className = getClassName(crawlerName)
    crawlerObject = import_from("crawlinator.spiders." + crawlerName[:-3], className)
    try:
        if crawlerObject.login_password:
            openCrawlSpiderWithLoginPasswordPlease(crawlerObject, className, crawlerName)
    except:
        p = multiprocessing.Process(target=runCrawlerScript, args=(crawlerName, className))
        p.start()

        btnStop = tk.Button(frame, text="Stop crawling " + className, padx="10", pady="10", fg="black", bg="#f8f8f8",
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


def openCreateNewLoginScraper():
    newWindow = tk.Toplevel(root, bg="#FFC0CB")
    label = Label(newWindow, text="Crawler name", bg="#FFC0CB")
    label.pack()
    nameTextbox = tk.Entry(newWindow, width=25, bg="#FFC0CB")
    nameTextbox.pack()
    label = Label(newWindow, text="Start url", bg="#FFC0CB")
    label.pack()
    startUrlTextbox = tk.Entry(newWindow, width=25, bg="#FFC0CB")
    startUrlTextbox.pack()
    label = Label(newWindow, text="Login url", bg="#FFC0CB")
    label.pack()
    loginUrlTextbox = tk.Entry(newWindow, width=25, bg="#FFC0CB")
    loginUrlTextbox.pack()
    label = Label(newWindow, text="Username", bg="#FFC0CB")
    label.pack()
    usernameTextbox = tk.Entry(newWindow, width=25, bg="#FFC0CB")
    usernameTextbox.pack()
    label = Label(newWindow, text="Password", bg="#FFC0CB")
    label.pack()
    passwordTextbox = tk.Entry(newWindow, show="*", width=25, bg="#FFC0CB")
    passwordTextbox.pack()
    btnAddCrawler = tk.Button(newWindow, text="Create crawler", padx="10", pady="10", fg="black", bg="#f8f8f8",
                              command=lambda: createNewScript(usernameTextbox.get(),
                                                              hashPassword(passwordTextbox.get()),
                                                              startUrlTextbox.get(), loginUrlTextbox.get(),
                                                              nameTextbox.get()))
    btnAddCrawler.pack()


def runPasswordCrawler(crawlerObject, className, password, crawlerName):
    if checkHash(crawlerObject.login_password, password):
        crawlerObject.login_password = password

        p = multiprocessing.Process(target=runCrawlerScript, args=(crawlerName, className))
        p.start()

        btnStop = tk.Button(frame, text="Stop crawling " + className, padx="10", pady="10", fg="black", bg="#f8f8f8",
                            command=lambda: stopCrawler(p, btnStop))
        btnStop.pack()
    else:
        print("wachtwoord fout")


def openCrawlSpiderWithLoginPasswordPlease(crawlerObject, className, crawlerName):
    newWindow = tk.Toplevel(root, bg="#FFC0CB")
    label = Label(newWindow, text="Crawler password", bg="#FFC0CB")
    label.pack()
    crawlerPasswordTextbox = tk.Entry(newWindow,show="*", width=25, bg="#FFC0CB")


    crawlerPasswordTextbox.pack()
    btnRunCrawler = tk.Button(newWindow, text="Create crawler", padx="10", pady="10", fg="black", bg="#f8f8f8",
                              command=lambda: runPasswordCrawler(crawlerObject, className, crawlerPasswordTextbox.get(), crawlerName))
    btnRunCrawler.pack()


def hashPassword(password):
    salt = "éJ!L@iL^9;1n#çàé"
    user_password = password
    sha = hashlib.sha512()
    sha.update((user_password + salt).encode('utf-8'))
    encrypted = sha.hexdigest()
    return encrypted


def checkHash(savedHashPassword, inputPassword):
    if savedHashPassword == hashPassword(inputPassword):
        return True
    else:
        return


def createNewScript(username, password, url, loginUrl, name):
    if username == "" and password == "" and loginUrl == "":
        newScript = "from scrapy.linkextractors import LinkExtractor\nfrom scrapy.spiders import CrawlSpider, " \
                    "Rule\nfrom crawlinator.items import crawlinatorItem\nimport hashlib\nclass " + name + "Spider(" \
                                                                                                           "CrawlSpider):\n    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]\n    name = '" + name + "'\n    allowed_domains = ['" + url + "']\n    start_urls = ['" + url + "']\n    custom_settings = {\n        'LOG_FILE': 'logs/" + name + ".log',\n        'LOG_LEVEL': 'INFO'\n    }\n    rules = (\n        Rule(\n            LinkExtractor(\n                tags='a',\n                attrs='href',\n                unique=True\n            ),\n            callback='parse_item',\n            follow=True\n        ),\n    )\n    def parse_item(self, response):\n        item = crawlinatorItem()\n        item['id'] = hashlib.sha256(response.url.encode('utf-8')).hexdigest()\n        item['title'] = response.css('title::text').extract_first()\n        item['url'] = response.url\n        item['status'] = response.status\n        item['body'] = response.text\n        return item "
        with open("crawlinator/spiders/" + name + ".py", "w") as text_file:
            print(newScript, file=text_file)
    else:
        newScript = "from crawlinator.items import crawlinatorItem\nimport scrapy\nfrom loginform import " \
                    "fill_login_form\nfrom scrapy.linkextractors import LinkExtractor\nfrom scrapy.spiders import " \
                    "CrawlSpider, Rule\nimport hashlib\nclass " + name + "Spider(CrawlSpider):\n    " \
                                                                         "handle_httpstatus_list = [400, 403, 404, " \
                                                                         "500, 502, 503, 504]\n    name = '" + name + \
                    "'\n    allowed_domains = ['onion']\n    start_urls = ['" + url + "']\n    login_url = '" + \
                    loginUrl + "'\n    login_password = '" + password + "'\n    login_user = '" + username + "'\n    " \
                                                                                                             "custom_settings = {\n        'LOG_FILE': 'logs/" + name + ".log',\n        'LOG_LEVEL': 'INFO'\n " \
                                                                                                                                                                        "   }\n    rules = (\n        Rule(\n  " \
                                                                                                                                                                        "          LinkExtractor(\n            " \
                                                                                                                                                                        "    tags='a',\n                " \
                                                                                                                                                                        "attrs='href',\n                " \
                                                                                                                                                                        "unique=True\n            )," \
                                                                                                                                                                        "\n            callback='parse_item'," \
                                                                                                                                                                        "\n            follow=True\n        )," \
                                                                                                                                                                        "\n    )\n    def start_requests(" \
                                                                                                                                                                        "self):\n        yield scrapy.Request(" \
                                                                                                                                                                        "self.login_url, self.parse_login)\n   " \
                                                                                                                                                                        " def parse_login(self, response):\n   " \
                                                                                                                                                                        "     data, url, " \
                                                                                                                                                                        "method = fill_login_form(" \
                                                                                                                                                                        "response.url, response.body, " \
                                                                                                                                                                        "self.login_user, " \
                                                                                                                                                                        "self.login_password)\n        return " \
                                                                                                                                                                        "scrapy.FormRequest(url, " \
                                                                                                                                                                        "formdata=dict(data), method=method, " \
                                                                                                                                                                        "callback=self.start_crawl)\n    " \
                                                                                                                                                                        "def start_crawl(self, response):\n    " \
                                                                                                                                                                        "    for url in self.start_urls:\n     " \
                                                                                                                                                                        "       yield scrapy.Request(url)\n    " \
                                                                                                                                                                        "def parse_item(self, response):\n     " \
                                                                                                                                                                        "   item = crawlinatorItem()\n        " \
                                                                                                                                                                        "item['id'] = hashlib.sha256(" \
                                                                                                                                                                        "response.url.encode(" \
                                                                                                                                                                        "'utf-8')).hexdigest()\n        item[" \
                                                                                                                                                                        "'title'] = response.css(" \
                                                                                                                                                                        "'title::text').extract_first()\n      " \
                                                                                                                                                                        "  item['url'] = response.url\n        " \
                                                                                                                                                                        "item['status'] = response.status\n    " \
                                                                                                                                                                        "    item['body'] = response.text\n    " \
                                                                                                                                                                        "    return item "
        with open("crawlinator/spiders/" + name + ".py", "w") as text_file:
            print(newScript, file=text_file)


if __name__ == "__main__":

    root = tk.Tk()

    canvas = tk.Canvas(root, height=500, width=500, bg='#ffffff')
    canvas.pack()

    frame = tk.Frame(root, bg="#FFC0CB")
    frame.place(relwidth=1, relheight=1)

    label = Label(frame, text="Crawlinator Dashboard", bg="#FFC0CB")
    label.config(font=("Courier", 22))
    label.pack()

    listbox = Listbox(frame)
    listbox.pack()

    findCrawlers()

    btnRefresh = tk.Button(frame, text="Refresh Crawlers", padx="10", pady="10", fg="black", bg="#f8f8f8",
                           command=findCrawlers)
    btnRefresh.pack()

    btnCrawl = tk.Button(frame, text="Crawl", padx="10", pady="10", fg="black", bg="#f8f8f8",
                         command=lambda: runCrawler(listbox.get(listbox.curselection())))
    btnCrawl.pack()

    buttonExample = tk.Button(frame,
                              text="Create new crawler with login", padx="10", pady="10", fg="black", bg="#f8f8f8",
                              command=openCreateNewLoginScraper)
    buttonExample.pack()

    label = Label(frame, text="Running crawlers:", bg="#FFC0CB")
    label.pack()

    root.mainloop()
