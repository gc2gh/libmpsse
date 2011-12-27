import pylibmpsse as _mpsse

MPSSE_OK = _mpsse.MPSSE_OK
MPSSE_FAIL = _mpsse.MPSSE_FAIL
	
MSB = _mpsse.MSB
LSB = _mpsse.LSB

SPI0 = _mpsse.SPI0
SPI1 = _mpsse.SPI1
SPI2 = _mpsse.SPI2
SPI3 = _mpsse.SPI3
I2C = _mpsse.I2C

IFACE_ANY = _mpsse.IFACE_ANY
IFACE_A = _mpsse.IFACE_A
IFACE_B = _mpsse.IFACE_B
IFACE_C = _mpsse.IFACE_C
IFACE_D = _mpsse.IFACE_D

ONE_HUNDRED_KHZ = _mpsse.ONE_HUNDRED_KHZ
FOUR_HUNDRED_KHZ = _mpsse.FOUR_HUNDRED_KHZ
ONE_MHZ = _mpsse.ONE_MHZ
TWO_MHZ = _mpsse.TWO_MHZ
FIVE_MHZ = _mpsse.FIVE_MHZ
SIX_MHZ = _mpsse.SIX_MHZ
TEN_MHZ = _mpsse.TEN_MHZ
TWELVE_MHZ = _mpsse.TWELVE_MHZ
THIRY_MHZ = _mpsse.THIRTY_MHZ

class MPSSE:
	"""
	Python class wrapper for libmpsse.
	"""

	def __init__(self, mode=None, frequency=None, endianess=MSB):
		"""
		If mode and frequency are specified, then attempt to connect to any known FTDI chip. If this fails, an exception will be thrown.
		If mode and frequency are not specified, this simply returns the class instance.
		Endianess defaults to MSB.
		"""
		self.context = None
		if mode is not None and frequency is not None:
			self.context = _mpsse.MPSSE(mode, frequency, endianess)
			if self.context.open == 0:
				raise Exception, self.ErrorString()

	def Open(self, vid, pid, mode, frequency, endianess=MSB, interface=IFACE_A, serial=None):
		"""
		Opens the specified USB device. If this fails, an exception will be thrown.
		Endianess defaults to MSB; interface defaults to IFACE_A; serial defaults to None.
		"""
		self.context = _mpsse.Open(vid, pid, serial, interface, mode, frequency, endianess)
		if self.context.open == 0:
			raise Exception, self.ErrorString()
		return MPSSE_OK

	def Close(self):
		"""
		Closes the device, deinitializes libftdi, and frees the libmpsse context.
		"""
		retval = _mpsse.Close(self.context)
		self.context = None
		return retval
	
	def ErrorString(self):
		"""
		Returns the last libftdi error string.
		"""
		return _mpsse.ErrorString(self.context)

	def SetMode(self, mode, endianess):
		"""
		Sets the appropriate transmit and receive commands based on the requested mode and byte order.
		Called internally by __init__ and Open.
		"""
		return _mpsse.SetMode(self.context, mode, endianess)

	def SetClock(self, frequency):
		"""
		Sets the appropriate divisor for the desired clock frequency. Frequency must be specified in hertz.
		Called internally by __init__ and Open.
		"""
		return _mpsse.SetClock(self.context, frequency)

	def GetClock(self):
		"""
		Gets the currently configured clock rate.
		"""
		return _mpsse.GetClock(self.context)

	def GetVid(self):
		"""
		Returns the vendor ID of the FTDI chip.
		"""
		return _mpsse.GetVid(self.context)

	def GetPid(self):
		"""
		Returns the product ID of the FTDI chip.
		"""
		return _mpsse.GetPid(self.context)

	def GetDescription(self):
		"""
		Returns the description of the FTDI chip, if any. 
		This will only be populated if __init__ is used to open the device.
		"""
		return _mpsse.GetDescription(self.context)

	def SetLoopback(self, enable):
		"""
		Enable / disable internal loopback. Loopback is disabled by default.
		Set enable = 1 to enable, enable = 0 to disable.
		"""
		return _mpsse.SetLoopback(self.context, enable)

	def SetCSIdle(self, idle):
		"""
		Sets the idle state of the chip select pin. CS idles high by default.
		Only appropriate when using one of the SPI modes.
		Set idle = 1 to idle high, idle = 0 to idle low.
		"""
		return _mpsse.SetCSIdle(self.context, idle)

	def Start(self):
		"""
		Send data start condition.
		"""
		return _mpsse.Start(self.context)

	def Stop(self):
		"""
		Send data stop condition.
		"""
		return _mpsse.Stop(self.context)

	def Write(self, data):
		"""
		Send data (string) out via the selected serial protocol.
		"""
		return _mpsse.Write(self.context, data)

	def Read(self, size):
		"""
		Reads size bytes of data over the selected serial protocol.
		"""
		return _mpsse.Read(self.context, size)

	def SetAck(self, ack):
		"""
		Sets the transmitted ACK bit. ACKs are sent by default.
		Set ack = 1 to send ACKs, ack = 0 to send NACKs.
		"""
		return _mpsse.SetAck(self.context, ack)

	def GetAck(self):
		"""
		Returns the last received ACK bit.
		Returns 0 for ACK, 1 for NACK.
		"""
		return _mpsse.GetAck(self.context)

	def PinHigh(self, pin):
		"""
		Sets the specified GPIO pin high.
		The pin can be GPIO pin 0 - 11.
		"""
		return _mpsse.PinHigh(self.context, pin)

	def PinLow(self, pin):
		"""
		Sets the specified GPIO pin low.
		The Pin can be GPIO pin 0 - 11.
		"""
		return _mpsse.PinLow(self.context, pin)
