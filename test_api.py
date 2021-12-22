import unittest
from flask import json
import app
from database.models import setup_db, User, Body_Measurement 
from auth.auth import AuthError, requires_auth

'''
This is the test class for the api.py file
'''
class ApiTestCase(unittest.TestCase):

    database_name = 'test_fit_tracker'

    '''
    This is the setup method for the test class
    '''
    def setUp(self):
        self.app = app.app
        self.client = self.app.test_client
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdSY3lMSUxkWlBMaWU4XzNjTFpRdyJ9.eyJpc3MiOiJodHRwczovL2Rldi1odDkxcDA4NS51cy5hdXRoMC5jb20vIiwic3ViIjoiMTBhSDU3UzlBMFFWWnlvUXF5WDBGcUljRmlmOVNuMVFAY2xpZW50cyIsImF1ZCI6InByb3RvbmVzIiwiaWF0IjoxNjQwMDcwMDUxLCJleHAiOjE2NDAxNTY0NTEsImF6cCI6IjEwYUg1N1M5QTBRVlp5b1FxeVgwRnFJY0ZpZjlTbjFRIiwic2NvcGUiOiJnZXQ6dXNlci1kZXRhaWwgZ2V0OmJvZHlfbWVhc3VyZW1lbnRzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OnVzZXItZGV0YWlsIiwiZ2V0OmJvZHlfbWVhc3VyZW1lbnRzIl19.R0L6P9haLma8NM96gH8WnNavKMZHSlQr5EBCjpm85a8VQ1T79HOoXDKyOOcIzlygVP4pUQo8MDisi4jzu2T3v9Im6eJEofVsJ2GNKBgZiUsWEuC1P5ZyVO3hEOF7kZOUqbqx4T2634c2Cs1amy2bi5QSUGM78RNU-Ct7RQY9ZBztXEW2x4jMF1VJQFXp0OVojHvtIXNPH4zOaWRtdYV31moJJEoEAmBUZrVqcyOjWIZlyVDPSDwYmAjvLpnm88SOSPvdqaNpIHnjk-wR0exM1DXZC5dKC-rS_palk6lriC3ePFBtQH5Tv9jxTeHVO05tl0sXys7qZIIwFiAPr31uhA'
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdSY3lMSUxkWlBMaWU4XzNjTFpRdyJ9.eyJpc3MiOiJodHRwczovL2Rldi1odDkxcDA4NS51cy5hdXRoMC5jb20vIiwic3ViIjoiMTBhSDU3UzlBMFFWWnlvUXF5WDBGcUljRmlmOVNuMVFAY2xpZW50cyIsImF1ZCI6InByb3RvbmVzIiwiaWF0IjoxNjQwMDY5MDUxLCJleHAiOjE2NDAxNTU0NTEsImF6cCI6IjEwYUg1N1M5QTBRVlp5b1FxeVgwRnFJY0ZpZjlTbjFRIiwic2NvcGUiOiJnZXQ6dXNlci1kZXRhaWwgZ2V0OmJvZHlfbWVhc3VyZW1lbnRzIGRlbGV0ZTpib2R5X21lYXN1cmVtZW50cyBwYXRjaDpib2R5X21lYXN1cmVtZW50cyBwb3N0OnVzZXJzIHBvc3Q6Ym9keV9tZWFzdXJlbWVudHMgZGVsZXRlOnVzZXJzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OnVzZXItZGV0YWlsIiwiZ2V0OmJvZHlfbWVhc3VyZW1lbnRzIiwiZGVsZXRlOmJvZHlfbWVhc3VyZW1lbnRzIiwicGF0Y2g6Ym9keV9tZWFzdXJlbWVudHMiLCJwb3N0OnVzZXJzIiwicG9zdDpib2R5X21lYXN1cmVtZW50cyIsImRlbGV0ZTp1c2VycyJdfQ.sxTLPmd1j1SfPq_4TymudpKB-RJ5Gi-rhVpqhqOJo7gTkeWA1yuJ68B4LrZHijwrOJI0-iQ8su_eHLbZgTj20bX2xwC_Zvvwelc9cOSKcOI16CngwXlb1wnG7MwIhK12J70EI2wBRdhtPXo0knuJBswQdTLiViLWX6lmH6od5Q8NYuDdRcnz-42RtUdHRCw-vKYeUrAtqEvbI6ZrdoBiNmEa11GSJTd7xLlmV5-RYALMAW3GGmJm84Q5A73RPQH_8kIgcT2y5oxN7s6RpjjRChMKoOWDyzlWONTPlV9IK1N5i8MTMGpj3Xirsu9ykwQql6bu3aUko0MRKKBgjnODZg'
        self.new_user = {'full_name': 'Test User', 'age': '20', 'nick_name': 'test_user'}
        self.new_body_measurement = {'weight': 100.0, 'height': 100.0, 'user_id': 1}

    def tearDown(self):
        pass
    '''
    Test access /users endpoint with no authorization header
    '''
    def test_get_users(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['users']) > 0)
    '''
    Test access /users-detail endpoint with authorization header
    '''
    def test_get_users_detail(self):
        res = self.client().get('/users-detail', headers={'Authorization': 'Bearer ' + self.admin_token}, json={'id': '1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['users']) > 0)
    '''
    Test creating a new user with authorized user
    '''
    def test_create_user(self):
        res = self.client().post('/users', json=self.new_user, headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])    

    '''
    Test creating a new body measurement with unauthorized user
    '''
    def test_create_user_unauthorized_user(self):
        res = self.client().post('/users', json=self.new_user, headers={'Authorization': 'Bearer ' + self.user_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    '''
    Test creating a new user with invalid payload
    '''
    def test_create_user_invalid_json(self):
        res = self.client().post('/users', json={}, headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    '''
    Test creating a new user with no authorization header
    '''
    def test_create_user_no_auth(self):
        res = self.client().post('/users', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')
    '''
    Test creating a new body_measurement with authorized user
    '''
    def test_create_body_measurement(self):
        res = self.client().post('/users/body_measurements', json=self.new_body_measurement, headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    '''
    Test creating a new body_measurement with empty payload
    '''
    def test_create_body_measurement_fail(self):
        res = self.client().post('/users/body_measurements', json={}, headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    '''
    Test creating a new body_measurement with unauthorized user
    '''
    def test_create_body_measurement_unauthorized_user(self):
        res = self.client().post('/users/body_measurements', json=self.new_body_measurement, headers={'Authorization': 'Bearer ' + self.user_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    '''
    Test updating a user with authorized user
    '''
    def update_body_measurements(self):
        res = self.client().patch('/body_measurements/1', json=self.new_user, headers={'Authorization': 'Bearer ' + self.admin_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    '''
    Test updating a user with unauthorized user
    '''
    def test_update_user_unauthorized_user(self):
        res = self.client().patch('/body_measurements/1', json=self.new_user, headers={'Authorization': 'Bearer ' + self.user_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')