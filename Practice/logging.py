from config import *

def debugCallback(*args):
    # print(f"Debug messager has {len(args)} components")
    # for arg in args:
    #     print(f"\t{arg}")
    print(f"Validation Layer{args[5]} {args[6]}")
    return 0


def make_debug_messanger(instance):
    
    # createInfo = vkCreateDebugReportCallbackEXT(
    #     flags=VK_DEBUG_REPORT_ERROR_BIT_EXT | VK_DEBUG_REPORT_WARNING_BIT_EXT,
    #     pfnCallback=debugCallback
    # )
    
    # creationFunction = vkGetInstanceProcAddr(instance, "vkCreateDebugReportCallbackEXT")
    
    return False

