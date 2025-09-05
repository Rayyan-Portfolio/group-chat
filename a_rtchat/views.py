from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import chatGroup,groupMessage
from .forms import ChatMessageForm

@login_required
def chat_group(request):
    chat_group=get_object_or_404(chatGroup, group_name="public-chat")  # Example to get a specific chat group
    chat_messages=chat_group.chat_messages.all().order_by('created')[:50]
    # .objects.filter(group=chat_group).order_by('created')
    form=ChatMessageForm()
    
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
            
            
    return render(request, 'a_rtchat/chat.html', {'chat_messages': chat_messages, 'form': form})


# from django.shortcuts import render,get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from .models import chatGroup,groupMessage
# from .forms import ChatMessageForm

# from django.template.loader import render_to_string
# from django.utils.safestring import mark_safe

# @login_required
# def chat_group(request):
#     grp = get_object_or_404(chatGroup, group_name="public-chat")
#     msgs = groupMessage.objects.filter(group=grp).order_by("created")[:50]

#     if request.method == "POST":
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             m = form.save(commit=False)
#             m.author = request.user
#             m.group  = grp
#             m.save()

#             # HTMX request -> return one rendered <li>
#             if request.headers.get("HX-Request") == "true":
#                 li_html = render_to_string(
#                     "a_rtchat/chat_message.html",
#                     {"message": m, "user": request.user},
#                     request=request,
#                 )
#                 from django.http import HttpResponse
#                 return HttpResponse(li_html)

#             return redirect("home")
#     else:
#         form = ChatMessageForm()

#     # Pre-render all saved messages to HTML
#     messages_html = "".join(
#         render_to_string(
#             "a_rtchat/chat_message.html",
#             {"message": msg, "user": request.user},
#             request=request,
#         )
#         for msg in msgs
#     )

#     return render(
#         request,
#         "a_rtchat/chat.html",
#         {
#             "messages_html": mark_safe(messages_html),  # already-rendered HTML
#             "form": form,
#         },
#     )
