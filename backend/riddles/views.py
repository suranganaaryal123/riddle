#views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Riddle, UserAnswer
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm

@login_required
def riddles_list(request):
    riddles = Riddle.objects.all()  # Fetch all riddles
    return render(request, 'riddles_list.html', {'riddles': riddles})

# View to handle submitting an answer
from django.shortcuts import render, get_object_or_404, redirect
from .models import Riddle, UserAnswer
from django.contrib import messages

def submit_answer(request, riddle_id):
    riddle = get_object_or_404(Riddle, id=riddle_id)

    # Check if the user has already answered this riddle
    user_answered = UserAnswer.objects.filter(
        user_name=request.user.username if request.user.is_authenticated else 'Guest',
        riddle=riddle
    ).exists()  # Check if any answer exists for this riddle by the user
    
    if user_answered:
        messages.info(request, "You have already answered this riddle.")
        return redirect('riddles:riddles_list')  # Redirect back to the riddles list if they have already answered

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        # Check if the user's answer is correct
        correct = user_answer.lower() == riddle.answer.lower()

        # Save the user's answer and whether it was correct
        UserAnswer.objects.create(
            user_name=request.user.username if request.user.is_authenticated else 'Guest',  # Use Django's username if logged in
            riddle=riddle,
            answer=user_answer,
            correct=correct
        )

        if correct:
            messages.success(request, "Correct answer! Your score has been updated.")
        else:
            messages.error(request, "Incorrect answer! Try again.")

        # Redirect to the riddles list after submitting an answer
        return redirect('riddles:riddles_list')

    return render(request, 'submit_answer.html', {'riddle': riddle})


def leaderboard(request):
    # Aggregate user scores based on the number of correct answers
    leaderboard_data = (
        UserAnswer.objects.filter(correct=True)
        .values('user_name')
        .annotate(score=Count('id'))
        .order_by('-score')  # Order by score descending
    )

    # Add rankings (enumerate starts at 1 for ranking)
    leaderboard_with_rank = [
        {'rank': rank + 1, 'user_name': entry['user_name'], 'score': entry['score']}
        for rank, entry in enumerate(leaderboard_data)
    ]

    return render(request, 'leaderboard.html', {'leaderboard': leaderboard_with_rank})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('riddles:riddles_list')  # Redirect to the riddles list page
    return render(request, 'login.html')  

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # Automatically log in the user after successful registration
            user = form.save(commit=False)
            login(request, user)
            return redirect('riddles:riddles_list')  # Redirect to riddles list or another page after login
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})