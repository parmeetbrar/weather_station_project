import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)

# Configure BME280
spi.max_speed_hz = 1000000  # Set the SPI speed for BME280
spi.mode = 0b00  # SPI mode 0

# Set the CS pin for BME280
bme280_cs = 0
GPIO.setup(bme280_cs, GPIO.OUT)

# Configure MCP3008
spi.max_speed_hz = 1000000  # Set the SPI speed for MCP3008
spi.mode = 0b01  # SPI mode 1

# Set the CS pin for MCP3008
mcp3008_cs = 1
GPIO.setup(mcp3008_cs, GPIO.OUT)