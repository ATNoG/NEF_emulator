from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum
from .commonData import Snssai

class ScheduledCommunicationTime(BaseModel):
    """Represents an offered scheduled communication time.""" 
    # daysOfWeek: List[DayOfWeek] = Field(None, description="Identifies the day(s) of the week. If absent, it indicates every day of the week.", min_items=1, max_items=6)
    # timeOfDayStart: TimeOfDay
    # timeOfDayEnd: TimeOfDay
    pass

class CpFailureCode(str, Enum):
    malfunction = "MALFUNCTION"
    set_id_duplicated = "SET_ID_DUPLICATED"
    other = "OTHER_REASON"
    pass

class CpReport(BaseModel):
    """ Represents a CP report indicating the CP set identifier(s) which CP parameter(s) 
    are not added or modified successfully and the corresponding failure cause(s). """ 
    setIds: List[str] = Field(None, description=" Identifies the CP set identifier(s) which CP parameter(s) are not added or modified successfully ", min_items=1)
    failureCode: CpFailureCode
    pass

#TODO: Heir from LocationArea5g
class UmtLocationArea5G(BaseModel):
    """Represents the user location area describing the UE moving trajectory. """
    # umtTime: TimeOfDay
    # umtDuration: int = Field(None, description="A period of time in units of seconds", ge=0)
    pass

class CommunicationIndicator(str, Enum):
    periodically = "PERIODICALLY"
    on_demand = "ON_DEMAND"

class ScheduledCommunicationType(str, Enum):
    downlink = "DOWNLINK"
    uplink = "UPLINK"
    bidirectional = "BIDIRECTIONAL"

class StationaryIndication(str, Enum):
    stationary = "STATIONARY"
    mobile = "MOBILE"

class BatteryIndication(str, Enum):
    recharge = "BATTERY_RECHARGE"
    replace = "BATTERY_REPLACE"
    no_recharge = "BATTERY_NO_RECHARGE"
    no_replace = "BATTERY_NO_REPLACE"
    no_battery = "NO_BATTERY"

class TrafficProfile(str, Enum):
    single_trans_ul = "SINGLE_TRANS_UL" 
    single_trans_dl = "SINGLE_TRANS_DL" 
    dual_trans_ul_first = "DUAL_TRANS_UL_FIRST" 
    dual_trans_dl_first = "DUAL_TRANS_DL_FIRST" 
    multi_trans = "MULTI_TRANS" 

class CpParameterSetCreate(BaseModel):
    """Represents an offered communication pattern parameter set."""
    setId: str = Field(None, description=" SCS/AS-chosen correlator provided by the SCS/AS in the request to create a resource fo CP parameter set(s).")
    validityTime: Optional[datetime] = Field(None, description="Identifies when the CP parameter set expires and shall be deleted.")
    periodicCommunicationIndicator: CommunicationIndicator
    communicationDurationTime: int = Field(None, description="A period of time in units of seconds", ge=0)
    periodicTime: int = Field(None, description="A period of time in units of seconds", ge=0)
    scheduledCommunicationTime: ScheduledCommunicationTime
    scheduledCommunicationType: ScheduledCommunicationType
    stationaryIndication: StationaryIndication
    batteryInds: List[BatteryIndication] = Field(None, description="", min_items=1)
    trafficProfile: TrafficProfile
    expectedUmts: List[UmtLocationArea5G] = Field(None, description="Identifies the UE's expected geographical movement. The attribute is only applicable in 5G. ", min_items=1)
    # expectedUmtDays: DayOfWeek

class CpParameterSet(CpParameterSetCreate):
    """Represents an offered communication pattern parameter set."""
    link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")   
    class Config:
            orm_mode = True


class CpInfoCreate(BaseModel):
    """Represents the configuration of a chargeable party."""    
    # supportedFeatures: SupportedFeatures
    mtcProviderId: str = Field(None, description="Identifies the MTC Service Provider and/or MTC Application.")
    dnn: Optional[str] = Field("province1.mnc01.mcc202.gprs", description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003")
    externalId: Optional[str] = Field("123456789@domain.com", description="Globally unique identifier containing a Domain Identifier and a Local Identifier. \<Local Identifier\>@\<Domain Identifier\>")
    msisdn: Optional[str] = Field("918369110173", description="Mobile Subscriber ISDN number that consists of Country Code, National Destination Code and Subscriber Number.")
    externalGroupId: Optional[str] = Field("Group1@domain.com", description="Identifies a group made up of one or more subscriptions associated to a group of IMSIs, containing a Domain Identifier and a Local Identifier. \<Local Identifier\>@\<Domain Identifier\>")
    cpParameterSets: List[CpParameterSet] = Field(None, description="Identifies a set of CP parameter information that may be part of this CpInfo structure. Any string value can be used as a key of the map. ", min_items=1)
    # cpReports: List[CpReport] = Field(None, description="Supplied by the SCEF and contains the CP set identifiers for which CP parameter(s) are not added or modified successfully. The failure reason is also included. Each element provides the related information for one or more CP set identifier(s) and is identified in the map via the failure identifier as key. ", min_items=1)
    snssai: Optional[Snssai] = None
    #ueIpAddr: Optional[IPvAnyAddress] = Field(None, description="String identifying an Ipv4 address")
    ueMacAddr: Optional[constr(regex=r'^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$')] = '22-00-00-00-00-00'

class CpInfo(CpInfoCreate):
    """Represents the resources for communication pattern parameter provisioning."""
    link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")   
    class Config:
            orm_mode = True