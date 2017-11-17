import wmi
c = wmi.WMI()
wql = "Select * From Win32_USBControllerDevice"
# print(c.query(wql))
for item in c.query(wql):
    # print(item.Antecedent.Name, " - ", item.Antecedent.PNPDeviceID, " - ", item.Antecedent.DeviceID)
    print(item.Dependent.Caption, " - ", item.Dependent.Description, " - ", item.Dependent.DeviceID, '\n')
    # print(item, item.Dependent.Caption)

'''
REF1: https://stackoverflow.com/a/15033798/5450936
REF2: https://msdn.microsoft.com/en-us/library/aa394505(v=vs.85).aspx
NB1: See "Dependent". See "CIM_LogicalDevice"
'''