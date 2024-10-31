import requests

def get_google_sheets_data():
    SHEET_ID = '1QlgU_VF_UdBq_ESpdOerW-jvxVtnHAFeFU3FUeV8ZRI'
    RANGE = 'Página1'
    API_KEY = 'AIzaSyCPBtiHtZaPPWoOa0jDVjmEsIdR9s00dJM'

    url = f'https://sheets.googleapis.com/v4/spreadsheets/1QlgU_VF_UdBq_ESpdOerW-jvxVtnHAFeFU3FUeV8ZRI/values/{RANGE}?key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('values', [])
    else:
        raise Exception(f"Erro ao acessar Google Sheets API: {response.status_code}")

