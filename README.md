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

### Create test database:

Unit Testing the API is discussed at the bottom of this README.
Let's go ahead and create a test database for later use.

```
createdb surf-events_test
```

### Setup Database using migrations

```
flask db uprade
```

## Insert Sample Data

The app comes with a sample database (psql) script you can run to insert sample data.

- Run the sample psql script to insert some initial test data into your database

  `psql -f surfEvents.sql surf_events`

- Run the same sample psql script to insert some initial test data into your TEST database

  `psql -f surfEvents.sql surf_events_test`

## Running the server

Change to the base backend directory

```
cd fsnd-surf-events-backend
```

Modify the setup script to point to your local database.
Replace the following line with your local database URL.

```
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/surf_events
```

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
URL for the API is located at https://localhost:5000/login

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
- curl -X PATCH -H "Authorization: Bearer ${JWT_TOKEN}" http://localhost:5000/add_surf_contestant/1/1
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

### PATCH '/remove_surf_contestant/<int:contest_id>/<int:surfer_id>',

- Removes a specific surfer from a specific contest on the FSND Surf Tour.
- Sample curl:
- curl -X PATCH -H "Authorization: Bearer ${JWT_TOKEN}" http://localhost:5000/remove_surf_contestant/1/1
- Sample response output:- Sample response output:

```
{
  "contest_info": {
    "contest_date": "Tue, 10 Aug 2021 00:00:00 GMT",
    "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
    "contest_name": "Corys Trestles Pro",
    "id": 1
  },
  "success": true,
  "surfers": []
}
```

- Sample response output if surfer not registered (or already removed):

```
{
  "description": "Surfer is not entered in contest",
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

## Surf Coordinators

Surf Coordinators can perform all Public API calls as well as Surf Manager API calls
Surf Coordinators can:

- Add new Surf Spots to host Contests on the FSND Surf Tour.
- Remove Surf Spots (Delete) from the FSND Surf Tour.
- Create Surf Contests
- Cancel (Delete) Surf Contests
- Modify Surf Contest details
- Edit Surf Contest details

### POST '/surf_spot/create'

- Adds a new surf spot to the FSND Surf Tour.
- Sample curl:
- curl -X POST -H "Authorization: Bearer ${JWT_TOKEN}" http://localhost:5000/surf_spot/create -H "Content-Type: application/json" -d \
  '{"name": "Playalinda","city": "Cape Canaveral","state": "FL","country": "USA","wave_type": "Beachbreak","wave_image": "test.png"}' \
  http://localhost:5000/surf_spot/create
- Sample response output:

```
{
  "success": true,
  "surf_spot_count": 4,
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
    {
      "city": "Ballina",
      "country": "Australia",
      "id": 3,
      "name": "Lennox Head",
      "state": "New South Wales",
      "wave_image": "https://i0.heartyhosting.com/www.surfer.com/wp-content/uploads/2017/02/Safety-Not-Guaranteed_LennoxHead_Shield.jpg",
      "wave_type": "Larger Right Point Break"
    },
    {
      "city": "Cape Canaveral",
      "country": "USA",
      "id": 5,
      "name": "Playalinda",
      "state": "FL",
      "wave_image": "test.png",
      "wave_type": "Beachbreak"
    }
  ]
}

```

### POST '/surf_contest/create'

- Adds a new surf contest to the FSND Surf Tour.
- Sample curl:
- curl -X POST -H "Authorization: Bearer ${JWT_TOKEN}" http://localhost:5000/surf_contest/create -H "Content-Type: application/json" -d \
  '{"surf_spot_id": 1,"contest_name": "Corys Ranch Pro 2","contest_date": "2021-08-09", \
   "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg"}' \
   http://localhost:5000/surf_contest/create
- Sample response output:

```
{
  "contest_count": 4,
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
    {
      "contest_date": "Sun, 10 Oct 2021 00:00:00 GMT",
      "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
      "contest_name": "Corys Rocky Pro",
      "id": 3
    },
    {
      "contest_date": "Mon, 09 Aug 2021 00:00:00 GMT",
      "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg?&x=640&y=360&icq=74&sig=6b2950bebceae322b8455652f32ad8c9",
      "contest_name": "Corys Ranch Pro 2",
      "id": 4
    }
  ]
}
```

### PATCH '/surf_contests/<int:contest_id>'

- Modifies surf contest on the FSND Surf Tour.
- Sample curl for changing the Surf Spot and Contest Date:
- curl -X PATCH -H "Authorization: Bearer ${JWT_TOKEN}" http://localhost:5000/surf_contests/<int:contest_id> -H "Content-Type: application/json" -d \
  '{"surf_spot_id": 1,"contest_date": "2021-08-09"}' \
   http://localhost:5000/surf_contest/create
- Sample response output:

```
{
  "contest_count": 4,
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
    {
      "contest_date": "Sun, 10 Oct 2021 00:00:00 GMT",
      "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
      "contest_name": "Corys Rocky Pro",
      "id": 3
    },
    {
      "contest_date": "Mon, 09 Aug 2021 00:00:00 GMT",
      "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg?&x=640&y=360&icq=74&sig=6b2950bebceae322b8455652f32ad8c9",
      "contest_name": "Corys Ranch Pro 2",
      "id": 5
    }
  ]
}
```

### DELETE '/surf_spots/<int:spot_id>'

- Removes a surf spot from the FSND Surf Tour.
  if there are any contests hosted at this surf spot, they are automatically cancelled.
- Sample curl:
- curl -X DELETE -H "Authorization: Bearer ${JWT_TOKEN}" http://localhost:5000/surf_spots/1
- Sample response output:

```
{
  "deleted": 1,
  "success": true,
  "surf_spot_count": 3,
  "surf_spots": [
    {
      "city": "San Onofre",
      "country": "U.S.A",
      "id": 2,
      "name": "Lower Trestles",
      "state": "CA",
      "wave_image": "https://d3qf8nvav5av0u.cloudfront.net/image/5f8dfb006ab4cb4e27a4bde419b0fcbf.png",
      "wave_type": "High Performance Left or Right"
    },
    {
      "city": "Ballina",
      "country": "Australia",
      "id": 3,
      "name": "Lennox Head",
      "state": "New South Wales",
      "wave_image": "https://i0.heartyhosting.com/www.surfer.com/wp-content/uploads/2017/02/Safety-Not-Guaranteed_LennoxHead_Shield.jpg",
      "wave_type": "Larger Right Point Break"
    },
    {
      "city": "Cape Canaveral",
      "country": "USA",
      "id": 6,
      "name": "Playalinda",
      "state": "FL",
      "wave_image": "test.png",
      "wave_type": "Beachbreak"
    }
  ]
}
```

### DELETE '/surf_contests/<int:contest_id>'

- Removes a surf spot from the FSND Surf Tour.
  if there are any contests hosted at this surf spot, they are automatically cancelled.
- Sample curl:
- curl -X DELETE -H "Authorization: Bearer ${JWT_TOKEN}" http://localhost:5000/surf_contests/1
- Sample response output:

```
{
  "contest_count": 1,
  "deleted": 2,
  "success": true,
  "surf_contests": [
    {
      "contest_date": "Sun, 10 Oct 2021 00:00:00 GMT",
      "contest_image": "https://d3qf8nvav5av0u.cloudfront.net/image/fa2b2318a96b6c2bce7bad3a8756e5ec.jpg",
      "contest_name": "Corys Rocky Pro",
      "id": 3
    }
  ]
}
```

Sample JWT token for testing endpoints: ``

## Error Handling

Errors in our API are returned as JSON objects. Here's an example of an error from a 'Bad request':

```

{
"success": False,
"error": 400,
"message": "Bad request"
}

```

The API will return these error types when requests fail:

- 401: Not Authorized - e.g. no bearer token provided or token expired
- 405: Not Allowed - e.g. POST/PATCH/DELETE for an endpoint when the endpoint doesn't support it
- 403: Forbidden - e.g. authorization provided, but user is not allowed access
- 400: Bad Request - Server couldn't process the request
- 404: Resource Not Found
- 422: Not Processable/Unprocessable - When the server can't process a request

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
    Example: https://fsnd-saylesc.us.auth0.com/authorize?audience=fsnd-surf-events&response_type=token&client_id=mqAYej6cSzNiLs53o6lHBaGvQTNPseaQ&redirect_uri=https://127.0.0.1:5000/login
5.  Based on the users credentials and assigned roles, the redirected page will provide the appropriate JWT
6.  Update the following entries in the `setup.sh` replacing them with your Auth0 Application and API details.
    - FLASK_APP
    - AUTH0_DOMAIN
    - API_AUDIENCE

## API Testing endpoints with Postman

Testing this API can be performed in 2 ways: Postman collection tests, or Python Unit Tests

### Postman Tests

Create a Postman account and test the API Endpoints live: https://www.postman.com/

The App has been set up to run on Heroku, and the sample postman collection uses the URL: https://capstone-surf-events.herokuapp.com/login
You can set up your own tests by starting with our test endpoints: `surf-events_postman_collection.json`
You can import this collection into Postman and modify the {{host}} and the authentication using the JWTs generated form the previous steps.

### Python Unit Tests

You can run the python unit tests after you have set up and run the application locally.
Ensure that the flask application is running, then run the unit tests to test the endpoints.

TODO: work on bearer tokens in unit tests

```
python test_flaskrsurf.py
```
