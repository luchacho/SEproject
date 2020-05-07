from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from .forms import GroupForm, PostForm
from .models import Group, GroupMember, Post


def home(request):
    return render(request, 'teamup/home.html', {'title': 'Home'})

@login_required(login_url="/login")
def groups(request):
    groups = Group.objects.all()
    return render(request, 'teamup/groups.html', {'title': 'Groups', 'groups': groups})

@login_required(login_url="/login")
def create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            if(form.checkExist()):
                messages.success(request, 'Group already created!')
                return redirect('/create')
            else:
                group = form.save(commit=False)
                group.owner = request.user
                group.slug = group.groupName
                group.save()
                groupmember = GroupMember(group=Group.objects.get(groupName=group.groupName), member=request.user)
                groupmember.save()
                messages.success(request, 'Group created Successfully!')
                return redirect('/groups')
    else:
        form = GroupForm()
        return render(request, 'teamup/makegroup.html', {'form':form})

@login_required(login_url="/login")
def PostFormView(request):
    form = PostForm(request.POST, request=request.user)
    if form.is_valid():
        post = form.save()
        messages.success(request, 'Success!')
        return redirect('/groups')
    return render(request, 'teamup/post.html', {'form': form})


class GroupDetail(generic.DetailView):
    model = Group
    template_name = 'teamup/groupdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = GroupMember.objects.all().filter(group=self.object)
        context['posts'] = Post.objects.filter(group=self.object)
        return context