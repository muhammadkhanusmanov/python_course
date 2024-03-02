import requests



with open('1.docx', 'rb') as file:
    file = {'file': file}

    data = {
        'name': 'Foydalanuvchi ismi',
        'url': 'https://example.com',
    }

    response = requests.post('http://127.0.0.1:8000/v2/create_lesson/', files=file, data=data)

    print(response)