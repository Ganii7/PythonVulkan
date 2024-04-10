from config import *

class QueueFamilyIndices:
    def __init__(self):
        self.graphicsQueueFamily = None
        self.presentQueueFamily = None
        
    def is_complete(self):
        return not(self.graphicsQueueFamily is None or self.presentQueueFamily is None)
    
class SwapChainSupportDetails:
    def __init__(self):
        self.capabilities = None
        self.formats = None
        self.presentModes = None
        
class SwapChainBundle:
    def __init__(self):
        self.swapchain = None
        self.images = None
        self.format = None
        self.extent = None

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
        
    deviceExtensions = [
        VK_KHR_SWAPCHAIN_EXTENSION_NAME,
    ]    
        
    
    createInfo = VkDeviceCreateInfo(
        queueCreateInfoCount = len(queueCreateInfo),
        pQueueCreateInfos = queueCreateInfo,
        enabledExtensionCount = len(deviceExtensions),
        ppEnabledExtensionNames = deviceExtensions,
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
    
def query_swapchain_support(instance, physicalDevice, surface, debug):
    support = SwapChainSupportDetails()
    vkGetPhysicalDeviceSurfaceCapabilitiesKHR = vkGetInstanceProcAddr(instance,"vkGetPhysicalDeviceSurfaceCapabilitiesKHR")
    support.capabilities = vkGetPhysicalDeviceSurfaceCapabilitiesKHR(physicalDevice, surface)
    
    vkGetPhysicalDeviceSurfaceFormatsKHR = vkGetInstanceProcAddr(instance, 'vkGetPhysicalDeviceSurfaceFormatsKHR')
    support.formats = vkGetPhysicalDeviceSurfaceFormatsKHR(physicalDevice, surface)
    
    vkGetPhysicalDeviceSurfacePresentModesKHR = vkGetInstanceProcAddr(instance, 'vkGetPhysicalDeviceSurfacePresentModesKHR')
    support.presentModes = vkGetPhysicalDeviceSurfacePresentModesKHR(physicalDevice, surface)

    
    if debug:
        print("Swapchain can support the following surface capabilities:")
        
        print(f"\tminimun image count: {support.capabilities.minImageCount}")
        print(f"\tminimun image count: {support.capabilities.maxImageCount}")
        
        print("\tcurrent extent:")
        print(f"\t\twith: {support.capabilities.currentExtent.width}")
        print(f"\t\theight: {support.capabilities.currentExtent.height}")
        
        print("\tminimum supported extent:")
        print(f"\t\twith: {support.capabilities.minImageExtent.width}")
        print(f"\t\theight: {support.capabilities.minImageExtent.height}")
        
        print("\tmaximum supported extent:")
        print(f"\t\twith: {support.capabilities.maxImageExtent.width}")
        print(f"\t\theight: {support.capabilities.maxImageExtent.height}")
        
        print(f"\tmaximum image array layers: {support.capabilities.maxImageArrayLayers}")
    
    # if debug:
    #     for supportedFormat in support.formats:
    #         print(f"supported pixel format: {logging.format_to_string(supportedFormat.format)}")
    #         print(f"supported color space: {logging.colorspace_to_string(supportedFormat.colorSpace)}")
    
    return support

def choose_swapchain_surface_format(formats):
    for format in formats:
        if (format.format == VK_FORMAT_B8G8R8_UNORM and format.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR):
            return format
    return formats[0]

def choose_swapchain_present_mode(presentModes):
    for presentMode in presentModes:
        if presentMode == VK_PRESENT_MODE_MAILBOX_KHR:
            return presentMode
    return VK_PRESENT_MODE_FIFO_KHR

def choose_swapchain_extent(width, height, capabilities):
    
    extent = VkExtent2D(width, height)
    
    extent.width = min(
        capabilities.maxImageExtent.width,
        max(capabilities.minImageExtent.width, extent.width)
    )
    extent.height = min(
        capabilities.maxImageExtent.height,
        max(capabilities.minImageExtent.height, extent.height)
    )
    return extent

def create_swapchain(instance, logicalDevice, physicalDevice, surface, width, height, debug):
    support = query_swapchain_support(instance, physicalDevice, surface, debug)
    format = choose_swapchain_surface_format(support.formats)
    presentMode = choose_swapchain_present_mode(support.presentModes)
    extent = choose_swapchain_extent(width, height, support.capabilities)
    imageCount = min(support.capabilities.maxImageCount, support.capabilities.minImageCount + 1)
    
    indices = find_queue_families(physicalDevice, instance, surface, debug)
    queueFamilyIndices = [
        indices.graphicsFamily, indices.presentFamily
    ]
    if (indices.graphicsFamily != indices.presentFamily):
        imageSharingMode = VK_SHARING_MODE_CONCURRENT
        queueFamilyIndexCount = 2
        pQueueFamilyIndices = queueFamilyIndices
    else:
        imageSharingMode = VK_SHARING_MODE_EXCLUSIVE
        queueFamilyIndexCount = 0
        pQueueFamilyIndices = None
    
    createInfo = VkSwapchainCreateInfoKHR(
        surface = surface,
        minImageCount = imageCount,
        imageFormat = format.format,
        imageColorSpace = format.colorSpace,
        imageExtent = extent,
        imageArrayLayers = 1,
        imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT,
        imageSharingMode = imageSharingMode,
        queueFamilyIndexCount = queueFamilyIndexCount,
        pQueueFamilyIndices = pQueueFamilyIndices,
        preTransform = support.capabilities.currentTransform,
        compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR,
        presentMode = presentMode,
        clipped = VK_TRUE
    )
    
    bundle = SwapChainBundle()
    
    vkCreateSwapchainKHR = vkGetDeviceProcAddr(logicalDevice, "vkCreateSwapchainKHR")
    bundle.swapchain = vkCreateSwapchainKHR(logicalDevice, createInfo, None)
    vkGetSwapchainImagesKHR = vkGetDeviceProcAddr(logicalDevice, "vkGetSwapchainImagesKHR")
    bundle.images = vkGetSwapchainImagesKHR(logicalDevice, bundle.swapchain)
    bundle.format = format.format
    bundle.extent = extent
    
    return bundle