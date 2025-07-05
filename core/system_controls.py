# Sound control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import screen_brightness_control as sbc


# Get interface for volume control
def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


# Set absolute volume level (0–100)
def set_volume_level(percent):
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(percent / 100.0, None)


# Increase/decrease volume
def change_volume(up=True):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    new = min(max(current + (0.1 if up else -0.1), 0.0), 1.0)
    volume.SetMasterVolumeLevelScalar(new, None)


# Mute/unmute system
def mute_volume(mute=True):
    volume = get_volume_interface()
    volume.SetMute(int(mute), None)


# Set brightness (0–100)
def set_brightness(percent):
    try:
        sbc.set_brightness(percent)
    except Exception as e:
        print(f"Brightness set error: {e}")


# Change brightness relatively (+10 / -10)
def change_brightness(up=True):
    try:
        current_list = sbc.get_brightness()
        if not current_list:
            print("No display found for brightness control.")
            return

        current = current_list[0]
        new = max(min(current + (10 if up else -10), 100), 0)
        sbc.set_brightness(new)
    except Exception as e:
        print(f"Brightness change error: {e}")
