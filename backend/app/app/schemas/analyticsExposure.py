from typing import Optional, List, Union
from datetime import datetime
from app.schemas.monitoringevent import CivicAddress, GeographicArea
from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl, constr
from enum import Enum
from .commonData import (
    Snssai,
    TimeWindow,
    FlowInfo,
    Ecgi,
    Ncgi,
    GlobalRanNodeId,
    Tai,
    UserLocation,
    RatType,
    QosResourceType,
    AnalyticsSubset,
    PartitioningCriteria,
    NotificationFlag,
    WebsockNotifConfig,
)
from .cpParameterProvisioning import ScheduledCommunicationTime
from .utils import ExtraBaseModel

############### TS 29.517 Types ###############


class AddrFqdn(ExtraBaseModel):
    """IP address and/or FQDN."""

    ipAddr: IPvAnyAddress
    fqdn: str = Field(None, description="Indicates an FQDN.")


class SvcExperience(ExtraBaseModel):
    """Contains a mean opinion score with the customized range."""

    mos: float
    upperRange: float
    lowerRange: float


###############################################

############### TS 29.508 Types ###############


class UpfInformation(ExtraBaseModel):
    """Represents the ID/address/FQDN of the UPF."""

    upfId: str
    upfAddr: AddrFqdn


class NotificationMethod(str, Enum):
    periodic = "PERIODIC"
    oneTime = "ONE_TIME"
    onEventDetection = "ON_EVENT_DETECTION"


###############################################

############### TS 29.523 Types ###############


class ReportingInformation(ExtraBaseModel):
    """Represents the type of reporting that the subscription requires."""

    immRep: bool
    notifMethod: NotificationMethod
    maxReportNbr: int = Field(None, description="", ge=0)
    monDur: datetime
    repPeriod: int = Field(None, description="", ge=0)
    sampRatio: int = Field(None, description="Expressed in percent.", ge=1, le=100)
    partitionCriteria: List[PartitioningCriteria] = Field(
        None, description="", min_items=1
    )
    grpRepTime: int = Field(None, description="", ge=0)
    notifFlag: NotificationFlag


###############################################


############### TS 29.503 Types ###############


class SuggestedPacketNumDl(ExtraBaseModel):
    suggestedPacketNumDl: int = Field(None, description="", ge=1)
    validityTime: datetime


class ExpectedUeBehaviourData(ExtraBaseModel):
    """IP address and/or FQDN."""

    # TODO: should be a map
    suggestedPacketNumDlList: List[SuggestedPacketNumDl]
    threeGppChargingCharacteristics: str
    supportedFeatures: constr(regex=r"^[A-Fa-f0-9]*$")


###############################################

############### TS 29.554 Types ###############


class NetworkAreaInfo(ExtraBaseModel):
    """Describes a network area information in which the NF service consumer requests the number of UEs."""

    ecgis: List[Ecgi] = Field(
        None, description="Contains a list of E-UTRA cell identities.", min_items=1
    )
    ncgis: List[Ncgi] = Field(
        None, description="Contains a list of NR cell identities.", min_items=1
    )
    gRanNodeIds: List[GlobalRanNodeId] = Field(
        None, description="Contains a list of NG RAN nodes.", min_items=1
    )
    tais: List[Tai] = Field(
        None, description="Contains a list of tracking area identities.", min_items=1
    )


###############################################

############### TS 29.512 Types ###############


class FlowDirection(str, Enum):
    downlink = "DOWNLINK"
    uplink = "UPLINK"
    bidirectional = "BIDIRECTIONAL"
    unspecified = "UNSPECIFIED"


###############################################

############### TS 29.514 Types ###############


class EthFlowDescription(ExtraBaseModel):
    """Identifies an Ethernet flow."""

    destMacAddr: constr(regex=r"^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$")
    ethType: str
    fDesc: str = Field(None, description="Defines a packet filter of an IP flow.")
    fDir: FlowDirection
    sourceMacAddr: constr(regex=r"^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$")
    vlanTags: List[str] = Field(None, description="", min_items=1, max_items=2)
    srcMacAddrEnd: constr(regex=r"^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$")
    destMacAddrEnd: constr(regex=r"^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$")


###############################################


############### TS 29.520 Types ###############


class NetworkPerfType(str, Enum):
    gnbActiveRatio = "GNB_ACTIVE_RATIO"
    gnbComputingUsage = "GNB_COMPUTING_USAGE"
    gnbMemoryUsage = "GNB_MEMORY_USAGE"
    gnbDiskUsage = "GNB_DISK_USAGE"
    numOfUE = "NUM_OF_UE"
    sessSuccRatio = "SESS_SUCC_RATIO"
    hoSuccRatio = "HO_SUCC_RATIO"


class ExceptionId(str, Enum):
    unexpectedUELocation = "UNEXPECTED_UE_LOCATION"
    unexpectedLongLiveFlow = "UNEXPECTED_LONG_LIVE_FLOW"
    unexpectedLargeRateFlow = "UNEXPECTED_LARGE_RATE_FLOW"
    unexpectedWakeup = "UNEXPECTED_WAKEUP"
    suspecionOfDdosAttack = "SUSPICION_OF_DDOS_ATTACK"
    wrongDestinationAddress = "WRONG_DESTINATION_ADDRESS"
    tooFrequentServiceAccess = "TOO_FREQUENT_SERVICE_ACCESS"
    unexpectedRatioLinkFailures = "UNEXPECTED_RADIO_LINK_FAILURES"
    pingPongAcrossCells = "PING_PONG_ACROSS_CELLS"


class ExceptionTrend(str, Enum):
    up = "UP"
    down = "DOWN"
    unknow = "UNKNOW"
    stable = "STABLE"


class DispersionClass(str, Enum):
    fixed = "FIXED"
    camper = "CAMPER"
    traveller = "TRAVELLER"
    topHeavy = "TOP_HEAVY"


class CongestionType(str, Enum):
    userPlane = "USER_PLANE"
    controlPlane = "CONTROL_PLANE"
    userAndControlPlane = "USER_AND_CONTROL_PLANE"


class TimeUnit(str, Enum):
    minute = "MINUTE"
    hour = "HOUR"
    day = "DAY"


class DispersionType(str, Enum):
    dvda = "DVDA"
    tda = "TDA"
    dvdaAndTda = "DVDA_AND_TDA"


class ServiceExperienceType(str, Enum):
    voice = "VOICE"
    video = "VIDEO"
    other = "OTHER"


class MatchingDirection(str, Enum):
    ascending = "ASCENDING"
    descending = "DESCENDING"
    crossed = "CROSSED"


class DispersionOrderingCriterion(str, Enum):
    timeSlotStart = "TIME_SLOT_START"
    dispersion = "DISPERSION"
    classification = "CLASSIFICATION"
    ranking = "RANKING"
    percentileRanking = "PERCENTILE_RANKING"


class ExpectedAnalyticsType(str, Enum):
    mobility = "MOBILITY"
    commun = "COMMUN"
    mobilityAndCommun = "MOBILITY_AND_COMMUN"


class DnPerfOrderingCriterion(str, Enum):
    avgTrafficRate = "AVERAGE_TRAFFIC_RATE"
    macTrafficRate = "MAXIMUM_TRAFFIC_RATE"
    avgPacketDelay = "AVERAGE_PACKET_DELAY"
    maxPacketDelay = "MAXIMUM_PACKET_DELAY"
    avgPacketLossRate = "AVERAGE_PACKET_LOSS_RATE"


class Accuracy(str, Enum):
    low = "LOW"
    high = "HIGH"


class AnalyticsMetadata(str, Enum):
    numOfSamples = "NUM_OF_SAMPLES"
    dataWindow = "DATA_WINDOW"
    dataStatProps = "DATA_STAT_PROPS"
    strategy = "STRATEGY"
    accuracy = "ACCURACY"


class DatasetStatisticalProperty(str, Enum):
    uniformDistData = "UNIFORM_DIST_DATA"
    noOutliers = "NO_OUTLIERS"


class OutputStrategy(str, Enum):
    binary = "BINARY"
    gradient = "GRADIENT"


class NwdafFailureCode(str, Enum):
    unavailableData = "UNAVAILABLE_DATA"
    bothStatPredNotAllowed = "BOTH_STAT_PRED_NOT_ALLOWED"
    unsatisfiedRequestedAnalyticsTime = "UNSATISFIED_REQUESTED_ANALYTICS_TIME"
    other = "OTHER"


class RetainabilityThreshold(ExtraBaseModel):
    """Represents a QoS flow retainability threshold."""

    relFlowNum: int = Field(None, description="", ge=0)
    relTimeUnit: TimeUnit
    relFlowRatio: int = Field(None, description="Expressed in percent", ge=1, le=100)


class ThresholdLevel(ExtraBaseModel):
    """Represents a threshold level."""

    congLevel: int
    nfLoadLevel: int
    nfCpuUsage: int
    nfMemoryUsage: int
    nfStorageUsage: int
    avgTrafficRate: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    maxTrafficRate: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    avgPacketDelay: int = Field(None, description="Expressed in milliseconds.", ge=1)
    maxPacketDelay: int = Field(None, description="Expressed in milliseconds.", ge=1)
    avgPacketLossRate: int = Field(
        None, description="Expressed in tenth of percent", ge=0, le=1000
    )
    svcExpLevel: float


class TopApplication(ExtraBaseModel):
    """Top application that contributes the most to the traffic."""

    appId: str = Field(None, description="String providing an application identifier.")
    ipTrafficFilter: FlowInfo
    ratio: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")


class Exception(ExtraBaseModel):
    """Represents the Exception information."""

    excepId: ExceptionId
    excepLevel: int
    excepTrend: ExceptionTrend


class IpEthFlowDescription(ExtraBaseModel):
    """Contains the description of an Uplink and/or Downlink Ethernet flow."""

    ipTrafficFilter: str = Field(
        None, description="Defines a packet filter of an IP flow."
    )
    ethTrafficFilter: EthFlowDescription


class AddressList(ExtraBaseModel):
    """Represents a list of IPv4 and/or IPv6 addresses."""

    ipv4Addrs: List[IPvAnyAddress] = Field(
        None, description="String identifying an Ipv4 address", min_items=1
    )
    ipv6Addrs: List[IPvAnyAddress] = Field(
        None, description="String identifying an Ipv6 address", min_items=1
    )


class CircumstanceDescription(ExtraBaseModel):
    """Contains the description of a circumstance."""

    freq: float
    tm: datetime
    locArea: NetworkAreaInfo
    vol: int = Field(
        None,
        description=" Unsigned integer identifying a volume in units of bytes.",
        ge=0,
    )


class AdditionalMeasurement(ExtraBaseModel):
    """Represents additional measurement information."""

    unexpLoc: NetworkAreaInfo
    unexpFlowTeps: List[IpEthFlowDescription] = Field(None, description="", min_items=1)
    unexpWakes: List[datetime] = Field(None, description="", min_items=1)
    ddosAttack: AddressList
    wrgDest: AddressList
    circums: List[CircumstanceDescription] = Field(None, description="", min_items=1)


class TrafficCharacterization(ExtraBaseModel):
    """Identifies the detailed traffic characterization."""

    dnn: str = Field(
        "province1.mnc01.mcc202.gprs",
        description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003",
    )
    snssai: Snssai
    appId: str = Field("", description="String providing an application identifier.")
    fDescs: List[IpEthFlowDescription] = Field(
        None, description="", min_items=1, max_items=2
    )
    ulVol: int = Field(
        None,
        description=" Unsigned integer identifying a volume in units of bytes.",
        ge=0,
    )
    ulVolVariance: float
    dlVol: int = Field(
        None,
        description=" Unsigned integer identifying a volume in units of bytes.",
        ge=0,
    )
    dlVolVariance: float


class AppListForUeComm(ExtraBaseModel):
    """Represents the analytics of the application list used by UE."""

    appId: str = Field("", description="String providing an application identifier.")
    startTime: datetime
    appDur: int = Field(None, description="", ge=0)
    occurRatio: int = Field(None, description="Expressed in percent", ge=1, le=100)
    spatialValidity: NetworkAreaInfo


class SessInactTimerForUeComm(ExtraBaseModel):
    """Represents the N4 Session inactivity timer."""

    n4SessId: int = Field(None, description="", ge=0, le=255)
    sessInactiveTimer: int = Field(None, description="", ge=0)


class UeCommunication(ExtraBaseModel):
    """Represents UE communication information."""

    commDur: int = Field(None, description="", ge=0)
    commDurVariance: float
    perioTime: int = Field(None, description="", ge=0)
    perioTimeVariance: float
    ts: int = Field(None, description="", ge=0)
    tsVariance: float
    recurringTime: ScheduledCommunicationTime
    trafChar: TrafficCharacterization
    ratio: int = Field(None, description="", ge=1, le=100)
    perioCommInd: bool
    confidence: int = Field(None, description="", ge=0)
    anaOfAppList: AppListForUeComm
    sessInactTimer: SessInactTimerForUeComm


class ApplicationVolume(ExtraBaseModel):
    """ApplicationVolume"""

    appId: str = Field(None, description="String providing an application identifier.")
    appVolume: int = Field(None, description="", ge=0)


class DispersionCollection(ExtraBaseModel):
    """Dispersion collection per UE location or per slice."""

    ueLoc: UserLocation
    snssai: Snssai
    supis: List[constr(regex=r"^(imsi-[0-9]{5,15}|nai-.+|gci-.+|gli-.+|.+)$")] = Field(
        None, description="", min_items=1
    )
    gpsis: List[constr(regex=r"^(msisdn-[0-9]{5,15}|extid-.+@.+|.+)$")] = Field(
        None, description="", min_items=1
    )
    appVolumes: List[ApplicationVolume] = Field(None, description="", min_items=1)
    disperAmount: int = Field(None, description="", ge=0)
    disperClass: DispersionClass
    usageRank: int = Field(None, description="", ge=1, le=3)
    percentileRank: int = Field(None, description="", ge=1, le=100)
    ueRatio: int = Field(None, description="", ge=1, le=100)
    confidence: int = Field(None, description="", ge=0)


class DispersionInfo(ExtraBaseModel):
    """Represents the Dispersion information. When subscribed event is "DISPERSION", the
    "disperInfos" attribute shall be included."""

    tsStart: datetime
    tsDuration: int = Field(None, description="", ge=0)
    disperCollects: List[DispersionCollection] = Field(
        None, description="", min_items=1
    )
    disperType = DispersionType


class PerfData(ExtraBaseModel):
    """Represents DN performance data."""

    avgTrafficRate: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    maxTrafficRate: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    avePacketDelay: int = Field(None, description="Expressed in milliseconds.", ge=1)
    maxPacketDelay: int = Field(None, description="Expressed in milliseconds.", ge=1)
    avgPacketLossRate: int = Field(
        None, description="Expressed in tenth of percent.", ge=0, le=1000
    )


class DnPerf(ExtraBaseModel):
    """Represents DN performance for the application."""

    appServerInsAddr: AddrFqdn
    upfInfo: UpfInformation
    dnai: str = Field(
        None,
        description="DNAI (Data network access identifier), see clause 5.6.7 of 3GPP TS 23.501.",
    )
    perfData: PerfData
    spatialValidCon: NetworkAreaInfo
    temporalValidCon: TimeWindow


class DnPerfInfo(ExtraBaseModel):
    """Represents DN performance information."""

    appId: str = Field(None, description="String providing an application identifier.")
    dnn: Optional[str] = Field(
        "province1.mnc01.mcc202.gprs",
        description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003",
    )
    snssai: Snssai
    dnPerf: List[DnPerf] = Field(None, description="", min_items=1)
    confidence: int = Field(None, description="", ge=0)


class LocationInfo(ExtraBaseModel):
    """Represents UE location information."""

    loc: UserLocation
    ratio: int = Field(None, description="Expressed in percent.", ge=1, le=100)
    confidence: int = Field(None, description="", ge=0)


class RatFreqInformation(ExtraBaseModel):
    """Represents the RAT type and/or Frequency information."""

    allFreq: Optional[bool] = Field(
        False,
        description="Set to true to indicate to handle all the frequencies the NWDAF received, otherwise set to false or omit. The allFreq attribute and the freq attribute are mutually exclusive.",
    )
    allRat: Optional[bool] = Field(
        False,
        description="Set to true to indicate to handle all the RAT Types the NWDAF received, otherwise set to false or omit. The allRat attribute and the ratType attribute are mutually exclusive. ",
    )
    freq: Optional[int] = Field(None, description="", ge=0, le=3279165)
    ratType: Optional[RatType]
    svcExpThreshold: ThresholdLevel
    matchingDir: MatchingDirection


class ServiceExperienceInfo(ExtraBaseModel):
    """Represents service experience information."""

    svcExprc: SvcExperience
    svcExprcVariance: float
    supis: List[constr(regex=r"^(imsi-[0-9]{5,15}|nai-.+|gci-.+|gli-.+|.+)$")] = Field(
        None, description="", min_items=1
    )
    snssai: Snssai
    appId: str = Field("", description="String providing an application identifier.")
    srvExpcType: ServiceExperienceType
    ueLocs: List[LocationInfo] = Field(None, description="", min_items=1)
    upfInfo: UpfInformation
    dnai: str = Field(
        None,
        description="DNAI (Data network access identifier), see clause 5.6.7 of 3GPP TS 23.501.",
    )
    appServerInst: AddrFqdn
    confidence: int = Field(None, description="", ge=0)
    dnn: Optional[str] = Field(
        "province1.mnc01.mcc202.gprs",
        description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003",
    )
    networkArea: NetworkAreaInfo
    nsiId: str = Field(
        None,
        description="Contains the Identifier of the selected Network Slice instance.",
    )
    ratio: int = Field(None, description="Expressed in percent.", ge=1, le=100)
    ratFreq: RatFreqInformation


class ClassCriterion(ExtraBaseModel):
    """Indicates the dispersion class criterion for fixed, camper and/or traveller UE, and/or the top-heavy UE dispersion class criterion."""

    disperClass: DispersionClass
    classThreshold: int = Field(None, description="Expressed in percent.", ge=1, le=100)
    thresMatch: MatchingDirection


class RankingCriterion(ExtraBaseModel):
    """Indicates the usage ranking criterion between the high, medium and low usage UE."""

    highBase: int = Field(None, description="Expressed in percent.", ge=1, le=100)
    lowBase: int = Field(None, description="Expressed in percent.", ge=1, le=100)


class DispersionRequirement(ExtraBaseModel):
    """Represents the dispersion analytics requirements."""

    disperType: DispersionType
    classCriters: List[ClassCriterion] = Field(None, description="", min_items=1)
    rankCriters: List[RankingCriterion] = Field(None, description="", min_items=1)
    dispOrderCriter: DispersionOrderingCriterion
    order: MatchingDirection


class NsiIdInfo(ExtraBaseModel):
    """Represents the S-NSSAI and the optionally associated Network Slice Instance(s)."""

    snssai: Snssai
    nsiIds: List[str] = Field(None, description="", min_items=1)


class QosRequirement(ExtraBaseModel):
    """Represents the QoS requirements."""

    fiveqi: int = Field(None, description="", ge=0, le=255)
    gfbrUl: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    gfbrDl: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    resType: QosResourceType
    pdb: int = Field(None, description="Expressed in milliseconds.", ge=1)
    per: constr(regex=r"^([0-9]E-[0-9])$")


class DnPerformanceReq(ExtraBaseModel):
    """Represents other DN performance analytics requirements."""

    dnPerfOrderCriter: DnPerfOrderingCriterion
    order: MatchingDirection
    reportThresholds: List[ThresholdLevel] = Field(None, description="", min_items=1)


class BwRequirement(ExtraBaseModel):
    """Represents bandwidth requirements."""

    appId: str = Field(None, description="String providing an application identifier.")
    marBwDl: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    marBwUl: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    mirBwDl: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    mirBwUl: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")


class AnalyticsMetadataIndication(ExtraBaseModel):
    """Contains analytics metadata information requested to be used during analytics generation."""

    dataWindow: TimeWindow
    dataStatProps: List[DatasetStatisticalProperty] = Field(
        None, description="", min_items=1
    )
    strategy: OutputStrategy
    aggrNwdafIds: List[str] = Field(None, description="", min_items=1)


class EventReportingRequirement(ExtraBaseModel):
    """Represents the type of reporting that the subscription requires."""

    accuracy: Accuracy
    accPerSubset: List[Accuracy] = Field(None, description="", min_items=1)
    startTs: datetime
    endTs: datetime
    offsetPeriod: int
    sampRatio: int = Field(None, description="Expressed in percent.", ge=1, le=100)
    maxObjectNbr: int = Field(None, description="", ge=0)
    maxSupiNbr: int = Field(None, description="", ge=0)
    timeAnaNeeded: datetime
    anaMeta: List[AnalyticsMetadata] = Field(None, description="", min_items=1)
    anaMetaInd: AnalyticsMetadataIndication


class NetworkPerfRequirement(ExtraBaseModel):
    """Represents a network performance requirement."""

    nwPerfType: NetworkPerfType
    relativeRatio: int = Field(None, description="Expressed in percent.", ge=1, le=100)
    absoluteNum: int = Field(None, description="", ge=0)


###############################################


class AnalyticsFailureCode(str, Enum):
    unavailableData = "UNAVAILABLE_DATA"
    bothStatPredNotAllowed = "BOTH_STAT_PRED_NOT_ALLOWED"
    unsatifiedRequestAnalyticsTime = "UNSATISFIED_REQUESTED_ANALYTICS_TIME"
    other = "OTHER"


class AnalyticsEvent(str, Enum):
    ueMobility = "UE_MOBILITY"
    ueComm = "UE_COMM"
    abnormalBehavior = "ABNORMAL_BEHAVIOR"
    congestion = "CONGESTION"
    networkPerformance = "NETWORK_PERFORMANCE"
    qosSustainability = "QOS_SUSTAINABILITY"
    dispersion = "DISPERSION"
    dnPerformance = "DN_PERFORMANCE"
    serviceExperience = "SERVICE_EXPERIENCE"


class GeographicalArea(ExtraBaseModel):
    civicAddress: Optional[CivicAddress] = None
    shapes: Optional[GeographicArea] = None


class LocationArea5G(ExtraBaseModel):
    geographicAreas: Optional[List[GeographicArea]] = Field(
        None,
        description="Identifies a list of geographic area of the user where the UE is located.",
        min_items=0,
    )
    civicAddresses: Optional[List[CivicAddress]] = Field(
        None,
        description="Identifies a list of civic addresses of the user where the UE is located.",
        min_items=0,
    )
    nwAreaInfo: Optional[NetworkAreaInfo] = None


class Supi(ExtraBaseModel):
    __root__: constr(regex=r"^(imsi-[0-9]{5,15}|nai-.+|gci-.+|gli-.+|.+)$") = Field(
        ...,
        description='String identifying a Supi that shall contain either an IMSI, a network specific identifier,\na Global Cable Identifier (GCI) or a Global Line Identifier (GLI) as specified in clause \n2.2A of 3GPP TS 23.003. It shall be formatted as follows\n - for an IMSI "imsi-<imsi>", where <imsi> shall be formatted according to clause 2.2\n   of 3GPP TS 23.003 that describes an IMSI.\n - for a network specific identifier "nai-<nai>, where <nai> shall be formatted\n   according to clause 28.7.2 of 3GPP TS 23.003 that describes an NAI.\n - for a GCI "gci-<gci>", where <gci> shall be formatted according to clause 28.15.2\n   of 3GPP TS 23.003.\n - for a GLI "gli-<gli>", where <gli> shall be formatted according to clause 28.16.2 of\n   3GPP TS 23.003.To enable that the value is used as part of an URI, the string shall\n   only contain characters allowed according to the "lower-with-hyphen" naming convention\n   defined in 3GPP TS 29.501.\n',
    )


class Gpsi(ExtraBaseModel):
    __root__: constr(regex=r"^(msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|.+)$") = Field(
        ...,
        description="String identifying a Gpsi shall contain either an External Id or an MSISDN.  It shall be formatted as follows -External Identifier= \"extid-'extid', where 'extid'  shall be formatted according to clause 19.7.2 of 3GPP TS 23.003 that describes an  External Identifier. \n",
    )


class GeoDistributionInfo1(ExtraBaseModel):
    loc: UserLocation
    supis: List[Supi] = Field(..., min_items=1)
    gpsis: Optional[List[Gpsi]] = Field(None, min_items=1)


class GeoDistributionInfo2(ExtraBaseModel):
    loc: UserLocation
    supis: Optional[List[Supi]] = Field(None, min_items=1)
    gpsis: List[Gpsi] = Field(..., min_items=1)


class GeoDistributionInfo(ExtraBaseModel):
    __root__: Union[GeoDistributionInfo1, GeoDistributionInfo2] = Field(
        ..., description="Represents the geographical distribution of the UEs."
    )


class UeLocationInfo(ExtraBaseModel):
    loc: LocationArea5G
    geoLoc: Optional[GeographicalArea] = None
    ratio: int = Field(None, description="Expressed in percent", ge=1, le=100)
    confidence: int = Field(None, description="", ge=0)
    geoDistrInfos: Optional[List[GeoDistributionInfo]] = Field(None, min_items=1)


class AnalyticsFailureEventInfo(ExtraBaseModel):
    """Represents an event for which the subscription request was not successful
    and including the associated failure reason."""

    event: AnalyticsEvent
    failureCode: AnalyticsFailureCode


class QosSustainabilityExposure(ExtraBaseModel):
    """Represents a QoS sustainability information."""

    # TODO: LocationArea5G
    # locArea: LocationArea5G
    startTs: datetime
    endTs: datetime
    qosFlowRetThd: RetainabilityThreshold
    ranUeThrouThd: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")
    snssai: Snssai
    confidence: int = Field(None, description="", ge=0)


class CongestionAnalytics(ExtraBaseModel):
    """Represents data congestion analytics for transfer over the user plane,
    control plane or both."""

    cngType: CongestionType
    tmWdw: TimeWindow
    nsi: ThresholdLevel
    confidence: int = Field(None, description="", ge=0)
    topAppListUl: List[TopApplication] = Field(None, description="", min_items=1)
    topAppListDl: List[TopApplication] = Field(None, description="", min_items=1)


class CongestInfo(ExtraBaseModel):
    """Represents a UE's user data congestion information."""

    # locArea: LocationArea5G
    cngAnas: List[CongestionAnalytics] = Field(None, description="", min_items=1)


class AbnormalExposure(ExtraBaseModel):
    """Represents a user's abnormal behavior information."""

    # TODO: test this list
    gpsis: List[constr(regex=r"^(msisdn-[0-9]{5,15}|extid-.+@.+|.+)$")] = Field(
        None, description="", min_items=1
    )
    appId: str = Field(None, description="String providing an application identifier.")
    dnn: Optional[str] = Field(
        "province1.mnc01.mcc202.gprs",
        description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003",
    )
    snssai: Snssai
    excep: List[Exception]
    ratio: int = Field(None, description="Expressed in percent", ge=1, le=100)
    confidence: int = Field(None, description="", ge=0)
    addtMeasInfo: AdditionalMeasurement


class NetworkPerfExposure(ExtraBaseModel):
    """Represents network performance information."""

    # locArea: LocationArea5G
    nwPerfType: NetworkPerfType
    relativeRatio: int = Field(None, description="Expressed in percent", ge=1, le=100)
    absoluteNum: int = Field(None, description="", ge=0)
    confidence: int = Field(None, description="", ge=0)


class AnalyticsEventFilter(ExtraBaseModel):
    """Represents analytics event filter information."""

    # locArea: LocationArea5G
    dnn: Optional[str] = Field(
        "province1.mnc01.mcc202.gprs",
        description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003",
    )
    dnais: List[str] = Field(
        None,
        description="DNAI (Data network access identifier), see clause 5.6.7 of 3GPP TS 23.501.",
        min_items=1,
    )
    nwPerfTypes: List[NetworkPerfType] = Field(None, description="", min_items=1)
    appIds: List[str] = Field(
        None, description="String providing an application identifier.", min_items=1
    )
    appIds: List[ExceptionId] = Field(None, description="", min_items=1)
    exptAnaType: ExpectedAnalyticsType
    exptUeBehav: ExpectedUeBehaviourData
    snssai: Snssai
    nsiIdInfos: List[NsiIdInfo] = Field(None, description="", min_items=1)
    qosReq: QosRequirement
    listOfAnaSubsets: List[AnalyticsSubset] = Field(None, description="", min_items=1)
    dnPerfReqs: List[DnPerformanceReq] = Field(None, description="", min_items=1)
    bwRequs: List[BwRequirement] = Field(None, description="", min_items=1)
    ratFreqs: List[RatFreqInformation] = Field(None, description="", min_items=1)
    appServerAddrs: List[AddrFqdn] = Field(None, description="", min_items=1)
    maxNumOfTopAppUl: int = Field(None, description="", ge=0)
    maxNumOfTopAppDl: int = Field(None, description="", ge=0)
    # visitedLocAreas: List[LocationArea5G] = Field(None, description="", min_items=1)


class TargetUeId(ExtraBaseModel):
    """Represents the target UE(s) information."""

    anyUeInd: Optional[bool]
    gpsi: constr(regex=r"^(msisdn-[0-9]{5,15}|extid-.+@.+|.+)$")
    exterGroupId: str = Field("Group1@domain.com", description="")


class UeMobilityExposure(ExtraBaseModel):
    """Represents a UE mobility information."""

    ts: Optional[datetime]
    recurringTime: Optional[ScheduledCommunicationTime]
    duration: int = Field(None, description="", ge=0)
    durationVariance: Optional[float]
    locInfo: List[UeLocationInfo] = Field(None, description="", min_items=1)


class AnalyticsRequest(ExtraBaseModel):
    """Represents the parameters to request to retrieve analytics information."""

    analyEvent: AnalyticsEvent
    analyEventFilter: Optional[AnalyticsEventFilter]
    analyRep: Optional[EventReportingRequirement]
    tgtUe: TargetUeId
    suppFeat: constr(regex=r"^[A-Fa-f0-9]*$")


class AnalyticsData(ExtraBaseModel):
    """Represents analytics data."""

    start: Optional[datetime]
    expiry: Optional[datetime]
    timeStampGen: Optional[datetime]
    ueMobilityInfos: List[UeMobilityExposure] = Field(None, description="", min_items=1)
    ueCommInfos: List[UeCommunication] = Field(None, description="", min_items=1)
    nwPerfInfos: List[NetworkPerfExposure] = Field(None, description="", min_items=1)
    abnormalInfos: List[AbnormalExposure] = Field(None, description="", min_items=1)
    congestInfos: List[CongestInfo] = Field(None, description="", min_items=1)
    qosSustainInfos: List[QosSustainabilityExposure] = Field(
        None, description="", min_items=1
    )
    disperInfos: List[DispersionInfo] = Field(None, description="", min_items=1)
    dnPerfInfos: List[DnPerfInfo] = Field(None, description="", min_items=1)
    svcExps: List[ServiceExperienceInfo] = Field(None, description="", min_items=1)
    disperReqs: List[DispersionRequirement] = Field(None, description="", min_items=1)
    suppFeat: constr(regex=r"^[A-Fa-f0-9]*$")


class UeLocationInfo(ExtraBaseModel):
    """Represents a UE location information."""

    loc: LocationArea5G
    ratio: int = Field(None, description="Expressed in percent", ge=1, le=100)
    confidence: int = Field(None, description="", ge=0)


class AnalyticsEventFilterSubsc(ExtraBaseModel):
    """Represents an analytics event filter."""

    nwPerfReqs: List[NetworkPerfRequirement] = Field(None, description="", min_items=1)
    # locArea: LocationArea5G
    appIds: List[str] = Field(
        None, description="String providing an application identifier."
    )
    dnn: Optional[str] = Field(
        "province1.mnc01.mcc202.gprs",
        description="String identifying the Data Network Name (i.e., Access Point Name in 4G). For more information check clause 9A of 3GPP TS 23.003",
    )
    dnais: List[str] = Field(
        None,
        description="DNAI (Data network access identifier), see clause 5.6.7 of 3GPP TS 23.501.",
        min_items=1,
    )
    excepRequs: List[Exception] = Field(None, description="", min_items=1)
    exptAnaType: ExpectedAnalyticsType
    exptUeBehav: ExpectedUeBehaviourData
    matchingDir: MatchingDirection
    reptThlds: List[ThresholdLevel] = Field(None, description="", min_items=1)
    snssai: Snssai
    nsiIdInfos: List[NsiIdInfo] = Field(None, description="", min_items=1)
    qosReq: QosRequirement
    qosFlowRetThds: List[RetainabilityThreshold] = Field(
        None, description="", min_items=1
    )
    ranUeThrouThds: List[constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$")] = (
        Field(None, description="", min_items=1)
    )
    disperReqs: List[DispersionRequirement] = Field(None, description="", min_items=1)
    listOfAnaSubsets: List[AnalyticsSubset] = Field(None, description="", min_items=1)
    dnPerfReqs: List[DnPerformanceReq] = Field(None, description="", min_items=1)
    bwRequs: List[BwRequirement] = Field(None, description="", min_items=1)
    ratFreqs: List[RatFreqInformation] = Field(None, description="", min_items=1)
    appServerAddrs: List[AddrFqdn] = Field(None, description="", min_items=1)
    extraReportReq: List[EventReportingRequirement] = Field(
        None, description="", min_items=1
    )
    maxNumOfTopAppUl: int = Field(None, description="", ge=0)
    maxNumOfTopAppDl: int = Field(None, description="", ge=0)
    # visitedLocAreas: List[LocationArea5G] = Field(None, description="", min_items=1)


class AnalyticsEventSubsc(ExtraBaseModel):
    """Represents a subscribed analytics event."""

    analyEvent: AnalyticsEvent
    analyEventFilter: AnalyticsEventFilterSubsc
    tgtUe: TargetUeId


class AnalyticsEventNotif(ExtraBaseModel):
    """Represents an analytics event to be reported."""

    analyEvent: AnalyticsEvent
    expiry: datetime
    timeStamp: datetime
    failNotifyCode: NwdafFailureCode
    rvWaitTime: int = Field(None, description="", ge=0)
    ueMobilityInfos: List[UeMobilityExposure] = Field(None, description="", min_items=1)
    ueCommInfos: List[UeCommunication] = Field(None, description="", min_items=1)
    abnormalInfos: List[AbnormalExposure] = Field(None, description="", min_items=1)
    congestInfos: List[CongestInfo] = Field(None, description="", min_items=1)
    nwPerfInfos: List[NetworkPerfExposure] = Field(None, description="", min_items=1)
    qosSustainInfos: List[QosSustainabilityExposure] = Field(
        None, description="", min_items=1
    )
    disperInfos: List[DispersionInfo] = Field(None, description="", min_items=1)
    dnPerfInfos: List[DnPerfInfo] = Field(None, description="", min_items=1)
    svcExps: List[ServiceExperienceInfo] = Field(None, description="", min_items=1)
    start: datetime
    timeStampGen: datetime


class AnalyticsEventNotification(ExtraBaseModel):
    """Represents an analytics event(s) notification."""

    notifId: str
    analyEventNotifs: List[AnalyticsEventNotif] = Field(
        None, description="", min_items=1
    )


class AnalyticsExposureSubscCreate(ExtraBaseModel):
    """Represents an analytics exposure subscription."""

    analyEventsSubs: List[AnalyticsEventSubsc] = Field(
        None, description="", min_items=1
    )
    analyRepInfo: ReportingInformation
    notifUri: str
    notifId: str
    eventNotifis: List[AnalyticsEventNotif] = Field(None, description="", min_items=1)
    failEventReports: List[AnalyticsFailureEventInfo] = Field(
        None, description="", min_items=1
    )
    suppFeat: constr(regex=r"^[A-Fa-f0-9]*$")
    requestTestNotification: bool = Field(
        None,
        description="Set to true by the AF to request the NEF to send a test notification as defined in clause 5.2.5.3 of 3GPP TS 29.122. Set to false or omitted otherwise.",
    )
    websockNotifConfig: WebsockNotifConfig


class AnalyticsExposureSubsc(AnalyticsExposureSubscCreate):
    """Represents an analytics exposure subscription."""

    link: Optional[AnyHttpUrl] = Field(
        "https://myresource.com",
        description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response",
    )

    class Config:
        orm_mode = True
