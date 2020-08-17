import markdown2
import random

from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect


from . import util

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))  

class NewWikiForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label ='')

class EditWikiForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='')


# List View
def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        
        if form.is_valid():
            item = form.cleaned_data["item"]

            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdown2.markdown(page)
                    
                    context = {
                        'content': page_converted,
                        'title': item,
                        'form': Search()
                    }
                    return render(request, "encyclopedia/entry.html", context)
                
                if item.lower() in i.lower(): 
                    searched.append(i)
                    context = {
                        'content': searched, 
                        'form': Search()
                    }
                    return render(request, "encyclopedia/search.html", context)
                
            return render(request, "encyclopedia/error.html", {"message" : "WORD IS NOT FOUND" , "errnum" : 100, 'form': Search()})

        else:
            return render(request, "encyclopedia/index.html", {"form": form})

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })

# 단어 누르면 상세 설명 페이지로
def entry(request, title):
    entries = util.list_entries()

    if title in entries :
        content = util.get_entry(title)
        content = markdown2.markdown(content)

        context = {
            'content' : content,
            'title' : title,
            'form': Search()
        }
        return render(request, "encyclopedia/entry.html",context)
    else :
        return render(request, "encyclopedia/error.html", {"message" : "WORD IS NOT FOUND" , "errnum" : 100, 'form': Search()})


# 새로운 단어 추가
def add(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewWikiForm(request.POST)

         # Check if form data is valid (server-side)       
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()

            if title not in entries :

                # save as dict
                newdata = {
                    "title": title,
                    "content": content,
                    'form': Search()
                    }
                # setup the filepath
                path_folder="./entries" 
                md_file = "{}/{}.md".format(path_folder, title)
                with open(md_file, 'w') as f:
                    f.write(content)
                return HttpResponseRedirect(reverse("index"))

            else :
                return render(request, "encyclopedia/error.html", {"message" : "Already  WIKI" , "errnum" : 200})

            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "encyclopedia/add.html",
            {
                "form" : form
            })

    return render(request, "encyclopedia/add.html",
    {
        "form" : NewWikiForm()
    })


# 내용 수정하기
def edit(request, title):
    if request.method == "POST":
    
        # Take in the data the user submitted and save it as form
        form = EditWikiForm(request.POST)

         # Check if form data is valid (server-side)       
        if form.is_valid():
            content = form.cleaned_data["content"]
            entries = util.list_entries()

            # save as dict
            newdata = {
                "form": Search(),
                "title": title,
                "content": content
                }
            # setup the filepath
            path_folder="./entries" 
            md_file = "{}/{}.md".format(path_folder, title)
            with open(md_file, 'w') as f:
                f.write(content)
            return HttpResponseRedirect(reverse("index"))

        else:
            content = {
                "form": Search(),
                "edit" : form
                }
            return render(request, "encyclopedia/edit.html", content)
    
    else :
        page = util.get_entry(title)
        context = {
            'form': Search(),
            'edit': EditWikiForm(initial={'content': page}),
            'title': title
        }
        return render(request, "encyclopedia/edit.html", context)


    return render(request, "encyclopedia/edit.html",
    {
        "form" : EditWikiForm()
    })


# 랜덤 페이지 -> entry랑 거의 유사
# 그냥 있는 페이지 골라서 전달하는 방법은 없나 ?
def randpage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)

        title = entries[num]
        content = util.get_entry(title)
        content = markdown2.markdown(content)

        context = {
            'form': Search(),
            'content' : content,
            'title' : title
        }
        return render(request, "encyclopedia/entry.html", context)

