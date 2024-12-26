from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth import get_user_model

@login_required
def conversation_list(request):
    """Display all conversations for the logged-in user."""
    conversations = request.user.conversations.all()  # Access conversations via related_name
    conversations_with_participants = []

    for conversation in conversations:
        # Get the other participant in the conversation
        other_participant = conversation.participants.exclude(id=request.user.id).first()
        conversations_with_participants.append({
            'conversation': conversation,
            'other_participant': other_participant
        })

    return render(request, 'messaging/conversation_list.html', {
        'conversations_with_participants': conversations_with_participants
    })


@login_required
def conversation_detail(request, conversation_id):
    """Display messages in a specific conversation."""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    other_participant = conversation.participants.exclude(id=request.user.id).first()

    # Handle message submission
    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():  # Ensure message content is not empty
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content.strip()
            )
            return redirect('conversation_detail', conversation_id=conversation_id)

    # Fetch all messages for the conversation
    messages = conversation.messages.all().order_by('timestamp')

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'other_participant': other_participant,
    })


User = get_user_model()
@login_required
def start_conversation(request, username):
    """Start a new conversation with another user."""
    # Get the user to start a conversation with
    other_user = get_object_or_404(User, username=username)

    # Prevent starting a conversation with self
    if request.user == other_user:
        return redirect('messaging:list')  # Redirect to conversation list if invalid

    # Check if a conversation already exists
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not conversation:
        # Create a new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    # Redirect to the conversation detail view
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def student_list(request):
    query = request.GET.get('q', '')
    # Exclude the current user and admin users
    students = User.objects.exclude(id=request.user.id).exclude(is_staff=True).exclude(is_superuser=True)
    if query:
        students = students.filter(username__icontains=query)
    return render(request, 'messaging/student_list.html', {'students': students, 'user': request.user})