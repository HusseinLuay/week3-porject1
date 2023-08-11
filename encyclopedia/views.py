from django.shortcuts import render

from . import util
from markdown2 import Markdown

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdown = Markdown()
    if content == None :
        return None
    else:
        return markdown.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request,"encyclopedia/error.html" , {"message":"This entry dose not exist"})
    else:
        return render(request,"encyclopedia/entry.html" , {"title" : title , "content" : html_content})
    

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request,"encyclopedia/entry.html" , {"title" : entry_search , "content" : html_content})
        else:
            AllEntries = util.list_entries()
            recommandation = []
            for entry in AllEntries :
                if entry_search.lower() in entry.lower():
                    recommandation.append(entry)
            return render (request , 'encyclopedia/search.html' , {"recommandation":recommandation})
        

def create_new_page(request):
    if request.method == "GET":
        return render ( request , "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title) #check if the entry is already exist 
        if titleExist is not None : #this mean that entry and title is already exist 
            return render ( request , "encyclopedia/error.html" , {"message":"Sorry , this Entry is already exist"})
        else:
            util.save_entry(title,content)
            html_content = convert_md_to_html(title)
            return render ( request , "encyclopedia/entry.html" , {"title":title , "content":html_content})
        

def edit_entry(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render ( request , "encyclopedia/edit.html" , {"title":title , "content":content})
    
def save_editing(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        html_content = convert_md_to_html(title)
        return render ( request , "encyclopedia/entry.html" , {"title":title , "content":html_content})
    
import random
def random_page(request):
    Entries = util.list_entries()
    random_entry = random.choice(Entries)
    html_content = convert_md_to_html(random_entry)
    return render(request , "encyclopedia/entry.html" , {"title":random_entry , "content" : html_content })

        






