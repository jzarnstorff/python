#!/usr/bin/python3
# -*- coding: utf-8 -*-
import smbus
import enum


# ----------------------------------
#|   Address Code    | Slave Address|
# ----------------------------------
#| A6 | A5 | A4 | A3 | A2 | A1 | A0 |
#|  0 |  0 |  1 |  1 |  x |  x |  x |
# ----------------------------------


class reg(enum.IntEnum):
    """An enumeration for the pointer register for MCP9808 device"""
    Reserved    = 0x00
    Config      = 0x01
    Alert_Upper = 0x02
    Alert_Lower = 0x03
    Critical    = 0x04
    Temp        = 0x05
    MfgId       = 0x06
    DevId       = 0x07
    Resolution  = 0x08


class MCP9808():

    def __init__(self, dev_addr, i2c_bus=1):
        """Initialize an smbus object on a specified I2C bus, and store the
        I2C address for the desired MCP9808 temperature sensor. The default 
        I2C bus for the Raspberry Pi is 1."""

        self.bus = smbus.SMBus(i2c_bus)
        self.addr = dev_addr


    def read_byte(self, register):
        """Returns one byte from specified register passed into method"""
        return self.bus.read_byte_data(self.addr, register)


    def write_byte(self, register, value):
        """Writes one byte to specified register passed into method"""
        return self.bus.write_byte_data(self.addr, register, value)


    def read_word(self, register):
        """Returns 16 bit word from specified register passed into method"""
        return self.bus.read_word_data(self.addr, register)


    def write_word(self, register, value):
        """Writes a 16 bit word to specified register passed into method"""
        return self.bus.write_word_data(self.addr, register, value)


    def byte_split_16(self, word):
        """The word read when using smbus returns the MSB and LSB swapped. 
        Return most significant byte and the least significant byte"""
        return (word & 0x00FF), ((word & 0xFF00) >> 8)


    def get_temperature(self):
        """Calculates and returns temperature as float in Celsius"""

        """Read word from temp reg and split word"""
        self.temp = self.read_word(reg.Temp)
        self.MSB, self.LSB = self.byte_split_16(self.temp)

        """Check the T_CRIT, T_UPPER, and T_LOWER flags"""
        #if(upper_byte & 0x80):
            #print('T_CRIT')
        #if(upper_byte & 0x40):
            #print('T_UPPER')
        #if(upper_byte & 0x20):
            #print('T_LOWER')

        """Clear T_CRIT, T_UPPER, and T_LOWER flags"""
        self.MSB &= 0x1F 

        """Calculate the temperature"""
        if(self.MSB & 0x10): # Temp < 0°C
            self.MSB &= 0x0F # Clear sign bit
            return (256 - ((self.MSB * 16) + (self.LSB / 16)))
        else:                # Temp >= 0°C
            return ((self.MSB * 16) + (self.LSB / 16))

