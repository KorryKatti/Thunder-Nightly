import requests


BASE_URL = 'http://127.0.0.1:5000'

def fetch_server_stats():
    try:
        response = requests.get(f'{BASE_URL}/server-stats')
        if response.status_code == 200:
            stats = response.json()
            return stats
        else:
            print("Failed to fetch server stats")
            return None
    except Exception as e:
        print("Error:", str(e))
        return None

def ping_server():
    try:
        response = requests.get(f'{BASE_URL}/ping')
        if response.status_code == 200:
            ping_response = response.json()
            return ping_response
        else:
            print("Failed to ping server")
            return None
    except Exception as e:
        print("Error:", str(e))
        return None