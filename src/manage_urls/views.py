from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Url, Group
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.


@login_required(login_url='/login/')
def add_new_url(request):
    groups = Group.objects.filter(user=request.user)
    if request.method == 'POST':
        group_id = request.POST["group_id"] \
            if "group_id" in request.POST else '0'
        group = None
        if group_id != '0':
            try:
                group = Group.objects.get(id=group_id)
            except:
                print("Exception in find group")

        new_url = request.POST['new_url']
        url = Url.objects.create(
            url=new_url,
            user=request.user,
            group=group,
            description=request.POST['description'],
        )
        url.save()
    return render(
        request,
        template_name='add_new_url.html',
        context={"groups": groups}
    )


@login_required(login_url='/login/')
def manage_urls(request):
    urls = Url.objects.filter(
        Q(user=request.user) & Q(group__isnull=True)
    ).order_by('-created_on')
    groups = Group.objects.filter(user=request.user)
    return render(
        request,
        template_name='manage_urls.html',
        context={"urls": urls, "groups": groups},
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


def update_url_group(request):
    if "selected_urls[]" in request.POST and "group_id" in request.POST:
        group_id = request.POST["group_id"]
        selected_urls = request.POST.getlist("selected_urls[]")
        if group_id != '0':
            try:
                print(group_id)
                group = Group.objects.get(id=group_id)
                for url_id in selected_urls:
                    try:
                        url = Url.objects.get(id=url_id)
                        url.group = group
                        url.save()
                        print(url.group.id, url.url)
                    except:
                        print("Exception in update url")
            except:
                print("Exception in find object")

    return HttpResponseRedirect('/manage_urls/')


def add_new_url_extension(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "error": "Please Login"
        })

    if request.user.is_authenticated and "url" in request.GET:
        url = request.GET["url"]
        if len(url) > 0:
            url = Url.objects.create(
                url=url,
                user=request.user
            )
            url.save()
            return JsonResponse({
                "success": True,
                "result": "Saved Successfully"
            })

    return JsonResponse(
        {
            "success": False,
            "error": "Something went wrong"
        }
    )
