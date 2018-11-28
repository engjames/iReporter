import datetime
from flask import jsonify, request
from app.model.redflag_model import RedFlag
from flask.views import MethodView
from app.view.helper import Validators

redflag_list = []
class RedFlagViews(MethodView):

    #self, id, "23/11/2018", "James", "red-flag", (12.6578.8.9090), "draft", "collapsed bridges"
    # redflag_record = RedFlag(1,"23/11/2018", "James", "red-flag", [12.6578,8.9090], "rejected", "collapsed bridges")
   
    def get(self, id):
        if id is None:
            if not redflag_list:
                return jsonify({"status":200, "data":[{"message":"No red-flags found. Please create one."}]})
            return jsonify({"status":200,"data": [redflag_record.__dict__ for redflag_record in redflag_list]})

        validate = Validators.validate_redflag_id(id)
        if validate is True:
            single_redflag_record = [redflag_record.__dict__ for redflag_record in redflag_list if redflag_record.__dict__['id'] == int(id) ]
            if single_redflag_record:
                return jsonify({"status":200, "data": single_redflag_record[0]})
            return jsonify({"status":404, "data":[{"error-message" : "No red-flag found"}]})
        return Validators.validate_redflag_id(id)
        
    # Create a red-flag record
    def post(self):
        
        if request.content_type == 'application/json':
           
            if 'createdBy' in request.json  and 'location' in request.json and 'comment' in request.json:
                validate_data = Validators.validate_create_redflag(request.json['createdBy'],request.json['location'],request.json['comment'])
                
                if validate_data is True:
                    if redflag_list:
                        check_for_existance = [redflag_record.__dict__ for redflag_record in redflag_list if redflag_record.__dict__['createdBy'] == request.json['createdBy'] and \
                                        redflag_record.__dict__['location'] == request.json['location'] and redflag_record.__dict__['comment'] == request.json['comment']]
                        if check_for_existance:
                            return jsonify({"status":400, "data":[{'error-message': 'This red-flag already exists, please create a new one.'}]})
            
                    # red flag record primary key
                    redflag_id = len(redflag_list)+1
                    new_redflag_record = RedFlag(redflag_id, str(datetime.datetime.now()), request.json['createdBy'], "red-flag", \
                                                    request.json['location'], "draft", request.json['comment'])

                    redflag_list.append(new_redflag_record)
                    return jsonify({"status":201, "data":[{"id":redflag_id, "message":"Created red-flag record"}]}),201
                return validate_data
            
            return jsonify({"status":400, "data": [{"error-message" : "wrong body format. follow this example ->> {'createdBy':​James​, 'location':​​[12.4567,3.6789]​, 'comment': '​collapsed bridges'"}]})
        return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]}) 

    def put(self, id):
        update_id = Validators.validate_redflag_id(id)
        if update_id is True:
            if request.content_type == 'application/json':
                if 'location' in request.json and type(request.json['location']) is list:
                    t = Validators.validate_location(request.json['location'])
                    if t is True:
                        redflag_json = request.get_json()
                        for redflag_record in redflag_list:
                            if redflag_record.__dict__['id'] == int(id):
                                if redflag_record.__dict__['status'] in ['under investigation','rejected','resolved']:
                                    return jsonify({"status":400, "data": [{"error-message" : "You can no longer edit or delete this red-flag"}]})
                                redflag_record.__dict__['location'] = redflag_json['location']
                                return jsonify({"status":400, "data":[{"id":int(id), "message":"Updated red-flag record’s location"}]})
                        return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
                    return t
                return jsonify({"status": 400, "data":[{"error-message" : "wrong body format. follow this example ->> {'status':'under investigation'}"}]})
            return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
        return update_id
            
        


    # Delete a specific red flag record
    def delete(self, id):
        get_id = Validators.validate_redflag_id(id)
        if get_id is True:
            if request.content_type == 'application/json':
                if 'createdBy' in request.json and isinstance(request.json['createdBy'], str): 
                    for redflag_record in redflag_list:
                        if redflag_record.__dict__['id'] == int(id):
                            if redflag_record.__dict__['createdBy'] == request.json['createdBy']:
                                status = redflag_record.__dict__['status']
                                if status in ['under investigation','rejected','resolved']:
                                    return jsonify({"status":400, "data": [{"error-message" : "You can no longer edit or delete this red-flag"}]})
                                redflag_list.remove(redflag_record)
                                return jsonify({"status":201, "data":[{"id":id, "message":"red-flag record has been deleted"}]})
                            return jsonify({"status": 400, "data":[{"error-message" : "invalid username"}]})
                    return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
                return jsonify({"status": 400, "data":[{"error-message" : "username is missing. follow this example ->> {'createdBy':'James']}"}]})
            return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
        return get_id
       


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
        app.add_url_rule('/api/v1/red-flags', view_func=redflag_view, methods=['POST',])
        app.add_url_rule('/api/v1/red-flags/<id>', view_func=redflag_view,  methods=['GET', 'PUT', 'DELETE'])
        app.add_url_rule('/api/v1/update-red-flags/<id>', view_func=update_status,  methods=['PUT'])
