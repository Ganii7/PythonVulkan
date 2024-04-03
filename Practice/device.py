from config import *

def choose_physical_device(instance, debug):
    if debug:
        print("Choosing Physical Device")
    
    availableDevices = vkEnumeratePhysicalDevices(instance)
    
    if debug:
        print(f"There are {len(availableDevices)} physical devices availables on this system")
    
    for device in availableDevices:
        if debug:
            log_device_properties(device)
        if is_suitable(device, debug):
            return device
    
    return None

def log_device_properties(device):
    properties = vkGetPhysicalDeviceProperties(device)
    
    print(f"Device name: {properties.deviceName}")
    
    print("Device type: ",end="")
    
    if properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_CPU:
        print("CPU")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU:
        print("Discrete GPU")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU:
        print("Integrate GPU")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU:
        print("Virtual GPU")
    else:
        print("Other")
        
def is_suitable(device, debug):
    
    if debug:
        print("Checking if device is suitable")
        
    requestedExtensions = [
        VK_KHR_SWAPCHAIN_EXTENSION_NAME
    ]
    
    if debug:
        print("We are requesting device extensions:")
        
        for extension in requestedExtensions:
            print(f"\t\"{extension}\"")
            
    if check_device_extension_support(device, requestedExtensions, debug):
        if debug:
            print("Device can support the requested extensions")
        return True
    if debug:
        print("Device can't support the requested extensions")
    return False

def check_device_extension_support(device, requestedExtensions, debug):
    supportedExtensions = [
        extension.extensionName
        for extension in vkEnumerateDeviceExtensionProperties(device, None)
    ]
    
    if debug:
        print("Device can support extensions:")
        for extension in supportedExtensions:
            print(f"\t\"{extension}\"")
    
    for extension in requestedExtensions:
        if extension not in supportedExtensions:
            return False
    return True