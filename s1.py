# -*- coding: gb2312 -*-
import clr
import sys
clr.AddReferenceByPartialName("IronPython")
initpath=r"D:\CS_Serial\CS3000\ONHCS\bin\Debug"
sys.path.append(initpath)
clr.AddReference("NCS.exe")
clr.AddReference("NcsDevice.dll")
import NCS
import System
print(NCS.DASK.NoError)
print(dir(NCS.CardManager))

