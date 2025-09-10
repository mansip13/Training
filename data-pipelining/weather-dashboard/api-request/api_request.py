import requests 


api_key="3bdf224ceff7afbc9e071f47d42ab9c7"
api_url= f"http://api.weatherstack.com/current?access_key={api_key}&query=Mumbai"

def fetch_data():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API Working")
        print(response.json())
        
    
    except requests.exceptions.RequestExeception as e:
        print(f"An Error Occured! {e}")
        raise
        
