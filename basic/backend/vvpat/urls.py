from django.urls import path

from vvpat.views import ApplyVoteView, CodeView, CountVoteView, DashboardView, OMRCountVote, ResetView, SetQBooths, VoteView, WelcomeView


urlpatterns = [
    path('', WelcomeView.as_view(), name="welcome"),
    path('code/', CodeView.as_view(), name="code_out"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('vote/<str:uuid>', VoteView.as_view(), name="vote"),
    path('apply_vote/<str:uuid>', ApplyVoteView.as_view(), name="apply_vote"),
    path('set-the-quantity-of-booth/', SetQBooths.as_view(), name="set_booth"),
    path('count_vote/', CountVoteView.as_view(), name="count_vote"),
    path('omr_count_vote/', OMRCountVote.as_view(), name="omr_count_vote"),
    path('reset/', ResetView.as_view(), name="reset"),
]
