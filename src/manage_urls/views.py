from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Url, Group

# Create your views here.


@login_required(login_url='/login/')
def add_new_url(request):
    if request.method == 'POST':
        new_url = request.POST['new_url']
        url = Url.objects.create(
            url=new_url,
            user=request.user,
            description=request.POST['description'],
        )
        url.save()
    return render(request, 'add_new_url.html')


@login_required(login_url='/login/')
def manage_urls(request):
    urls = Url.objects.filter(user=request.user)
    return render(
        request,
        template_name='manage_urls.html',
        context={"urls": urls}
    )


@login_required(login_url='/login/')
def add_new_group(request):
    if request.method == 'POST':
        new_group = request.POST['new_group']
        group = Group.objects.create(
            name=new_group,
            user=request.user,
            description=request.POST['description']
        )
        group.save()
    return render(
        request,
        template_name='new_group.html',
    )
