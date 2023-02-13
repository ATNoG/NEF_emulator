from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum
from .commonData import Snssai

class ConfigurationNotification(BaseModel):
    """Represents a configuration result notification. """
    configuration: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource.")
    # configResults: List[ConfigResult] = Field(None, description="The grouping configuration result notification provided by the SCEF. ", min_items=1)
    #TODO: checkar este parametro do MonitoringEvent 29.122
    # appliedParam: AppliedParameterConfiguration

class NpConfigurationCreate(BaseModel):
    # supportedFeatures: SupportedFeatures
    # mtcProviderId: Optional[str] = Field(None, description="Identifies the MTC Service Provider and/or MTC Application")
    dnn: Optional[str] = Field("province1.mnc01.mcc202.gprs", description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003")
    externalId: Optional[str] = Field("123456789@domain.com", description="Globally unique identifier containing a Domain Identifier and a Local Identifier. \<Local Identifier\>@\<Domain Identifier\>")
    # msisdn: Optional[str] = Field("918369110173", description="Mobile Subscriber ISDN number that consists of Country Code, National Destination Code and Subscriber Number.")
    # externalGroupId: Optional[str] = Field("Group1@domain.com", description="Identifies a group made up of one or more subscriptions associated to a group of IMSIs, containing a Domain Identifier and a Local Identifier. \<Local Identifier\>@\<Domain Identifier\>")
    maximumLatency: int = Field(None, description="Maximum delay acceptable for downlink data transfers.", ge=0)
    maximumResponseTime: int = Field(None, description="Identifies the length of time for which the UE stays reachable to allow the SCS/AS to reliably deliver the required downlink data. ", ge=0)
    suggestedNumberOfDlPackets: int = Field(None, description="This parameter may be included to identify the number of packets that the serving gateway shall buffer in case that the UE is not reachable.", min=0)
    groupReportingGuardTime: int = Field(None, description="Identifies the time for which the SCEF can aggregate the reports detected by the UEs in a group and report them together to the SCS/AS", ge=0)
    #TODO: check url
    notificationDestination: AnyHttpUrl = Field("http://localhost:80/api/v1/utils/monitoring/callback", description="Reference resource (URL) identifying service consumer's endpoint, in order to receive the asynchronous notification.") #Default value for development testing
    requestTestNotification: Optional[bool] = Field(False, description="Set to true by the SCS/AS to request the SCEF to send a test notification as defined in clause 5.2.5.3. Set to false or omitted otherwise. ")
    # websockNotifConfig: WebsockNotifConfig
    validityTime: datetime
    snssai: Snssai
    ueIpAddr: Optional[IPvAnyAddress] = Field(None, description="String identifying an Ipv4 address")
    ueMacAddr: constr(regex=r'^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$')

class NpConfiguration(NpConfigurationCreate):
    """Represents a network parameters configuration."""
    link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")
    class Config:
            orm_mode = True

