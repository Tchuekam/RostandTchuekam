
import sys
import os
import wmi
import requests
import jwt
from Telemetry.tracker import track_installation

# Configuration
LICENSING_URL = "http://your-production-server.com:5000/activate"
PUBLIC_KEY = "your-public-key-here"

def get_machine_id():
    c = wmi.WMI()
    return c.Win32_BaseBoard()[0].SerialNumber

def verify_license():
    machine_id = get_machine_id()
    
    # 1. Track installation
    track_installation()
    
    # 2. Activation Request
    try:
        response = requests.post(LICENSING_URL, json={'machine_id': machine_id})
        token = response.json().get('token')
        
        # 3. Verify Token
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["HS256"])
        if decoded['machine_id'] == machine_id:
            return True
    except Exception as e:
        print(f"Activation failed: {e}")
        return False
    return False

if __name__ == "__main__":
    if not verify_license():
        print("Unauthorized access.")
        sys.exit(1)
    
    # Proceed to launch Hermes
    os.system("hermes")
