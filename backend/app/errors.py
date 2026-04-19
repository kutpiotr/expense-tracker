from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        # Pydantic zwraca listę szczegółowych błędów pól
        return (
            jsonify(
                {
                    "error": "validation_error",
                    "details": [
                        {
                            "field": ".".join(str(x) for x in err["loc"]),
                            "message": err["msg"],
                        }
                        for err in e.errors()
                    ],
                }
            ),
            400,
        )

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e: IntegrityError):
        # Np. złamanie UNIQUE constraint
        return (
            jsonify(
                {
                    "error": "integrity_error",
                    "message": "database constraint violated (e.g. duplicate value)",
                }
            ),
            409,
        )

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "not_found", "message": str(e)}), 404

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"error": "bad_request", "message": str(e)}), 400
