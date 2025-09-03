import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for

from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Get MongoDB connection details from environment variables
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]

data = []

routedelete = []


@app.route("/")
def main():
    data = list(mycol.find())
    # for x in mycol.find():
    #     data.append(x)
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    yourname = request.form.get("yourname")
    password = request.form.get("password")

    if yourname and password and ip:
        mydict = {"ip": ip, "yourname": yourname, "password": password}
        mycol.insert_one(mydict)
    return redirect(url_for("main"))


@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = request.form.get("idx")
        myq = {"_id": ObjectId(idx)}
        print(idx)
        print(myq)
        mycol.delete_one(myq)
    except Exception:
        pass
    return redirect(url_for("main"))


@app.route("/routers/<router_id>")
def router_detail(router_id):
    router = mycol.find_one({"_id": ObjectId(router_id)})
    if router:
        # Get interface status collection
        interface_col = mydb["interface_status"]

        # Get last 5 interface status records for this router IP
        interface_records = list(
            interface_col.find({"router_ip": router["ip"]})
            .sort("timestamp", -1)
            .limit(5)
        )

        # Flatten the interfaces data for easier template rendering
        router_interfaces = []
        for record in interface_records:
            timestamp = record.get("timestamp", "N/A")
            interfaces = record.get("interfaces", [])

            # If interfaces is a list, process each interface
            if isinstance(interfaces, list):
                for interface in interfaces:
                    router_interfaces.append(
                        {
                            "timestamp": timestamp,
                            "interface": interface.get("interface", "N/A"),
                            "ip": interface.get("ip_address", "N/A"),
                            "status": interface.get("status", "N/A"),
                            "proto": interface.get("proto", "N/A"),
                        }
                    )

        return render_template(
            "router_detail.html", router=router, router_interfaces=router_interfaces
        )
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
