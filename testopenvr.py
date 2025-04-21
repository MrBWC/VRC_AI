from pythonosc import udp_client
import time

# Set up the OSC client to send messages to VRChat on port 9000
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)  # VRChat listens on localhost:9000

# Test function to make the arm move up and down
def move_arm_up_and_down():
    while True:
        # Send OSC message to make the arm move up
        osc_client.send_message("/avatar/parameters/BoxToggle", 1)  # Replace 'ArmMove' with the correct parameter in your avatar
        print("Sent OSC Arm Up signal!")
        
        time.sleep(1)  # Wait for 1 second

        # Send OSC message to make the arm move down
        osc_client.send_message("/avatar/parameters/BoxToggle", 0)  # Replace 'ArmMove' with the correct parameter in your avatar
        print("Sent OSC Arm Down signal!")
        
        time.sleep(1)  # Wait for 1 second

if __name__ == "__main__":
    move_arm_up_and_down()
