from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum
from .commonData import Snssai

class RacsFailureCode(str, Enum):
    malfunction = "MALFUNCTION"
    resourceLimitation = "RESOURCE_LIMITATION"
    racsIdDuplicated = "RACS_ID_DUPLICATED"
    other = "OTHER_REASON"

class RacsConfiguration(BaseModel):
    """Represents a single UE radio capability configuration data."""
    racsId: str = Field(None, description="The UE radio capability ID provided by the SCS/AS to identify the UE radio capability data. See 3GPP TS 23.003 for the encoding.")
    racsParamEps: str = Field(None, description="The UE radio capability data in EPS.")
    racsParam5Gs: str = Field(None, description="The UE radio capability data in 5GS.")
    # imeiTacs: List[TypeAllocationCode] = Field(None, description=" Related UE model's IMEI-TAC values.", min_items=1)
    
class RacsFailureReport(BaseModel):
    """Represents a radio capability data provisioning failure report."""
    racsIds: List[str] = Field(None, description="Identifies the RACS ID(s) for which the RACS data are not provisioned successfully", min_items=1)
    failureCode: RacsFailureCode

class RacsProvisioningDataCreate(BaseModel):
    # supportedFeatures: Optional[SupportedFeatures]
    #TODO: map instead of list
    racsConfig: List[RacsConfiguration] = Field(None, description="Identifies the configuration related to manufacturer specific UE radio capability. Each element uniquely identifies an RACS configuration for an RACS ID and is identified in the map via the RACS ID as key. The response shall include successfully provisioned RACS data.",min_items=1)
    racsReports: List[RacsFailureReport] = Field(None, description="Supplied by the SCEF. Contains the RACS IDs for which the RACS data are not provisioned successfully. Any string value can be used as a key of the map.",min_items=1)
    

class RacsProvisioningData(RacsProvisioningDataCreate):
    """Represents a UE's radio capability data."""
    link: Optional[AnyHttpUrl] = Field("https://myresource.com", description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response")
    class Config:
            orm_mode = True

