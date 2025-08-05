"""
IP Address Calculator (ipfx)
A comprehensive command-line tool for IP address calculations and network analysis.
Licensed under the MIT License
"""

import ipaddress
import sys
from typing import Dict, Union, Optional


class IPCalculator:
    """IP address calculation and analysis class."""
    
    @staticmethod
    def get_address_version(address: str) -> int:
        """
        Get IP address version (4 or 6).
        
        Args:
            address: IP address string
            
        Returns:
            4 for IPv4, 6 for IPv6, -1 for invalid
        """
        try:
            addr = ipaddress.ip_address(address)
            return 4 if isinstance(addr, ipaddress.IPv4Address) else 6
        except ValueError:
            return -1
    
    @staticmethod
    def calculate_ipv4(network: ipaddress.IPv4Network, interface: ipaddress.IPv4Interface) -> Dict[str, Union[str, int, bool]]:
        """
        Calculate IPv4 network information.
        
        Args:
            network: IPv4Network object
            interface: IPv4Interface object
            
        Returns:
            Dictionary containing network information
        """
        ip_addr = interface.ip
        network_address = network.network_address
        broadcast_address = network.broadcast_address
        host_count = network.num_addresses - 2  # Exclude network and broadcast addresses
        
        return {
            "ipaddress": str(ip_addr),
            "network_address": str(network_address),
            "broadcast_address": str(broadcast_address),
            "host_count": host_count,
            "is_private": network.is_private,
            "is_global": network.is_global,
            "is_network_address": network_address == ip_addr,
            "is_broadcast_address": broadcast_address == ip_addr,
            "reverse": interface.reverse_pointer,
            "cidr_notation": f"{ip_addr}/{network.prefixlen}",
            "cisco_notation": f"{ip_addr} {network.netmask}",
            "ubuntu_subnet": f"{network_address}/{network.prefixlen}"
        }
    
    @staticmethod
    def calculate_ipv6(network: ipaddress.IPv6Network, interface: ipaddress.IPv6Interface) -> Dict[str, Union[str, bool]]:
        """
        Calculate IPv6 network information.
        
        Args:
            network: IPv6Network object
            interface: IPv6Interface object
            
        Returns:
            Dictionary containing network information
        """
        network_address = network.network_address
        
        return {
            "network_address": str(network_address),
            "is_private": network.is_private,
            "is_global": network.is_global,
            "is_link_local": network.is_link_local,
            "is_multicast": network.is_multicast,
            "reverse": network.reverse_pointer,
            "cidr_notation": f"{network_address}/{network.prefixlen}",
            "ubuntu_notation": f"{network_address}/{network.prefixlen}"
        }


class OutputFormatter:
    """Output formatting class."""
    
    @staticmethod
    def print_ipv4_info(info: Dict[str, Union[str, int, bool]]) -> None:
        """Print IPv4 information in formatted output."""
        print("=" * 42)
        print("IPv4 Address Information".center(42))
        print("=" * 42)
        for key, value in info.items():
            print(f"{key:20}: {value}")
        print("=" * 42)
    
    @staticmethod
    def print_ipv6_info(info: Dict[str, Union[str, bool]]) -> None:
        """Print IPv6 information in formatted output."""
        print("=" * 42)
        print("IPv6 Address Information".center(42))
        print("=" * 42)
        for key, value in info.items():
            print(f"{key:20}: {value}")
        print("=" * 42)
    
    @staticmethod
    def print_error(message: str) -> None:
        """Print error message."""
        print(f"Error: {message}")
    
    @staticmethod
    def print_help() -> None:
        """Print help message."""
        help_text = """
IP Address Calculator (ipfx) - Network Analysis Tool

Usage:
    ipfx [address/prefix] [options]
    
Arguments:
    address/prefix    IP address with CIDR notation (e.g., 192.168.1.1/24)
    
Options:
    -h, --help       Show this help message and exit
    
Examples:
    ipfx 192.168.1.1/24       # Calculate IPv4 network
    ipfx 2001:db8::1/64       # Calculate IPv6 network
    ipfx                      # Enter interactive mode
    
Interactive Mode:
    In interactive mode, you can enter multiple addresses:
    address: 192.168.1.1/24
    address: 10.0.0.1/8
    address: exit            # Exit interactive mode
        """
        print(help_text.strip())


class IPAddressProcessor:
    """Main IP address processing class."""
    
    def __init__(self):
        self.calculator = IPCalculator()
        self.formatter = OutputFormatter()
    
    def process_address(self, input_data: str) -> int:
        """
        Process a single IP address input.
        
        Args:
            input_data: Address input in format "address/prefix"
            
        Returns:
            0 for success, -1 for error
        """
        try:
            address, prefix = input_data.split('/')
        except ValueError:
            self.formatter.print_error("Invalid input format. Please use 'address/prefix'.")
            return -1
        
        address_version = self.calculator.get_address_version(address)
        if address_version == -1:
            self.formatter.print_error("Invalid address format.")
            return -1
        
        try:
            if address_version == 4:
                network = ipaddress.IPv4Network(f"{address}/{prefix}", strict=False)
                interface = ipaddress.IPv4Interface(f"{address}/{prefix}")
                info = self.calculator.calculate_ipv4(network, interface)
                self.formatter.print_ipv4_info(info)
            elif address_version == 6:
                network = ipaddress.IPv6Network(f"{address}/{prefix}", strict=False)
                interface = ipaddress.IPv6Interface(f"{address}/{prefix}")
                info = self.calculator.calculate_ipv6(network, interface)
                self.formatter.print_ipv6_info(info)
            else:
                self.formatter.print_error("Unknown address version.")
                return -1
                
        except ValueError as e:
            self.formatter.print_error(f"Invalid network specification: {e}")
            return -1
        
        return 0
    
    def interactive_mode(self) -> int:
        """
        Run interactive mode for continuous address processing.
        
        Returns:
            Exit code (0 for success)
        """
        print("IP Address Calculator - Interactive Mode")
        print("Enter IP addresses in format 'address/prefix' or 'exit' to quit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("address: ").strip()
                if user_input.lower() in ('exit', 'quit', 'q'):
                    break
                
                if not user_input:
                    continue
                    
                self.process_address(user_input)
                print()  # Add blank line for readability
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except EOFError:
                break
        
        return 0
    
    def command_line_mode(self, address: str) -> int:
        """
        Run command line mode for single address processing.
        
        Args:
            address: IP address with prefix
            
        Returns:
            Exit code (0 for success, -1 for error)
        """
        return self.process_address(address)


def main(input_address: Optional[str] = None) -> int:
    """
    Main application entry point.
    
    Args:
        input_address: Optional IP address input
        
    Returns:
        Exit code
    """
    processor = IPAddressProcessor()
    
    if input_address is not None:
        return processor.command_line_mode(input_address)
    else:
        return processor.interactive_mode()


if __name__ == "__main__":
    args = sys.argv[1:]  # Exclude script name
    
    if not args:
        # No arguments - enter interactive mode
        exit_code = main()
        sys.exit(exit_code)
    
    # Process command line arguments
    for arg in args:
        if arg in ("-h", "--help"):
            OutputFormatter.print_help()
            sys.exit(0)
        
        # Process each address argument
        print(f"Processing: {arg}")
        exit_code = main(arg)
        if exit_code != 0:
            sys.exit(exit_code)
        print()  # Add blank line between results
    
    sys.exit(0)
