from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures in the data list."""
    if data:
        return jsonify(data), 200
    return jsonify({"message": "No pictures found"}), 404


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture with the specified id."""
    # Loop through the data list to find a picture with the given id
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200
    # Return a 404 error if the picture is not found
    return jsonify({"message": "Picture not found"}), 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry."""
    # Extract data from the request body
    picture = request.get_json()
    picture_id = picture.get("id")

    # Check if a picture with the same ID already exists
    if any(p.get("id") == picture_id for p in data):
        return jsonify({"Message": f"picture with id {picture_id} already present"}), 302

    # Append the new picture to the data list
    data.append(picture)
    return jsonify(picture), 201  # Return the created picture with a 201 status code


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture by ID."""
    # Extract updated data from the request body
    updated_data = request.get_json()

    # Find the picture in the data list by ID
    for picture in data:
        if picture.get("id") == id:
            # Update the picture with the new data
            picture.update(updated_data)
            return jsonify(picture), 200  # Return the updated picture with a 200 status code

    # Return a 404 error if the picture is not found
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID."""
    # Find the picture in the data list by ID
    for index, picture in enumerate(data):
        if picture.get("id") == id:
            # Remove the picture from the data list
            data.pop(index)
            return "", 204  # Return a 204 No Content status to indicate successful deletion

    # Return a 404 error if the picture is not found
    return jsonify({"message": "picture not found"}), 404
