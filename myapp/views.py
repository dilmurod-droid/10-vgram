from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserProfileForm, PostForm, ChatMessageForm, UserRegisterProfileForm
from .models import Post, ChatMessage, Profile


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserRegisterProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterProfileForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile, created = Profile.objects.get_or_create(user=user)
    user_posts = Post.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile', username=user.username)
    else:
        p_form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'p_form': p_form, 'user': user, 'posts': user_posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.none()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts, 'users': users, 'query': query})

@login_required
def chat(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.recipient = recipient
            chat_message.save()
            return redirect('chat', recipient_id=recipient.id)
    else:
        form = ChatMessageForm()

    sent_messages = ChatMessage.objects.filter(sender=request.user, recipient=recipient)
    received_messages = ChatMessage.objects.filter(sender=recipient, recipient=request.user)
    chat_messages = sent_messages.union(received_messages).order_by('timestamp')

    return render(request, 'chat.html', {'form': form, 'recipient': recipient, 'chat_messages': chat_messages})

@login_required
def chat_view(request):
    current_user = request.user
    # Fetch all messages where the current user is either the sender or the recipient
    messages = ChatMessage.objects.filter(
        recipient=current_user
    ).select_related('sender') | ChatMessage.objects.filter(
        sender=current_user
    ).select_related('recipient')

    # Initialize sets for senders and recipients
    senders = set()
    recipients = set()

    # Populate senders and recipients sets
    for message in messages:
        if message.recipient == current_user:
            senders.add(message.sender)
        elif message.sender == current_user:
            recipients.add(message.recipient)

    # Move users from recipients to senders if they have replied
    for recipient in list(recipients):
        if ChatMessage.objects.filter(sender=current_user, recipient=recipient).exists():
            recipients.remove(recipient)
            senders.add(recipient)

    # Prepare senders and recipients info
    senders_info = [{'username': sender.username, 'id': sender.id}
                    for sender in senders]
    recipients_info = [
        {'username': recipient.username,
         'profile_picture': "https://www.vecteezy.com/vector-art/439863-vector-users-icon", 'id': recipient.id}
        for recipient in recipients]

    return render(request, 'chats.html', {'senders_info': senders_info, 'recipients_info': recipients_info})
@login_required
def reels(request):
    videos = Post.objects.exclude(video__isnull=True).order_by('-created_at')
    return render(request, 'reels.html', {'videos': videos})
