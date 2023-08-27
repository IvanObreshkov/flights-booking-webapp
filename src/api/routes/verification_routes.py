from flask import Blueprint, request

from api.services.verification_service import Verification

verification_bp = Blueprint("verification", __name__)

@verification_bp.get("/verify")
def verify_user_route():
    verification_token = request.args["token"]
    return Verification.verify_user(verification_token)