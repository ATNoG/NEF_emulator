from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum

#TODO: check openAPI $ref meaning

class FailureCode(str, Enum):
    malfunction = "MALFUNCTION"
    resourceLimitation = "RESOURCE_LIMITATION"
    shortDelay = "SHORT_DELAY"
    appIdDuplicated = "APP_ID_DUPLICATED"
    partialFailure = "PARTIAL_FAILURE"
    otherReason = "OTHER_REASON"

class DomainNameProtocol(str, Enum):
    dnsQName = "DNS_QNAME"
    tlsSNI = "TLS_SNI"
    tlsSAN = "TLS_SAN"
    tlsSCN = "TSL_SCN"

class UserPlaneLocationArea(BaseModel):
    """Represents location area(s) of the user plane functions which are unable to 
enforce the provisioned PFD(s) successfully."""
    # locationArea: LocationArea
    # locationArea5G: LocationArea5G
    # dnais: List[Dnai] =Field(None, description="Identifies a list of DNAI which the user plane functions support.", min_items=0)

class PfdReport(BaseModel):
    """Represents a PFD report indicating the external application identifier(s) which 
PFD(s) are not added or modified successfully and the corresponding failure cause(s)."""
    externalAppIds: List[str] = Field("", description="Identifies the external application identifier(s) which PFD(s) are not added or modified successfully.", min_items=1)
    # failureCode: FailureCode
    #TODO:update cachingTime description
    cachingTime: int = Field(None, description="A volume in units of bytes", ge=0)
    # locationArea: UserPlaneLocationArea



class Pfd(BaseModel):
    """Represents a PFD for an external Application Identifier.""" 
    pfdId: str
    flowDescriptions: List[str] = Field("", description="Represents a 3-tuple with protocol, server ip and server port for UL/DL application traffic. The content of the string has the same encoding as the IPFilterRule AVP value as defined in IETF RFC 6733.", min_items=1)
    urls: List[str] = Field("", description="Indicates a URL or a regular expression which is used to match the significant parts of the URL.", min_items=1)
    domainNames: List[str] = Field("", description="Indicates an FQDN or a regular expression as a domain name matching criteria.", min_items=1)
    # dnProtocol: DomainNameProtocol

class PfdData(BaseModel):
    """Represents a PFD request to add, update or remove PFD(s) for one external 
application identifier.""" 
    externalAppId: Optional[str] = Field("123456789@domain.com", description="Globally unique identifier containing a Domain Identifier and a Local Identifier. \<Local Identifier\>@\<Domain Identifier\>")
    #link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")   
    #TODO: map instead of list
    # pfds: List[Pfd] = Field("", description="Contains the PFDs of the external application identifier. Each PFD is identified in the map via a key containing the PFD identifier", min_items=1)
    # allowedDelay: DurationSecRm
    # cachingTime: DurationSecRo

class PfdManagementCreate(BaseModel):
    """Represents the configuration of a chargeable party."""    
    # supportedFeatures: SupportedFeatures
    #TODO: map instead of list
    pfdDatas: List[PfdData] = Field(None, description="Each element uniquely identifies the PFDs for an external application identifier. Each element is identified in the map via an external application identifier as key. The response shall include successfully provisioned PFD data of application(s). ", min_items=1)
    pfdReports: List[PfdReport] = Field(None, description="Supplied by the SCEF and contains the external application identifiers for which PFD(s) are not added or modified successfully. The failure reason is also included. Each element provides the related information for one or more external application identifier(s) and is identified in the map via the failure identifier as key.", min_items=1)
    #TODO: mudar aqui o url
    notificationDestination: AnyHttpUrl = Field("http://localhost:80/api/v1/utils/monitoring/callback", description="Reference resource (URL) identifying service consumer's endpoint, in order to receive the asynchronous notification.") #Default value for development testing
    requestTestNotification: Optional[bool] = Field(False, description="Set to true by the SCS/AS to request the SCEF to send a test notification as defined in clause 5.2.5.3. Set to false or omitted otherwise. ")
    # websockNotifConfig: WebsockNotifConfig

class PfdManagement(PfdManagementCreate):
    """Represents a PFD management resource for a PFD management request."""
    link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")   
    class Config:
            orm_mode = True