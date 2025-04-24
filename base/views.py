from django.shortcuts import render, redirect
from .data import tasks, collections
from datetime import datetime

def get_collection_name(cid):
    col = next((c for c in collections if c['id'] == cid), None)
    return col['name'] if col else 'Невідомо'

def task_list(request):
    search_query = request.GET.get('search', '')
    selected_col = request.GET.get('collection')
    selected_col = int(selected_col) if selected_col and selected_col.isdigit() else None

    filtered_tasks = tasks
    if search_query:
        filtered_tasks = [t for t in filtered_tasks if search_query.lower() in t['title'].lower()]
    if selected_col:
        filtered_tasks = [t for t in filtered_tasks if t['collection'] == selected_col]

    # Додаємо 'collection_name' до кожного завдання
    for task in filtered_tasks:
        task['collection_name'] = get_collection_name(task['collection'])

    return render(request, 'base/task_list.html', {
        'tasks': filtered_tasks,
        'search': search_query,
        'collections': collections,
        'selected_col': selected_col,
        'get_collection_name': get_collection_name
    })
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        collection = int(request.POST.get('collection', '1'))
        deadline = request.POST.get('deadline')
        tasks.append({
            'id': len(tasks)+1,
            'title': title,
            'done': False,
            'collection': collection,
            'deadline': deadline
        })
        return redirect('task_list')
    return render(request, 'base/task_form.html', {'collections': collections})

def complete_task(request, task_id):
    for t in tasks:
        if t['id'] == task_id:
            t['done'] = not t['done']
            break
    return redirect('task_list')

def delete_task(request, task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect('task_list')

def edit_task(request, task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return redirect('task_list')

    if request.method == 'POST':
        task['title'] = request.POST['title']
        task['collection'] = int(request.POST.get('collection', '1'))
        task['deadline'] = request.POST.get('deadline')
        return redirect('task_list')

    return render(request, 'base/task_form.html', {'task': task, 'collections': collections})

def collection_list(request):
    for col in collections:
        col['count'] = sum(1 for t in tasks if t['collection'] == col['id'])

    return render(request, 'base/collection_list.html', {
        'collections': collections
    })

def add_collection(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            collections.append({'id': max([c['id'] for c in collections], default=0)+1, 'name': name})
        return redirect('collection_list')
    return render(request, 'base/collection_form.html')

def delete_collection(request, col_id):
    global tasks, collections
    collections = [c for c in collections if c['id'] != col_id]
    tasks = [t for t in tasks if t['collection'] != col_id]
    return redirect('collection_list')

def edit_collection(request, col_id):
    collection = next((c for c in collections if c['id'] == col_id), None)
    if not collection:
        return redirect('collection_list')

    if request.method == 'POST':
        new_name = request.POST['name']
        collection['name'] = new_name
        return redirect('collection_list')
    return render(request, 'base/collection_form.html', {'name': collection['name'], 'col_id': collection['id']})
