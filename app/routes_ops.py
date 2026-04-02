import time
from flask import Blueprint, jsonify

ops_bp = Blueprint("ops", __name__)

APP_NAME = "user-api"
APP_VERSION = "1.0.0"

_start_time = time.time()


@ops_bp.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "healthy", "name": APP_NAME, "version": APP_VERSION})


@ops_bp.route("/version", methods=["GET"])
def version():
    return jsonify({"name": APP_NAME, "version": APP_VERSION})


@ops_bp.route("/readyz", methods=["GET"])
def readyz():
    try:
        uptime_seconds = round(time.time() - _start_time, 2)
        return jsonify({
            "status": "ready",
            "name": APP_NAME,
            "version": APP_VERSION,
            "uptime_seconds": uptime_seconds,
        })
    except Exception as e:
        return jsonify({
            "status": "not_ready",
            "name": APP_NAME,
            "version": APP_VERSION,
            "reason": str(e),
        }), 503
