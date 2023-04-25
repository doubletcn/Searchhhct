from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.db.models import Q

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm, ClothingFilterForm


# class CustomLoginView(LoginView):
#     template_name = 'base/login.html'
#     fields = '__all__'
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

# class ClothingListView(View):
#     def get(self, request):
#         form = ClothingFilterForm(request.GET)
#         if form.is_valid():
#             tags = form.cleaned_data.get('tags')
#             items = Task.objects.filter(tags__in=tags).distinct()
#         else:
#             items = Task.objects.all()
#         context = {'form': form, 'items': items}
#         return render(request, 'task_list.html', context)


class TaskListView(SuccessMessageMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'items'
    paginate_by = 10
    success_message = "Các trang phục có từ khóa: {} là"
    # fail_message = "Không có trang phục có phong cách: {}"

    def get_queryset(self):
        tag_query = self.request.GET.get('tags')
        if tag_query:
            tags = [tag.strip() for tag in tag_query.split(',')]
            queryset = Task.objects.filter(tags__icontains=tags[0].lower())
            for tag in tags[1:]:
                queryset = queryset.filter(tags__icontains=tag.lower())
            items = queryset.distinct()
            if len(items) == 0:
                messages.warning(self.request, "")
            else:
                messages.success(self.request, self.success_message.format(tag_query))
        else:
            items = Task.objects.all()
        return items

# class TaskList(ListView):
#     model = Task
#     context_object_name = 'tasks'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tasks'] = context['tasks'].filter(user=self.request.user)
#         context['count'] = context['tasks'].filter(complete=False).count()

#         search_input = self.request.GET.get('search-area') or ''
#         if search_input:
#             context['tasks'] = context['tasks'].filter(
#                 title__contains=search_input)

#         context['search_input'] = search_input

#         return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
