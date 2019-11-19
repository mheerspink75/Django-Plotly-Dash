from django.shortcuts import render


def register(request):
    return render(request, 'accounts/register.html')