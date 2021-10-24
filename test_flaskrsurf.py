import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskrsurf import create_app
from models import setup_db, SurfSpot, SurfContest, Surfer

surfManagerToken = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpMWEtodFZhWnkxWWloaVVpY3ItayJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2F5bGVzYy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTMzOTQ5NTc3ODc3NDA4Nzk3MDIiLCJhdWQiOlsiZnNuZC1zdXJmLWV2ZW50cyIsImh0dHBzOi8vZnNuZC1zYXlsZXNjLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MzUxMTA5MzAsImV4cCI6MTYzNTE1NDEzMCwiYXpwIjoibXFBWWVqNmNTek5pTHM1M282bEhCYUd2UVROUHNlYVEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicGF0Y2g6YWRkX3N1cmZlciIsInBhdGNoOnJlbW92ZV9zdXJmZXIiXX0.l_Thp4P-v4Bx1qkYTnrISH034Ptuyanh9d1pvEs1-nHNjwt8-iY3EBUXo4s3kaXf-fyXCxhv92yC3QyFh-a1mnyyo5fWE-GAcRBcxon3cVnbJ2y3FISpDejgM0RNml20M0TwQpLKUJe6kMQpyRQN6WRbgRPf77Sc4o_0oKrP6gxR8o3gMkOARgxu0PQUZjftnyRgBIJOfRURd4gGwtBzfsYqxM6MLV_D1fl4R6kNyf0RibIRvD_ylX_ISYVi3VY8jRTdfdARQS1TV5jUAabEsMXJSNLaEVo2GD_rdWfwpwkVL5QeyYicP4lALnqk_t0lRn3OSR9wNlWPklBzBiO7xA'
surfCoordinatorToken = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpMWEtodFZhWnkxWWloaVVpY3ItayJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2F5bGVzYy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc1OTk3NTk0ODIxODcwMzM5MTMiLCJhdWQiOlsiZnNuZC1zdXJmLWV2ZW50cyIsImh0dHBzOi8vZnNuZC1zYXlsZXNjLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MzUxMTA3NzIsImV4cCI6MTYzNTE1Mzk3MiwiYXpwIjoibXFBWWVqNmNTek5pTHM1M282bEhCYUd2UVROUHNlYVEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnN1cmZfY29udGVzdHMiLCJkZWxldGU6c3VyZl9zcG90cyIsInBhdGNoOmFkZF9zdXJmZXIiLCJwYXRjaDpyZW1vdmVfc3VyZmVyIiwicGF0Y2g6c3VyZl9jb250ZXN0IiwicG9zdDpzdXJmX2NvbnRlc3RzIiwicG9zdDpzdXJmX3Nwb3RzIl19.xOE3aod1y6AS0BGw9eoqtAp5fMnH97w7R-gXFcKweA_6zrgPSTP31VWJfLleZ-Ttwpcyf19l7y66NajiAyI9z62lSGfaXa4JU7hdnBDPOs1nbMW92oZGkc6i8KCqV3zkls6CW_Ky_VSuk5lw3yZNOtZbu8S_JCVomBpLn9Lzbae4BG8IfT5sCqthKCEbpmtxGxblojvdtg4Rt7OHBGN2vs5-HMxTaDcQaTIN2WkyP0wRK4V5U7VuAh9wrsPW4mv1113S42TeowmrUx0zMHmm7oqDq_zt4_kG4uSmY3rrE8k198g8mZSsJr2bIX-0jK1q2Y9Ombr9lVCltv4ZJWSA3Q'

class SurfEventsTestCase(unittest.TestCase):
    """This class represents the Surf Events test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "surf_events_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test case for surfers
    """
    def test_surfers(self):
        res = self.client().get('/surfers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surfers']))

    def test_surfers_invalid_method(self):
        res = self.client().post('/surfers')

        self.assertEqual(res.status_code, 405)

    def test_specific_surfer(self):
        res = self.client().get('/surfers/43')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['surfer_info'])

    def test_nonexistent_surfer(self):
        res = self.client().get('/surfers/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_surf_spots(self):
        res = self.client().get('/surf_spots')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_spots']))

    def test_method_not_allowed_surf_spots(self):
        res = self.client().patch('/surf_spots')

        self.assertEqual(res.status_code, 405)

    def test_surf_contests(self):
        res = self.client().get('/surf_contests')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_contests']))

    def test_specific_surf_contests(self):
        res = self.client().get('/surf_contests/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_contest']))

    def test_invalid_surf_contests(self):
        res = self.client().get('/surf_contests/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_surf_contests_at_spot_1(self):
        res = self.client().get('/surf_spots/1/contests')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['surf_contests'])

    def test_422_if_surf_spot_does_not_exist(self):
        res = self.client().get('/surf_spots/11111/contests')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_surfer(self):
        search_criteria = {
            'search_term': 'aN'
        }

        res = self.client().post('/surfers/search', json=search_criteria)
        data = json.loads(res.data)

        # Verify results are positive
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['count'])
        self.assertTrue(len(data['surfers']))

    def test_no_results_search_surfer(self):
        search_criteria = {
            'search_term': 'aNdi843'
        }

        res = self.client().post('/surfers/search', json=search_criteria)
        data = json.loads(res.data)

        # Verify results are positive
        self.assertEqual(res.status_code, 404)

    def test_create_surf_spot(self):
        new_surf_spot = {
            'name': "Playalinda",
            'city': 'Cape Canaveral',
            'state': "FL",
            'country': "USA",
            'wave_type': "Beachbreak",
            'wave_image': "test.png"
            }

        headers = {
            'Authorization': surfCoordinatorToken
        }
        res = self.client().post('/surf_spot/create', headers=headers, json=new_surf_spot)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['surf_spots']))
        self.assertTrue(data['surf_spot_count'])

    def test_create_surf_contest(self):
        new_contest = {
            'surf_spot_id': 1,
            'contest_name': '2021 Volcom Pro',
            'contest_date': '2021-11-14',
            'contest_image': 'test.png'
            }

        headers = {
            'Authorization': surfCoordinatorToken
        }
        res = self.client().post('/surf_contest/create', headers=headers, json=new_contest)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['surf_contests']))
        self.assertTrue(data['contest_count'])

    def test_add_invalid_missing_data(self):
        new_contest = {
            'surf_spot_id': 1,
            'contest_name': '2021 Volcom Pro',
            'contest_date': "INVALID_DATE",
            'contest_image': "test.png"
            }

        headers = {
            'Authorization': surfCoordinatorToken
        }
        res = self.client().post('/surf_contest/create', headers=headers, json=new_contest)
        data = json.loads(res.data)

        # What error do I get here?
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_edit_surf_contests(self):
        edit_contest = {
            'surf_spot_id': 2,
            'contest_name': '2021 Trestles Billabong Pro',
            'contest_date': "2021-08-14",
            }

        headers = {
            'Authorization': surfCoordinatorToken
        }
        res = self.client().patch('/surf_contests/2', headers=headers, json=edit_contest)
        data = json.loads(res.data)

        # Verify by checking http://localhost:5000/surf_spots/2/contests
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_contests']))
        self.assertTrue(data['contest_count'])

    def test_delete_surf_spots(self):
        headers = {
            'Authorization': surfCoordinatorToken
        }

        res = self.client().delete('/surf_spots/1', headers=headers)

        # Verify deleted surf spot is now None (doesn't exist in DB)
        surfSpot = SurfSpot.query.filter(SurfSpot.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(surfSpot, None)

    def test_delete_surf_contests(self):
        headers = {
            'Authorization': surfCoordinatorToken
        }

        res = self.client().delete('/surf_contests/2', headers=headers)
        data = json.loads(res.data)

        # Verify deleted surf contest is now None (doesn't exist in DB)
        surfContest = SurfContest.query.filter(
            SurfContest.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['contest_count'])
        self.assertTrue(len(data['surf_contests']))
        self.assertEqual(surfContest, None)

    def test_delete_surf_contests_invalid_token(self):
        headers = {
            'Authorization': surfManagerToken
        }

        res = self.client().delete('/surf_contests/2', headers=headers)
        data = json.loads(res.data)

        # Verify deleted surf contest is now None (doesn't exist in DB)
        surfContest = SurfContest.query.filter(
            SurfContest.id == 2).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
