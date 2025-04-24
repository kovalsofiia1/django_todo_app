from datetime import date

collections = [
    {'id': 1, 'name': 'Особисте'},
    {'id': 2, 'name': 'Робота'},
    {'id': 3, 'name': 'Навчання'},
    {'id': 4, 'name': 'Покупки'}
]
tasks = [
    {
        'id': 1,
        'title': 'Прочитати книжку',
        'done': False,
        'collection': 1,
        'deadline': '2025-04-30'
    },
    {
        'id': 2,
        'title': 'Підготувати звіт',
        'done': True,
        'collection': 2,
        'deadline': '2025-04-25'
    },
    {
        'id': 3,
        'title': 'Написати конспект',
        'done': False,
        'collection': 3,
        'deadline': '2025-04-26'
    },
    {
        'id': 4,
        'title': 'Купити продукти',
        'done': False,
        'collection': 4,
        'deadline': ''
    }
]
