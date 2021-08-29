# Description

FSND Surf now has an API for staff to mange the various surf events taking place around the globe.
We opened our API to the public and give Surf Coordinator and Managers a utility to quickly access
key Surf Events.

# Surf Events API Overview

FSND-Surf is invested in creating an API that is available to the public, as well as official staff members. The public can now gain access to the information about our surf Events - including surfers, surf locations, and contests.

# Getting Started

## Tech Stack

Our tech stack will include the following:

- **SQLAlchemy ORM** to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **Python3** and **Flask** as our server language and server framework
- **Flask-Migrate** for creating and running schema migrations
- **virtualenv** as a tool to create isolated Python environments

## Setup Virtual Environment

Setup a virtual environment:

```
virtual surf-events
. surf-events/bin/activate
```

## PIP Dependencies

Setup a virtual environment and install all necessary dependencies for this application using the following command:

```
pip install -r requirements.txt
```

This will install all of the required packages.

## Setup Database and Perform Database Migration

### Create your database:

```
createdb surf-events
```

### Setup Database using migrations

```
flask db uprade
```

## Running the server

Source the setup

```
. setup.sh
```

Run the backend using:

```
flask run
```

## API URL

### Heroku API URL

This application is currently hosted on Heroku.
The URL for the API is located at https://capstone-surf-events.herokuapp.com/login

### Local API URL

When you run the flask application locally, the URl for the
URL for the API is located at https://localhost/login

## PUBLIC API

### GET '/surfers'

- Returns a list of all surfers on the FSND Surf Tour.
- Sample curl:
- curl -X GET http://localhost:5000/surfers
- Sample response output:

```
{
  "success": true,
  "surfers": [
    {
      "id": 1,
      "surfer_age": 40,
      "surfer_hometown": "Penrith, New South Wales, Australia",
      "surfer_name": "Mick Fanning",
      "surfer_ranking": 50,
      "surfer_stance": "Regular"
        },
    {
      "id": 2,
      "surfer_age": 49,
      "surfer_hometown": "Cocoa Beach, FL",
      "surfer_name": "Kelly Slater",
      "surfer_ranking": 18,
      "surfer_stance": "Regular"
    },
    ...
```

### GET '/surfers/<surfer_id>'

- Returns a specific surfer, by id, on the FSND Surf Tour.
- Sample curl:
- curl -X GET http://localhost:5000/surfers/1
- Sample response output:

```
{
  "success": true,
  "surfer_info": {
    "id": 1,
    "surfer_age": 40,
    "surfer_hometown": "Penrith, New South Wales, Australia",
    "surfer_name": "Mick Fanning",
    "surfer_ranking": 50,
    "surfer_stance": "Regular"
  }
}

```

### POST '/surfers/search'

- Returns a list of surfers on the FSND Surf Tour that match search criteria
- Using the `/surfers/search` API call, you can pass in search terms to find surfers by name (case insensitive).
- Example: curl -X POST -H "Content-Type: application/json" -d '{"search_term":"Kel"}' https://capstone-surf-events.herokuapp.com/surfers/search
- Sample response output:

```
{
    "count":1,
    "success":true,
    "surfers":[
        {
            "id":2,
            "surfer_age":49,
            "surfer_hometown":"Cocoa Beach, FL",
            "surfer_name":"Kelly Slater",
            "surfer_ranking":18,"surfer_stance":"Regular"
        }
    ]
}
```

### GET '/surf_spots'

- Returns a list of all surf spots currently on the FSND Surf Tour.
- Sample curl:
- curl -X GET http://localhost:5000/surf_spots
- Sample response output:

```
{
  "success": true,
  "surf_spots": [
    {
      "city": "Oaxaca",
      "country": "Mexico",
      "id": 1,
      "name": "Barra de la Cruz",
      "state": "N/A",
      "wave_image": "https://d3qf8nvav5av0u.cloudfront.net/image/6c61c6bfe9f3aa5ef089dae6d336cd04.jpg",
      "wave_type": "Rocky Right Point Break"
    },
    {
      "city": "San Onofre",
      "country": "U.S.A",
      "id": 2,
      "name": "Lower Trestles",
      "state": "CA",
      "wave_image": "https://d3qf8nvav5av0u.cloudfront.net/image/5f8dfb006ab4cb4e27a4bde419b0fcbf.png",
      "wave_type": "High Performance Left or Right"
    },
    ...
```

### GET '/surf_spots/<int:spot_id>'

- Returns a specific surf spot on the FSND Surf Tour.
- Sample curl:
- curl -X GET http://localhost:5000/surf_spots/1
- Sample response output:

```
{
  "success": true,
  "surf_spot": {
    "city": "Oaxaca",
    "country": "Mexico",
    "id": 1,
    "name": "Barra de la Cruz",
    "state": "N/A",
    "wave_image": "https://d3qf8nvav5av0u.cloudfront.net/image/6c61c6bfe9f3aa5ef089dae6d336cd04.jpg",
    "wave_type": "Rocky Right Point Break"
  }
}
```

### GET '/surf_contests'

- Returns a list of all surf contests currently on the FSND Surf Tour.
- Sample curl:
- curl -X GET http://localhost:5000/surf_contests
- Sample response output:

```

{
"success": true,
"surf_contests": [
{
"contest_date": "Tue, 10 Aug 2021 00:00:00 GMT",
"contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
"contest_name": "Corys Trestles Pro",
"id": 1
},
{
"contest_date": "Fri, 10 Sep 2021 00:00:00 GMT",
"contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
"contest_name": "Corys Oaxaca Pro",
"id": 2
},

```

### GET '/surf_contests/<int:contest_id>'

- Returns a specific surf contest hosted by the FSND Surf Tour.
- Sample curl:
- curl -X GET http://localhost:5000/surf_contests/1
- Sample response output:

```

{
"success": true,
"surf_contest": {
"contest_date": "Tue, 10 Aug 2021 00:00:00 GMT",
"contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
"contest_name": "Corys Trestles Pro",
"id": 1
}
}

```

### GET 'surf_spots/<int:spot_id>/contests'

- Returns a list of all surf contests hosted at a specific spot on the FSND Surf Tour.
- Sample curl:
- curl -X GET http://localhost:5000/surf_spots/1/contests
- Sample response output:

```
{
  "success": true,
  "surf_contests": [
    {
      "contest_date": "Tue, 10 Aug 2021 00:00:00 GMT",
      "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
      "contest_name": "Corys Trestles Pro",
      "id": 1
    }
  ],
  "surf_spot": {
    "city": "Oaxaca",
    "country": "Mexico",
    "id": 1,
    "name": "Barra de la Cruz",
    "state": "N/A",
    "wave_image": "https://d3qf8nvav5av0u.cloudfront.net/image/6c61c6bfe9f3aa5ef089dae6d336cd04.jpg",
    "wave_type": "Rocky Right Point Break"
  }
}

```

## Restricted API

This application runs with a restricted API for Surf Manager and Surf Coordinator Roles
A token needs to be passed to each endpoint.
The following only works for /products endpoints:
The token can be retrived by following these steps:

1. Go to https: https://warranty-tracker.herokuapp.com
2. Click on Login and enter any credentials into the Auth0 login page. The role is automatically assigned by Auth0.
   Alternatively, sample account that has already been created can be used:
   Email: test_user_role@gmail.com
   Password: test1234!

## Surf Manager

Surf Managers can perform all Public API calls.
Surf managers can only add and remove surfers from surf contests using the below API calls

### PATCH '/add_surf_contestant/<int:contest_id>/<int:surfer_id>'

- Adds a specific surfer to a contest on the FSND Surf Tour.
- Sample curl:
- curl -X PATCH http://localhost:5000/add_surf_contestant/1/1
- Sample response output:

```
{
  "contest_info": {
    "contest_date": "Tue, 10 Aug 2021 00:00:00 GMT",
    "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
    "contest_name": "Corys Trestles Pro",
    "id": 1
  },
  "success": true,
  "surfers": [
    {
      "id": 1,
      "surfer_age": 40,
      "surfer_hometown": "Penrith, New South Wales, Australia",
      "surfer_name": "Mick Fanning",
      "surfer_ranking": 50,
      "surfer_stance": "Regular"
    }
  ]
}
```

- Sample response output if surfer already exists:

```
{
  "description": "Surfer is already entered in contest",
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

Sample JWT token for testing endpoints: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpMWEtodFZhWnkxWWloaVVpY3ItayJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2F5bGVzYy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTMzOTQ5NTc3ODc3NDA4Nzk3MDIiLCJhdWQiOlsiZnNuZC1zdXJmLWV2ZW50cyIsImh0dHBzOi8vZnNuZC1zYXlsZXNjLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MjkwNTg2NTksImV4cCI6MTYyOTEwMTg1OSwiYXpwIjoibXFBWWVqNmNTek5pTHM1M282bEhCYUd2UVROUHNlYVEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicGF0Y2g6YWRkX3N1cmZlciIsInBhdGNoOnJlbW92ZV9zdXJmZXIiXX0.HvO2M2q-iVS0FeP2ErVDviw-EphWKSniogLtndrG-RrepEPKSSvUsmhGcOBk8zBaz-_PqbLBHDwjEUmwsDO3BkN4jKWvXaS9pSR6-FL-Jbr2Yt6SpyUyoYRjvkra65RG_QBx0ILlA63yjny1O5UeWGe-2FKNC6IjUWH0_GbQbmgJcruwdDttvDvCWzggI1H-g7A_0QPp8iehD6A4UNJoznnRAq4ZoeU_7ZoejIOFf0rmDDmY4v1kkN1f2TqcK4TV42xTVze8nTpgVZWsvmmiZH0iplVmwnaPSZQP4JB9bkSLT8ELQ_tljp04Fzp0vr_0JBVHsM8IeK393qQZcHsZHA`

- Enter surfers into Surf Contests
  Example: curl -X PATCH -H https://capstone-surf-events.herokuapp.com/add_surf_contestant/3/6

- Remove surfers from a Surf Contest
  Example: curl -X PATCH -H https://capstone-surf-events.herokuapp.com/remove_surf_contestant/3/6

## Surf Coordinators

#### Surf Coordinators can perform all Public API calls plus the following:

Sample JWT token for testing endpoints: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpMWEtodFZhWnkxWWloaVVpY3ItayJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2F5bGVzYy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc1OTk3NTk0ODIxODcwMzM5MTMiLCJhdWQiOlsiZnNuZC1zdXJmLWV2ZW50cyIsImh0dHBzOi8vZnNuZC1zYXlsZXNjLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MjkwNTg1MTgsImV4cCI6MTYyOTEwMTcxOCwiYXpwIjoibXFBWWVqNmNTek5pTHM1M282bEhCYUd2UVROUHNlYVEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnN1cmZfY29udGVzdHMiLCJkZWxldGU6c3VyZl9zcG90cyIsInBhdGNoOmFkZF9zdXJmZXIiLCJwYXRjaDpyZW1vdmVfc3VyZmVyIiwicGF0Y2g6c3VyZl9jb250ZXN0IiwicG9zdDpzdXJmX2NvbnRlc3RzIiwicG9zdDpzdXJmX3Nwb3RzIl19.oHYahJxA7dBP4CwGyKQxSfDp3vQ5HM5z2N56Nh1nQTM0cACpP2obMi8FSw7_Xl7zt3MD9eoQT2swYGOy5xKPOa6g6xKrp4h4nfq2uJwXyME6h5wscZhIfG2iukHQo77zI1nv-XVTZFAfEcrj2cDcYVNlgGjbUho55K8M-SFS7_gVG_DwEvAOD-9F31HwQEF6h4lVBzaSdibifg3OMeiGP6Yyq9JiqWq_DvM7ri99QQ63VikksFbRVU3wpMIQTL2NkWs1BAOFzwkl33pAmoQRO_e5I8SmuAB_pP-QHfEQx9TdtdPleF4ni6ZUKJ50shCaFjGkQYzzYZJSfZy_HCIg6g`

- Create Surf Contests
- Cancel (Delete) Surf Contests
  curl -X DELETE https://capstone-surf-events.herokuapp.com/surf_contests/3
- Edit Surf Contest details

- Add new Surf Spots to host Contests
- Remove Surf Spots (Delete) from the tour
- Enter / Remove surfers into Surf Contests

## Error Handling

Errors in our API are returned as JSON objects. Here's an example of an error from a 'Bad request':

```

{
"success": False,
"error": 400,
"message": "Bad request"
}

```

The API will return three error types when requests fail:

- 401: Not Authorized
- 403: Not Allowed
- 400: Bad Request
- 404: Resource Not Found
- 405: Not Allowed
- 422: Not Processable/Unprocessable

## Setting up the Authentication

Setting up your own version of this API is easy with the help of Auth0.

1.  Create a new application and API on https://manage.auth0.com
2.  Add a new Role representing a Surf Manager with the following permissions:
    - patch:add_surfer
    - patch:remove_surfer
3.  Add a new Role representing a Surf Coordinator with the following permissions:
    - post:surf_spots
    - post:surf_contests
    - patch:surf_contest
    - delete:surf_spots
    - delete:surf_contests
4.  Generate a JWT token using your Auth0 Applicaton URL so that you can access the JWT
    Example https://fsnd-saylesc.us.auth0.com/authorize?audience=fsnd-surf-events&response_type=token&client_id=mqAYej6cSzNiLs53o6lHBaGvQTNPseaQ&redirect_uri=https://127.0.0.1:5000/login
5.  Based on the users credentials and assigned roles, the redirected page will provide the appropriate JWT

## API Testing endpoints with Postman

Create a Postman account and test the API Endpoints live: https://www.postman.com/

The App has been set up to run on Heroku, and the sample postman collection uses the URL: https://capstone-surf-events.herokuapp.com/login
You can set up your own tests by starting with our test endpoints: `surf-events_postman_collection.json`
You can import this collection into Postman and modify the {{host}} and the authentication using the JWTs generated form the previous steps.

```

```

```

```

```

```

```

```

```

```
