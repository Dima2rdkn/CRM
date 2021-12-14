from django.shortcuts import render


def references(request):
    return render(request, 'references/references.html')


def contacts(request):
    return render(request, 'references/contacts/detail.html')
