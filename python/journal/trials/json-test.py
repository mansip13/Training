import json
data = {
    "name": "Alex Doe",
    "age": 30,
    "city": "New York"
}


with open("test.json","w")as file:
    json.dump(data,file,indent=4)