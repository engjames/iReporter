from flask import make_response, jsonify


class Validators:
    @staticmethod
    def validate_redflag_id(id):
        try:
            redflag_id = int(id)
        except:
            return make_response(jsonify({"status": 400, "data": [{"error-message": "id should be a non negative integer"}]}))
        if redflag_id > 0:
            return True
        return make_response(jsonify({"status": 400, "data": [{"error-message": "id should be a non negative integer"}]}))

    @staticmethod
    def validate_location(get_location):
        get_errors = []
        if type(get_location) is list:
            if len(get_location) == 2:
                if (type(get_location[0]) not in [int, float]) or (type(get_location[1]) not in [int, float]):
                    get_errors.append(
                        "location should contain only integers or floats")
            else:
                get_errors.append(
                    "location expects only two parameters in the list")
        if not type(get_location) is list:
            get_errors.append(
                "wrong location format. follow this example ->> {'location': [12.3453,9.6589]}")
        if not get_errors:
            return True
        return jsonify({"status": 400, "data": [{'error-message': get_errors}]})

    def validate_create_redflag(createdBy, comment):
        errors = []
        if not createdBy or not comment:
            errors.append("createdBy, location, and comment cannot be empty.")
        if not isinstance(createdBy, str):
            errors.append("createdBy should be a string")
        if not isinstance(comment, str):
            errors.append("comment should be string")
        if errors:
            return jsonify({"status": 400, "data": [{'error-message': errors}]})
        return True

    @staticmethod
    def validate_content_type(contentType):
        if contentType == 'application/json':
            return True
        return jsonify({"status": 202, "data": [{'error-message': 'Content-type must be json'}]})

    @staticmethod
    def validate_tt(data, redflag_list, createdBy):
        errors = []
        if 'createdBy' not in data:
            return jsonify({"status": 400, "error": "username is missing. follow this example ->> {'createdBy': 'James'}"})
        if not isinstance(data['createdBy'], str):
            errors.append(
                "Username must be a string. follow this example ->> {'createdBy': 'James'}")
        if Validators.validate_data(createdBy, redflag_list) is not True:
            return Validators.validate_data(createdBy, redflag_list)
        if errors:
            return errors
        return True

    @staticmethod
    def validate_data(createdBy, redflags):
        check_record = [i for i in redflags if i.__dict__[
            'createdBy'] == createdBy]
        if not check_record:
            return jsonify({"status": 400, "data": [{"error-message": "invalid username"}]})
        status = check_record[0].__dict__['status']
        if status in ['under investigation', 'rejected', 'resolved']:
            return jsonify({"status": 400,
                            "data": [{"error-message":
                                      "You can no longer edit or delete this red-flag"}]})
        return True
