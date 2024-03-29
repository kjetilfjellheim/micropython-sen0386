from sys import maxsize
import ustruct

PACKET_HEADER = 0x55
ACC_PACKET_HEADER = 0x51
ANGVEL_PACKET_HEADER = 0x52
ANG_PACKET = 0x53
ACCPACKET_BUFFER_START = 0
ACCPACKET_BUFFER_END = 10
ANGVELPACKET_BUFFER_START = 11
ANGVELPACKET_BUFFER_END = 21
ANGPACKET_BUFFER_START = 22
ANGPACKET_BUFFER_END = 32
BUFFER_SIZE = 44
PACKET_LENGTH = 10
BYTE_PACKET_HEADER = 0
BYTE_PACKET_TYPE = 1
BYTE_AXL_DATA_CONTENT = 2
BYTE_AXH_DATA_CONTENT = 3
BYTE_AYL_DATA_CONTENT = 4
BYTE_AYH_DATA_CONTENT = 5
BYTE_AZL_DATA_CONTENT = 6
BYTE_AZH_DATA_CONTENT = 7
BYTE_WXL_DATA_CONTENT = 2
BYTE_WXH_DATA_CONTENT = 3
BYTE_WYL_DATA_CONTENT = 4
BYTE_WYH_DATA_CONTENT = 5
BYTE_WZL_DATA_CONTENT = 6
BYTE_WZH_DATA_CONTENT = 7
BYTE_ROLLL_DATA_CONTENT = 2
BYTE_ROLLH_DATA_CONTENT = 3
BYTE_PITCHL_DATA_CONTENT = 4
BYTE_PITCHH_DATA_CONTENT = 5
BYTE_YAWL_DATA_CONTENT = 6
BYTE_YAWH_DATA_CONTENT = 7
MAX_16_BIT_INTEGER_SIZE = 32768.00
GRAVITY_CONSTANT = 9.81
CALCULATION_GRAVITY_CONSTANT = GRAVITY_CONSTANT * 16.00
CALCULATION_ROTATION_CONSTANT = 2000.00
CALCULATION_ANGLE_CONSTANT = 180.00

UNDEFINED = maxsize

def convertShort(packet, highByte, lowByte):
    b = bytearray(2)
    b[0] = packet[highByte]
    b[1] = packet[lowByte]
    result = ustruct.unpack(">h", b)[0]
    return result

def handleAccPacket(accPacketData):
    if len(accPacketData) == PACKET_LENGTH and accPacketData[BYTE_PACKET_HEADER] is PACKET_HEADER and accPacketData[BYTE_PACKET_TYPE] is ACC_PACKET_HEADER:
        ax = (CALCULATION_GRAVITY_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(accPacketData, BYTE_AXH_DATA_CONTENT, BYTE_AXL_DATA_CONTENT)
        ay = (CALCULATION_GRAVITY_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(accPacketData, BYTE_AYH_DATA_CONTENT, BYTE_AYL_DATA_CONTENT)
        az = (CALCULATION_GRAVITY_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(accPacketData, BYTE_AZH_DATA_CONTENT, BYTE_AZL_DATA_CONTENT)
        return ax, ay, az
    else:
        return UNDEFINED, UNDEFINED ,UNDEFINED

def handleAngVelPacket(angVelPacketData):
    if len(angVelPacketData) == PACKET_LENGTH and angVelPacketData[BYTE_PACKET_HEADER] is PACKET_HEADER and angVelPacketData[BYTE_PACKET_TYPE] is ANGVEL_PACKET_HEADER:
        wx = (CALCULATION_ROTATION_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(angVelPacketData, BYTE_WXH_DATA_CONTENT, BYTE_WXL_DATA_CONTENT)
        wy = (CALCULATION_ROTATION_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(angVelPacketData, BYTE_WYH_DATA_CONTENT, BYTE_WYL_DATA_CONTENT)
        wz = (CALCULATION_ROTATION_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(angVelPacketData, BYTE_WZH_DATA_CONTENT, BYTE_WZL_DATA_CONTENT)
        return wx, wy, wz
    else:
        return UNDEFINED, UNDEFINED , UNDEFINED

def handleAngPacket(angPacketData):
    if len(angPacketData) == PACKET_LENGTH and angPacketData[BYTE_PACKET_HEADER] is PACKET_HEADER and angPacketData[BYTE_PACKET_TYPE] is ANG_PACKET:
        roll = (CALCULATION_ANGLE_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(angPacketData, BYTE_ROLLH_DATA_CONTENT, BYTE_ROLLL_DATA_CONTENT)
        pitch = (CALCULATION_ANGLE_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(angPacketData, BYTE_PITCHH_DATA_CONTENT, BYTE_PITCHL_DATA_CONTENT)
        yaw = (CALCULATION_ANGLE_CONSTANT / MAX_16_BIT_INTEGER_SIZE) * convertShort(angPacketData, BYTE_YAWH_DATA_CONTENT, BYTE_YAWL_DATA_CONTENT)
        return roll, pitch, yaw
    return UNDEFINED, UNDEFINED, UNDEFINED

def handlePackets(accPacketData, angVelPacketData, angPacketData):
    ax, ay, az = handleAccPacket(accPacketData)
    wx, wy, wz = handleAngVelPacket(angVelPacketData)
    roll, pitch, yaw = handleAngPacket(angPacketData)
    return ax, ay, az, wx, wy, wz, roll, pitch, yaw

def readSensorValues(uart):
    data = uart.read(BUFFER_SIZE)
    if data is not None and len(data) == BUFFER_SIZE:
        accPacket = data[ACCPACKET_BUFFER_START:ACCPACKET_BUFFER_END]
        angVelPacket = data[ANGVELPACKET_BUFFER_START:ANGVELPACKET_BUFFER_END]
        angPacket = data[ANGPACKET_BUFFER_START:ANGPACKET_BUFFER_END]
        ax, ay, az, wx, wy, wz, roll, pitch, yaw = handlePackets(accPacket, angVelPacket, angPacket)
        return ax, ay, az, wx, wy, wz, roll, pitch, yaw
    else:
        return UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED
