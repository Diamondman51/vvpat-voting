# from django.shortcuts import render
import datetime
from django.core.cache import cache
from hashlib import sha256
from typing import Union
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.template.response import TemplateResponse
from .forms import CustomTextWidgetForm
import sweetify
from .models import Director, President, Voter, User
from celery import shared_task


class CodeView(View):
    cache.set('counter', 0, None)
    def get(self, request,) -> TemplateResponse:
        form = CustomTextWidgetForm()
        context = {
            'form': form,
        }
        return TemplateResponse(request, 'printQrcode.html', context)

    def post(self, request) -> TemplateResponse:
        print('PrintCode post: ', request.POST)
        phone = request.POST.get("phone")
        try:
            user = User.objects.get(phone=phone)
            uuid = user.uuid
            if user.is_employee:
                voter = Voter.objects.get(user_id=uuid)

                if not voter.is_registered:
                    # form = CustomTextWidgetForm()
                    # context = {
                    #     'form': form,
                    # }
                    sweetify.warning(request, f'Dear {voter.first_name} {voter.last_name} you are not registered!!!', timer=3000)
                    return TemplateResponse(request, 'dashboard.html')
                elif voter.is_voted:
                    sweetify.info(request, f'Dear {voter.first_name} {voter.last_name}, you have voted!!!', timer=3000)
                    return redirect('dashboard')
                BOOTHS = cache.get("BOOTHS")
                booth = cache.get('counter') % BOOTHS

                if not booth:
                    booth = BOOTHS
                context = {
                    'booth': booth,
                    'qrcode': str(uuid),
                }
                sweetify.success(request, 'Your operation was successful!', timer=1000)
                cache.incr("counter", 1)                
                return TemplateResponse(request, "outputPrint.html", context)

            else:
                sweetify.info(request, "You are not noted as Employee!!!")
                return redirect("code_out")

        except User.DoesNotExist or Voter.DoesNotExist:
            sweetify.error(request, 'Can not find the Voter')
            return redirect("code_out")



class WelcomeView(View):
    def get(self, request) -> TemplateResponse:
        return TemplateResponse(request, "welcome.html",)


class DashboardView(View):
    def get(self, request) -> TemplateResponse:
        is_all_voted = False
        voters = Voter.objects.all()
        if voters.filter(is_voted=True).count() == voters.count():
            is_all_voted = True
        context = {
            'is_all_voted': is_all_voted,
            'timer': cache.get('timer'),
        }
        return TemplateResponse(request, "dashboard.html", context)


class VoteView(View):
    def get(self, request, uuid) -> TemplateResponse:
        # president_vote_form = PresidentVoteForm()
        # director_formset = DirectorFormSet(queryset=Director.objects.all())
        directors = Director.objects.all()
        presidents = President.objects.all()
        # data = [directors[i:i+2] for i in range(0, len(directors), 2)]
        data = [directors[i:i+2] for i in range(0, len(directors), 2)]
        # data = [director_formset[i:i+2] for i in range(0, len(director_formset), 2)]
        current_time = datetime.datetime.now().strftime("%d %B, %Y")
        # print('DATA', data)
        context = [
            {"counter": i, "directors": raw} for i, raw in enumerate(data, start=1)
        ]
        context = {
            'data': context,
            'time': current_time,
            'presidents': presidents,
            # 'presidents': president_vote_form,
            "uuid": uuid,
        }
        # print(context)
        return TemplateResponse(request, "index.html", context)


class CountVoteView(View):
    def get(self, request) -> TemplateResponse:
        return TemplateResponse(request, "countVote.html",)


class ApplyVoteView(View):
    def post(self, request, uuid) -> Union[HttpResponse, TemplateResponse]:
        try:
            voter = Voter.objects.get(user_id=uuid)
            if not voter.is_voted:
                selected_president_id: str = request.POST.get('selected_president')
                
                selected_director_ids: list = request.POST.getlist('selected_directors')
                voter.president_vote = sha256(selected_president_id.encode("utf-8")).hexdigest()
                for director in selected_director_ids:
                    voter.directors_vote.append(sha256(director.encode("utf-8")).hexdigest())
                voter.is_voted = True
                voter.save()
                
                print("Selected President ID:", selected_president_id)
                print("Selected Director IDs:", selected_director_ids)
                sweetify.success(request, f"Dear {voter.first_name} {voter.last_name} your vote has been counted", timer=3000)
                return redirect('dashboard')
            else:
                sweetify.info(request, f"Dear {voter.first_name} {voter.last_name} you have voted, that is why your vote UNCOUNTED")
                return redirect('dashboard')
        except Exception as e:
            print("Error handled: ", e)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SetQBooths(View):
    def get(self, request,) -> TemplateResponse:
        return TemplateResponse(request, 'booths.html')
    
    def post(self, request) -> TemplateResponse:
        booth = request.POST.get("booth")
        cache.set('BOOTHS', int(booth), 60*60*24)
        cache.set('timer', True, 60*60*18)
        

        return redirect("code_out")
    
    @shared_task
    def timer(self):
        cache.set('timer', False, 60*60*18)