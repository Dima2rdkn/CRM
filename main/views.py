from django.shortcuts import render

def main(request):
    return render(request, 'main/mainpage.html')

def admin(request):
    return render(request, 'main/admin.html')
