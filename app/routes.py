from flask import jsonify, redirect, url_for, request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app import app, jwt
import uuid
from typing import Type
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

drivers = {}

@app.route("/", methods=["GET"])
def index():
    
    return redirect(url_for("login"))

@app.route("/login", methods=["POST"])
def login():
    
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/start', methods=['POST'])
@jwt_required()
def start_chromedriver():
    
    driver_id = str(uuid.uuid4())
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_service.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1600,900")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--kiosk-printing')
    
    drivers[driver_id] = chrome_service
    return jsonify({"message": "ChromeDriver started", "driver_id": driver_id, "service_url": chrome_service.service_url})

@app.route('/stop', methods = ["POST"])
@jwt_required()
def stop_driver():
    
    chrome_service: Type[ChromeService] = drivers.get(request.json.get("driver_id", "None"), None)
    
    if chrome_service is None:
        return jsonify({"error": "Nenhum driver encontrado!"}), 404

    chrome_service.stop()
    
    return jsonify({"success": "stopped"}), 200
    
    
    