import openvr

def get_device_indices():
    vr = openvr.init(openvr.VRApplication_Utility)
    poses = vr.getDeviceToAbsoluteTrackingPose(
        openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount
    )

    devices = {'headset': None, 'left_controller': None, 'right_controller': None}

    for i, pose in enumerate(poses):
        if pose.bDeviceIsConnected:
            device_class = vr.getTrackedDeviceClass(i)
            if device_class == openvr.TrackedDeviceClass_HMD:
                devices['headset'] = i
            elif device_class == openvr.TrackedDeviceClass_Controller:
                role = vr.getControllerRoleForTrackedDeviceIndex(i)
                if role == openvr.TrackedControllerRole_LeftHand:
                    devices['left_controller'] = i
                elif role == openvr.TrackedControllerRole_RightHand:
                    devices['right_controller'] = i

    openvr.shutdown()
    return devices

# Run test
devices = get_device_indices()
print("Detected devices:", devices)
