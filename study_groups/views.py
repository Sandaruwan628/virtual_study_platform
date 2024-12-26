from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudyGroup
from .forms import StudyGroupForm

# View to list all study groups
@login_required
def study_group_list(request):
    groups = StudyGroup.objects.all()
    return render(request, 'study_groups/study_group_list.html', {'groups': groups})

# View to create a new study group
@login_required
def create_study_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            study_group = form.save(commit=False)
            study_group.created_by = request.user
            study_group.save()
            return redirect('study_group_list')
    else:
        form = StudyGroupForm()
    return render(request, 'study_groups/create_study_group.html', {'form': form})

# View to manage a study group
@login_required
def manage_study_group(request, group_id):
    # Get the group or return a 404 if not found
    group = get_object_or_404(StudyGroup, id=group_id)

    # Handle the form submission for updating the group
    if request.method == 'POST':
        form = StudyGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()  # Save the updated group
            return redirect('study_group_list')  # Redirect to the study group list
    else:
        # Pre-fill the form with the existing group data
        form = StudyGroupForm(instance=group)

    return render(request, 'study_groups/manage_study_group.html', {'form': form, 'group': group})

# View to delete a study group
@login_required
def delete_study_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)

    # Ensure that only the creator can delete the group
    if group.created_by == request.user:
        group.delete()  # Delete the study group

    return redirect('study_group_list')  # Redirect to the study group list

# View to join a study group
@login_required
def join_study_group(request, group_id):
    group = StudyGroup.objects.get(id=group_id)
    group.members.add(request.user)
    group.save()
    return redirect('study_group_list')


# View to leave a study group
@login_required
def leave_study_group(request, group_id):
    group = StudyGroup.objects.get(id=group_id)

    # Check if the user is already a member
    if request.user in group.members.all():
        group.members.remove(request.user)  # Remove the user from the group

    return redirect('study_group_list')

# View to show the members of a study group
@login_required
def view_study_group_members(request, group_id):
    # Get the study group or return a 404 if not found
    group = get_object_or_404(StudyGroup, id=group_id)

    # Retrieve all members of the study group
    members = group.members.all()

    return render(request, 'study_groups/view_study_group_members.html', {'group': group, 'members': members})