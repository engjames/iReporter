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
        if validate is not True:
            return Validators.validate_redflag_id(id)
        single_redflag_record = [redflag_record.__dict__ for redflag_record in redflag_list if redflag_record.__dict__['id'] == int(id) ]
        if single_redflag_record:
            return jsonify({"status":200, "data": single_redflag_record[0]})
        return jsonify({"status":404, "data":[{"error-message" : "No red-flag found"}]})
        
        
    # Create a red-flag record
    def post(self):
        
        if not request.content_type == 'application/json':
            return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
           
        if 'createdBy' not in request.json  and 'location' not in request.json and 'comment' not in request.json:
            return jsonify({"status":400, "data": [{"error-message" : "wrong body format. follow this example ->> {'createdBy':​James​, 'location':​​[12.4567,3.6789]​, 'comment': '​collapsed bridges'"}]})
        
        validate_data = Validators.validate_create_redflag(request.json['createdBy'],request.json['location'],request.json['comment'])
        
        if validate_data is not True:
            return validate_data
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
        
        
        
         

    def put(self, id):
        update_id = Validators.validate_redflag_id(id)
        if update_id is not True:
            return Validators.validate_redflag_id(id)
        if not request.content_type == 'application/json':
             return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
        if 'location' not in request.json:
            return jsonify({"status": 400, "data":[{"error-message" : "wrong body format. follow this example ->> {'status':'under investigation'}"}]})
        
        location_validations = Validators.validate_location(request.json['location'])
        if location_validations is not True:
            return location_validations

        redflag_json = request.get_json()
        for redflag_record in redflag_list:
            if redflag_record.__dict__['id'] == int(id):
                if redflag_record.__dict__['status'] in ['under investigation','rejected','resolved']:
                    return jsonify({"status":400, "data": [{"error-message" : "You can no longer edit or delete this red-flag"}]})
                redflag_record.__dict__['location'] = redflag_json['location']
                return jsonify({"status":400, "data":[{"id":int(id), "message":"Updated red-flag record’s location"}]})
        return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
    
        
    # Delete a specific red flag record
    def delete(self, id):
        get_id = Validators.validate_redflag_id(id)
        if get_id is not True:
             return  Validators.validate_redflag_id(id)
        if not request.content_type == 'application/json':
            return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
        if 'createdBy' not in request.json: 
            return jsonify({"status": 400, "data":[{"error-message" : "username is missing. follow this example ->> {'createdBy':'James'}"}]})
        if not isinstance(request.json['createdBy'],str):
            return jsonify({"status":400, "data": [{"error-message" : "Username must be a string. follow this example ->> {'createdBy':'James'}"}]})

        for redflag_record in redflag_list:
            if redflag_record.__dict__['id'] == int(id):
                if not redflag_record.__dict__['createdBy'] == request.json['createdBy']:
                    return jsonify({"status": 400, "data":[{"error-message" : "invalid username"}]})
                status = redflag_record.__dict__['status']
                if status in ['under investigation','rejected','resolved']:
                    return jsonify({"status":400, "data": [{"error-message" : "You can no longer edit or delete this red-flag"}]})
                redflag_list.remove(redflag_record)
                return jsonify({"status":201, "data":[{"id":int(id), "message":"red-flag record has been deleted"}]})
                
        return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
        
        
       
       


class UpdateStatus(MethodView):

     def put(self, id):
        update_id = Validators.validate_redflag_id(id)
        if update_id is not True:
            return Validators.validate_redflag_id(id)
        if not request.content_type == 'application/json':
            return jsonify({"status":202, "data":[{'error-message' : 'Content-type must be json'}]})
        if not 'status' in request.json:
            return jsonify({"status": 400, "data":[{"error-message" : "wrong body format. follow this example ->> {'status':'under investigation'}"}]})
        if not isinstance(request.json['status'], str):
            return jsonify({"status":400, "data": [{"error-message" : "the status must be a string. follow this example ->> {'status':'resolved'}"}]})
        
        redflag_json = request.get_json()
        for redflag_record in redflag_list:
            if redflag_record.__dict__['id'] == int(id):
                if not redflag_json['status'].lower() in ['under investigation','rejected', 'resolved']:
                    return jsonify({"status":400, "data": [{"error-message" : "The status can either be 'under investigation', 'rejected', or 'resolved'"}]})
                redflag_record.__dict__['status'] = redflag_json['status'].lower()
                return jsonify({"status":200, "data":[{"id":int(id), "message":"Updated red-flag record’s location"}]})
                
        return jsonify({"status":404, "data": [{"error-message" : "No red-flag found"}]})
        
        
        


class RedFlagUrls:
    @staticmethod
    def fetch_urls(app):
        redflag_view  = RedFlagViews.as_view('ireporter')
        update_status  = UpdateStatus.as_view('update_status')
        app.add_url_rule('/red-flags', defaults={'id': None},
                         view_func=redflag_view, methods=['GET',])
        app.add_url_rule('/red-flags', view_func=redflag_view, methods=['POST',])
        app.add_url_rule('/red-flags/<id>', view_func=redflag_view,  methods=['GET', 'PUT', 'DELETE'])
        app.add_url_rule('/update-red-flags/<id>', view_func=update_status,  methods=['PUT'])
