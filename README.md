# REST API for movie database
Simple REST API made with Flask. Endpoints and data format are defined in the assignment.
## Usage
The solution is dockerized. To build the image navigate into the folder with the solution and use __docker build__. (root/elevated permissions are needed to build and run the docker image).
```bash
docker build --tag moviesapi .
```
Now run the created image with the following command: 
```bash
docker run --publish 5000:5000 moviesapi
```
The REST API should be up and running. To try it out you can use any API testing tool like [postman](https://www.postman.com/downloads/), or you can use the python script I created. It uses the [requests](https://pypi.org/project/requests/) package, so if you don't already have it, install it using pip. Then run it like this :
```bash
python3 test.py
```
After that just follow the prompts on screen.