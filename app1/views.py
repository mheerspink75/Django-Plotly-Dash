from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect

from app1.dashapps import stock_charts2
from app1.dashapps import crypto_quotes


##### Main Pages #####

def home(request):
    return render(request, 'app1/pages/index.html')


def DASHBOARD(request):
    return render(request, 'app1/pages/DASHBOARD.html')


def stocks(request):
    return render(request, 'app1/pages/stocks.html')


def account(request):
    return render(request, 'app1/pages/account.html')



#### Registration/Login #####

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = RegisterForm()
    return render(response, 'registration/register.html', {"form":form})


#### Jinja Test ####





























##### User Lists #####

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():

        if response.method == "POST":
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                else:
                    item.complete = False
        
                item.save()
    
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
        
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")
    
    
        return render(response, "app1/pages/list.html", {"ls":ls})
    
    return render(response, "app1/pages/view.html", {})


def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect("/%i" %t.id)

    else:
        form = CreateNewList()

    return render(response, "app1/pages/create.html", {"form":form})


def view(response):
    return render(response, "app1/pages/view.html", {})


