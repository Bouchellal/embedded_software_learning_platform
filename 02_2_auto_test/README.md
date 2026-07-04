# Auto Test

To do this auto test, we need to write C code for STM32 and a Python script for the Raspberry Pi.

## C Code for STM32

Let's create a new STM32 project and configure these pins:

1. Open the .ioc file,
2. Go to connectivity,
3. For each interface shown in green, enable the interface via the mode dropdown menu:
    - UART1: Asynchronous
    - I2C1: I2C
    - SPI1: Full-Duplex Master
4. Go through the configuration panels, discover the parameters for each interface,
5. Set the GPIOs to GPIO_OUTPUT,
6. Save with ctrl+s to generate the code.


![Auto Test Pin Configuration](../.images/02_hands_on_platform/auto_test.png)


In the main.c file, the idea is to test each group of interfaces (GPIOs, UART, I2C, SPI) one by one. 

For each interface, we will send a message and wait for a response. If the response is correct, else, there maybe a problem:

- Either the interface is broken, grilled,
- Or the cable is not connected properly,
- Or the cable is connected on the wrong pin,
- Or the auto test script is not working properly.

```C
int main(void)
{

  /* USER CODE BEGIN 1 */

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
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, GPIO_PIN_RESET);

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
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, GPIO_PIN_SET);
  HAL_Delay(2000);

  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, GPIO_PIN_RESET);
  /* ----------- TEST GPIO END ---------- */



  /* ----------- TEST USART ---------- */
	uint8_t rxBuffer[RX_BUFFER_SIZE]; // The buffer to store incoming data
	uint16_t bytesReceived = 0;       // This will track exactly how many bytes we got

	// Clear out the buffer before receiving new data
    memset(rxBuffer, 0, RX_BUFFER_SIZE);
    bytesReceived = 0;

    /* * 3. Call the Receive To Idle function
     * Arguments:
     * &huart1       -> Pointer to your UART configuration handle
     * rxBuffer      -> Where to store the incoming bytes
     * RX_BUFFER_SIZE-> The absolute maximum bytes we are willing to take
     * &bytesReceived-> Variable that the function updates with the actual count
     * 2000          -> Timeout in milliseconds (2 seconds)
     */
    HAL_StatusTypeDef status = HAL_UARTEx_ReceiveToIdle(&huart1, rxBuffer, RX_BUFFER_SIZE, &bytesReceived, 2000);
    if (status == HAL_OK && bytesReceived > 0)
        {
            // Transmit back exactly what we received
            // We use a 500ms timeout for the transmission
            HAL_UART_Transmit(&huart1, rxBuffer, bytesReceived, 500);
        }
        // Optional: handle what happens if it hits the 2-second timeout without any data
        else if (status == HAL_TIMEOUT)
        {
            // 2 seconds passed, no data came in or the packet was incomplete
        	char errorBuffer[64];

			/* Format the error message.
			 * Note: HAL Status values are:
			 * 0 = HAL_OK, 1 = HAL_ERROR, 2 = HAL_BUSY, 3 = HAL_TIMEOUT
			 */
			int msgLength = sprintf(errorBuffer, "\r\n[FAIL] HAL_Status: %d, BytesRx: %d\r\n", status, bytesReceived);

			// Send the error message back over UART
			HAL_UART_Transmit(&huart1, (uint8_t*)errorBuffer, msgLength, 500);
        }
    /* ----------- TEST USART END ---------- */


  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */
	/* Toggle the state of PA5 */
	HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
	/* Insert a delay of 500ms */
	HAL_Delay(500);
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

To be able to use the UART on the Raspberry Pi, we need to enable it first.

1. Enable UART & Disable Serial Console/
    - Since you are running OS Lite, you will do this via the terminal or raspi-config.
    - Run the configuration tool: ```sudo raspi-config```
    - Navigate to: 3 Interface Options -> I6 Serial Port.
    - It will ask two critical questions:
      - Would you like a login shell to be accessible over serial? Select No.
      - Would you like the serial port hardware to be enabled? Select Yes.

    - Select Finish and choose Yes to reboot the Raspberry Pi.

2. Install pyserial
    - Run the following command to install pyserial: ```sudo pip3 install pyserial```


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

        # GPIO mapping: STM32 pin name -> RPi BOARD pin number
        # To be configured by user using set_gpio_mapping()
        self.stm32_to_rpi_gpio = {
            'PD0': 23,   # STM32 PD0 on RPi GPIO 23
            'PD3': 21,   # STM32 PD3 on RPi GPIO 21
            'PD4': 19,   # STM32 PD4 on RPi GPIO 19
            'PC14': 15   # STM32 PC14 on RPi GPIO 15
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
            stm32_pin: STM32 pin name as key (e.g., 'PD0', 'PD3', 'PD4', 'PC14')
        Returns:
            True if test passed, False otherwise
        """
        if stm32_pin not in self.gpio_inputs:
            print(f"[ERROR] Unknown STM32 pin: {stm32_pin}")
            return False

        rpi_pin = self.stm32_to_rpi_gpio[stm32_pin]
        gpio_device = self.gpio_inputs[stm32_pin]
        print(f"[TEST] STM32 GPIO {stm32_pin} -- RPi GPIO {rpi_pin} ... ")

        time.sleep(0.5)  # Allow time for STM32 to set the pin HIGH
        # Verify it stays HIGH for some duration
        start_value = gpio_device.is_active
        time.sleep(1)
        end_value = gpio_device.is_active
        time.sleep(0.45)  # complete ~2 seconds of duration

        if start_value and end_value:
            print(f"{self.GREEN}[PASS] GPIO {stm32_pin}: start_value: {start_value}, end_value: {end_value} {self.RESET}")
            return True
        else:
            print(f"{self.RED}[FAIL] GPIO {stm32_pin}: start_value: {start_value}, end_value: {end_value}{self.RESET}")
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

    def test_gpio_pc14(self) -> bool:
        """Test STM32 GPIO PC14."""
        return self.test_gpio_pin('PC14')

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
            response = self.uart.readline().decode('utf-8', errors='ignore').strip()

            if test_message in response:
                print(f"{self.GREEN}[PASS] Received echo: '{response}'{self.RESET}")
                return True
            else:
                print(f"{self.RED}[FAIL] Unexpected response: '{response}'{self.RESET}")
                print(f"{self.RED}[FAIL] Expected: '{test_message}'{self.RESET}")
                return False

        except Exception as e:
            print(f"[ERROR] UART test failed: {str(e)}")
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
            return False

        if not self.initialize_uart():
            return False

        # Flash STM32
        if not self.flash_stm32():
            return False

        self.show_testing_state()

        all_passed = True

        self.test_gpio_pd0()
        self.test_gpio_pd3()
        self.test_gpio_pd4()
        self.test_gpio_pc14()

        all_passed = all_passed and self.test_uart()

        if all_passed:
            self.show_pass_state()
        else:
            self.show_fail_state()

        self.cleanup()

        return all_passed



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
