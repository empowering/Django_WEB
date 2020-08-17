from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value = 1, max_value = 10)

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render(request, "tasks/index.html",
    {
        # html takes : python takes
        "tasks" : request.session["tasks"]
    })

def add(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewTaskForm(request.POST)

         # Check if form data is valid (server-side)       
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            task = form.cleaned_data["task"]
            # Add the new task to our list of tasks
            request.session["tasks"] += [task]
            # redirect
            return HttpResponseRedirect(reverse("tasks:index"))

        else:
            return render(request, "tasks/add.html",
            {
                "form" : form
            })

    return render(request, "tasks/add.html",
    {
        "form" : NewTaskForm()
    })

