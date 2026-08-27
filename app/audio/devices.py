import sounddevice as sd

def list_audio_devices():
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()
    
    print("Available Audio Devices")
    print("= " * 60)
    
    for index, device in enumerate(devices):
        hostapi_name = hostapis[device["hostapi"]]["name"]
        
        print(f"\nDevice ID: {index}")
        print(f"Name: {device['name']}")
        print(f"Host API: {hostapi_name}")
        print(f"Input channels: {device['max_input_channels']}")
        print(f"Output channels: {device['max_output_channels']}")
        
def find_stereo_mix():
    devices = sd.query_devices()
    
    for index, device in enumerate(devices):
        if "stereo mix" in device["name"].lower():
            return index, device
        
    return None, None

if __name__ == "__main__":
    list_audio_devices()
    
    print("\n" + "=" * 60)
    print("Stereo Mix Detection")
    print("=" * 60)
    
    index, device = find_stereo_mix()
    
    if device is not None:
        print(f"Stereo Mix found!")
        print(f"Device ID: {index}")
        print(f"Name: {device['name']}")
        
    else:
        print("Stereo Mix not found.")