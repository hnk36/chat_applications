from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from .models import ChatRoom, Contact, Message, Conversation
from django.db import DatabaseError


def main(request):
    return render(request, 'main.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')


def base(request):
    return render(request, 'base.html')


def create_room(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('room_name')

        # Check if username and room_name are provided
        if not username or not room_name:
            return HttpResponseBadRequest('Missing "username" or "room name" in POST data')

        # Check if the user exists
        try:
            user_contact = Contact.objects.get(user__username=username)
        except Contact.DoesNotExist:
            return HttpResponseBadRequest('User does not exist')
        # check if the room exists or create a new room
        rooms = ChatRoom.objects.filter(name=room_name)
        if rooms.exists():
            room = rooms.first()  # Get the first room if multiple are found
        else:
            room = ChatRoom.objects.create(name=room_name)
        # Add the user to the room's members and save
        room.members.add(user_contact)
        room.save()

        # Redirect to the chat page
        return redirect('chat', room_name=room_name, username=username)
    # Render the initial page if the request method is not post
    return render(request, 'index.html')


def chat(request, room_name, username):
    try:
        get_room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        return HttpResponseBadRequest('Chat room does not exist')
    if request.method == 'POST':
        message_content = request.POST['message']
        try:
            user_contact = Contact.objects.get(user__username=username)
        except Contact.DoesNotExist:
            return HttpResponseBadRequest('User does not exist')
        # create a new conversation if one doesn't exist
        conversation = Conversation.objects.filter(chat_room=get_room, participants=user_contact)
        if conversation.exists():
            conversation = conversation.first()
        else:
            conversation = Conversation.objects.create(chat_room=get_room, participants=user_contact)
            conversation.participants.set([user_contact])  # Use set() to assign participant

        try:
            new_message = Message.objects.create(conversation=conversation, sender=user_contact, message=message_content)
        except DatabaseError as e:
            return HttpResponseBadRequest(f'Database error: {e}')

    get_messages = Message.objects.filter(conversation__chat_room__name=room_name)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'chat.html', context)
