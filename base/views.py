from django.shortcuts import render, redirect
from .data import tasks, collections

def task_list(request):
    search_query = request.GET.get('search', '')
    filtered_tasks = [t for t in tasks if search_query.lower() in t['title'].lower()]
    return render(request, 'base/task_list.html', {
        'tasks': filtered_tasks,
        'search': search_query,
        'collections': collections
    })

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        collection = request.POST.get('collection', 'Загальне')
        tasks.append({'id': len(tasks)+1, 'title': title, 'done': False, 'collection': collection})
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
        task['collection'] = request.POST.get('collection', 'Загальне')
        return redirect('task_list')

    return render(request, 'base/task_form.html', {'task': task, 'collections': collections})

def collection_list(request):
    collection_data = [
        {'name': col, 'count': sum(1 for t in tasks if t['collection'] == col)}
        for col in collections
    ]
    return render(request, 'base/collection_list.html', {
        'collections': collection_data
    })


def add_collection(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name and name not in collections:
            collections.append(name)
        return redirect('collection_list')
    return render(request, 'base/collection_form.html')

def delete_collection(request, name):
    global tasks, collections
    if name in collections:
        collections.remove(name)
        tasks = [t for t in tasks if t['collection'] != name]
    return redirect('collection_list')

def edit_collection(request, name):
    if request.method == 'POST':
        new_name = request.POST['name']
        if new_name and name in collections:
            index = collections.index(name)
            collections[index] = new_name
            for t in tasks:
                if t['collection'] == name:
                    t['collection'] = new_name
        return redirect('collection_list')
    return render(request, 'base/collection_form.html', {'name': name})