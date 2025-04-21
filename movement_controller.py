import testopenvr
import random
import time

# Initialize OpenVR
def init_openvr():
    try:
        testopenvr.initialize()
        print("✅ OpenVR Initialized")
    except Exception as e:
        print(f"⚠️ OpenVR init failed: {e}")

# Shutdown OpenVR
def shutdown_openvr():
    try:
        testopenvr.shutdown()
        print("🛑 OpenVR Shutdown")
    except Exception as e:
        print(f"⚠️ Shutdown error: {e}")

# Trigger OSC animation (via VRChat or other clients that accept OSC)
def trigger_osc_animation(animation_name, intensity=1.0):
    try:
        # Here you'd replace this with real OSC or OpenVR code.
        print(f"🎬 Triggering animation: {animation_name} | Intensity: {intensity}")
        # testopenvr.send_osc(animation_name, intensity)  # Placeholder for real implementation
    except Exception as e:
        print(f"⚠️ Animation trigger error: {e}")

# Simulate head movement for social behaviors
def simulate_head_movement(yaw_degrees=0, pitch_degrees=0):
    try:
        print(f"🧠 Simulating head: yaw {yaw_degrees}°, pitch {pitch_degrees}°")
        # Replace with real head movement control, e.g.:
        # testopenvr.set_head_rotation(yaw_degrees, pitch_degrees)
    except Exception as e:
        print(f"⚠️ Head movement error: {e}")

# Simulate full body pose updates (e.g., idle shift, lean, posture adjustments)
def simulate_full_body_tracking():
    try:
        positions = {
            "hip_x": random.uniform(-0.1, 0.1),
            "hip_y": random.uniform(-0.05, 0.05),
            "hip_z": random.uniform(-0.1, 0.1)
        }
        print(f"🦿 Simulating body shift: {positions}")
        # Send positions to VR system here
    except Exception as e:
        print(f"⚠️ Body tracking simulation error: {e}")

# Example idle loop (optional if called directly for testing)
if __name__ == "__main__":
    init_openvr()
    try:
        for _ in range(5):
            simulate_full_body_tracking()
            simulate_head_movement(random.uniform(-20, 20), random.uniform(-10, 10))
            trigger_osc_animation("IdleLookAround", 1.0)
            time.sleep(3)
    except KeyboardInterrupt:
        print("🔌 Interrupted.")
    finally:
        shutdown_openvr()
