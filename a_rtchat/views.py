from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import chatGroup,groupMessage
from .forms import ChatMessageForm

@login_required
def chat_group(request):
    chat_group=get_object_or_404(chatGroup, group_name="Public-Chat")  # Example to get a specific chat group
    chat_messages=groupMessage.objects.filter(group=chat_group).order_by('created')
    form=ChatMessageForm()
    
    if request.htmx:
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
            # if request.headers.get('Hx-Request') == 'true':
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
            # return redirect('home')
            
    return render(request, 'a_rtchat/chat.html', {'chat_messages': chat_messages, 'form': form})