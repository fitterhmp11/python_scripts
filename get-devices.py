# this script connects to a fortigate using API to get the devices detected and puts them into a csv file for sorting and using.



import requests
import pandas as pd  # For creating the CSV
import json

# FortiGate details
fortigate_ip = "192.168.4.75"  # Replace with your FortiGate's IP
fortigate_port = "8443" # Replace with your FortiGate's mgmt port
api_token = "czb106Q90g1016pk1340s1tm3h1Hm1"   # Replace with your API token

url = f"https://{fortigate_ip}:{fortigate_port}/api/v2/monitor/user/device/query?access_token={api_token}"

# Make the API request
response = requests.get(url, verify=False)  # Disable SSL verification for testing

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()["results"]  # Assuming "results" holds the device list
    
    # Convert JSON to a Pandas DataFrame.  Uses pandas to convert the list of devices into a table-like DataFrame.
    df = pd.DataFrame(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv("fortigate_devices.csv", index=False)
    print("Data has been successfully exported to fortigate_devices.csv!")
else:
    print(f"Failed to retrieve devices. Status Code: {response.status_code}")
