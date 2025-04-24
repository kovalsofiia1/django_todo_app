from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Collection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'base/register.html', {'form': form})


def welcome(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'base/welcome.html')


@login_required
def task_list(request):
    query = request.GET.get('query', '')  # Отримуємо пошуковий запит
    collection_filter = request.GET.get('collection', '')  # Отримуємо параметр фільтрації по колекції (як рядок)

    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(title__icontains=query)  # Пошук по назві задачі

    if collection_filter:
        tasks = tasks.filter(collection_id=collection_filter)  # Фільтрація по колекції

    collections = Collection.objects.all()  # Отримуємо всі колекції для фільтрації
    return render(request, 'base/task_list.html', {
        'tasks': tasks,
        'collections': collections,
        'query': query,
        'collection_filter': collection_filter  # передаємо як рядок
    })

@login_required
def add_task(request):
    error = ''
    if request.method == 'POST':
        title = request.POST['title'].strip()
        deadline = request.POST.get('deadline', '').strip()
        collection_id = request.POST.get('collection')
        collection = None

        if collection_id:
            try:
                collection = Collection.objects.get(id=collection_id, owner=request.user)
            except Collection.DoesNotExist:
                collection = None

        # Перевірка формату дати
        if deadline:
            try:
                from datetime import datetime
                datetime.strptime(deadline, '%Y-%m-%d')  # Перевірка формату
            except ValueError:
                error = 'Невірний формат дати. Використовуйте YYYY-MM-DD.'

        if not error:
            Task.objects.create(
                title=title,
                collection=collection,
                deadline=deadline if deadline else None,
                owner=request.user
            )
            return redirect('task_list')

    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'base/add_task.html', {
        'collections': collections,
        'error': error,
        'task': request.POST  # щоб заповнити попередні значення
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.done = not task.done  # Перемикаємо статус виконаного завдання
    task.save()
    return redirect('task_list')  # Після зміни статусу повертаємося на список завдань

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.delete()
    return redirect('task_list')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    error = ''

    if request.method == 'POST':
        title = request.POST['title'].strip()
        deadline = request.POST.get('deadline', '').strip()
        collection_id = request.POST.get('collection')
        collection = None

        if collection_id:
            try:
                collection = Collection.objects.get(id=collection_id, owner=request.user)
            except Collection.DoesNotExist:
                collection = None

        # Перевірка формату дати
        if deadline:
            try:
                from datetime import datetime
                datetime.strptime(deadline, '%Y-%m-%d')  # Перевірка формату
            except ValueError:
                error = 'Невірний формат дати. Використовуйте YYYY-MM-DD.'

        if not error:
            task.title = title
            task.deadline = deadline if deadline else None
            task.collection = collection
            task.save()
            return redirect('task_list')

    return render(request, 'base/task_form.html', {
        'task': task,
        'collections': Collection.objects.filter(owner=request.user),
        'error': error
    })

@login_required
def collection_list(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'base/collection_list.html', {'collections': collections})


@login_required
def delete_collection(request, col_id):
    collection = get_object_or_404(Collection, id=col_id, owner=request.user)
    collection.delete()
    return redirect('collection_list')

@login_required
def add_or_edit_collection(request, col_id=None):
    # Якщо col_id є, це редагування існуючої колекції
    if col_id:
        collection = get_object_or_404(Collection, id=col_id, owner=request.user)
    else:
        collection = None

    if request.method == 'POST':
        name = request.POST['name']

        # Якщо це редагування, зберігаємо зміни
        if collection:
            collection.name = name
            collection.save()
        # Якщо це створення нової колекції
        else:
            Collection.objects.create(name=name, owner=request.user)

        return redirect('collection_list')

    return render(request, 'base/collection_form.html', {'collection': collection})

