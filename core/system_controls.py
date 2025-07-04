# Sound control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


import screen_brightness_control as sbc


def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def set_volume_level(percent):
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(percent / 100.0, None)


def change_volume(up=True):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    new = min(max(current + (0.1 if up else -0.1), 0.0), 1.0)
    volume.SetMasterVolumeLevelScalar(new, None)


def mute_volume(mute=True):
    volume = get_volume_interface()
    volume.SetMute(int(mute), None)


# Brightness control
def set_brightness(percent):
    sbc.set_brightness(percent)


def change_brightness(up=True):
    current = sbc.get_brightness(display=0)[0]
    new = max(min(current + (10 if up else -10), 100), 0)
    sbc.set_brightness(new)
