import win32com.client

strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")
# colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_PnPEntity")
colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_USBControllerDevice")
print(colItems.__dict__)

# for objItem in colItems:
#     if objItem.Name is not None and objItem.Name == 'USB Token':
#         print("Name: " + repr(objItem.Name))
#         print("Status: " + repr(objItem.Status))
#         print("Manufacturer: " + repr(objItem.Manufacturer))
#         print("DeviceID: " + repr(objItem.DeviceID))
#         print("Status: " + repr(objItem.Status))

'''
REF: https://www.daniweb.com/programming/software-development/threads/372815/how-to-check-available-usb-ports-in-windows
'''