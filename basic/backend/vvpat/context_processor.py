from .models import Voter
from django.core.cache import cache

def total_voters(req):
    voters_count = Voter.objects.count()
    voted_voters = Voter.objects.filter(is_voted=True)
    voted = voted_voters.count()
    slips = cache.get("counter")
    context = {
        "voters_count": voters_count,
        'voted': voted,
        'voted_voters': voted_voters,
        'slips': slips,
        }
    return context