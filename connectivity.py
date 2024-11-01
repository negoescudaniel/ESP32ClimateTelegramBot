import subprocess
import time

# Replace with the actual IP address of your ESP32
esp32_ip = "192.168.1.131"  
url = f"coap://{esp32_ip}/sensor"

# Function to send CoAP requests using the coap-client command and read response
def send_coap_request(state):
    command = ["coap-client", "-e", state, "-m", "put", url]

    # Debugging info: print the command being executed
    print(f"Executing command: {' '.join(command)}")

    # Execute the command and capture the response (stdout)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Decode and print the response from ESP32
    response = result.stdout.decode()
    error = result.stderr.decode()
    
    print("Command output (response from ESP32):", response)
    print("Command error (if any):", error)

    # Return the response from ESP32 for further processing (if needed)
    return response

# Function to send request for Sensor Readings every 3 seconds
def send_data_periodically():
    while True:
        # Send Sensor Readings
        print("Sending request to get DATA")
        response_on = send_coap_request("1")
        print(f"ESP32 Response to DATA: {response_on}")
        time.sleep(3)

# Function to send request for Sensor Readings
def send_data():
    # Send Sensor Readings  
    print("Sending request to get DATA")
    response_on = send_coap_request("1")
    print(f"ESP32 Response to DATA: {response_on}")
    return response_on

#if __name__ == "__main__":
#    send_data_periodically()

