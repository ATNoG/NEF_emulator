from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum

class Snssai(BaseModel):
    sst: int = Field(default=1, description="Unsigned integer representing the Slice/Service Type. Value 0 to 127 correspond to the standardized SST range. Value 128 to 255 correspond to the Operator-specific range.", ge=0, le=255)
    sd: Optional[constr(regex=r'^[0-9a-fA-F]{6}$')] = Field(default='000001', description="This value respresents the Slice Differentiator, in hexadecimal representation.")

class FlowInfo(BaseModel):
    pass

class Dnai(BaseModel):
    pass

class EthFlowDescription(BaseModel):
    pass


#TODO: see required
class ChargeablePartyCreate(BaseModel):
    """Represents the configuration of a chargeable party."""    
    # supportedFeatures: SupportedFeatures
    dnn: Optional[str] = Field("province1.mnc01.mcc202.gprs", description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003")
    snssai: Optional[Snssai] = None
    notificationDestination: AnyHttpUrl = Field("http://localhost:80/api/v1/utils/chargeable-party/callback", description="Reference resource (URL) identifying service consumer's endpoint, in order to receive the asynchronous notification. For testing use 'http://localhost:80/api/v1/utils/chargeable-party/callback'") #Default value for development testing
    requestTestNofication: bool = Field(None, description=" Set to true by the SCS/AS to request the SCEF to send a test notification as defined in clause 5.2.5.3. Set to false or omitted otherwise. ")
    # websockNotifConfig
    exterAppId: str = Field(None, description="Identifies the external Application Identifier.")
    ipv4Addr: Optional[IPvAnyAddress] = Field(default='10.0.0.0', description="String identifying an Ipv4 address")    
    ipv6Addr: Optional[IPvAnyAddress] = Field(default="0:0:0:0:0:0:0:0", description="String identifying an Ipv6 address. Default value ::1/128 (loopback)")
    macAddr: Optional[constr(regex=r'^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$')] = '22-00-00-00-00-00'
    # ipDomain: str
    # flowInfo: List[FlowInfo] = Field(None,description="Describes the application flows.",min_items=1)
    # ethFlowInfo: List[EthFlowDescription] = Field(None, description="Identifies Ethernet packet flows.", min_items=1)
    # sponsorInformation: SponsorInformation
    # sponsoringEnabled: bool = Field(None, description="Whether the sponsoring data connectivity is enabled (true) or not (false).")
    # referenceId: BdtReferenceId
    # servAuthInfo: ServAuthInfo
    # usageThreshold: UsageThreshold
    # events: List[Event] = Field(None, description="Represents the list of event(s) to which the SCS/AS requests to subscribe to.", min_items=1)




class ChargeableParty(ChargeablePartyCreate):
    """Represents the configuration of a chargeable party."""
    link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")
    ipv4Addr: Optional[IPvAnyAddress] = Field(None, description="String identifying an Ipv4 address")   
    class Config:
            orm_mode = True


class ChargeablePartyPatch(BaseModel):
    pass