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
    def validate_location(location):
        errors = []
        if type(location) is list:
            if len(location) == 2:
                if (type(location[0]) not in [int, float]) or (type(location[0]) not in [int, float]):
                    errors.append("location should contain only integers or floats")
            else:
                errors.append("location expects only two parameters in the list")

            if not errors:
                return True

            return jsonify({"status":400, "data": [{'error-message' : errors}]})

    @staticmethod
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