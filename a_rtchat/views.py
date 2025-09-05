from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import *
from .forms import ChatMessageForm

@login_required
def chat_group(request, chatroom_name="public-chat"):
    chat_group=get_object_or_404(chatGroup, group_name=chatroom_name)  # Example to get a specific chat group
    chat_messages=chat_group.chat_messages.all().order_by('created')[:50]
    # .objects.filter(group=chat_group).order_by('created')
    form=ChatMessageForm()
    
    other_user=None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404("You are not a member of this private chatroom.")
        for member in chat_group.members.all():
            if member != request.user:
                other_user=member
                break       
    
    if request.method=='POST':
        form=ChatMessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.author=request.user
            message.group=chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user
                }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
            
    context = {
        'chat_messages': chat_messages,
        'form': form, 
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        }
            
    return render(request, 'a_rtchat/chat.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if  request.user.username ==username:
        return redirect('home')
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = chatGroup.objects.create(is_private=True)
                chatroom.members.add(request.user, other_user)            
    else:
        chatroom = chatGroup.objects.create(is_private=True)
        chatroom.members.add(request.user, other_user)
        
    return redirect('chatroom', chatroom_name=chatroom.group_name) 