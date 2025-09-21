import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load .env files

app = Flask(__name__)
# Allow ALL origins (works for frontend on any port)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load WHOIS API Key from .env
WHOIS_API_KEY = "at_IZqeqW3oeV2CSzTrMcStkw8x7Ub8Z"


@app.route("/")
def home():
    return jsonify({"message": "Domain Suggester API is running"})


# 1. Check domain availability
@app.route("/check_domain", methods=["POST", "GET"])
def check_domain():
    if request.method == "POST":
        data = request.json
        domain = data.get("domain")
    else:  # GET request
        domain = request.args.get("domain")  # get from URL query param

    print("API Request received:", domain)

    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    url = f"https://whoisxmlapi.com/whoisserver/WhoisService"
    params = {
        "apiKey": WHOIS_API_KEY,
        "domainName": domain,
        "outputFormat": "JSON"
    }

    response = requests.get(url, params=params)
    result = response.json()

    available = "registryData" not in result

    return jsonify({"domain": domain, "available": available})


# 2. Suggest alternative domains
@app.route("/suggest_alternatives", methods=["POST"])
def suggest_alternatives():
    data = request.json
    print("✅ Alternative domain request:", data)

    domain = data.get("domain")
    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    name, _, tld = domain.partition(".")
    alternatives = [
        f"{name}.xyz",
        f"{name}.co",
        f"get{name}.com",
        f"my{name}.net"
    ]

    return jsonify({"domain": domain, "suggestions": alternatives})


# 3. Notify user when domain is available (dummy for now)
@app.route("/notify_me", methods=["POST"])
def notify_me():
    data = request.json
    print("✅ Notify request:", data)

    domain = data.get("domain")
    email = data.get("email")

    if not domain or not email:
        return jsonify({"error": "Domain and email are required"}), 400

    return jsonify({"status": "success", "message": f"You’ll be notified at {email}"})


# 4. Brand name suggestions
@app.route("/brand_suggestions", methods=["POST"])
def brand_suggestions():
    data = request.json
    print("✅ Brand suggestion request:", data)

    brand = data.get("brand")
    if not brand:
        return jsonify({"error": "Brand name is required"}), 400

    ideas = [
        f"get{brand.lower()}.com",
        f"try{brand.lower()}.io",
        f"join{brand.lower()}.app",
        f"uses{brand.lower()}.net"
    ]

    return jsonify({"brand": brand, "suggestions": ideas})


if __name__ == "__main__":
    app.run(debug=True)