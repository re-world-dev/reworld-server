#===================
#     RE:WORLD
#===================
# Auto Libraries Install

#Auto download the lib required if nessessary
def start():
    import os
    
    print("CHECKING LIBRAIRIES...")
    

    
    #pyyaml
    try:
        import yaml
        print("PyYaml : INSTALLED")
    except ModuleNotFoundError:
        os.system("pip install pyyaml")
    

    #requests
    try:
        import requests
        print("Request : INSTALLED")
    except ModuleNotFoundError:
        os.system("pip install requests")
    

    #signal
    try:
        import signal
        print("signal : INSTALLED")
    except ModuleNotFoundError:
        os.system("pip install signal")
    
    print("LIBRAIRIES CHECKED !")