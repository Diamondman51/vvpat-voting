# from django.shortcuts import render
import datetime
from hashlib import sha256
import json
from typing import Union
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
    def get(self, request) -> TemplateResponse:
        return TemplateResponse(request, "dashboard.html",)


class VoteView(View):
    def get(self, request, uuid) -> TemplateResponse:
        directors = Director.objects.all()
        presidents = President.objects.all()
        data = [directors[i:i+2] for i in range(0, len(directors), 2)]
        current_time = datetime.datetime.now().strftime("%d %B, %Y")
        # print('DATA', data)
        context = [
            {"counter": i, "directors": raw} for i, raw in enumerate(data, start=1)
        ]
        context = {
            'data': context,
            'time': current_time,
            'presidents': presidents,
            "uuid": uuid,
        }
        # print(context)
        return TemplateResponse(request, "index.html", context)
    
    def post(self, request, uuid) -> TemplateResponse:
        return TemplateResponse(request, "",)


class CountVoteView(View):
    def get(self, request) -> TemplateResponse:
        return TemplateResponse(request, "countVote.html",)


class ApplyVoteView(View):
    def post(self, request, uuid) -> Union[HttpResponse, TemplateResponse]:
        user = User.objects.get(uuid=uuid)
        voter = Voter.objects.get(user_id=user)
        print(voter.is_voted)
        if not voter.is_voted:
            try:
                data = json.loads(request.body)
                print('Body: ', data)
                president = data.get('president')
                president = President.objects.get(membership_num=president.get('mem_num'))
                voter.president_id = sha256(str(president.pk).encode("utf-8")).hexdigest()
                directors: list = data.get("directors")
                for director in directors:
                    pass
                    # voter.directors_id.append(sha256(str()))
                print('President: ', president)
                print('Directors: ', directors)

                return TemplateResponse(request, 'dashboard.html')
            except Exception as e:
                print("Error Handled: ", e)
                return HttpResponse("Error Handled: ", e)
