from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from kura import forms
from .models import Poll, Choice
from .forms import CandidateForm
from django.core.mail import send_mail
from .models import Voter



def home(request):
    return render(request, 'kura/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'kura/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'kura/profile.html')

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'kura/poll_detail.html', {'poll': poll})

def vote(request, poll_id):
    if request.method == "POST":
        poll = get_object_or_404(Poll, pk=poll_id)
        try:
            selected_choice = poll.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'kura/poll_detail.html', {
                'poll': poll,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return redirect('polls:results', poll_id=poll.id)    

def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidates')
    else:
        form = CandidateForm()
    return render(request, 'kura/add_candidate.html', {'form': form})

@login_required
def register_voter(request):
    voter = Voter.objects.create(user=request.user)
    subject = 'Your voter ID'
    message = 'Your voter ID is: ' + voter.voter_id
    recipient_list = [request.user.email]
    send_mail(subject, message, 'sender@example.com', recipient_list)
    return redirect('home')    