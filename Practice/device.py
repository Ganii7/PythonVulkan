from config import *

class QueueFamilyIndices:
    def __init__(self):
        self.graphicsQueueFamily = None
        self.presentQueueFamily = None
        
    def is_complete(self):
        return not(self.graphicsQueueFamily is None or self.presentQueueFamily is None)
    
    

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

def find_queue_families(device, instance, surface, debug):
    indices = QueueFamilyIndices()
    
    surfaceSupport = vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfaceSupportKHR")
    
    queueFamiles = vkGetPhysicalDeviceQueueFamilyProperties(device)
                    
    if debug:
        print(f"There are {len(queueFamiles)} queue families available on the system.")
        
    for i,queueFamily in enumerate(queueFamiles):
        if queueFamily.queueFlags & VK_QUEUE_GRAPHICS_BIT:
            indices.graphicsFamily = i
            
            if debug:
                print(f"Queue Family {i} is suitable for graphics.") 
            
        if surfaceSupport(device, i, surface):
            indices.presentFamily = i
            
            if debug:
                print(f"Queue Family {i} is suitable for presenting.") 
            
        
        if indices.is_complete():
            break
    
    return indices

def create_logical_device(physicalDevice, instance, surface, debug):
    
    indices = find_queue_families(physicalDevice, instance, surface, debug)
    uniqueIndices = [indices.graphicsFamily,]
    if indices.graphicsFamily != indices.presentFamily:
        uniqueIndices.append(indices.presentFamily)
        
    queueCreateInfo = []
    
    for queueFamilyIndex in uniqueIndices:
        queueCreateInfo.append(
            VkDeviceQueueCreateInfo(
                queueFamilyIndex = queueFamilyIndex,
                queueCount = 1,
                pQueuePriorities = [1.0,]
            )
        )
    
    
    deviceFeatures = VkPhysicalDeviceFeatures()
    
    enabledLayers = []
    if debug:
        enabledLayers.append("VK_LAYER_KHRONOS_validation")
        
    createInfo = VkDeviceCreateInfo(
        queueCreateInfoCount = len(queueCreateInfo),
        pQueueCreateInfos = queueCreateInfo,
        enabledExtensionCount = 0,
        pEnabledFeatures = [deviceFeatures,],
        enabledLayerCount = len(enabledLayers),
        ppEnabledLayerNames = enabledLayers
    )
    
    return vkCreateDevice(
        physicalDevice = physicalDevice,
        pCreateInfo = [createInfo,],
        pAllocator = None
        )
    
def get_queues(physicalDevice, device, instance, surface, debug):
    indices = find_queue_families(physicalDevice, instance, surface, debug)
    
    return [
        vkGetDeviceQueue(
            device = device,
            queueFamilyIndex = indices.graphicsFamily,
            queueIndex = 0
        ),
        vkGetDeviceQueue(
            device = device,
            queueFamilyIndex = indices.presentFamily,
            queueIndex = 0
        )
    ]