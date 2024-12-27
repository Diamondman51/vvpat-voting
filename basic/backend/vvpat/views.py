# from django.shortcuts import render
import datetime
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.template.response import TemplateResponse
from django.contrib.auth import login
import random
from .forms import CustomTextWidgetForm

from .models import Director, President, Voter, User


class CodeView(View):
    def get(self, request,) -> TemplateResponse:
        form = CustomTextWidgetForm()
        context = {
            'form': form,
        }
        return TemplateResponse(request, 'printQrcode.html', context)


class PrintCodeView(View):
    # def get(self, request) -> TemplateResponse:
    #     qrcode = random.randint(1000000, 9999999)
    #     context = {
    #         'qrcode': qrcode,
    #     }
    #     return TemplateResponse(request, 'outputPrint.html', context)

    def post(self, request, *args,) -> TemplateResponse:
        print('PrintCode post: ', request.POST)
        qrcode = random.randint(1000000, 9999999)
        phone = request.POST.get("phone")
        user = get_object_or_404(User, phone=phone)
        uuid = user.uuid
        voter = get_object_or_404(Voter, user_id=uuid)
        print("Phone", voter)
        context = {
            'qrcode': uuid,
        }
        return TemplateResponse(request, "outputPrint.html", context)

class WelcomeView(View):
    def get(self, request) -> TemplateResponse:
        return TemplateResponse(request, "welcome.html",)


class DashboardView(View):
    def post(self, request) -> TemplateResponse:
        return TemplateResponse(request, "dashboard.html",)


class VoteView(View):
    def get(self, request, uuid) -> TemplateResponse:

        directors = Director.objects.all()
        presidents = President.objects.all()
        data = [directors[i:i+2] for i in range(0, len(directors), 2)]
        current_time = datetime.datetime.now().strftime("%d %B, %Y")
        print('DATA', data)
        context = [
            {"counter": i, "directors": raw} for i, raw in enumerate(data, start=1)
        ]
        context = {
            'data': context,
            'time': current_time,
            'presidents': presidents,
            "uuid": uuid,
        }
        print(context)
        return TemplateResponse(request, "index copy.html", context)
    

class CountVoteView(View):
    def get(self, request) -> TemplateResponse:
        return TemplateResponse(request, "countVote.html",)


class PostMeth(View):
    def post(self, request, uuid) -> TemplateResponse:
        print("--------------------------------------------------------")
        data = json.loads(request.body)
        print('Body: ', data)
        president = data.get('president')
        print('President: ', president)
        directors: list = data.get("directors")
        print('Directors: ', directors)

        return HttpResponse('Success')
