from config import *

def supported(extensions, layers, debug):
    supportedExtensions = [extension.extensionName for extension in vkEnumerateInstanceExtensionProperties(None)]
    
    if debug:
        print("Device can support the following extensions:")
        for supportedExtension in supportedExtensions:
            print(f"\t\"{supportedExtension}\"")
    
    for extension in extensions:
        if extension in supportedExtensions:
            if debug:
                print(f"Extension \"{extension}\" is supported")
            else:
                if debug:
                    print(f"Extension \"{extension}\" is not supported")
                return False
            
    supportedLayers = [layer.layerName for layer in vkEnumerateInstanceLayerProperties()]
    
    if debug:
        print("Device can support the following layers:")
        for supportedLayer in supportedLayers:
            print(f"\t\"{supportedLayer}\"")
    
    for layer in layers:
        if layer in supportedLayers:
            if debug:
                print(f"Layer \"{layer}\" is supported")
            else:
                if debug:
                    print(f"Layer \"{layer}\" is not supported")
                return False
    
    return True
        
def make_instance(debug, applicationName):
    
    if debug:
        print("Making an interface")
        
    version = vkEnumerateInstanceVersion()
        
    version = VK_MAKE_VERSION(1, 0, 0)
    
    appInfo = VkApplicationInfo(
        pApplicationName = applicationName,
        applicationVersion = version,
        pEngineName = "Enginer3r",
        engineVersion = version,
        apiVersion = version
    )
    
    extensions = glfw.get_required_instance_extensions()
    
    if debug:
        extensions.append(VK_EXT_DEBUG_REPORT_EXTENSION_NAME)
    
    if debug:
        print(f"extensions to be requested:")
        
        for extensionName in extensions:
            print(f"\t\" {extensionName}\"")
            
    layers = []
    if debug:
        layers.append("VK_LAYER_KHRONOS_validation")
    
    supported(extensions, layers, debug)
    
    createInfo = VkInstanceCreateInfo(
        pApplicationInfo = appInfo,
        enabledLayerCount = len(layers),
        ppEnabledLayerNames = layers,
        enabledExtensionCount = len(extensions),
        ppEnabledExtensionNames = extensions
    )
    
    try:
        return vkCreateInstance(createInfo, None)
    except:
        if (debug):
            print("Failed to create Instance ahhhhhh")
        return None            