import os, sys
from flask import Flask, request, jsonify, abort
from models import setup_db, rollback_db, SurfSpot, Surfer, SurfContest
from auth.auth import AuthError, requires_auth
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    # ROUTES

    ## PUBLIC GET API
    ''' The default GET API's for any public user'''
    @app.route('/login')
    def hello_home():
        return jsonify({
            "success": True,
            "message": "Hello! From the Surf Events page"
        })

    ### GET SURFERS
    @app.route('/surfers', methods=['GET'])
    def get_surfers():
        try:
            surfers_resp = []
            surfers = Surfer.query.order_by(Surfer.id).all()
            for surfer in surfers:
                surfers_resp.append(surfer.format())
            return jsonify({
                "success": True,
                "surfers": surfers_resp
            })

        except:
            return bad_request(400)

    @app.route('/surfers/<int:surfer_id>', methods=['GET'])
    def get_surfer(surfer_id):
        try:
            surfer = Surfer.query.get(surfer_id)
            if surfer is None:
                return no_resource(404)

            return jsonify({
                "success": True,
                "surfer_info": surfer.format()
            })

        except:
            return no_resource(404)

    ### GET SURF SPOTS
    @app.route('/surf_spots', methods=['GET'])
    def get_surf_spots():
        try:
            surfspot_resp = []
            surfspots = SurfSpot.query.order_by(SurfSpot.id).all()
            for surfspot in surfspots:
                surfspot_resp.append(surfspot.format())
            return jsonify({
                "success": True,
                "surf_spots": surfspot_resp
            })

        except:
            abort(400)

    ### GET SURF Contests
    @app.route('/surf_contests', methods=['GET'])
    def get_all_surf_contests():
        try:
            surfcontests_resp = []
            surfcontests = SurfContest.query.order_by(SurfContest.id).all()
            for contest in surfcontests:
                surfcontests_resp.append(contest.format())
            return jsonify({
                "success": True,
                "surf_contests": surfcontests_resp
            })

        except:
            abort(400)

    ### GET specific SURF Contests
    @app.route('/surf_contests/<int:contest_id>')
    def get_surf_contest(contest_id):
        try:
            contest = SurfContest.query.get(contest_id)

            # unprocessable(422, "")
            if not contest:
                return no_resource(404)

            return jsonify({
                "success": True,
                "surf_contest": contest.format()
            })
        except:
            return unprocessable(422)

    ### GET specific SURF Spots
    @app.route('/surf_spots/<int:spot_id>')
    def get_surf_spot(spot_id):
        try:
            spot = SurfSpot.query.get(spot_id)

            if not spot:
                return no_resource(404)

            return jsonify({
                "success": True,
                "surf_spot": spot.format()
            })
        except:
            return unprocessable(422)


    ### GET specific SURF Contests hosted at a specific spot
    @app.route('/surf_spots/<int:spot_id>/contests', methods=['GET'])
    def get_surf_spot_contests(spot_id):
        try:
            surfSpot = SurfSpot.query.get(spot_id)

            if not surfSpot:
                return no_resource(404)

            contest_resp = []
            contests = surfSpot.contests

            for contest in contests:
                contest_resp.append(contest.format())

            return jsonify({
                "success": True,
                "surf_spot": surfSpot.format(),
                "surf_contests": contest_resp
            })

        except:
            return unprocessable(422)


    ### POST to search for specific Surfers
    @app.route('/surfers/search', methods=['POST'])
    def search_surfers():
        body = request.get_json()
        surferSearchTerm = body['search_term'].lower()
        searchTerm = "%{}%".format(surferSearchTerm)
        error = False
        surferSearchResults = []
        try:
            surfers = Surfer.query.filter(Surfer.name.ilike(searchTerm)).all()
            for surfer in surfers:
                surferSearchResults.append(surfer.format())

            return jsonify({
                "success": True,
                "count": len(surfers),
                "surfers": surferSearchResults
            })
        except:
            error = True


    ## RESTRICTED ACCESS API
    '''
    The GET/PATCH/POST/DELETE API's for Surf Coordinator and Surf Manager users
    '''

    ### Surf Manager API
    '''
    Surf Managers can only add/remove surfers to/from a surf contest
    '''

    @app.route('/add_surf_contestant/<int:contest_id>/<int:surfer_id>', methods=['PATCH'])
    @requires_auth('patch:add_surfer')
    def add_surfer_to_contest(payload, contest_id, surfer_id):
        try:
            if type(payload) is AuthError:
                return auth_error(payload)

            else:
                contest = SurfContest.query.get(contest_id)
                if not contest:
                    return no_resource(404)

                surfer = Surfer.query.get(surfer_id)
                if not surfer:
                    return no_resource(404)

                # If surfer is not already entered, enter them
                foundContest = False
                for surfContest in surfer.contests:
                    if surfContest.id == contest_id:
                        foundContest = True

                if foundContest:
                    return unprocessable(422, "Surfer is already entered in contest")

                surfer.contests.append(contest)
                surfer.update()

                surferSearchResults = []
                for contestSurfer in contest.surfers:
                    surferSearchResults.append(contestSurfer.format())


                return jsonify({
                    "success": True,
                    "contest_info": contest.format(),
                    "surfers": surferSearchResults
                })
        except:
            rollback_db()
            return unprocessable(422)

    @app.route('/remove_surf_contestant/<int:contest_id>/<int:surfer_id>', methods=['PATCH'])
    @requires_auth('patch:remove_surfer')
    def remove_surfer_from_contest(payload, contest_id, surfer_id):
        try:
            if type(payload) is AuthError:
                return auth_error(payload)

            else:
                contest = SurfContest.query.get(contest_id)
                if not contest:
                    return no_resource(404)

                surfer = Surfer.query.get(surfer_id)
                if not surfer:
                    return no_resource(404)

                # If surfer is not already entered, enter them
                if surfer in contest.surfers:
                    contest.surfers.remove(surfer)
                    contest.update()

                    surferSearchResults = []
                    for contestSurfer in contest.surfers:
                        surferSearchResults.append(contestSurfer.format())

                    return jsonify({
                        "success": True,
                        "contest_info": contest.format(),
                        "surfers": surferSearchResults
                    })

                else:
                    return unprocessable(422, "Surfer is not entered in contest")
        except:
            rollback_db()
            return unprocessable(422)


    ### Surf Coordinator API

    # POST route for adding  Surf Spots to the tour
    @app.route('/surf_spot/create', methods=['POST'])
    @requires_auth('post:surf_spots')
    def create_surf_spot(payload):
        createError = False
        errorDescr = ''
        try:
            if type(payload) is AuthError:
                return auth_error(payload)

            else:
                body = request.get_json()
                surfSpotName = body['name']
                surfSpotCity = body['city']
                surfSpotState = body['state']
                surfSpotCountry = body['country']
                surfSpotWaveType = body['wave_type']
                surfSpotWaveImage = body['wave_image']

                # name, city, state, country, waveType, waveImage):
                newSurfSpot = SurfSpot(
                    name=surfSpotName,
                    city=surfSpotCity,
                    state=surfSpotState,
                    country=surfSpotCountry,
                    waveType=surfSpotWaveType,
                    waveImage=surfSpotWaveImage)

                newSurfSpot.insert()

                surfSpots = SurfSpot.query.order_by(SurfSpot.id).all()
                listSurfSpots = []

                for surfSpot in surfSpots:
                    listSurfSpots.append(surfSpot.format())

                return jsonify({
                    "success": True,
                    "surf_spot_count": len(listSurfSpots),
                    "surf_spots": listSurfSpots
                })
        except:
            error = True
            errorDescr = "Error creating new Surf Spot"

        # TODO: Return error code here instead
        return jsonify({
            "success": False,
            "message": errorDescr
        })

    # POST route for Creating Surf Contests
    @app.route('/surf_contest/create', methods=['POST'])
    @requires_auth('post:surf_contests')
    def create_surf_contest(payload):
        createError = False
        errorDescr = ''
        try:
            if type(payload) is AuthError:
                return auth_error(payload)

            else:
                body = request.get_json()
                surfSpotId = body['surf_spot_id']
                contestName = body['contest_name']
                contestDate = body['contest_date']
                contestImage = body['contest_image']

                # Find the surf spot this contest will be held at
                surfSpot = SurfSpot.query.get(surfSpotId)
                if surfSpot == None:
                    errorDescr += 'Surf Spot not found. '
                    createError = True

                if not createError:
                    newContest = SurfContest(
                        name=contestName,
                        date=contestDate,
                        image=contestImage,
                        spotId=surfSpotId)

                    newContest.insert()

                    surfContests = SurfContest.query.order_by(SurfContest.id).all()
                    listSurfContests = []

                    for contest in surfContests:
                        listSurfContests.append(contest.format())

                    return jsonify({
                        "success": True,
                        "contest_count": len(surfContests),
                        "surf_contests": listSurfContests
                    })
        except:
            error = True
            errorDescr = "Error creating new Surf Contest"

        # TODO: Return error code here instead
        return jsonify({
            "success": False,
            "message": errorDescr
        })

    # PATCH route for Editing Surf Contests
    @app.route('/surf_contests/<int:contest_id>', methods=['PATCH'])
    @requires_auth('patch:surf_contest')
    def edit_surf_contest(payload, contest_id):
        editError = False
        errorDescr = ''
        try:
            if type(payload) is AuthError:
                return auth_error(payload)

            else:
                # Get the json body to update the surf contest
                body = request.get_json()

                # Find the surf spot this contest will be held at
                surfContest = SurfContest.query.get(contest_id)

                if not surfContest:
                    return no_resource(404)

                # Get the json body to update the surf contest
                if 'surf_spot_id' in body:
                    surfSpotId = body['surf_spot_id']
                    surfContest.surfSpotId = surfSpotId

                if 'contest_name' in body:
                    contestName = body['contest_name']
                    surfContest.contest_name = contestName

                if 'contest_date' in body:
                    contestDate = body['contest_date']
                    surfContest.contest_date = contestDate

                if 'contest_image' in body:
                    contestImage = body['contest_image']
                    surfContest.contest_image = contestImage

                # Update the contest table row DB entry
                surfContest.update()

                surfContests = SurfContest.query.order_by(SurfContest.id).all()
                listSurfContests = []

                for contest in surfContests:
                    listSurfContests.append(contest.format())

                return jsonify({
                    "success": True,
                    "contest_count": len(surfContests),
                    "surf_contests": listSurfContests
            })
        except:
            errorDescr = "Could not edit Surf Contest"

        return unprocessable(422, errorDescr)

    '''
    DELETE route for taking surf spots off the tour (Deleting surf spots)
    This should cascade remove all contests associated with this surf spot
    '''
    @app.route('/surf_spots/<int:spot_id>', methods=['DELETE'])
    @requires_auth('delete:surf_spots')
    def delete_surf_spot(payload, spot_id):
        try:
            if type(payload) is AuthError:
                return auth_error(payload)

            else:
                surfSpot = SurfSpot.query.get(spot_id)
                if surfSpot is not None:
                    # First find any contests associated with this Surf Spot
                    surfSpotContests = surfSpot.contests
                    if len(surfSpotContests):
                        # Clean up surfers entered in each contest
                        for surfContest in surfSpotContests:
                            surfContest.surfers = []
                            surfContest.update()
                            surfContest.delete()

                        # Delete Surf Contests
                        surfSpot.contests = []
                        surfSpot.update()

                    # Delete the surf spot if all succeeds
                    surfSpot.delete()

                    surfSpots = SurfSpot.query.order_by(SurfSpot.id).all()
                    listSurfSpots = []

                    for spot in surfSpots:
                        listSurfSpots.append(spot.format())

                    return jsonify({
                        "success": True,
                        "deleted": spot_id,
                        "surf_spot_count": len(listSurfSpots),
                        "surf_spots": listSurfSpots
                    })
        except:
            rollback_db()
            return jsonify({
                    "success": False,
                    "message": "Could not delete Surf Spot"
                })

    # DELETE route for removing (Cancelling/Postponing) Surf Contests
    @app.route('/surf_contests/<int:contest_id>', methods=['DELETE'])
    @requires_auth('delete:surf_contests')
    def delete_surf_contest(payload, contest_id):
        try:
            if type(payload) is AuthError:
                return auth_error(payload)

            else:
                surfContest = SurfContest.query.get(contest_id)
                if surfContest is not None:
                    # Delete Surf contestants (surfers)
                    surfContest.surfers = []
                    surfContest.update()

                    # Delete this contest
                    surfContest.delete()

                    surfContests = SurfContest.query.order_by(SurfContest.id).all()
                    listSurfContests = []

                    for contest in surfContests:
                        listSurfContests.append(contest.format())

                    return jsonify({
                        "success": True,
                        "deleted": contest_id,
                        "contest_count": len(surfContests),
                        "surf_contests": listSurfContests
                    })
        except:
            rollback_db()
            error = True


    # Error Handlers for various API Error codes
    @app.errorhandler(422)
    # def unprocessable(error):
    def unprocessable(error, description="Unprocessable entity"):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable",
            "description": description
        }), 422

    @app.errorhandler(400)
    def bad_request(error, description="Bad Request"):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request."
        }, 400)


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized."
        }, 401)


    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Content Forbidden."
        }, 403)

    @app.errorhandler(404)
    def no_resource(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(authError):
        return jsonify({
            "success": False,
            "error": authError.status_code,
            "message": authError.error
        }), authError.status_code


    return app
app = create_app()

if __name__ == '__main__':
    app.run()