from bson import json_util
from router_client import get_interfaces
from database import save_interface_status
import json

def callback(ch, method, props, body):
    job = json_util.loads(body.decode())
    router_ip = job["ip"]
    router_yourname = job["yourname"]
    router_password = job["password"]
    print(f"Received job for router {router_ip}")
    output = get_interfaces(router_ip, router_yourname, router_password)
    save_interface_status(router_ip, output)

    try:
        output = get_interfaces(router_ip, router_yourname, router_password)
    except Exception as e:
        print(f" Error: {e}")