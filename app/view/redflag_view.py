import datetime
from flask import jsonify, request
from app.model.redflag_model import RedFlag
from flask.views import MethodView

redflag_list = []


class RedFlagViews(MethodView):

    def get(self, id):
        if id is None:
            if not redflag_list:
                return jsonify({"status":200, "data": "No red-flags found. Please create one."})

            return jsonify({"status":200,"data": [redflag_record.__dict__ for redflag_record in redflag_list]})

        
        try:
            redflag_id = int(id)
        except:
            return jsonify({"status": 400, "data":[{"error-message":"id should be a non negative integer" }]})
        
        if redflag_id > 0:
            single_redflag_record = [redflag_record.__dict__ for redflag_record in redflag_list if redflag_record.__dict__['id'] == redflag_id ]
            if single_redflag_record:
                return jsonify({"status":200, "data": single_redflag_record[0]})
            return jsonify({"status":404, "data":[{"error-message" : "No red-flag found"}]})
        return jsonify({"status": 400, "data":[{"error-message" : "id should be a non negative integer"}]})




    # Create a red-flag record
    def post(self):
        if request.content_type == 'application/json':
            if 'createdBy' in request.json  and 'location' in request.json and 'comment' in request.json:
                errors = []
                if not request.json['createdBy'] or  not request.json['location'] or not request.json['comment']:
                    errors.append("createdBy, location, and comment cannot be empty.")
                if not isinstance(request.json['createdBy'], str):
                    errors.append("createdBy should be a string")

                if type(request.json['location']) is list:
                    if len(request.json['location']) == 2:
                        if (type(request.json['location'][0]) not in [int, float]) or (type(request.json['location'][0]) not in [int, float]):
                            errors.append("location should contain only integers or floats")
                    else:
                        errors.append("location expects only two parameters in the list")
                if not type(request.json['location']) is list:
                    errors.append("wrong location format. follow this example ->> {'location':[12.3453,9.6589]}")
                if not isinstance(request.json['comment'], str):
                    errors.append("comment should be string")

                if errors:
                    return jsonify({"status":400, "data": [{'error-message' : errors}]})
                
                if redflag_list:
                    check_for_existance = [redflag_record.__dict__ for redflag_record in redflag_list if redflag_record.__dict__['createdBy'] == request.json['createdBy'] and \
                                    redflag_record.__dict__['location'] == request.json['location'] and redflag_record.__dict__['comment'] == request.json['comment']]
                    if check_for_existance:
                        return jsonify({"status":400, "data":[{'error-message': 'This red-flag already exists, please create a new one.'}]})
            
                # red flag record primary key
                id = len(redflag_list)+1
                new_redflag_record = RedFlag(id, str(datetime.datetime.now()), request.json['createdBy'], "red-flag", \
                                                request.json['location'], "draft", request.json['comment'])

                redflag_list.append(new_redflag_record)
                return jsonify({"status":201, "data":[{"id":id, "message":"Created red-flag record"}]}), 201
            
            return jsonify({"status":400, "data": [{'error-message' : 'wrong body format. follow this example ->> '+'{“createdBy”:​James​, “location”:​​[12.4567,3.6789]​, “comment”:​collapsed bridges}'}]})
        return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]}) 

    def put(self, id):
        try:
            redflag_id = int(id)
        except:
            return jsonify({"status": 400, "data":[{"error-message":"id should be a non negative integer" }]})
        
        if redflag_id > 0:
            if request.content_type == 'application/json':
                if 'location' in request.json and type(request.json['location']) is list:
                    errors = []
                    if type(request.json['location']) is list:
                        if len(request.json['location']) == 2:
                            if (type(request.json['location'][0]) not in [int, float]) or (type(request.json['location'][0]) not in [int, float]):
                                errors.append("location should contain only integers or floats")
                        else:
                            errors.append("location expects only two parameters in the list")
                    if not type(request.json['location']) is list:
                        errors.append("wrong location format. follow this example ->> {'location':[12.3453,9.6589]}")

                    if not errors:
                        redflag_json = request.get_json()
                        for redflag_record in redflag_list:
                            if redflag_record.__dict__['id'] == redflag_id:
                                if redflag_record.__dict__['status'] in ['under investigation','rejected','resolved']:
                                    return jsonify({"status":400, "data": [{"error-message" : "You can no longer edit or delete this red-flag"}]})
                                redflag_record.__dict__['location'] = redflag_json['location']
                                return jsonify({"status":400, "data":[{"id":redflag_id, "message":"Updated red-flag record’s location"}]})
                        return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
                    return jsonify({"status":400, "data": [{'error-message' : errors}]})
                return jsonify({"status": 400, "data":[{"error-message" : "wrong body format. follow this example ->> {'status':'under investigation'}"}]})
            return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
        return jsonify({"status": 400, "data":[{"error-message" : "id cannot be a negative"}]})

    # Delete a specific red flag record
    def delete(self, id):
        try:
            redflag_id = int(id)
        except:
           return jsonify({"status": 400, "data":[{"error-message" : "id should be a non negative integer"}]})

        if 'createdBy' in request.json and isinstance(request.json['createdBy'], str): 
            if redflag_id > 0:
                for redflag_record in redflag_list:
                    if redflag_record.__dict__['id'] == redflag_id:
                        if redflag_record.__dict__['createdBy'] == request.json['createdBy']:
                            if redflag_record.__dict__['status'] in ['under investigation','rejected','resolved']:
                                return jsonify({"status":400, "data": [{"error-message" : "You can no longer edit or delete this red-flag"}]})
                            redflag_list.remove(redflag_record)
                            return jsonify({"status":201, "data":[{"id":id, "message":"red-flag record has been deleted"}]})
                        return jsonify({"status": 400, "data":[{"error-message" : "invalid username"}]})
                return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
            return jsonify({"status": 400, "data":[{"error-message" : "id cannot be a negative"}]})
        return jsonify({"status": 400, "data":[{"error-message" : "username is missing. follow this example ->> {'createdBy':'James']}"}]})
        
class UpdateStatus(MethodView):

     def put(self, id):
        try:
            redflag_id = int(id)
        except:
            return jsonify({"status": 400, "data":[{"error-message":"id should be a non negative integer" }]})
        
        if redflag_id > 0:
            if request.content_type == 'application/json':
                if 'status' in request.json and isinstance(request.json['status'], str):
                    redflag_json = request.get_json()
                    for redflag_record in redflag_list:
                        if redflag_record.__dict__['id'] == redflag_id:
                            if redflag_json['status'].lower() in ['under investigation','rejected', 'resolved']:
                                redflag_record.__dict__['status'] = redflag_json['status'].lower()
                                return jsonify({"status":200, "data":[{"id":redflag_id, "message":"Updated red-flag record’s location"}]})
                            return jsonify({"status":400, "data": [{"error-message" : "The status can either be 'under investigation', 'rejected', or 'resolved'"}]})
                    return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
                return jsonify({"status": 400, "data":[{"error-message" : "wrong body format. follow this example ->> {'status':'under investigation'}"}]})
            return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
        return jsonify({"status": 400, "data":[{"error-message" : "id cannot be a negative"}]})


class RedFlagUrls:
    @staticmethod
    def fetch_urls(app):
        redflag_view  = RedFlagViews.as_view('ireporter')
        update_status  = UpdateStatus.as_view('update_status')
        app.add_url_rule('/api/v1/red-flags', defaults={'id': None},
                         view_func=redflag_view, methods=['GET',])
        app.add_url_rule('/api/v1/red-flags', view_func=redflag_view, methods=['POST'])
        app.add_url_rule('/api/v1/red-flags/<id>', view_func=redflag_view,  methods=['GET', 'PUT', 'DELETE'])
        app.add_url_rule('/api/v1/update-red-flags/<id>', view_func=update_status,  methods=['PUT'])
