from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum
from .commonData import Snssai
from .utils import ExtraBaseModel

class NiddConfigurationTriggerReply(ExtraBaseModel):
    """Represents a reply to a NIDD configuration trigger."""
    # suppFeat: SupportedFeatures
    pass


class NiddConfigurationTrigger(ExtraBaseModel):
    """Represents a NIDD configuration trigger."""
    adId: str = Field(None, description="Identifies the trigger receiving entity.")
    nefId: str = Field(None, description=" Identifies the trigger sending entity.")
    # gpsi: Gpsi
    # suppFeat: SupportedFeatures
