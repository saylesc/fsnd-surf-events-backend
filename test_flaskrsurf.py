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
            'wave_image': "data:image/jpeg;base64,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"
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
        surfContest = SurfContest.query.filter(SurfContest.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['contest_count'])
        self.assertTrue(len(data['surf_contests']))
        self.assertEqual(surfContest, None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
