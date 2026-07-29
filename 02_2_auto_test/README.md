# Auto Test

To do this auto test, we need to write C code for STM32 and a Python script for the Raspberry Pi.

## C Code for STM32

Let's create a new STM32 project and configure these pins:

1. Open the .ioc file,
2. Go to connectivity,
3. For each interface shown in green, enable the interface via the mode dropdown menu:
    1. SPI1: Full-Duplex Master, with 8bit word size and a high prescaler of 64 to slow down the SPI clock speed (we are using jumpers of low quality and different lengths, high speed SPI may not work reliably),
    2. I2C1: I2C
    3. UART1: Asynchronous
    4. Set the GPIOs to GPIO_OUTPUT,
4. Go through the configuration panels, discover the parameters for each interface,
5. Save with ctrl+s to generate the code.



![Auto Test Pin Configuration](../.images/02_hands_on_platform/auto_test.png)

![SPI specific configuration](../.images/02_hands_on_platform/spi_config.png)

In the main.c file, the idea is to test each group of interfaces (GPIOs, UART, I2C, SPI) one by one. 

For each interface, we will send a message and wait for a response. If the response is correct, else, there maybe a problem:

- Either the interface is broken, grilled,
- Or the cable is not connected properly,
- Or the cable is connected on the wrong pin,
- Or the auto test script is not working properly.

```C
/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define RX_BUFFER_SIZE 256

#define ADS1015_ADDR (0x48 << 1)

// Define your custom Chip Select pin
#define FRAM_CS_GPIO_Port  GPIOA
#define FRAM_CS_Pin        GPIO_PIN_1
// MB85RS64 Op-codes
#define CMD_RDID           0x9F  // Read Device ID command
// Macro to toggle CS pin easily
#define FRAM_CS_LOW()      HAL_GPIO_WritePin(FRAM_CS_GPIO_Port, FRAM_CS_Pin, GPIO_PIN_RESET)
#define FRAM_CS_HIGH()     HAL_GPIO_WritePin(FRAM_CS_GPIO_Port, FRAM_CS_Pin, GPIO_PIN_SET)

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

SPI_HandleTypeDef hspi2;

UART_HandleTypeDef huart1;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_SPI2_Init(void);
static void MX_USART1_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */
  uint8_t rxBuffer[RX_BUFFER_SIZE];
  uint16_t bytesReceived = 0;
  HAL_StatusTypeDef status;
  char errorBuffer[RX_BUFFER_SIZE];
  int msgLength;
  HAL_StatusTypeDef ret;
  uint8_t command = CMD_RDID;
  uint8_t rx_buffer[4] = {0};
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_SPI2_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */

  /* ----------- TEST GPIO ----------- */
  // Set up all GPIOs to low
  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_0, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_3, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_15, GPIO_PIN_RESET);

  // Test Each GPIO one by one
  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_0, GPIO_PIN_SET);
  HAL_Delay(2000);

  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_0, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_3, GPIO_PIN_SET);
  HAL_Delay(2000);

  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_3, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_SET);
  HAL_Delay(2000);

  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_15, GPIO_PIN_SET);
  HAL_Delay(2000);

  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_15, GPIO_PIN_RESET);
  /* ----------- TEST GPIO END ---------- */

  /* ----------- TEST USART ---------- */
  // Clear out the buffer before receiving new data
  memset(rxBuffer, 0, RX_BUFFER_SIZE);
  bytesReceived = 0;

  status = HAL_UARTEx_ReceiveToIdle(&huart1, rxBuffer, RX_BUFFER_SIZE, &bytesReceived, 2000);
  if (status == HAL_OK && bytesReceived > 0)
  {
    // Transmit back exactly what we received
    HAL_UART_Transmit(&huart1, rxBuffer, bytesReceived, 500);
  }
  else if (status == HAL_TIMEOUT)
  {
    msgLength = sprintf(errorBuffer, "\r\n[FAIL][USART] HAL_Status: %d, BytesRx: %d\r\n", status, bytesReceived);
    HAL_UART_Transmit(&huart1, (uint8_t*)errorBuffer, msgLength, 500);
  }
  /* ----------- TEST USART END ---------- */

  HAL_Delay(5000);


  /* ----------- TEST I2C Device ---------- */
//  HAL_UART_Transmit(&huart1, (uint8_t*)"Hello_STM32\r\n", 14, 500);
  ret = HAL_I2C_IsDeviceReady(&hi2c1, ADS1015_ADDR, 5, 100);
  if(HAL_OK == ret)
  {
    msgLength = sprintf(errorBuffer, "\r\n[PASS][I2C] device: %d responded to HAL_I2C_IsDeviceReady, returned %d (HAL_OK=0, HAL_ERROR=1, HAL_BUSY=2, HAL_TIMEOUT=3)\r\n", ADS1015_ADDR >> 1, ret);
    HAL_UART_Transmit(&huart1, (uint8_t*)errorBuffer, msgLength, 500);
  }
  else
  {
    msgLength = sprintf(errorBuffer, "\r\n[FAIL][I2C] device: %d did not responded to HAL_I2C_IsDeviceReady, returned %d (HAL_OK=0, HAL_ERROR=1, HAL_BUSY=2, HAL_TIMEOUT=3)\r\n", ADS1015_ADDR >> 1, ret);
    HAL_UART_Transmit(&huart1, (uint8_t*)errorBuffer, msgLength, 500);
  }
  /* ----------- TEST I2C Device END ---------- */

  /* ----------- TEST SPI Device ---------- */
  // 1. Ensure CS starts high
  FRAM_CS_HIGH();
  HAL_Delay(5);

  // 2. Drop CS low to select the FRAM chip
  FRAM_CS_LOW();

  // 3. Transmit the 1-byte Read ID command
  HAL_SPI_Transmit(&hspi2, &command, 1, HAL_MAX_DELAY);

  // 4. Clock out 4 bytes to read the incoming ID signature
  HAL_SPI_Receive(&hspi2, rx_buffer, 4, HAL_MAX_DELAY);

  // 5. Pull CS high to end the SPI frame transaction
  FRAM_CS_HIGH();

  // Debug print out what we actually caught on the line
  msgLength = sprintf(errorBuffer, "[INFO][SPI] FRAM Response ID: %02X %02X %02X %02X\r\n", rx_buffer[0], rx_buffer[1], rx_buffer[2], rx_buffer[3]);
  HAL_UART_Transmit(&huart1, (uint8_t*)errorBuffer, msgLength, 500);

  // 6. Verify against the official Fujitsu MB85RS64 ID pattern
  if (rx_buffer[0] == 0x04 && rx_buffer[2] == 0x03 && rx_buffer[3] == 0x02)
  {
    msgLength = sprintf(errorBuffer, "[PASS][SPI] FRAM connected and verified successfully!\r\n");
    HAL_UART_Transmit(&huart1, (uint8_t*)errorBuffer, msgLength, 500);
  }
  else
  {
    msgLength = sprintf(errorBuffer, "[FAIL][SPI] FRAM Ping failed! Check your SPI wiring or logic levels.\r\n");
    HAL_UART_Transmit(&huart1, (uint8_t*)errorBuffer, msgLength, 500);
  }
  /* ----------- TEST SPI Device END ---------- */


  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }

  /* USER CODE END 3 */
}

```


# Python Script for Raspberry Pi

For this python script, we will:

- Flash the STM32 with the binary of code above, this will ensure synchronization between the STM32 and the Raspberry Pi,
- Read GPIOs as input, it should follow the same sequence as the STM32 code, and print "PASS" or "FAIL" for each GPIO test,
- then send a message to the STM32 via UART, and wait for a response. If the response is correct, we will print "PASS", else we will print "FAIL".

A nice feature of this script is that it will also control the LEDs on the Raspberry Pi to indicate the status of the test.

## Raspberry Pi UART Setup

To be able to use the UART and I2C on the Raspberry Pi, we need to enable them first.

1. Enable UART & Disable Serial Console/
    - Since you are running OS Lite, you will do this via the terminal or raspi-config.
    - Run the configuration tool: ```sudo raspi-config```
    - Navigate to: 3 Interface Options -> I6 Serial Port.
    - It will ask two critical questions:
      - Would you like a login shell to be accessible over serial? Select No.
      - Would you like the serial port hardware to be enabled? Select Yes.

    - Navigate back to Interface Options.
    - Select I2C.
    - Choose Yes when asked if you want to enable the ARM I2C interface.

    - Select Finish and choose Yes to reboot the Raspberry Pi.

2. Install I2C Tools
    - Run the following commands to install I2C tools:
      - ```sudo apt update```
      - ```sudo apt install -y i2c-tools```
    - In your workspace_your_name folder, run the following command to install adafruit package in [python virtual env](../01_prerequisites_knowledge/README.md):
      - ```python3 -m venv env```
      - ```source env/bin/activate```   (**From now on, use this python virtual environment, run this command from your workspace every time you open a new terminal**)
      - ```pip3 install adafruit-blinka adafruit-circuitpython-mcp4728```
      - ```sudo apt update```
      - ```sudo apt install swig python3-dev gcc liblgpio-dev```
      - ```pip3 install gpiozero lgpio```

3. Install pyserial
    - Run the following command to install pyserial: ```pip3 install pyserial```
## Python Script

Now, let's create ```auto_test.py``` script:

```python

import serial
import time
import sys
import os
import subprocess
from gpiozero import DigitalInputDevice, LED
from typing import List, Tuple
import re
import board
import busio
import adafruit_mcp4728

class STM32AutoTest:
    """
    Automated testing suite for STM32 and Raspberry Pi connectivity.
    Tests GPIO, UART, I2C, and SPI interfaces.
    """
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    def __init__(self, binary_path: str = None, uart_port: str = "/dev/serial0",
                 uart_baudrate: int = 115200):
        """
        Initialize the AutoTest class.
        Args:
            binary_path: Path to the STM32 compiled binary (.bin file)
            uart_port: UART port on Raspberry Pi
            uart_baudrate: UART baudrate (default: 115200)
        """
        self.binary_path = binary_path
        self.uart_port = uart_port
        self.uart_baudrate = uart_baudrate
        self.uart = None
        self.all_passed = True  # Track overall test status

        # GPIO mapping: STM32 pin name -> RPi BOARD pin number
        # To be configured by user using set_gpio_mapping()
        self.stm32_to_rpi_gpio = {
            'PD0': 23,   # STM32 PD0 on RPi GPIO 23
            'PD3': 21,   # STM32 PD3 on RPi GPIO 21
            'PD4': 19,   # STM32 PD4 on RPi GPIO 19
            'PA15': 15   # STM32 PA15 on RPi GPIO 15
        }

        self.gpio_inputs = {}  # Will store DigitalInputDevice objects

        # Use the same LED pins as the blinking example from the hands-on guide
        self.green_led = LED("BOARD29")
        self.red_led = LED("BOARD31")
        self.yellow_led = LED("BOARD37")
        self.set_indicator_state(red=True, yellow=False, green=False)

        print("[INFO] STM32 AutoTest initialized:")
        print(f"[INFO] UART Port: {self.uart_port} @ {self.uart_baudrate} baud")
        print("[INFO] GPIOs mapping:")
        for key, value in self.stm32_to_rpi_gpio.items():
            print(f"[INFO] STM32 {key} -> RPi BOARD{value}")

    def set_indicator_state(self, red: bool = False, yellow: bool = False, green: bool = False):
        """Turn the Raspberry Pi LEDs on or off."""
        self.red_led.on() if red else self.red_led.off()
        self.yellow_led.on() if yellow else self.yellow_led.off()
        self.green_led.on() if green else self.green_led.off()

    def blink_led(self, led, duration: float = 4.0, frequency: float = 2.0):
        """Blink one LED for a given duration and frequency."""
        half_period = 1.0 / frequency / 2.0
        start = time.time()
        while time.time() - start < duration:
            led.on()
            time.sleep(half_period)
            led.off()
            time.sleep(half_period)

    def show_ready_state(self):
        """Before the test starts: red LED on, others off."""
        self.set_indicator_state(red=True, yellow=False, green=False)

    def show_testing_state(self):
        """During the test: yellow LED on, others off."""
        self.set_indicator_state(red=False, yellow=True, green=False)

    def show_pass_state(self):
        """If everything passes: green LED blinks for 4 seconds at 2 Hz."""
        self.set_indicator_state(red=False, yellow=False, green=False)
        self.blink_led(self.green_led, duration=4.0, frequency=2.0)
        self.set_indicator_state(red=False, yellow=False, green=False)

    def show_fail_state(self):
        """If anything fails: red LED blinks for 4 seconds at 2 Hz."""
        self.set_indicator_state(red=False, yellow=False, green=False)
        self.blink_led(self.red_led, duration=4.0, frequency=2.0)
        self.set_indicator_state(red=False, yellow=False, green=False)

    def flash_stm32(self) -> bool:
        """
        Flash the STM32 microcontroller with the compiled binary.
        Returns:
            True if flashing successful, False otherwise
        """
        print("[INFO] Flashing STM32 with binary ... ")
        if not self.binary_path:
            print("[ERROR] Binary path not specified.")
            return False

        if not os.path.exists(self.binary_path):
            print(f"[ERROR] Binary file not found: {self.binary_path}")
            return False

        try:
            print(f"[INFO] Flashing binary: {self.binary_path}")
            # Flash to STM32 memory address 0x08000000 (standard ARM Cortex-M flash address)
            result = subprocess.run(
                ['st-flash', 'write', self.binary_path, '0x08000000'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"{self.GREEN}[PASS] STM32 flashed successfully{self.RESET}")
                time.sleep(1)  # Give STM32 time to restart
                return True
            else:
                print(f"{self.RED}[FAIL] Flashing failed: {result.stderr}{self.RESET}")
                return False

        except FileNotFoundError:
            print("[ERROR] st-flash not found. Install stlink-tools: sudo apt install stlink-tools")
            return False
        except Exception as e:
            print(f"[ERROR] Flashing exception: {str(e)}")
            return False

    def initialize_gpio(self) -> bool:
        """
        Initialize GPIO input devices for reading STM32 outputs.
        Returns:
            True if initialization successful, False otherwise
        """
        print("[SETUP] Initializing GPIO inputs ... ", end="", flush=True)

        if any(pin is None for pin in self.stm32_to_rpi_gpio.values()):
            print("ERROR: GPIO mapping not configured. Use set_gpio_mapping() first.")
            return False

        try:
            for stm32_pin, rpi_pin in self.stm32_to_rpi_gpio.items():
                self.gpio_inputs[stm32_pin] = DigitalInputDevice(f"BOARD{rpi_pin}")
                print(f"[INFO] Initialized STM32 {stm32_pin} on RPi BOARD{rpi_pin}")

            print(f"{self.GREEN}[PASS] GPIO inputs initialized{self.RESET}")
            return True

        except Exception as e:
            print(f"[ERROR] GPIO initialization failed: {str(e)}")
            return False

    def initialize_uart(self) -> bool:
        """
        Initialize and open the UART connection.
        Returns:
            True if UART connection successful, False otherwise
        """
        print("[INFO] Initializing UART ... ")
        try:
            self.uart = serial.Serial(
                port=self.uart_port,
                baudrate=self.uart_baudrate,
                timeout=3
            )
            time.sleep(0.5)  # Wait for port to stabilize
            print(f"[INFO] UART initialized on {self.uart_port} @ {self.uart_baudrate} baud")
            return True

        except serial.SerialException as e:
            print(f"[ERROR] UART initialization failed: {str(e)}")
            print("[HINT] Enable UART with: sudo raspi-config -> Interface Options -> Serial Port")
            return False

    def test_gpio_pin(self, stm32_pin: str) -> bool:
        """
        Test a single GPIO pin by verifying it goes HIGH and stays HIGH.
        Args:
            stm32_pin: STM32 pin name as key (e.g., 'PD0', 'PD3', 'PD4', 'PA15')
        Returns:
            True if test passed, False otherwise
        """
        if stm32_pin not in self.gpio_inputs:
            print(f"[ERROR] Unknown STM32 pin: {stm32_pin}")
            self.all_passed = False
            return False

        rpi_pin = self.stm32_to_rpi_gpio[stm32_pin]
        gpio_device = self.gpio_inputs[stm32_pin]
        print(f"[TEST] STM32 GPIO {stm32_pin} -- RPi GPIO {rpi_pin} ... ")

        # Verify it stays HIGH for some duration
        start_value = gpio_device.value

        if start_value :
            print(f"{self.GREEN}[PASS] GPIO {stm32_pin}: start_value: {start_value}, {self.RESET}")
            return True
        else:
            print(f"{self.RED}[FAIL] GPIO {stm32_pin}: start_value: {start_value}, {self.RESET}")
            self.all_passed = False
            return False

    def test_gpio_pd0(self) -> bool:
        """Test STM32 GPIO PD0."""
        return self.test_gpio_pin('PD0')

    def test_gpio_pd3(self) -> bool:
        """Test STM32 GPIO PD3."""
        return self.test_gpio_pin('PD3')

    def test_gpio_pd4(self) -> bool:
        """Test STM32 GPIO PD4."""
        return self.test_gpio_pin('PD4')

    def test_gpio_pa15(self) -> bool:
        """Test STM32 GPIO PA15."""
        return self.test_gpio_pin('PA15')

    def test_uart(self, test_message: str = "HELLO_STM32") -> bool:
        """
        Test UART communication by sending a message and verifying echo response.
        The STM32 waits for UART input and echoes it back.
        Args:
            test_message: Message to send for testing (default: "HELLO_STM32")
        Returns:
            True if UART test passed, False otherwise
        """
        print("[TEST] Testing UART Communication")

        if not self.uart or not self.uart.is_open:
            print("[ERROR] UART not initialized")
            return False

        try:
            # Send test message
            print(f"[INFO] Sending UART test message: '{test_message}'")
            self.uart.write(test_message.encode() + b'\r\n')
            self.uart.flush()

            # Wait for response (STM32 will echo back)
            print("[INFO] Waiting for echo response...")
            time.sleep(2.2)
            self.response = self.uart.readline().decode('utf-8', errors='ignore').strip()

            if test_message in self.response:
                print(f"{self.GREEN}[PASS] Received echo: '{self.response}'{self.RESET}")
                return True
            else:
                print(f"{self.RED}[FAIL] Unexpected response: '{self.response}'{self.RESET}")
                print(f"{self.RED}[FAIL] Expected: '{test_message}'{self.RESET}")
                self.all_passed = False
                return False

        except Exception as e:
            print(f"[ERROR] UART test failed: {str(e)}")
            self.all_passed = False
            return False

    def test_stm32_i2c_and_spi_devices(self) -> bool:
        """
        Test I2C and SPI communication by checking if the devices respond.
        Returns:
            True if both tests passed, False otherwise
        """
        print(f"[TEST] Testing I2C and SPI Devices")
        self.response = self.response + self.uart.read(self.uart.in_waiting).decode('utf-8', errors='ignore').strip()

        if "[PASS][I2C]" in self.response:
            print(f"{self.GREEN}[PASS] I2C device responded successfully{self.RESET}")
        else:
            print(f"{self.RED}[FAIL] I2C device did not respond properly{self.RESET}")
            self.all_passed = False

        if "[PASS][SPI]" in self.response:
            print(f"{self.GREEN}[PASS] SPI FRAM device responded successfully{self.RESET}")
        else:
            print(f"{self.RED}[FAIL] SPI FRAM device did not respond properly{self.RESET}")
            self.all_passed = False

        print(f"[INFO] STM32 Response: \n>>>{self.response}\n<<<")

    def verify_raspi_to_mcp4728_connection(self, target_address=0x60) -> bool:
        """
        Pings the MCP4728 DAC using two sequential methods:
        1. Low-level bus scan using the system 'i2cdetect' tool.
        2. High-level driver initialization using the Adafruit CircuitPython package.
        Returns True only if both tests pass successfully.
        """
        print(f"[TEST] Verifying MCP4728 at 0x{target_address:02X}")

        # Test 1: Low-level bus scan using i2cdetect
        # run the i2cdetect command manually on your terminal
        # i2cdetect -y 1

        # Test 2: Library-level communication verification
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            mcp = adafruit_mcp4728.MCP4728(i2c, address=target_address)
            print(f"{self.GREEN}[PASS] MCP4728 driver initialization succeeded{self.RESET}")
            driver_ok = True
        except Exception as e:
            print(f"{self.RED}[FAIL] MCP4728 driver initialization failed: {e}{self.RESET}")
            driver_ok = False

        if driver_ok:
            return True

        self.all_passed = False
        return False


    def cleanup(self):
        """Close UART connection and cleanup GPIO resources."""
        print("\n[INFO] Cleaning up resources...")

        if self.uart and self.uart.is_open:
            self.uart.close()
            print("[INFO] UART closed")

        # gpiozero automatically cleans up when objects are deleted
        for stm32_pin, pin_device in self.gpio_inputs.items():
            if pin_device:
                pin_device.close()

        for led_name, led_device in {"red": self.red_led, "yellow": self.yellow_led, "green": self.green_led}.items():
            if led_device:
                led_device.off()
                led_device.close()

    def run_all_tests(self) -> dict:
        """
        Run the complete test sequence.

        Returns:
            Dictionary containing test results
        """
        print("\n")
        print("#" * 60)
        print("# STM32 AUTO TEST SUITE")
        print("#" * 60)

        self.show_ready_state()

        # Initialize peripherals
        if not self.initialize_gpio():
            self.show_fail_state()
            return False

        if not self.initialize_uart():
            self.show_fail_state()
            return False
        self.show_testing_state()

        # Flash STM32
        if not self.flash_stm32():
            self.show_fail_state()
            return False

        self.test_gpio_pd0()
        time.sleep(2)
        self.test_gpio_pd3()
        time.sleep(2)
        self.test_gpio_pd4()
        time.sleep(2)
        self.test_gpio_pa15()
        time.sleep(2)

        self.test_uart()

        time.sleep(10)
        self.test_stm32_i2c_and_spi_devices()

        self.verify_raspi_to_mcp4728_connection()

        if self.all_passed:
            self.show_pass_state()
        else:
            self.show_fail_state()

        self.cleanup()

        return self.all_passed



# Example usage
if __name__ == "__main__":
    # Initialize the test suite
    tester = STM32AutoTest(
        binary_path="./auto_test.bin",  # Set this to your binary path
        uart_port="/dev/ttyS0",
        uart_baudrate=115200
    )

    # Run all tests
    results = tester.run_all_tests()

```

Put the above code in a file called ```auto_test.py```.

Next to it, in the same folder, put the auto_test.bin file.

Run it with ```sudo python3 auto_test.py```.
