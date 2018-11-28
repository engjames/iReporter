from flask import  make_response, jsonify

class Validators:
    @staticmethod
    def validate_redflag_id(id):
        try:
                redflag_id = int(id)
        except:
            return make_response(jsonify({"status": 400, "data":[{"error-message":"id should be a non negative integer" }]}))

        if redflag_id > 0:
            return True
        return make_response(jsonify({"status": 400, "data":[{"error-message" : "id should be a non negative integer"}]}))

    @staticmethod
    def validate_location(get_location):
        get_errors = []
        if type(get_location) is list:
            if len(get_location) == 2:
                if (type(get_location[0]) not in [int, float]) or (type(get_location[0]) not in [int, float]):
                    get_errors.append("location should contain only integers or floats")
            else:
                get_errors.append("location expects only two parameters in the list")
        if not type(get_location) is list:
            get_errors.append("wrong location format. follow this example ->> {'location':[12.3453,9.6589]}")
        
        if not get_errors:
            return True

        return jsonify({"status":400, "data": [{'error-message' : get_errors}]})


    def validate_create_redflag(createdBy,location,comment):
        errors = []
        if not createdBy or  not location or not comment:
            errors.append("createdBy, location, and comment cannot be empty.")
        if not isinstance(createdBy, str):
            errors.append("createdBy should be a string")

        if type(location) is list:
            if len(location) == 2:
                if (type(location[0]) not in [int, float]) or (type(location[0]) not in [int, float]):
                    errors.append("location should contain only integers or floats")
            else:
                errors.append("location expects only two parameters in the list")
        if not type(location) is list:
            errors.append("wrong location format. follow this example ->> {'location':[12.3453,9.6589]}")
        if not isinstance(comment, str):
            errors.append("comment should be string")

        if errors:
            return jsonify({"status":400, "data": [{'error-message' : errors}]})

        return True