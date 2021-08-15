# Description

FSND Surf now has an API for staff to mange the various surf events taking place around the globe.

# API

## Surf Events API Overview

FSND-Surf is invested in creating an API that is available to the public, as well as official staff members. The public can now gain access to the information about our surf Events - including surfers, surf locations, and contests.

## PUBLIC API

#### Anyone can:

- View Surf Contests
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surf_contests
- View Specific Surf Contests
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surf_contests/1
- View Surf Spots
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surf_spots
- View All Surfers
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surfers
- Search for Surfers
  Example: curl -X POST -H "Content-Type: application/json" -d '{"search_term":"Kel"}' https://capstone-surf-events.herokuapp.com/surfers/search
- View Individual Surfer Info
  Example: curl -X GET https://capstone-surf-events.herokuapp.com/surfers/2

## Surf Manager

#### Surf Managers can perform all Public API calls plus the following:

- Enter surfers into Surf Contests

#####

Example: curl -X PATCH -H https://capstone-surf-events.herokuapp.com/add_surf_contestant/3/6

- Remove surfers from a Surf Contest

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
