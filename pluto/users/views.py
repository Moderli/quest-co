# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .forms import SignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .models import UserProfile, Question, Interest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question
from .forms import QuestionForm, CommentForm, AnswerForm
from django.contrib import messages
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to the login page after logging out
    return redirect('http://127.0.0.1:8000/accounts/login/')


def login_view(request):
    if request.user.is_authenticated:
        # If the user is already logged in, redirect to the home page
        return redirect('profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('http://127.0.0.1:8000/questions/')  # Redirect to the home page after successful login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import UserProfile, Question
from .forms import ProfileForm


def error_view(request, error_code=None):
    error_code= 505
    return render(request, 'error.html', {'error_code': error_code})



@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile does not exist, create a new one
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    form = ProfileForm(instance=user_profile)  # Initialize form here

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()

    # Fetch user's posted questions
    user_questions = Question.objects.filter(user=request.user)

    return render(request, 'profile.html', {'form': form, 'user_questions': user_questions})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string(
                'acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                'Please confirm your email address to complete the registration'
            )
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            'Thank you for your email confirmation. Now you can log in to your account.'
        )
    else:
        return HttpResponse('Activation link is invalid.')


from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name = "user"
    return render(request, 'index.html', {'user_name': user_name})

@login_required
def question_view(request):
    questions = Question.objects.all()
    form = QuestionForm()
    comment_form = CommentForm()
    answer_form = AnswerForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_view')
    return render(request, 'question_view.html', {'questions': questions, 'form': form, 'comment_form': comment_form, 'answer_form': answer_form})


# do not disturb from this line on
@login_required
def add_comment(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.save()
            return redirect('question_view')
    return render(request, 'question_view.html', {'form': form, 'question': question})


@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    form = AnswerForm()

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_view')

    return render(request, 'question_view.html', {'form': form, 'question': question})

def handler404(request, exception):
    return HttpResponse("404: Page not found")