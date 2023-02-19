import requests

api_url = "http://127.0.0.1:5000/movies"

def menu():
    print("-----------------------")
    print("1 - display all movies")
    print("2 - display movie with specific id")
    print("3 - insert new movie")
    print("4 - update existing movie")
    print("5 - exit program")
    choice = input("Select what action to perform : ")
    print("-----------------------")
    if(choice == "1"):
        display_all()
    elif(choice == "2"):
        display_one()
    elif(choice == "3"):
        insert_new()
    elif(choice == "4"):
        update()
    elif(choice == "5" or choice == "q"):
        exit(0)
    else:
        print("Invalid action.")
        menu()


def print_movie(movie):
    try:
        print(str(movie["id"]) + ":" + movie["title"])
        print(movie["description"])
        print(movie["release_year"])
    except: 
        # Object passed in is not a movie dict -> print it as is
        print(movie)
        

def display_all():
    response = requests.get(api_url)
    if not response.ok:
        print(response.json())
    if response.json() == []:
        print("No movies in database.")
        return
    for movie in response.json():
        print_movie(movie)
        print("")
    

def display_one():
    id = input("Enter id: ")
    response = requests.get(api_url + "/" + id)
    if response.ok:
        print_movie(response.json())
    else:
        print("Returned status code : " + str(response.status_code))
        print(response.json())
    
def insert_new():
    title = input("Title: ")
    description = input("Description: ")
    release_year = input("Release year: ")
    movie = {"title": title, "description": description, "release_year": release_year}
    response = requests.post(api_url, json=movie)
    print("Status code : " + str(response.status_code))

def update():
    id = input("Enter id: ")
    original = requests.get(api_url + "/" + id)
    if original.ok:
        print("You are editing this movie:")
        print_movie(original.json())
        print("===========================")
    else:
        print("Returned status code : " + str(original.status_code))
        print(original.json())
        return
        
    title = input("New title: ")
    description = input("New description: ")
    release_year = input("New release year: ")
    movie = {"title": title, "description": description, "release_year": release_year}
    response = requests.put(api_url + "/" + id, json=movie)
    print("Updated movie :")
    print_movie(response.json())
    print("Status code : " + str(response.status_code))

while(True):
    menu()