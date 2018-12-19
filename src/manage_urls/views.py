from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Url, Group, UnManagedUrl
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
import structlog

logger = structlog.get_logger()
# Create your views here.


@login_required(login_url="/login/")
def add_new_url(request):
    groups = Group.objects.filter(user=request.user)
    if request.method == "POST":
        group_id = (
            request.POST["group_id"] if "group_id" in request.POST else "0"
        )

        new_url = request.POST["new_url"]
        if group_id != "0":
            try:
                group = Group.objects.get(id=group_id)
                url = Url.objects.update_or_create(
                    url=new_url,
                    user=request.user,
                    group=group,
                    description=request.POST["description"],
                )
            except:
                print("Exception in find group")
        else:
            url = UnManagedUrl.objects.update_or_create(
                url=new_url,
                user=request.user,
                description=request.POST["description"],
            )

    return render(
        request, template_name="add_new_url.html", context={"groups": groups}
    )


@login_required(login_url="/login/")
def manage_urls(request):
    urls = UnManagedUrl.objects.filter(Q(user=request.user)).order_by(
        "-created_on"
    )
    groups = Group.objects.filter(user=request.user)
    return render(
        request,
        template_name="manage_urls.html",
        context={"urls": urls, "groups": groups},
    )


@login_required(login_url="/login/")
def add_new_group(request):
    if request.method == "POST":
        new_group = request.POST["new_group"]
        group = Group.objects.create(
            name=new_group,
            user=request.user,
            description=request.POST["description"],
        )
        group.save()
    return render(request, template_name="new_group.html")


@login_required(login_url="/login/")
def update_url_group(request):
    if "selected_urls[]" in request.POST and "group_id" in request.POST:
        group_id = request.POST["group_id"]
        selected_urls = request.POST.getlist("selected_urls[]")
        if group_id != "0":
            try:
                print(group_id)
                group = Group.objects.get(id=group_id)
                for url_id in selected_urls:
                    try:
                        un_manage_url = UnManagedUrl.objects.get(id=url_id)
                        url = Url.objects.create(
                            url=un_manage_url.url,
                            user=un_manage_url.user,
                            group=group,
                            description=un_manage_url.description,
                        )
                        un_manage_url.delete()
                        url.save()
                    except:
                        print("Exception in update url")
            except:
                print("Exception in find object")

    return HttpResponseRedirect("/manage_urls/")


def add_new_url_extension(request):
    logger.info("add_new_url_extension_api_request", user=request.user)

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Please Login First"})

    if request.user.is_authenticated and "url" in request.GET:
        url = request.GET["url"]
        if len(url) > 0:
            url = UnManagedUrl.objects.update_or_create(
                url=url, user=request.user
            )
            print(url)
            return JsonResponse(
                {"success": True, "result": "Saved Successfully"}
            )

    return JsonResponse({"success": False, "error": "Something went wrong"})


@login_required(login_url="/login/")
def managed_urls(request):
    logger.info(
        "managed_urls_api_request",
        user=request.user.email,
        method=request.method,
    )
    groups = Group.objects.filter(user=request.user)
    if request.method == "POST":
        group_id = (
            request.POST["group_id"] if "group_id" in request.POST else "0"
        )
        if group_id != "0":
            group = Group.objects.get(id=group_id)
            urls = Url.objects.filter(group=group, user=request.user).order_by(
                "-created_on"
            )
        else:
            urls = Url.objects.filter(user=request.user).order_by("-created_on")
    else:
        urls = Url.objects.filter(user=request.user).order_by("-created_on")
    return render(
        request=request,
        template_name="managed_urls.html",
        context={"urls": urls, "groups": groups},
    )


def test(request):
    if request.method == "POST":
        print("Post method")

    return HttpResponseRedirect(
        request=request,
        template_name="test.html"
    )
