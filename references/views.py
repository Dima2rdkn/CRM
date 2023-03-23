from django.shortcuts import render


def references(request):
    return render(request, 'references/references.html')

