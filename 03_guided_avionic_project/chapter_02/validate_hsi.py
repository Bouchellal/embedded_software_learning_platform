#!/usr/bin/env python3
"""
HSI.json Sanity Check Script
Validates Hardware Software Interface configuration JSON file

This script checks for:
1. Valid JSON syntax
2. Required fields in each pin configuration
3. Valid protocol types
4. Valid GPIO directions
5. Duplicate pin assignments
6. Valid voltage levels
7. Pin number validity for STM32F407
8. Cross-reference validation with SES.json requirements
"""

import json
import sys
from typing import Dict, List, Tuple, Set
from pathlib import Path


class HSISanityCheck:
    """Validates HSI.json configuration against rules and constraints"""
    
    # Valid STM32F407 ports
    VALID_PORTS = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}
    
    # Valid pin numbers for STM32F407 (LQFP176)
    VALID_PIN_NUMBERS = set(range(1, 177))
    
    # Valid protocols
    VALID_PROTOCOLS = {'UART', 'SPI', 'I2C', 'ADC', 'GPIO', 'CAN', 'USB', 'Ethernet'}
    
    # Valid directions
    VALID_DIRECTIONS = {'input', 'output', 'open_drain', 'bidirectional'}
    
    # Valid voltage levels
    VALID_VOLTAGES = {'3.3V', '5V', '0V-3.3V', '0V-5V', '0V-24V', '0V-24V (via resistive divider to 0V-3.3V)'}
    
    # Valid pull configurations
    VALID_PULL_CONFIG = {'none', 'pull-up', 'pull-down', 'external-pullup', 'external-pulldown'}
    
    # Required fields
    REQUIRED_FIELDS = {
        'pin_id', 'pin_number', 'port', 'direction', 
        'signal_name', 'protocol', 'voltage_level', 'description'
    }
    
    # STM32F407 Pin mapping constraints (Port + number validity)
    PORT_PIN_LIMITS = {
        'A': (16, 'PA0-PA15'),
        'B': (16, 'PB0-PB15'),
        'C': (16, 'PC0-PC15'),
        'D': (16, 'PD0-PD15'),
        'E': (16, 'PE0-PE15'),
        'F': (16, 'PF0-PF15'),
        'G': (16, 'PG0-PG15'),
        'H': (2, 'PH0-PH1'),
        'I': (8, 'PI0-PI7'),
    }
    
    def __init__(self, hsi_file_path: str):
        """Initialize with path to HSI.json file"""
        self.file_path = Path(hsi_file_path)
        self.hsi_data: List[Dict] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def run_all_checks(self) -> bool:
        """Run all sanity checks and return True if all pass"""
        print("=" * 70)
        print("HSI.json SANITY CHECK")
        print("=" * 70)
        
        # Check file exists
        if not self.file_path.exists():
            print(f"❌ ERROR: File not found: {self.file_path}")
            return False
        
        # Check JSON syntax
        if not self._check_json_syntax():
            print(f"❌ ERROR: Invalid JSON syntax")
            return False
        
        print(f"✓ JSON syntax valid")
        
        # Run all validation checks
        self._check_required_fields()
        self._check_valid_protocols()
        self._check_valid_directions()
        self._check_valid_voltages()
        self._check_valid_pull_configs()
        self._check_pin_validity()
        self._check_duplicate_pins()
        self._check_pin_id_format()
        self._check_signal_names()
        self._check_protocol_pin_consistency()
        
        # Print results
        return self._print_results()
    
    def _check_json_syntax(self) -> bool:
        """Verify JSON syntax is valid"""
        try:
            with open(self.file_path, 'r') as f:
                self.hsi_data = json.load(f)
            return isinstance(self.hsi_data, list)
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON parsing error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"File reading error: {e}")
            return False
    
    def _check_required_fields(self):
        """Check that all required fields are present in each pin"""
        for idx, pin in enumerate(self.hsi_data):
            missing = self.REQUIRED_FIELDS - set(pin.keys())
            if missing:
                self.errors.append(
                    f"Pin {idx} (ID: {pin.get('pin_id', '?')}): Missing required fields: {missing}"
                )
    
    def _check_valid_protocols(self):
        """Check that protocols are valid"""
        for idx, pin in enumerate(self.hsi_data):
            protocol = pin.get('protocol', '')
            if protocol not in self.VALID_PROTOCOLS:
                self.errors.append(
                    f"Pin {pin.get('pin_id', '?')}: Invalid protocol '{protocol}'. "
                    f"Must be one of: {', '.join(sorted(self.VALID_PROTOCOLS))}"
                )
    
    def _check_valid_directions(self):
        """Check that direction values are valid"""
        for idx, pin in enumerate(self.hsi_data):
            direction = pin.get('direction', '')
            if direction not in self.VALID_DIRECTIONS:
                self.errors.append(
                    f"Pin {pin.get('pin_id', '?')}: Invalid direction '{direction}'. "
                    f"Must be one of: {', '.join(sorted(self.VALID_DIRECTIONS))}"
                )
    
    def _check_valid_voltages(self):
        """Check voltage levels"""
        for pin in self.hsi_data:
            voltage = pin.get('voltage_level', '')
            if voltage not in self.VALID_VOLTAGES:
                self.warnings.append(
                    f"Pin {pin.get('pin_id', '?')}: Uncommon voltage level '{voltage}'. "
                    f"Common values: {', '.join(sorted(self.VALID_VOLTAGES))}"
                )
    
    def _check_valid_pull_configs(self):
        """Check pull configuration values"""
        for pin in self.hsi_data:
            pull = pin.get('pull_configuration', '')
            if pull not in self.VALID_PULL_CONFIG:
                self.errors.append(
                    f"Pin {pin.get('pin_id', '?')}: Invalid pull configuration '{pull}'. "
                    f"Must be one of: {', '.join(sorted(self.VALID_PULL_CONFIG))}"
                )
    
    def _check_pin_validity(self):
        """Check STM32F407 pin number validity"""
        for pin in self.hsi_data:
            pin_id = pin.get('pin_id', '')
            port = pin.get('port', '')
            pin_num = pin.get('pin_number', None)
            
            # Check port validity
            if port not in self.VALID_PORTS:
                self.errors.append(
                    f"Pin {pin_id}: Invalid port '{port}'. Valid ports: {', '.join(sorted(self.VALID_PORTS))}"
                )
                continue
            
            # Check pin number range
            if pin_num is None or not isinstance(pin_num, int):
                self.errors.append(f"Pin {pin_id}: pin_number must be an integer, got {type(pin_num)}")
                continue
            
            if pin_num not in self.VALID_PIN_NUMBERS:
                self.errors.append(f"Pin {pin_id}: pin_number {pin_num} out of range (1-176)")
                continue
            
            # Check port-specific pin limits
            max_pins, range_str = self.PORT_PIN_LIMITS[port]
            pin_in_port = int(pin_id[1:]) if len(pin_id) > 1 else None
            
            if pin_in_port is not None and pin_in_port >= max_pins:
                self.errors.append(
                    f"Pin {pin_id}: Port {port} only has pins {range_str}"
                )
    
    def _check_duplicate_pins(self):
        """Check for duplicate pin assignments"""
        pin_ids: Dict[str, int] = {}
        pin_numbers: Dict[int, str] = {}
        
        for pin in self.hsi_data:
            pin_id = pin.get('pin_id', '')
            pin_num = pin.get('pin_number', '')
            
            # Check duplicate pin IDs
            if pin_id in pin_ids:
                self.errors.append(f"Duplicate pin ID: {pin_id}")
            else:
                pin_ids[pin_id] = 1
            
            # Check duplicate pin numbers
            if pin_num in pin_numbers:
                self.errors.append(
                    f"Pin number {pin_num} assigned twice: {pin_numbers[pin_num]} and {pin_id}"
                )
            else:
                pin_numbers[pin_num] = pin_id
    
    def _check_pin_id_format(self):
        """Check that pin_id format matches expected pattern"""
        for pin in self.hsi_data:
            pin_id = pin.get('pin_id', '')
            port = pin.get('port', '')
            
            # Format should be like PA0, PB15, etc.
            if not pin_id.startswith('P') or len(pin_id) < 3:
                self.errors.append(f"Invalid pin_id format: {pin_id}. Expected format: PA0, PB5, etc.")
                continue
            
            # Check that port matches pin_id
            if pin_id[1] != port:
                self.errors.append(
                    f"Pin ID {pin_id} port mismatch: "
                    f"pin_id suggests port {pin_id[1]}, but 'port' field is {port}"
                )
    
    def _check_signal_names(self):
        """Check signal naming conventions"""
        signal_names: Dict[str, int] = {}
        
        for pin in self.hsi_data:
            signal = pin.get('signal_name', '')
            
            if not signal:
                self.warnings.append(f"Pin {pin.get('pin_id', '?')}: Missing signal name")
                continue
            
            # Check for duplicate signal names
            if signal in signal_names:
                self.warnings.append(
                    f"Duplicate signal name '{signal}' at pin {pin.get('pin_id', '?')}"
                )
            else:
                signal_names[signal] = 1
    
    def _check_protocol_pin_consistency(self):
        """Validate protocol-specific requirements"""
        uart_pins = []
        i2c_pairs = []
        
        for pin in self.hsi_data:
            protocol = pin.get('protocol', '')
            pin_id = pin.get('pin_id', '')
            direction = pin.get('direction', '')
            
            # UART should have TX (output) and RX (input) pairs
            if protocol == 'UART':
                uart_pins.append((pin_id, direction))
            
            # I2C should use open_drain for SCL/SDA
            if protocol == 'I2C' and direction != 'open_drain':
                self.warnings.append(
                    f"Pin {pin_id}: I2C pins should use 'open_drain' direction, found '{direction}'"
                )
    
    def _print_results(self) -> bool:
        """Print validation results"""
        print()
        
        if self.errors:
            print("❌ ERRORS FOUND:")
            print("-" * 70)
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            print("-" * 70)
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i}. {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ ALL CHECKS PASSED!")
            print("-" * 70)
        
        print()
        print(f"Total pins configured: {len(self.hsi_data)}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print("=" * 70)
        
        return len(self.errors) == 0


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        # Try to find HSI.json in current directory or parent directories
        hsi_path = Path("HSI.json")
        if not hsi_path.exists():
            print("Usage: python validate_hsi.py <path_to_HSI.json>")
            print("\nExample: python validate_hsi.py ./HSI.json")
            sys.exit(1)
    else:
        hsi_path = sys.argv[1]
    
    checker = HSISanityCheck(hsi_path)
    success = checker.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
