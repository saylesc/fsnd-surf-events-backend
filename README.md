# Description

FSND Surf now has an API for staff to mange the various surf events taking place around the globe.
We opened our API to the public and give Surf Coordinator and Managers a utility to quickly access
key Surf Events.

# API

## Surf Events API Overview

FSND-Surf is invested in creating an API that is available to the public, as well as official staff members. The public can now gain access to the information about our surf Events - including surfers, surf locations, and contests.

## API URL

The URL for the API is located at https://capstone-surf-events.herokuapp.com/login

## PUBLIC API URL

#### Anyone can:

- View Surf Contests

  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surf_contests

```
{
    "success":true,
    "surf_spots":[
        {
            "city":"Oaxaca",
            "country":"Mexico",
            "id":1,
            "name":"Barra de la Cruz",
            "state":"N/A",
            "wave_image":"https://d3qf8nvav5av0u.cloudfront.net/image/6c61c6bfe9f3aa5ef089dae6d336cd04.jpg",
            "wave_type":"Rocky Right Point Break"},
        {
            "city":"Ballina",
            "country":"Australia",
            "id":3,
            "name":"Lennox Head",
            "state":"New South Wales",
            "wave_image":"https://i0.heartyhosting.com/www.surfer.com/wp-content/uploads/2017/02/Safety-Not-Guaranteed_LennoxHead_Shield.jpg",
            "wave_type":"Larger Right Point Break"},
        {
            "city":"Cape Canaveral",
            "country":"USA",
            "id":5,
            "name":"Playalinda",
            "state":"FL",
            "wave_image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3aaWHaOtRM9JXl2IVAcLWDysWvjsiRbQHFqmsSAf4ShmS8j3AHN95I9TLxsPWVApAkSk&usqp=CAU","wave_type":"Beachbreak"
        }
    ]
}
```

- View Specific Surf Contests
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surf_contests/1
- View Surf Spots
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surf_spots
- View All Surfers
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surfers
- Search for Surfers
  Using the `/surfers/search` API call, you can pass in search terms to find surfers by name.
  Example: curl -X POST -H "Content-Type: application/json" -d '{"search_term":"Kel"}' https://capstone-surf-events.herokuapp.com/surfers/search
- View Individual Surfer Info
  You can also filter by specific surfers using the id
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surfers/2

## Surf Manager

#### Surf Managers can perform all Public API calls plus the following:

- Enter surfers into Surf Contests
  Example: curl -X PATCH -H https://capstone-surf-events.herokuapp.com/add_surf_contestant/3/6

- Remove surfers from a Surf Contest
  Example: curl -X PATCH -H https://capstone-surf-events.herokuapp.com/remove_surf_contestant/3/6

## Surf Coordinators

#### Surf Coordinators can perform all Public API calls plus the following:

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

## Testing endpoints with Postman

https://www.postman.com/

You can set up your own tests by starting with our test endpoints: `surf-events_postman_collection.json`
You can import this collection into Postman and modify the {{host}} and the authentication using the JWTs generated form the previous steps.
