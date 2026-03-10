import os
import requests
import time
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
EXPECTED_ISSUER = os.getenv("KEYCLOAK_ISSUER")


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

    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=["RS256"],
        options={"verify_aud": False},
    )

    token_issuer = payload.get("iss", "")
    expected_issuer = EXPECTED_ISSUER or f"{KEYCLOAK_URL}/realms/{REALM}"
    if token_issuer not in {expected_issuer, expected_issuer.replace("http://", "https://")}:
        raise ValueError(f"Invalid issuer: {token_issuer}")

    audiences = payload.get("aud", [])
    if isinstance(audiences, str):
        audiences = [audiences]

    authorized_party = payload.get("azp")
    if AUDIENCE not in audiences and authorized_party != AUDIENCE:
        raise ValueError("Token not meant for configured client")

    return payload


def get_realm_roles(payload: dict):
    return payload.get("realm_access", {}).get("roles", [])


def require_auth(required_role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            print(f"DEBUG: Auth header: {auth_header[:50] if auth_header else 'MISSING'}")
            if not auth_header.startswith("Bearer "):
                print(f"DEBUG: No Bearer token found. Headers: {dict(request.headers)}")
                return jsonify({"error": "Missing bearer token"}), 401

            token = auth_header.replace("Bearer ", "")
            try:
                payload = _decode_token(token)
                print(f"DEBUG: Token payload: {payload}")
            except Exception as ex:
                print(f"DEBUG: Token decode error: {str(ex)}")
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
    # Retry mechanism to wait for MySQL to be ready
    max_retries = 30
    retry_count = 0
    while retry_count < max_retries:
        try:
            db.init_schema()
            print("✓ Database schema initialized successfully")
            break
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                print(f"✗ Failed to initialize database after {max_retries} attempts")
                raise
            wait_time = min(2 ** retry_count, 10)  # Exponential backoff, max 10 seconds
            print(f"⏳ Waiting for MySQL... (attempt {retry_count}/{max_retries}, next retry in {wait_time}s)")
            time.sleep(wait_time)
    
    app.run(host="0.0.0.0", port=5000, debug=True)
