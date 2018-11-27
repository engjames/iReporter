import pytest
from flask import json
from app import app
CLIENT = app.test_client 

############################# Tests for addng a new red-flag ######################################
def test_to_create_a_new_redflag():
    """
    Method for addng a new red-flag
    """
    result = CLIENT().post('/api/v1/red-flags', content_type='application/json',
                           data=json.dumps({"createdBy" : "James",
                                            "location" : [8.6784, 2.5673],
                                            "comment" : "collapsed bridges"}))
    assert result.status_code == 201

    json_data = json.loads(result.data)
    assert "data" in json_data
    assert json_data['data'][0]['id'] == 1
    assert json_data['data'][0]['message'] == "Created red-flag record"

    #make a get request to check whether the red-flag exists
    check_redflag = CLIENT().get('/api/v1/red-flags')
    assert check_redflag.status_code == 200
    json_data = json.loads(check_redflag.data)
    assert json_data['data'][0]['id'] == 1
    assert json_data['data'][0]['location'] == [8.6784, 2.5673]
    assert json_data['data'][0]['createdBy'] == "James"
    assert json_data['data'][0]['comment'] == "collapsed bridges"
    

############################# Tests for getting all red-flags ######################################

def test_to_get_all_redflags():
    """
    Method for fetching all red-flags.
    """
    result = CLIENT().get('/api/v1/red-flags')
    assert result.status_code == 200
    json_data = json.loads(result.data)
    assert json_data['data'][0]['id'] == 1
    assert json_data['data'][0]['category'] == "red-flag"
    assert json_data['data'][0]['location'] == [8.6784, 2.5673]
    assert json_data['data'][0]['createdBy'] == "James"
    assert json_data['data'][0]['comment'] == "collapsed bridges"
    assert json_data['data'][0]['status'] == "draft"

############################# Tests for getting a specific red-flag ######################################
def test_to_get_a_specific_redflags():
    """
    Method for fetching a specific red-flag
    """
    result = CLIENT().get('/api/v1/red-flags/1')
    assert result.status_code == 200
    json_data = json.loads(result.data)
    assert json_data['data']['id'] == 1
    assert json_data['data']['category'] == "red-flag"
    assert json_data['data']['location'] == [8.6784, 2.5673]
    assert json_data['data']['createdBy'] == "James"
    assert json_data['data']['comment'] == "collapsed bridges"
    assert json_data['data']['status'] == "draft"

############################# Tests for changing geolocation ######################################
def test_to_change_geolocation_of_a_redflag():
    """
    Method for changing geolocation
    """
    result = CLIENT().put('/api/v1/red-flags/1', content_type='application/json',
                           data=json.dumps({"location" : [0.9090,5.9090]}))
    
    assert result.status_code == 200

    json_data = json.loads(result.data)
    assert "data" in json_data
    assert json_data['data'][0]['id'] == 1
    assert json_data['data'][0]['message'] == "Updated red-flag record’s location"

    #make a put request to check whether the red-flag has been updated
    check_redflag = CLIENT().get('/api/v1/red-flags/1')
    assert check_redflag.status_code == 200
    json_data = json.loads(check_redflag.data)
    assert json_data['data']['id'] == 1
    assert json_data['data']['location'] == [0.9090,5.9090]
    assert json_data['data']['category'] == "red-flag"
    assert json_data['data']['createdBy'] == "James"
    assert json_data['data']['comment'] == "collapsed bridges"
    assert json_data['data']['status'] == "draft"
