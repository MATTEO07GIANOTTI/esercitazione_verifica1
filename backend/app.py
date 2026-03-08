import os
import requests
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS
from jose import jwt
from db_wrapper import Database

app = Flask(__name__)
CORS(app)

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
REALM = os.getenv("KEYCLOAK_REALM", "registro-realm")
AUDIENCE = os.getenv("KEYCLOAK_CLIENT_ID", "registro-frontend")


db = Database()

def _get_jwks():
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
    return requests.get(url, timeout=5).json()


def _decode_token(token: str):
    jwks = _get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if not rsa_key:
        raise ValueError("Invalid token key")

    issuer = f"{KEYCLOAK_URL}/realms/{REALM}"
    return jwt.decode(token, rsa_key, algorithms=["RS256"], audience=AUDIENCE, issuer=issuer)


def get_realm_roles(payload: dict):
    return payload.get("realm_access", {}).get("roles", [])


def require_auth(required_role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing bearer token"}), 401

            token = auth_header.replace("Bearer ", "")
            try:
                payload = _decode_token(token)
            except Exception as ex:
                return jsonify({"error": f"Token invalid: {str(ex)}"}), 401

            if required_role:
                roles = get_realm_roles(payload)
                if required_role not in roles:
                    return jsonify({"error": "Forbidden"}), 403

            request.jwt_payload = payload
            return fn(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/grades", methods=["GET"])
@require_auth()
def get_grades():
    payload = request.jwt_payload
    roles = get_realm_roles(payload)
    username = payload.get("preferred_username")

    if "docente" in roles:
        grades = db.get_all_grades()
    else:
        grades = db.get_grades_for_student(username)

    return jsonify(grades)


@app.route("/grades", methods=["POST"])
@require_auth(required_role="docente")
def add_grade():
    body = request.get_json(silent=True) or {}
    student_username = body.get("student_username", "").strip()
    student_name = body.get("student_name", "").strip()
    subject = body.get("subject", "").strip()
    grade = body.get("grade")

    if not all([student_username, student_name, subject]) or grade is None:
        return jsonify({"error": "Missing fields"}), 400

    db.add_grade(student_username, student_name, subject, float(grade))
    return jsonify({"message": "Grade added"}), 201


if __name__ == "__main__":
    db.init_schema()
    app.run(host="0.0.0.0", port=5000, debug=True)
