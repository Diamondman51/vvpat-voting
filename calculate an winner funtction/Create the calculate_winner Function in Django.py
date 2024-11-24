from django.shortcuts import render
from collections import Counter
from .models import Vote

def calculate_winner(request):
    # Fetch all votes from the database
    votes = Vote.objects.values_list('candidate', flat=True)

    # Count votes for each candidate
    vote_count = Counter(votes)

    # Determine the winner (candidate with the most votes)
    if vote_count:
        winner, max_votes = vote_count.most_common(1)[0]
    else:
        winner, max_votes = None, 0

    # Pass the results to the template or return as JSON
    context = {
        'winner': winner,
        'max_votes': max_votes
    }
    return render(request, 'winner.html', context)
