import json
import time
import random

# Dummy function for OSC Animation trigger
def trigger_osc_animation(animation_name, value):
    print(f"Triggering animation: {animation_name} with value: {value}")

# Dummy function to simulate head movement
def simulate_head_movement(x_angle, y_angle):
    print(f"Simulating head movement: x={x_angle}, y={y_angle}")

# Dummy function for full body tracking simulation (as placeholder)
def simulate_full_body_tracking(x, y, z):
    print(f"Simulating full body tracking: x={x}, y={y}, z={z}")

# This function can be extended for additional movement logic
def get_movement_commands():
    return {
        "move": "Move",
        "dance": "Dance",
        "jump": "Jump",
        "walk": "Walk",
        "run": "Run",
        "wave": "Wave",
        "sit": "Sit",
        "patrol": "Patrol"
    }

# Function for idle behavior (patrolling or random movement)
def behavior_tree_idle():
    print("🤖 Idle: Patrolling...")
    while True:
        trigger_osc_animation("Patrol", 1)  # Looping patrol
        time.sleep(5)  # Simulate walking for 5 sec
        simulate_head_movement(random.uniform(-30, 30), random.uniform(-30, 30))
        # Exit the loop if new voice command was recorded
        if os.path.exists("input.wav"):
            break
