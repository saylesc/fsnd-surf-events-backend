import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, SurfSpot, SurfContest, Surfer


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
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_specific_surfer(self):
        res = self.client().get('/surfers/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['surfer_info'])

    def test_nonexistent_surfer(self):
        res = self.client().get('/surfers/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['surfer_info'])

    def test_surf_spots(self):
        res = self.client().get('/surf_spots')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_spots']))

    def test_method_not_allowed_surf_spots(self):
        res = self.client().patch('/surf_spots')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data['surf_spots']))

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
        self.assertTrue(len(data['surf_contests']))

    def test_surf_contests_at_spot_1(self):
        res = self.client().get('/surf_spots/1/contests')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['surf_contests'])

    def test_422_if_surf_spot_does_not_exist(self):
        res = self.client().get('/surf_spots/11111/contests')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

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

        res = self.client().post('/surf_spot/create', json=new_surf_spot)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_spots']))
        self.assertTrue(data['surf_spot_count'])

    def test_create_surf_contest(self):
        new_contest = {
            'surf_spot_id': 1,
            'contest_name': '2021 Volcom Pro',
            'contest_date': "2021-08-14",
            'contest_image': "test.png"
            }

        res = self.client().post('/surf_contest/create', json=new_contest)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_contests']))
        self.assertTrue(data['contest_count'])

    def test_add_invalid_missing_data(self):
        new_contest = {
            'surf_spot_id': 1,
            'contest_name': '2021 Volcom Pro',
            'contest_date': "INVALID_DATE",
            'contest_image': "test.png"
            }

        res = self.client().post('/surf_contest/create', json=new_contest)
        data = json.loads(res.data)

        # What error do I get here?
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_edit_surf_contests(self):
        edit_contest = {
            'surf_spot_id': 2,
            'contest_name': '2021 Trestles Billabong Pro',
            'contest_date': "2021-08-14",
            }
        res = self.client().post('/surf_contests/2', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['surf_contests']))
        self.assertTrue(data['contest_count'])

    def test_delete_surf_spots(self):
        res = self.client().delete('/surf_spots/1')
        data = json.loads(res.data)

        # Verify deleted surf spot is now None (doesn't exist in DB)
        surfSpot = SurfSpot.query.filter(SurfSpot.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['contest_count'])
        self.assertTrue(len(data['surf_contests']))
        self.assertEqual(surfSpot, None)

    def test_delete_surf_contests(self):
        res = self.client().delete('/surf_contests/2')
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
