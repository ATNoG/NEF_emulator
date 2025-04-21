from typing import List, Optional, Union
from datetime import datetime
from pydantic import Field, IPvAnyAddress, AnyHttpUrl, confloat, conint, constr
from enum import Enum
from .utils import ExtraBaseModel

# Shared properties | used for request body in endpoint/items.py
# We can declare a UserBase model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes


class ExternalId(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description='string containing a local identifier followed by "@" and a domain identifier. Both the local identifier and the domain identifier shall be encoded as strings that do not contain any "@" characters. See Clause 4.6.2 of 3GPP TS 23.682 for more information.',
    )


class ApplicationId(ExtraBaseModel):
    __root__: str = Field(
        ..., description="String providing an application identifier."
    )


class Msisdn(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description="string formatted according to clause 3.3 of 3GPP TS 23.003 that describes an MSISDN.",
    )


class DurationSecModel(ExtraBaseModel):
    __root__: conint(ge=0) = Field(
        ...,
        description="Unsigned integer identifying a period of time in units of seconds.",
    )


class Snssai(ExtraBaseModel):
    sst: conint(ge=0, le=255) = Field(
        ...,
        description="Unsigned integer, within the range 0 to 255, representing the Slice/Service Type.  It indicates the expected Network Slice behaviour in terms of features and services. Values 0 to 127 correspond to the standardized SST range. Values 128 to 255 correspond  to the Operator-specific range. See clause 28.4.2 of 3GPP TS 23.003. Standardized values are defined in clause 5.15.2.2 of 3GPP TS 23.501.",
    )
    sd: Optional[constr(regex=r"^[A-Fa-f0-9]{6}$")] = Field(
        None,
        description='3-octet string, representing the Slice Differentiator, in hexadecimal representation. Each character in the string shall take a value of "0" to "9", "a" to "f" or "A" to "F" and shall represent 4 bits. The most significant character representing the 4 most significant bits of the SD shall appear first in the string, and the character representing the 4 least significant bit of the SD shall appear last in the string. This is an optional parameter that complements the Slice/Service type(s) to allow to  differentiate amongst multiple Network Slices of the same Slice/Service type. This IE shall be absent if no SD value is associated with the SST.',
    )


class Dnn(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description='String representing a Data Network as defined in clause 9A of 3GPP TS 23.003;  it shall contain either a DNN Network Identifier, or a full DNN with both the Network  Identifier and Operator Identifier, as specified in 3GPP TS 23.003 clause 9.1.1 and 9.1.2. It shall be coded as string in which the labels are separated by dots  (e.g. "Label1.Label2.Label3").',
    )


class Ipv4Addr(ExtraBaseModel):
    __root__: constr(
        regex=r"^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
    ) = Field(
        ...,
        description="String identifying a IPv4 address formatted in the 'dotted decimal' notation as defined in RFC 1166.",
        example="198.51.100.1",
    )


class Ipv6Addr(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description="String identifying an IPv6 address formatted according to clause 4 of RFC5952. The mixed IPv4 IPv6 notation according to clause 5 of RFC5952 shall not be used.",
    )


class Ipv6Prefix(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description="String identifying an IPv6 address prefix formatted according to clause 4 of RFC 5952. IPv6Prefix data type may contain an individual /128 IPv6 address.",
    )


class MacAddr48(ExtraBaseModel):
    __root__: constr(regex=r"^([0-9a-fA-F]{2})((-[0-9a-fA-F]{2}){5})$") = Field(
        ...,
        description="String identifying a MAC address formatted in the hexadecimal notation according to clause 1.1 and clause 2.1 of RFC 7042.",
    )


class Ipv4AddrModel(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description='string identifying a Ipv4 address formatted in the "dotted decimal" notation as defined in IETF RFC 1166.',
    )


class Ipv6AddrModel(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description="string identifying a Ipv6 address formatted according to clause 4 in IETF RFC 5952. The mixed Ipv4 Ipv6 notation according to clause 5 of IETF RFC 5952 shall not be used.",
    )


class DurationMin(ExtraBaseModel):
    __root__: conint(ge=0) = Field(
        ...,
        description="Unsigned integer identifying a period of time in units of minutes.",
    )


class Tac(ExtraBaseModel):
    __root__: constr(regex=r"(^[A-Fa-f0-9]{4}$)|(^[A-Fa-f0-9]{6}$)") = Field(
        ...,
        description='2 or 3-octet string identifying a tracking area code as specified in clause 9.3.3.10  of 3GPP TS 38.413, in hexadecimal representation. Each character in the string shall  take a value of "0" to "9", "a" to "f" or "A" to "F" and shall represent 4 bits. The most significant character representing the 4 most significant bits of the TAC shall  appear first in the string, and the character representing the 4 least significant bit  of the TAC shall appear last in the string. \n',
    )


class Nid(ExtraBaseModel):
    __root__: constr(regex=r"^[A-Fa-f0-9]{11}$") = Field(
        ...,
        description="This represents the Network Identifier, which together with a PLMN ID is used to identify an SNPN (see 3GPP TS 23.003 and 3GPP TS 23.501 clause 5.30.2.1). \n",
    )


class EutraCellId(ExtraBaseModel):
    __root__: constr(regex=r"^[A-Fa-f0-9]{7}$") = Field(
        ...,
        description='28-bit string identifying an E-UTRA Cell Id as specified in clause 9.3.1.9 of  3GPP TS 38.413, in hexadecimal representation. Each character in the string shall take a  value of "0" to "9", "a" to "f" or "A" to "F" and shall represent 4 bits. The most  significant character representing the 4 most significant bits of the Cell Id shall appear  first in the string, and the character representing the 4 least significant bit of the  Cell Id shall appear last in the string. \n',
    )


class N3IwfId(ExtraBaseModel):
    __root__: constr(regex=r"^[A-Fa-f0-9]+$") = Field(
        ...,
        description='This represents the identifier of the N3IWF ID as specified in clause 9.3.1.57 of  3GPP TS 38.413 in hexadecimal representation. Each character in the string shall take a value  of "0" to "9", "a" to "f" or "A" to "F" and shall represent 4 bits. The most significant  character representing the 4 most significant bits of the N3IWF ID shall appear first in the  string, and the character representing the 4 least significant bit of the N3IWF ID shall  appear last in the string. \n',
    )


class GNbId(ExtraBaseModel):
    bitLength: conint(ge=22, le=32) = Field(
        ...,
        description="Unsigned integer representing the bit length of the gNB ID as defined in clause 9.3.1.6 of 3GPP TS 38.413 [11], within the range 22 to 32.\n",
    )
    gNBValue: constr(regex=r"^[A-Fa-f0-9]{6,8}$") = Field(
        ...,
        description='This represents the identifier of the gNB. The value of the gNB ID shall be encoded in hexadecimal representation. Each character in the string shall take a value of "0" to "9", "a" to "f" or "A" to "F" and shall represent 4 bits. The padding 0 shall be added to make multiple nibbles,  the most significant character representing the padding 0 if required together with the 4 most significant bits of the gNB ID shall appear first in the string, and the character representing the 4 least significant bit of the gNB ID shall appear last in the string.\n',
    )


class WAgfId(ExtraBaseModel):
    __root__: constr(regex=r"^[A-Fa-f0-9]+$") = Field(
        ...,
        description='This represents the identifier of the W-AGF ID as specified in clause 9.3.1.162 of  3GPP TS 38.413 in hexadecimal representation. Each character in the string shall take a value  of "0" to "9", "a" to "f" or "A" to "F" and shall represent 4 bits. The most significant  character representing the 4 most significant bits of the W-AGF ID shall appear first in the  string, and the character representing the 4 least significant bit of the W-AGF ID shall  appear last in the string. \n',
    )


class TngfId(ExtraBaseModel):
    __root__: constr(regex=r"^[A-Fa-f0-9]+$") = Field(
        ...,
        description='This represents the identifier of the TNGF ID as specified in clause 9.3.1.161 of  3GPP TS 38.413  in hexadecimal representation. Each character in the string shall take a value of "0" to "9", "a"  to "f" or "A" to "F" and shall represent 4 bits. The most significant character representing the  4 most significant bits of the TNGF ID shall appear first in the string, and the character  representing the 4 least significant bit of the TNGF ID shall appear last in the string. \n',
    )


class NgeNbId(ExtraBaseModel):
    __root__: constr(
        regex=r"^(MacroNGeNB-[A-Fa-f0-9]{5}|LMacroNGeNB-[A-Fa-f0-9]{6}|SMacroNGeNB-[A-Fa-f0-9]{5})$"
    ) = Field(
        ...,
        description='This represents the identifier of the ng-eNB ID as specified in clause 9.3.1.8 of  3GPP TS 38.413. The value of the ng-eNB ID shall be encoded in hexadecimal representation.  Each character in the string shall take a value of "0" to "9", "a" to "f" or "A" to "F" and  shall represent 4 bits. The padding 0 shall be added to make multiple nibbles, so the most  significant character representing the padding 0 if required together with the 4 most  significant bits of the ng-eNB ID shall appear first in the string, and the character  representing the 4 least significant bit of the ng-eNB ID (to form a nibble) shall appear last  in the string. \n',
        example="SMacroNGeNB-34B89",
    )


class ENbId(ExtraBaseModel):
    __root__: constr(
        regex=r"^(MacroeNB-[A-Fa-f0-9]{5}|LMacroeNB-[A-Fa-f0-9]{6}|SMacroeNB-[A-Fa-f0-9]{5}|HomeeNB-[A-Fa-f0-9]{7})$"
    ) = Field(
        ...,
        description='This represents the identifier of the eNB ID as specified in clause 9.2.1.37 of  3GPP TS 36.413. The string shall be formatted with the following pattern  \'^(\'MacroeNB-[A-Fa-f0-9]{5}|LMacroeNB-[A-Fa-f0-9]{6}|SMacroeNB-[A-Fa-f0-9]{5} |HomeeNB-[A-Fa-f0-9]{7})$\'. The value of the eNB ID shall be encoded in hexadecimal representation. Each character in the  string shall take a value of "0" to "9", "a" to "f" or "A" to "F" and shall represent 4 bits.  The padding 0 shall be added to make multiple nibbles, so the most significant character  representing the padding 0 if required together with the 4 most significant bits of the eNB ID  shall appear first in the string, and the character representing the 4 least significant bit  of the eNB ID (to form a nibble) shall appear last in the string.\n',
    )


class Uinteger(ExtraBaseModel):
    __root__: conint(ge=0) = Field(
        ...,
        description="Unsigned Integer, i.e. only value 0 and integers above 0 are permissible.",
    )


class NrCellId(ExtraBaseModel):
    __root__: constr(regex=r"^[A-Fa-f0-9]{9}$") = Field(
        ...,
        description='36-bit string identifying an NR Cell Id as specified in clause 9.3.1.7 of 3GPP TS 38.413,  in hexadecimal representation. Each character in the string shall take a value of "0" to "9",  "a" to "f" or "A" to "F" and shall represent 4 bits. The most significant character  representing the 4 most significant bits of the Cell Id shall appear first in the string, and  the character representing the 4 least significant bit of the Cell Id shall appear last in the  string. \n',
    )


class SupportedFeatures(ExtraBaseModel):
    __root__: constr(regex=r"^[A-Fa-f0-9]*$") = Field(
        ...,
        description='A string used to indicate the features supported by an API that is used as defined in clause  6.6 in 3GPP TS 29.500.\nThe string shall contain a bitmask indicating supported features in  hexadecimal representation Each character in the string shall take a value of "0" to "9",  "a" to "f" or "A" to "F" and shall represent the support of 4 features as described in  table\xa05.2.2-3. The most significant character representing the highest-numbered features shall  appear first in the string, and the character representing features 1 to 4 shall appear last  in the string. The list of features and their numbering (starting with 1) are defined  separately for each API. If the string contains a lower number of characters than there are  defined features for an API, all features that would be represented by characters that are not  present in the string are not supported.',
    )


class Gpsi(ExtraBaseModel):
    __root__: constr(regex=r"^(msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|.+)$") = Field(
        ...,
        description="String identifying a Gpsi shall contain either an External Id or an MSISDN.  It shall be formatted as follows -External Identifier= \"extid-'extid', where 'extid'  shall be formatted according to clause 19.7.2 of 3GPP TS 23.003 that describes an  External Identifier. \n",
    )


class BitRate(ExtraBaseModel):
    __root__: constr(regex=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$") = Field(
        ...,
        description='String representing a bit rate; the prefixes follow the standard symbols from The International System of Units, and represent x1000 multipliers, with the exception that prefix "K" is used to represent the standard symbol "k".\n',
    )


class Volume(ExtraBaseModel):
    __root__: conint(ge=0) = Field(
        ..., description="Unsigned integer identifying a volume in units of bytes."
    )


class TransportProtocol(Enum):
    UDP = "UDP"
    TCP = "TCP"


class HfcNId(ExtraBaseModel):
    __root__: constr(max_length=6) = Field(
        ...,
        description="This IE represents the identifier of the HFC node Id as specified in CableLabs WR-TR-5WWC-ARCH. It is provisioned by the wireline operator as part of wireline operations and may contain up to six characters.\n",
    )


class Bytes(ExtraBaseModel):
    __root__: str = Field(
        ..., description="string with format 'bytes' as defined in OpenAPI"
    )


class Gli(ExtraBaseModel):
    __root__: Bytes


class Gci(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description="Global Cable Identifier uniquely identifying the connection between the 5G-CRG or FN-CRG to the 5GS. See clause 28.15.4 of 3GPP TS 23.003. This shall be encoded as a string per clause 28.15.4 of 3GPP TS 23.003, and compliant with the syntax specified  in clause 2.2  of IETF RFC 7542 for the username part of a NAI. The GCI value is specified in CableLabs WR-TR-5WWC-ARCH.\n",
    )


class Uncertainty(ExtraBaseModel):
    __root__: confloat(ge=0.0) = Field(
        ..., description="Indicates value of uncertainty."
    )


class Altitude(ExtraBaseModel):
    __root__: confloat(ge=-32767.0, le=32767.0) = Field(
        ..., description="Indicates value of altitude."
    )


class InnerRadius(ExtraBaseModel):
    __root__: conint(ge=0, le=327675) = Field(
        ..., description="Indicates value of the inner radius."
    )


class Confidence(ExtraBaseModel):
    __root__: conint(ge=0, le=100) = Field(
        ..., description="Indicates value of confidence."
    )


class Angle(ExtraBaseModel):
    __root__: conint(ge=0, le=360) = Field(..., description="Indicates value of angle.")


class Orientation(ExtraBaseModel):
    __root__: conint(ge=0, le=180) = Field(
        ..., description="Indicates value of orientation angle."
    )


class HorizontalSpeed(ExtraBaseModel):
    __root__: confloat(ge=0.0, le=2047.0) = Field(
        ..., description="Indicates value of horizontal speed."
    )


class VerticalSpeed(ExtraBaseModel):
    __root__: confloat(ge=0.0, le=255.0) = Field(
        ..., description="Indicates value of vertical speed."
    )


class SpeedUncertainty(ExtraBaseModel):
    __root__: confloat(ge=0.0, le=255.0) = Field(
        ..., description="Indicates value of speed uncertainty."
    )


class Accuracy(ExtraBaseModel):
    __root__: confloat(ge=0.0) = Field(..., description="Indicates value of accuracy.")


class ApplicationlayerId(ExtraBaseModel):
    __root__: str = Field(
        ...,
        description="String identifying an UE with application layer ID. The format of the application  layer ID parameter is same as the Application layer ID defined in clause 11.3.4 of  3GPP TS 24.554.\n",
    )


class PlmnId(ExtraBaseModel):
    mcc: int
    mnc: int


class Tai(ExtraBaseModel):
    plmnId: PlmnId
    tac: Tac
    nid: Optional[Nid] = None


class Ecgi(ExtraBaseModel):
    plmnId: PlmnId
    eutraCellId: EutraCellId
    nid: Optional[Nid] = None


class SupportedGADShapes(Enum):
    POINT = "POINT"


class GADShape(ExtraBaseModel):
    shape: SupportedGADShapes


class GeographicalCoordinates(ExtraBaseModel):
    lon: confloat(ge=-180.0, le=180.0)
    lat: confloat(ge=-90.0, le=90.0)


class PointList(ExtraBaseModel):
    __root__: List[GeographicalCoordinates] = Field(
        ..., description="List of points.", max_items=15, min_items=3
    )


class Point(GADShape):
    point: GeographicalCoordinates


class PointUncertaintyCircle(GADShape):
    point: GeographicalCoordinates
    uncertainty: Uncertainty


class Polygon(GADShape):
    pointList: PointList


class PointAltitude(GADShape):
    point: GeographicalCoordinates
    altitude: Altitude


class EllipsoidArc(GADShape):
    point: GeographicalCoordinates
    innerRadius: InnerRadius
    uncertaintyRadius: Uncertainty
    offsetAngle: Angle
    includedAngle: Angle
    confidence: Confidence


class UncertaintyEllipse(ExtraBaseModel):
    semiMajor: Uncertainty
    semiMinor: Uncertainty
    orientationMajor: Orientation


class PointUncertaintyEllipse(GADShape):
    point: GeographicalCoordinates
    uncertaintyEllipse: UncertaintyEllipse
    confidence: Confidence


class PointAltitudeUncertainty(GADShape):
    point: GeographicalCoordinates
    altitude: Altitude
    uncertaintyEllipse: UncertaintyEllipse
    uncertaintyAltitude: Uncertainty
    confidence: Confidence
    vConfidence: Optional[Confidence] = None


class GeographicArea(ExtraBaseModel):
    __root__: Union[
        Point,
        PointUncertaintyCircle,
        PointUncertaintyEllipse,
        Polygon,
        PointAltitude,
        PointAltitudeUncertainty,
        EllipsoidArc,
    ] = Field(..., description="Geographic area specified by different shape.")


class GlobalRanNodeId(ExtraBaseModel):
    plmnId: PlmnId
    n3IwfId: Optional[N3IwfId] = None
    gNbId: Optional[GNbId] = None
    ngeNbId: Optional[NgeNbId] = None
    wagfId: Optional[WAgfId] = None
    tngfId: Optional[TngfId] = None
    nid: Optional[Nid] = None
    eNbId: Optional[ENbId] = None


class EutraLocation(ExtraBaseModel):
    tai: Tai
    ignoreTai: Optional[bool] = False
    ecgi: Ecgi
    ignoreEcgi: Optional[bool] = Field(
        False,
        description="This flag when present shall indicate that the Ecgi shall be ignored When present, it shall be set as follows: - true: ecgi shall be ignored. - false (default): ecgi shall not be ignored.\n",
    )
    ageOfLocationInformation: Optional[conint(ge=0, le=32767)] = Field(
        None,
        description='The value represents the elapsed time in minutes since the last network contact of the mobile station.  Value "0" indicates that the location information was obtained after a successful paging procedure for Active Location Retrieval when the UE is in idle mode or after a successful NG-RAN location reporting procedure with the eNB when the UE is in connected mode.  Any other value than "0" indicates that the location information is the last known one.  See 3GPP TS 29.002 clause 17.7.8.\n',
    )
    ueLocationTimestamp: Optional[datetime] = None
    geographicalInformation: Optional[constr(regex=r"^[0-9A-F]{16}$")] = Field(
        None,
        description="Refer to geographical Information. See 3GPP TS 23.032 clause 7.3.2. Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )
    geodeticInformation: Optional[constr(regex=r"^[0-9A-F]{20}$")] = Field(
        None,
        description="Refers to Calling Geodetic Location. See ITU-T Recommendation Q.763 (1999) [24] clause 3.88.2. Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )
    globalNgenbId: Optional[GlobalRanNodeId] = None
    globalENbId: Optional[GlobalRanNodeId] = None


class Ncgi(ExtraBaseModel):
    plmnId: PlmnId
    nrCellId: NrCellId
    nid: Optional[Nid] = None


class PlmnIdNid(ExtraBaseModel):
    mcc: int
    mnc: int
    nid: Optional[Nid] = None


class NtnTaiInfo(ExtraBaseModel):
    plmnId: PlmnIdNid
    tacList: List[Tac] = Field(..., min_items=1)
    derivedTac: Optional[Tac] = None


class TnapId(ExtraBaseModel):
    ssId: Optional[str] = Field(
        None,
        description="This IE shall be present if the UE is accessing the 5GC via a trusted WLAN access network.When present, it shall contain the SSID of the access point to which the UE is attached, that is received over NGAP,  see IEEE Std 802.11-2012. \n",
    )
    bssId: Optional[str] = Field(
        None,
        description="When present, it shall contain the BSSID of the access point to which the UE is attached, that is received over NGAP, see IEEE Std 802.11-2012. \n",
    )
    civicAddress: Optional[Bytes] = None


class TwapId(ExtraBaseModel):
    ssId: str = Field(
        ...,
        description="This IE shall contain the SSID of the access point to which the UE is attached, that is received over NGAP, see IEEE Std 802.11-2012. \n",
    )
    bssId: Optional[str] = Field(
        None,
        description="When present, it shall contain the BSSID of the access point to which the UE is attached, for trusted WLAN access, see IEEE Std 802.11-2012. \n",
    )
    civicAddress: Optional[Bytes] = None


class HfcNodeId(ExtraBaseModel):
    hfcNId: HfcNId


class LineType(Enum):
    DSL = "DSL"
    PON = "PON"


class N3gaLocation(ExtraBaseModel):
    n3gppTai: Optional[Tai] = None
    n3IwfId: Optional[constr(regex=r"^[A-Fa-f0-9]+$")] = Field(
        None,
        description='This IE shall contain the N3IWF identifier received over NGAP and shall be encoded as a  string of hexadecimal characters. Each character in the string shall take a value of "0"  to "9", "a" to "f" or "A" to "F" and shall represent 4 bits. The most significant  character representing the 4 most significant bits of the N3IWF ID shall appear first in  the string, and the character representing the 4 least significant bit of the N3IWF ID  shall appear last in the string. \n',
    )
    ueIpv4Addr: Optional[Ipv4Addr] = None
    ueIpv6Addr: Optional[Ipv6Addr] = None
    portNumber: Optional[Uinteger] = None
    protocol: Optional[TransportProtocol] = None
    tnapId: Optional[TnapId] = None
    twapId: Optional[TwapId] = None
    hfcNodeId: Optional[HfcNodeId] = None
    gli: Optional[Gli] = None
    w5gbanLineType: Optional[LineType] = None
    gci: Optional[Gci] = None


class NrLocation(ExtraBaseModel):
    tai: Tai
    ncgi: Ncgi
    ignoreNcgi: Optional[bool] = False
    ageOfLocationInformation: Optional[conint(ge=0, le=32767)] = Field(
        None,
        description='The value represents the elapsed time in minutes since the last network contact of the mobile station. Value "0" indicates that the location information was obtained after a successful paging procedure for Active Location Retrieval when the UE is in idle mode or after a successful  NG-RAN location reporting procedure with the eNB when the UE is in connected mode. Any other value than "0" indicates that the location information is the last known one. See 3GPP TS 29.002 clause 17.7.8.\n',
    )
    ueLocationTimestamp: Optional[datetime] = None
    geographicalInformation: Optional[constr(regex=r"^[0-9A-F]{16}$")] = Field(
        None,
        description="Refer to geographical Information. See 3GPP TS 23.032 clause 7.3.2. Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )
    geodeticInformation: Optional[constr(regex=r"^[0-9A-F]{20}$")] = Field(
        None,
        description="Refers to Calling Geodetic Location. See ITU-T Recommendation Q.763 (1999) [24] clause 3.88.2. Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )
    globalGnbId: Optional[GlobalRanNodeId] = None
    ntnTaiInfo: Optional[NtnTaiInfo] = None


class CellGlobalId(ExtraBaseModel):
    plmnId: PlmnId
    lac: constr(regex=r"^[A-Fa-f0-9]{4}$")
    cellId: constr(regex=r"^[A-Fa-f0-9]{4}$")


class ServiceAreaId(ExtraBaseModel):
    plmnId: PlmnId
    lac: constr(regex=r"^[A-Fa-f0-9]{4}$") = Field(
        ..., description="Location Area Code."
    )
    sac: constr(regex=r"^[A-Fa-f0-9]{4}$") = Field(
        ..., description="Service Area Code."
    )


class RoutingAreaId(ExtraBaseModel):
    plmnId: PlmnId
    lac: constr(regex=r"^[A-Fa-f0-9]{4}$") = Field(
        ..., description="Location Area Code"
    )
    rac: constr(regex=r"^[A-Fa-f0-9]{2}$") = Field(..., description="Routing Area Code")


class LocationAreaId(ExtraBaseModel):
    plmnId: PlmnId
    lac: constr(regex=r"^[A-Fa-f0-9]{4}$") = Field(
        ..., description="Location Area Code."
    )


class UtraLocation(ExtraBaseModel):
    cgi: CellGlobalId
    sai: Optional[ServiceAreaId] = None
    lai: Optional[LocationAreaId] = None
    rai: Optional[RoutingAreaId] = None
    ageOfLocationInformation: Optional[conint(ge=0, le=32767)] = Field(
        None,
        description='The value represents the elapsed time in minutes since the last network contact of the mobile station.  Value "0" indicates that the location information was obtained after a successful paging procedure for  Active Location Retrieval when the UE is in idle mode\n or after a successful location reporting procedure  the UE is in connected mode. Any\nother value than "0" indicates that the location information is the last known one.  See 3GPP TS 29.002 clause 17.7.8.\n',
    )
    ueLocationTimestamp: Optional[datetime] = None
    geographicalInformation: Optional[constr(regex=r"^[0-9A-F]{16}$")] = Field(
        None,
        description="Refer to geographical Information.See 3GPP TS 23.032 clause 7.3.2. Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )
    geodeticInformation: Optional[constr(regex=r"^[0-9A-F]{20}$")] = Field(
        None,
        description="Refers to Calling Geodetic Location. See ITU-T\xa0Recommendation Q.763 (1999) clause 3.88.2. Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )


class GeraLocation(ExtraBaseModel):
    locationNumber: Optional[str] = Field(
        None,
        description="Location number within the PLMN. See 3GPP TS 23.003, clause 4.5.",
    )
    cgi: Optional[CellGlobalId] = None
    sai: Optional[ServiceAreaId] = None
    lai: Optional[LocationAreaId] = None
    rai: Optional[RoutingAreaId] = None
    vlrNumber: Optional[str] = Field(
        None, description="VLR number. See 3GPP TS 23.003 clause 5.1."
    )
    mscNumber: Optional[str] = Field(
        None, description="MSC number. See 3GPP TS 23.003 clause 5.1."
    )
    ageOfLocationInformation: Optional[conint(ge=0, le=32767)] = Field(
        None,
        description='The value represents the elapsed time in minutes since the last network contact of the mobile station. Value "0" indicates that the location information was obtained after a successful paging procedure for  Active Location Retrieval when the UE is in idle mode or after a successful location reporting procedure the UE is in connected mode. Any other value than "0" indicates that the location information is the last known one. See 3GPP TS 29.002 clause 17.7.8.\n',
    )
    ueLocationTimestamp: Optional[datetime] = None
    geographicalInformation: Optional[constr(regex=r"^[0-9A-F]{16}$")] = Field(
        None,
        description="Refer to geographical Information.See 3GPP TS 23.032 clause 7.3.2. Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )
    geodeticInformation: Optional[constr(regex=r"^[0-9A-F]{20}$")] = Field(
        None,
        description="Refers to Calling Geodetic Location.See ITU-T Recommendation Q.763 (1999) clause 3.88.2.  Only the description of an ellipsoid point with uncertainty circle is allowed to be used.\n",
    )


class UserLocation(ExtraBaseModel):
    eutraLocation: Optional[EutraLocation] = None
    nrLocation: Optional[NrLocation] = None
    n3gaLocation: Optional[N3gaLocation] = None
    utraLocation: Optional[UtraLocation] = None
    geraLocation: Optional[GeraLocation] = None


class CivicAddress(ExtraBaseModel):
    country: Optional[str] = None
    A1: Optional[str] = None
    A2: Optional[str] = None
    A3: Optional[str] = None
    A4: Optional[str] = None
    A5: Optional[str] = None
    A6: Optional[str] = None
    PRD: Optional[str] = None
    POD: Optional[str] = None
    STS: Optional[str] = None
    HNO: Optional[str] = None
    HNS: Optional[str] = None
    LMK: Optional[str] = None
    LOC: Optional[str] = None
    NAM: Optional[str] = None
    PC: Optional[str] = None
    BLD: Optional[str] = None
    UNIT: Optional[str] = None
    FLR: Optional[str] = None
    ROOM: Optional[str] = None
    PLC: Optional[str] = None
    PCN: Optional[str] = None
    POBOX: Optional[str] = None
    ADDCODE: Optional[str] = None
    SEAT: Optional[str] = None
    RD: Optional[str] = None
    RDSEC: Optional[str] = None
    RDBR: Optional[str] = None
    RDSUBBR: Optional[str] = None
    PRM: Optional[str] = None
    POM: Optional[str] = None
    usageRules: Optional[str] = None
    method: Optional[str] = None
    providedBy: Optional[str] = None


class PositioningMethod(Enum):
    CELLID = "CELLID"
    ECID = "ECID"
    OTDOA = "OTDOA"
    BAROMETRIC_PRESSURE = "BAROMETRIC_PRESSURE"
    WLAN = "WLAN"
    BLUETOOTH = "BLUETOOTH"
    MBS = "MBS"
    MOTION_SENSOR = "MOTION_SENSOR"
    DL_TDOA = "DL_TDOA"
    DL_AOD = "DL_AOD"
    MULTI_RTT = "MULTI-RTT"
    NR_ECID = "NR_ECID"
    UL_TDOA = "UL_TDOA"
    UL_AOA = "UL_AOA"
    NETWORK_SPECIFIC = "NETWORK_SPECIFIC"
    SL_TDOA = "SL_TDOA"
    SL_TOA = "SL_TOA"
    SL_AoA = "SL_AoA"
    SL_RT = "SL_RT"


class AccuracyFulfilmentIndicator(Enum):
    REQUESTED_ACCURACY_FULFILLED = "REQUESTED_ACCURACY_FULFILLED"
    REQUESTED_ACCURACY_NOT_FULFILLED = "REQUESTED_ACCURACY_NOT_FULFILLED"


class VerticalDirection(Enum):
    UPWARD = "UPWARD"
    DOWNWARD = "DOWNWARD"


class HorizontalVelocity(ExtraBaseModel):
    hSpeed: HorizontalSpeed
    bearing: Angle


class HorizontalWithVerticalVelocity(ExtraBaseModel):
    hSpeed: HorizontalSpeed
    bearing: Angle
    vSpeed: VerticalSpeed
    vDirection: VerticalDirection


class HorizontalVelocityWithUncertainty(ExtraBaseModel):
    hSpeed: HorizontalSpeed
    bearing: Angle
    hUncertainty: SpeedUncertainty


class HorizontalWithVerticalVelocityAndUncertainty(ExtraBaseModel):
    hSpeed: HorizontalSpeed
    bearing: Angle
    vSpeed: VerticalSpeed
    vDirection: VerticalDirection
    hUncertainty: SpeedUncertainty
    vUncertainty: SpeedUncertainty


class VelocityEstimate(ExtraBaseModel):
    __root__: Union[
        HorizontalVelocity,
        HorizontalWithVerticalVelocity,
        HorizontalVelocityWithUncertainty,
        HorizontalWithVerticalVelocityAndUncertainty,
    ] = Field(..., description="Velocity estimate.")


class LdrType(Enum):
    UE_AVAILABLE = "UE_AVAILABLE"
    PERIODIC = "PERIODIC"
    ENTERING_INTO_AREA = "ENTERING_INTO_AREA"
    LEAVING_FROM_AREA = "LEAVING_FROM_AREA"
    BEING_INSIDE_AREA = "BEING_INSIDE_AREA"
    MOTION = "MOTION"


class MinorLocationQoS(ExtraBaseModel):
    hAccuracy: Optional[Accuracy] = None
    vAccuracy: Optional[Accuracy] = None


class RangeDirection(ExtraBaseModel):
    distance: Optional[float] = None
    azimuthDirection: Optional[Angle] = None
    elevationDirection: Optional[Angle] = None


class Field2DRelativeLocation(ExtraBaseModel):
    semiMinor: Optional[Uncertainty] = None
    semiMajor: Optional[Uncertainty] = None
    orientationAngle: Optional[Angle] = None


class Field3DRelativeLocation(ExtraBaseModel):
    semiMinor: Optional[Uncertainty] = None
    semiMajor: Optional[Uncertainty] = None
    verticalUncertainty: Optional[Uncertainty] = None
    orientationAngle: Optional[Angle] = None


class UpCumEvtRep(ExtraBaseModel):
    upLocRepStat: Optional[Uinteger] = None


class LocationInfo(ExtraBaseModel):
    ageOfLocationInfo: Optional[DurationMin] = None
    cellId: Optional[str] = Field(
        None,
        description="Indicates the Cell Global Identification of the user which identifies the cell the UE is registered.\n",
    )
    enodeBId: Optional[str] = Field(
        None, description="Indicates the eNodeB in which the UE is currently located."
    )
    routingAreaId: Optional[str] = Field(
        None,
        description="Identifies the Routing Area Identity of the user where the UE is located.",
    )
    trackingAreaId: Optional[str] = Field(
        None,
        description="Identifies the Tracking Area Identity of the user where the UE is located.",
    )
    plmnId: Optional[str] = Field(
        None,
        description="Identifies the PLMN Identity of the user where the UE is located.",
    )
    twanId: Optional[str] = Field(
        None,
        description="Identifies the TWAN Identity of the user where the UE is located.",
    )
    userLocation: Optional[UserLocation] = None
    geographicArea: Optional[GeographicArea] = None
    civicAddress: Optional[CivicAddress] = None
    positionMethod: Optional[PositioningMethod] = None
    qosFulfilInd: Optional[AccuracyFulfilmentIndicator] = None
    ueVelocity: Optional[VelocityEstimate] = None
    ldrType: Optional[LdrType] = None
    achievedQos: Optional[MinorLocationQoS] = None
    relAppLayerId: Optional[ApplicationlayerId] = None
    rangeDirection: Optional[RangeDirection] = None
    twoDRelLoc: Optional[Field2DRelativeLocation] = None
    threeDRelLoc: Optional[Field3DRelativeLocation] = None
    relVelocity: Optional[VelocityEstimate] = None
    upCumEvtRep: Optional[UpCumEvtRep] = None


class MonitoringType(str, Enum):
    locationReporting = "LOCATION_REPORTING"
    lossOfConnectivity = "LOSS_OF_CONNECTIVITY"
    ueReachability = "UE_REACHABILITY"


class ReachabilityType(str, Enum):
    sms = "SMS"
    data = "DATA"


class AssociationTypeModel(Enum):
    IMEI = "IMEI"
    IMEISV = "IMEISV"


class PduSessionInformation(ExtraBaseModel):
    snssai: Snssai
    dnn: Dnn
    ueIpv4: Optional[Ipv4Addr] = None
    ueIpv6: Optional[Ipv6Prefix] = None
    ipDomain: Optional[str] = None
    ueMac: Optional[MacAddr48] = None


class IdleStatusInfo(ExtraBaseModel):
    activeTime: Optional[DurationSecModel] = None
    edrxCycleLength: Optional[confloat(ge=0.0)] = None
    suggestedNumberOfDlPackets: Optional[conint(ge=0)] = Field(
        None,
        description='Identifies the number of packets shall be buffered in the serving gateway. It shall be present if the idle status indication is requested by the SCS/AS with "idleStatusIndication" in the "monitoringEventSubscription" sets to "true".',
    )
    idleStatusTimestamp: Optional[datetime] = None
    periodicAUTimer: Optional[DurationSecModel] = None


class LocationFailureCause(Enum):
    POSITIONING_DENIED = "POSITIONING_DENIED"
    UNSUPPORTED_BY_UE = "UNSUPPORTED_BY_UE"
    NOT_REGISTED_UE = "NOT_REGISTED_UE"
    UNSPECIFIED = "UNSPECIFIED"
    REQUESTED_AREA_NOT_ALLOWED = "REQUESTED_AREA_NOT_ALLOWED"


class UePerLocationReport(ExtraBaseModel):
    ueCount: conint(ge=0) = Field(..., description="Identifies the number of UEs.")
    externalIds: Optional[List[ExternalId]] = Field(
        None, description="Each element uniquely identifies a user.", min_items=1
    )
    msisdns: Optional[List[Msisdn]] = Field(
        None,
        description="Each element identifies the MS internal PSTN/ISDN number allocated for a UE.",
        min_items=1,
    )
    servLevelDevIds: Optional[List[str]] = Field(
        None, description="Each element uniquely identifies a UAV.", min_items=1
    )


class FailureCauseModel(ExtraBaseModel):
    bssgpCause: Optional[int] = Field(
        None,
        description="Identifies a non-transparent copy of the BSSGP cause code. Refer to 3GPP TS 29.128.",
    )
    causeType: Optional[int] = Field(
        None,
        description="Identify the type of the S1AP-Cause. Refer to 3GPP TS 29.128.",
    )
    gmmCause: Optional[int] = Field(
        None,
        description="Identifies a non-transparent copy of the GMM cause code. Refer to 3GPP TS 29.128.",
    )
    ranapCause: Optional[int] = Field(
        None,
        description="Identifies a non-transparent copy of the RANAP cause code. Refer to 3GPP TS 29.128.",
    )
    ranNasCause: Optional[str] = Field(
        None,
        description="Indicates RAN and/or NAS release cause code information, TWAN release cause code information or untrusted WLAN release cause code information. Refer to 3GPP TS 29.214.",
    )
    s1ApCause: Optional[int] = Field(
        None,
        description="Identifies a non-transparent copy of the S1AP cause code. Refer to 3GPP TS 29.128.",
    )
    smCause: Optional[int] = Field(
        None,
        description="Identifies a non-transparent copy of the SM cause code. Refer to 3GPP TS 29.128.",
    )


class PdnConnectionStatus(Enum):
    CREATED = "CREATED"
    RELEASED = "RELEASED"


class PdnType(Enum):
    IPV4 = "IPV4"
    IPV6 = "IPV6"
    IPV4V6 = "IPV4V6"
    NON_IP = "NON_IP"
    ETHERNET = "ETHERNET"


class InterfaceIndication(Enum):
    EXPOSURE_FUNCTION = "EXPOSURE_FUNCTION"
    PDN_GATEWAY = "PDN_GATEWAY"


class PdnConnectionInformation(ExtraBaseModel):
    status: PdnConnectionStatus
    apn: Optional[str] = Field(
        None,
        description="Identify the APN, it is depending on the SCEF local configuration whether or not this attribute is sent to the SCS/AS.",
    )
    pdnType: PdnType
    interfaceInd: Optional[InterfaceIndication] = None
    ipv4Addr: Optional[Ipv4AddrModel] = None
    ipv6Addrs: Optional[List[Ipv6AddrModel]] = Field(None, min_items=1)
    macAddrs: Optional[List[MacAddr48]] = Field(None, min_items=1)


class DlDataDeliveryStatus(Enum):
    BUFFERED = "BUFFERED"
    TRANSMITTED = "TRANSMITTED"
    DISCARDED = "DISCARDED"


class DddTrafficDescriptor(ExtraBaseModel):
    ipv4Addr: Optional[Ipv4Addr] = None
    ipv6Addr: Optional[Ipv6Addr] = None
    portNumber: Optional[Uinteger] = None
    macAddr: Optional[MacAddr48] = None


class ApiCapabilityInfo(ExtraBaseModel):
    apiName: str
    suppFeat: SupportedFeatures


class SACInfo(ExtraBaseModel):
    numericValNumUes: Optional[int] = None
    numericValNumPduSess: Optional[int] = None
    percValueNumUes: Optional[conint(ge=0, le=100)] = None
    percValueNumPduSess: Optional[conint(ge=0, le=100)] = None
    uesWithPduSessionInd: Optional[bool] = False


class SACEventStatus(ExtraBaseModel):
    reachedNumUes: Optional[SACInfo] = None
    reachedNumPduSess: Optional[SACInfo] = None


class GroupMembListChanges(ExtraBaseModel):
    addedUEs: Optional[List[Gpsi]] = Field(None, min_items=1)
    removedUEs: Optional[List[Gpsi]] = Field(None, min_items=1)


class TrafficInformation(ExtraBaseModel):
    uplinkRate: Optional[BitRate] = None
    downlinkRate: Optional[BitRate] = None
    uplinkVolume: Optional[Volume] = None
    downlinkVolume: Optional[Volume] = None
    totalVolume: Optional[Volume] = None


class MonitoringEventReport(ExtraBaseModel):
    imeiChange: Optional[AssociationTypeModel] = None
    externalId: Optional[ExternalId] = None
    appId: Optional[ApplicationId] = None
    pduSessInfo: Optional[PduSessionInformation] = None
    idleStatusInfo: Optional[IdleStatusInfo] = None
    locationInfo: Optional[LocationInfo] = None
    locFailureCause: Optional[LocationFailureCause] = None
    lossOfConnectReason: Optional[int] = Field(
        None,
        description='If "monitoringType" is "LOSS_OF_CONNECTIVITY", this parameter shall be included if available to identify the reason why loss of connectivity is reported. Refer to 3GPP TS 29.336 clause 8.4.58.',
    )
    unavailPerDur: Optional[DurationSecModel] = None
    maxUEAvailabilityTime: Optional[datetime] = None
    msisdn: Optional[Msisdn] = None
    monitoringType: MonitoringType
    uePerLocationReport: Optional[UePerLocationReport] = None
    plmnId: Optional[PlmnId] = None
    reachabilityType: Optional[ReachabilityType] = None
    roamingStatus: Optional[bool] = Field(
        None,
        description='If "monitoringType" is "ROAMING_STATUS", this parameter shall be set to "true" if the new serving PLMN is different from the HPLMN. Set to false or omitted otherwise.',
    )
    failureCause: Optional[FailureCauseModel] = None
    eventTime: Optional[datetime] = None
    pdnConnInfoList: Optional[List[PdnConnectionInformation]] = Field(None, min_items=1)
    dddStatus: Optional[DlDataDeliveryStatus] = None
    dddTrafDescriptor: Optional[DddTrafficDescriptor] = None
    maxWaitTime: Optional[datetime] = None
    apiCaps: Optional[List[ApiCapabilityInfo]] = Field(None, min_items=0)
    nSStatusInfo: Optional[SACEventStatus] = None
    afServiceId: Optional[str] = None
    servLevelDevId: Optional[str] = Field(
        None,
        description='If "monitoringType" is "AREA_OF_INTEREST", this parameter may be included to identify the UAV.',
    )
    uavPresInd: Optional[bool] = Field(
        None,
        description='If "monitoringType" is "AREA_OF_INTEREST", this parameter shall be set to true if the specified UAV is in the monitoring area. Set to false or omitted otherwise.',
    )
    groupMembListChanges: Optional[GroupMembListChanges] = None
    sessInactiveTime: Optional[DurationSecModel] = None
    trafficInfo: Optional[TrafficInformation] = None


class MonitoringEventSubscriptionCreate(ExtraBaseModel):
    # mtcProviderId: Optional[str] = Field(None, description="Identifies the MTC Service Provider and/or MTC Application")
    externalId: Optional[str] = Field(
        "123456789@domain.com",
        description="Globally unique identifier containing a Domain Identifier and a Local Identifier. \<Local Identifier\>@\<Domain Identifier\>",
    )
    msisdn: Optional[str] = Field(
        "918369110173",
        description="Mobile Subscriber ISDN number that consists of Country Code, National Destination Code and Subscriber Number.",
    )
    # externalGroupId: Optional[str] = Field("Group1@domain.com", description="Identifies a group made up of one or more subscriptions associated to a group of IMSIs, containing a Domain Identifier and a Local Identifier. \<Local Identifier\>@\<Domain Identifier\>")
    # addExtGroupIds: Optional[str] = None
    # Remember, when you actually trying to access the database through CRUD methods you need to typecast the pydantic types to strings, int etc.
    # ipv4Addr: Optional[IPvAnyAddress] = Field(None, description="String identifying an Ipv4 address")
    # ipv6Addr: Optional[IPvAnyAddress] = Field("0:0:0:0:0:0:0:1", description="String identifying an Ipv6 address. Default value ::1/128 (loopback)")
    notificationDestination: AnyHttpUrl = Field(
        "http://localhost:80/api/v1/utils/monitoring/callback",
        description="Reference resource (URL) identifying service consumer's endpoint, in order to receive the asynchronous notification.",
    )  # Default value for development testing
    monitoringType: MonitoringType
    maximumNumberOfReports: Optional[int] = Field(
        None,
        description="Identifies the maximum number of event reports to be generated. Value 1 makes the Monitoring Request a One-time Request",
        ge=1,
    )
    monitorExpireTime: Optional[datetime] = Field(
        None,
        description="Identifies the absolute time at which the related monitoring event request is considered to expire",
    )
    maximumDetectionTime: Optional[int] = Field(
        1,
        description='If monitoringType is "LOSS_OF_CONNECTIVITY", this parameter may be included to identify the maximum period of time after which the UE is considered to be unreachable.',
        gt=0,
    )
    reachabilityType: Optional[ReachabilityType] = Field(
        "DATA",
        description='If monitoringType is "UE_REACHABILITY", this parameter shall be included to identify whether the request is for "Reachability for SMS" or "Reachability for Data"',
    )


class MonitoringEventSubscription(MonitoringEventSubscriptionCreate):
    link: Optional[AnyHttpUrl] = Field(
        "https://myresource.com",
        description="String identifying a referenced resource. This is also returned as a location header in 201 Created Response",
    )
    ipv4Addr: Optional[IPvAnyAddress] = Field(
        None, description="String identifying an Ipv4 address"
    )

    class Config:
        orm_mode = True


class ResultReason(Enum):
    ROAMING_NOT_ALLOWED = "ROAMING_NOT_ALLOWED"
    OTHER_REASON = "OTHER_REASON"


class ConfigResult(ExtraBaseModel):
    externalIds: Optional[List[ExternalId]] = Field(
        ...,
        description="Each element indicates an external identifier of the UE.",
        min_items=1,
    )
    msisdns: Optional[List[Msisdn]] = Field(
        None,
        description="Each element identifies the MS internal PSTN/ISDN number allocated for the UE.",
        min_items=1,
    )
    resultReason: ResultReason


class AppliedParameterConfiguration(ExtraBaseModel):
    externalIds: Optional[List[ExternalId]] = Field(
        None, description="Each element uniquely identifies a user.", min_items=1
    )
    msisdns: Optional[List[Msisdn]] = Field(
        None,
        description="Each element identifies the MS internal PSTN/ISDN number allocated for a UE.",
        min_items=1,
    )
    maximumLatency: Optional[DurationSecModel] = None
    maximumResponseTime: Optional[DurationSecModel] = None
    maximumDetectionTime: Optional[DurationSecModel] = None


class MonitoringNotification(ExtraBaseModel):
    subscription: AnyHttpUrl
    configResults: Optional[List[ConfigResult]] = Field(
        None,
        description="Each element identifies a notification of grouping configuration result.",
        min_items=1,
    )
    monitoringEventReports: Optional[List[MonitoringEventReport]] = Field(
        None, description="Monitoring event reports.", min_items=1
    )
    addedExternalIds: Optional[List[ExternalId]] = Field(
        None,
        description='Identifies the added external Identifier(s) within the active group via the "externalGroupId" attribute within the MonitoringEventSubscription data type.',
        min_items=1,
    )
    addedMsisdns: Optional[List[Msisdn]] = Field(
        None,
        description='Identifies the added MSISDN(s) within the active group via the "externalGroupId" attribute within the MonitoringEventSubscription data type.',
        min_items=1,
    )
    cancelExternalIds: Optional[List[ExternalId]] = Field(
        None,
        description='Identifies the cancelled external Identifier(s) within the active group via the "externalGroupId" attribute within the MonitoringEventSubscription data type.',
        min_items=1,
    )
    cancelMsisdns: Optional[List[Msisdn]] = Field(
        None,
        description='Identifies the cancelled MSISDN(s) within the active group via the "externalGroupId" attribute within the MonitoringEventSubscription data type.',
        min_items=1,
    )
    cancelInd: Optional[bool] = Field(
        None,
        description="Indicates whether to request to cancel the corresponding monitoring subscription. Set to false or omitted otherwise.",
    )
    appliedParam: Optional[AppliedParameterConfiguration] = None


class MonitoringEventReportReceived(ExtraBaseModel):
    ok: bool
