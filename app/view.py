import os
import glob
import json
import requests

from app import app
from flask import jsonify, render_template, request

STATIC_DIR = "../static"
IMAGES_DIR = STATIC_DIR + "/images"
API_URL = "https://a.4cdn.org"
IMAGE_API_URL = "https://i.4cdn.org"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/get_boards", methods=["GET"])
def get_boards():
    required_board = request.args["board"]
    required_page = int(request.args["page"])
    print(f"Required Board: {required_board}")
    print(f"Required Page: {required_page}")

    # Page Index to track which page we're on list-index-wise
    page_index = required_page - 1

    # Ensure the board we've requested is valid
    if not is_valid_board(required_board):
        raise ValueError(f"Invalid Board Requested: {required_board}")

    catalog_api_endpoint = API_URL + "/" + required_board + "/catalog.json"

    print(f"Requesting data from endpoint: {catalog_api_endpoint}")
    try:
        res = requests.get(catalog_api_endpoint)
        res.raise_for_status()
        print(f"Successful response from endpoint")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Ensure HTTP response code was 200
    if not res.status_code == 200:
        print(f"HTTP response status code: {res.status_code}")
        print(f"HTTP response reason: {res.reason}")
        raise Exception(f"HTTP response from {catalog_api_endpoint} was not 200")

    # Load the response into a JSON object
    try:
        json_data = json.loads(res.text)
    except json.decoder.JSONDecodeError as jde:
        raise ValueError("JSON Decoding error occurred: {jde}")

    # Remove all images from IMAGES_DIR
    image_files = glob.glob(IMAGES_DIR+"/*")
    _ = [os.remove(file) for file in image_files]

    for thread in json_data[page_index]["threads"]:
        tim = thread["tim"]
        ext = thread["ext"]
        if tim == 0:
            # Thread doesn't have a thumbnail, skip
            continue
        
        tn_download_url = f"{IMAGE_API_URL}/{required_board}/{tim}{ext}"
        image_path = f"{IMAGES_DIR}/{tim}{ext}"

        download_image(tn_download_url, image_path)
    
    if required_page == len(json_data):
        # We're on the last page
        next_page = 0
        previous_page = required_page - 1
    elif required_page == 0:
        # We're on the first page
        next_page = required_page + 1
        previous_page = 0
    else:
        # We're somewhere in between
        next_page = required_page + 1
        previous_page = required_page - 1
    
    

def is_valid_board(board):
    valid_boards = [
		"a", "c", "w", "m", "cgl",
		"cm", "cm", "n", "jp", "vt", "v",
		"vg", "vmg", "vm", "vp", "vr", "vrpg",
		"vst", "co", "g", "tv", "k", "o",
		"an", "tg", "sp", "xs", "pw", "sci",
		"his", "int", "out", "toy", "i", "po",
		"p", "ck", "ic", "wg", "lit", "mu",
		"fa", "3", "gd", "diy", "wsg", "qst",
		"biz", "trv", "fit", "x", "adv", "lgbt",
		"mlp", "news", "wsr", "vip", "b", "r9k",
		"pol", "bant", "soc", "s4s", "s", "hc",
		"hm", "h", "e", "u", "d", "y",
		"t", "hr", "gif", "aco", "r",
	]

    return board in valid_boards

def download_image(tn_download_url, image_path):
    # Attempt to download the image
    try:
        res = requests.get(tn_download_url)
        res.raise_for_status()
        print(f"Successful response from endpoint")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    if not res.status_code == 200:
        print(f"HTTP response status code: {res.status_code}")
        print(f"HTTP response reason: {res.reason}")
        raise Exception(f"HTTP response from {catalog_api_endpoint} was not 200")

    img_data = res.content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)