from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum


#Defined with other classes, without making a new class type
#Link - AnyHttpUrl
#DateTime - datetime
#Dnn - str -> example: province1.mnc01.mcc202.gprs
#ExternalId - str -> example: 123456789@domain.com
#Msisdn - str -> example: 918369110173
#ExternalGroupId - str -> example: Group1@domain.com
#IpAddr - IPvAnyAddress
#MacAddr48 - constr(regex=r'^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$')
#DurationSec - int -> ge = 0
#DayOfWeek ???
#TimeOfDay ???
#DurationSecRm ???
#DurationSecRo ???

#TODO:
#29.571
#SupportedFeatures
#Dnai
#TypeAllocationCode
#Gpsi

#TODO:
#29.122
#WebsockNotifConfig
#LocationArea
#LocationArea5G
#ConfigResult


class Snssai(BaseModel):
    sst: int = Field(default=1, description="Unsigned integer representing the Slice/Service Type. Value 0 to 127 correspond to the standardized SST range. Value 128 to 255 correspond to the Operator-specific range.", ge=0, le=255)
    sd: Optional[constr(regex=r'^[0-9a-fA-F]{6}$')] = Field(default='000001', description="This value respresents the Slice Differentiator, in hexadecimal representation.")

class UsageThreshold(BaseModel):
    duration: int = Field(None, description="A period of time in units of seconds", ge=0)
    totalVolume: int = Field(None, description="A volume in units of bytes", ge=0)
    downlinkVolume: int = Field(None, description="A volume in units of bytes", ge=0)
    uplinkVolume: int = Field(None, description="A volume in units of bytes", ge=0)

