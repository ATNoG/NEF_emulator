from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl
from enum import Enum

class CongestionType(str, Enum):
    high = "HIGH"
    medium = "MEDIUM"
    low = "LOW"

class NetworkStatusReportingSubscriptionCreate(BaseModel):
    """Represents a subscription to network status information reporting."""
    # supportedFeatures: Optional[SupportedFeatures]
    #TODO: utils
    notificationDestination: AnyHttpUrl = Field("http://localhost:80/api/v1/utils/netStatReport/callback", description="Reference resource (URL) identifying service consumer's endpoint, in order to receive the asynchronous notification.") #Default value for development testing
    requestTestNotification: bool = Field(True, description="Set to true by the SCS/AS to request the SCEF to send a test notification as defined in clause 5.2.5.3. Set to false or omitted otherwise.")
    # websockNotifConfig: WebsockNotifConfig
    # locationArea: LocationArea
    timeDuration: datetime = Field(None, description="Identifies the time for which a continuous reporting is requested.")
    thresholdValues: Optional[List[int]] = Field(None, description="Identifies a list of congestion level(s) with exact value that the SCS/AS requests to be informed of when reached.", min_items=1, ge=0,le=31)
    thresholdTypes: Optional[List[CongestionType]] = Field(None, description="Identifies a list of congestion level(s) with abstracted value that the SCS/AS requests to be informed of when reached.", min_items=1)


class NetworkStatusReportingSubscription(NetworkStatusReportingSubscriptionCreate):
    """Represents a subscription to network status information reporting."""
    link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")
    class Config:
            orm_mode = True

class NetworkStatusReportingNotification(BaseModel):
    """Represents a network status reporting notification."""
    subscription: AnyHttpUrl
    nsiValue: Optional[int] = Field(None, description= "Network Status Indicator based on exact value for congestion status received from RCAF(s).", ge=0, le=31)
    nsiType: Optional[CongestionType] = Field(None, description="Network Status Indicator based on abstracted value for congestion status.")

