from django.urls import path

from vvpat.views import ApplyVoteView, CodeView, CountVoteView, DashboardView, PrintCodeView, VoteView, WelcomeView


urlpatterns = [
    path('', WelcomeView.as_view(), name="welcome"),
    path('code/', CodeView.as_view(), name="code"),
    path('output_print/', PrintCodeView.as_view(), name="output_print"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('vote/<str:uuid>', VoteView.as_view(), name="vote"),
    # path('count_vote/', CountVoteView.as_view(), name="count_vote"),
    # path('count_vote/', CountVoteView.as_view(), name="count_vote"),
    path('apply_vote/<str:uuid>', ApplyVoteView.as_view(), name="apply_vote"),
]
