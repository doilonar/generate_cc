"""Credit Card Number Generator"""

import random
import datetime
from typing import Tuple, Optional, Dict
import sys
import logging

#Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CreditCardGenerator:
        """Credit card generator using Luhn algorithm validation."""

        # Constants
        BIN_LENGTH = 6
        CARD_LENGTH = 16
        CVV_LENGTH = 3
        ADDITIONAL_DIGITS = 9
        MIN_FUTURE_YEARS = 1
        MAX_FUTURE_YEARS = 5

        def __init__(self):
                """Initialize the generator with current time."""
                self.current_time = datetime.datetime.now()


        def get_bin_input(self) -> str:
                """
                Get and validate BIN input from user with improved error handling.

                Returns:
                    str: Valid 6-digit BIN

                Raises:
                    KeyboardInterrupt: When user interrupts input (ex: CTRL+C)
                    EOFError: When input stream ends unexpectedly
                """
                attempt_count = 0
                max_attempts = 5

                while attempt_count < max_attempts:
                        try:
                                bin_input = input("BIN (6 digits): ").strip()

                                #Validate BIN input
                                if self._validate_bin(bin_input):
                                        logger.info(f"Valid BIN entered: {bin_input}")
                                        return bin_input
                                else:
                                        attempt_count += 1
                                        remaining = max_attempts - attempt_count
                                        if remaining > 0:
                                                print(f"BIN Error: Please enter exactly 6 digits. {remaining} attempts remaining.")
                                        else:
                                                print("\nMaximum attempts reached. Exiting.")
                                                sys.exit(1)

                        except (KeyboardInterrupt, EOFError) as e:
                                print(f"\nInput interrupted: {type(e).__name__}")
                                logger.warning(f"Input interrupted: {e}")
                                sys.exit(1)
                        except Exception as e:
                                print(f"Unexpected error during input: {e}")
                                logger.error(f"Unexpected input error: {e}")
                                attempt_count += 1
                                continue

                print("Maximum attempts exceeded.")
                sys.exit(1)

        def _validate_bin(self, bin_str: str) -> bool:
                """
                Validate BIN format.

                Args:
                    bin_str: String to validate as BIN

                Returns:
                    bool: True if a valid BIN had been entered(6 digits),
                          False otherwise
                """
                if not bin_str:
                        return False

                #Check if it's exactly 6 digits
                if not bin_str.isdigit() or len(bin_str) != self.BIN_LENGTH:
                        return False

                #Additional validation: BIN shouldn't start with 0
                #(though some test card ranges do start with 0, we'll allow it with a warning)
                if bin_str.startswith('0'):
                        logger.warning(f"BIN {bin_str} starts with 0 - this is unusual but allowed")

                return True

        def _calculate_luhn_digit(self, partial_card: str) -> int:
                """
                Calculate Luhn check digit for partial card number.

                Args:
                    partial_card: 15-digit partial card number

                Returns:
                    int: Luhn check digit (0-9)

                Raises:
                    ValueError: If partial_card is not exactly 15 digits
                """
                if len(partial_card) != 15:
                        raise ValueError(f"Partial card must be exactly 15 digits, got {len(partial_card)}")

                if not partial_card.isdigit():
                        raise ValueError("Partial card must contain only digits")

                total = 0

                #Process digits from right to left (Luhn algorithm standard)
                for i, digit in enumerate(partial_card):
                        digit_val = int(digit)

                        #Double every second digit from the right
                        #In 0-indexed from left, this means even positions for 15-digit string
                        if i % 2 == 0:
                                doubled = digit_val * 2
                                #If doubled value >= 10, subtract 9 (equivalent to sum of digits)
                                if doubled >= 10:
                                        doubled -= 9
                                total += doubled
                        else:
                                total += digit_val

                #Calculate check digit
                check_digit = (10 - (total % 10)) % 10
                logger.debug(f"Calculated Luhn check digit: {check_digit}")
                return check_digit

        def generate_card_number(self, bin_number: str) -> str:
                """
                Generate a 16-digit card number from BIN.

                Args:
                    bin_number: 6-digit BIN

                Returns:
                    str: Complete 16-digit card number

                Raises:
                    ValueError: If BIN is invalid or generation fails
                """
                if not self._validate_bin(bin_number):
                        raise ValueError(f"Invalid BIN provided: {bin_number}")

                try:
                        #Start with the 6digit BIN
                        partial_card = bin_number

                        #Generate 9 additional random digits
                        for _ in range(self.ADDITIONAL_DIGITS):
                                partial_card += str(random.randint(0, 9))

                        #Calculate and append Luhn check digit
                        check_digit = self._calculate_luhn_digit(partial_card)
                        complete_card = partial_card + str(check_digit)

                        #Final validation
                        if len(complete_card) != self.CARD_LENGTH:
                                raise ValueError(f"Generated card has wrong length: {len(complete_card)}")

                        logger.info(f"Generated card number for BIN {bin_number}")
                        return complete_card

                except Exception as e:
                        logger.error(f"Error generating card number: {e}")
                        raise ValueError(f"Error generating card number: {e}")

        def generate_cvv(self) -> str:
                """
                Generate 3 digit CVV.

                Returns:
                    str: 3 digit CVV

                Raises:
                    ValueError: If CVV generation fails
                """
                try:
                        cvv = random.randint(0, 999)
                        formatted_cvv = f"{cvv:0{self.CVV_LENGTH}d}"
                        logger.debug(f"Generated CVV: {formatted_cvv}")
                        return formatted_cvv
                except Exception as e:
                        logger.error(f"Error generating CVV: {e}")
                        raise ValueError(f"Error generating CVV: {e}")

        def generate_expiration_date(self) -> Tuple[str, str]:
                """
                Generate expiration date.

                Returns:
                    Tuple[str, str]: (month, year) both as strings

                Raises:
                    ValueError: If date generation fails
                """
                try:
                        current_year = self.current_time.year % 100  # Get 2-digit year
                        current_month = self.current_time.month

                        #Generate year between current+1 and current+5 years
                        year = random.randint(
                                current_year + self.MIN_FUTURE_YEARS,
                                current_year + self.MAX_FUTURE_YEARS
                        )

                        #Generate month - always valid since we're using future years
                        month = random.randint(1, 12)

                        formatted_month = f"{month:02d}"
                        formatted_year = f"{year:02d}"

                        logger.debug(f"Generated expiration: {formatted_month}/{formatted_year}")
                        return formatted_month, formatted_year

                except Exception as e:
                        logger.error(f"Error generating expiration date: {e}")
                        raise ValueError(f"Error generating expiration date: {e}")

        def generate_complete_card_data(self, bin_number: Optional[str] = None) -> Dict[str, str]:
                """
                Generate complete card data including number, CVV, and expiration.

                Args:
                    bin_number: Optional BIN number. If None, will prompt user for input.

                Returns:
                    Dict[str, str]: Dictionary containing card_number, cvv, month, year, bin

                Raises:
                    RuntimeError: If card data generation fails
                """
                try:
                        if bin_number is None:
                                bin_number = self.get_bin_input()
                        elif not self._validate_bin(bin_number):
                                raise ValueError("Invalid BIN provided")

                        card_number = self.generate_card_number(bin_number)
                        cvv = self.generate_cvv()
                        month, year = self.generate_expiration_date()

                        card_data = {
                                'card_number': card_number,
                                'cvv': cvv,
                                'month': month,
                                'year': year,
                                'bin': bin_number
                        }

                        logger.info("Successfully generated complete card data")
                        return card_data

                except Exception as e:
                        logger.error(f"Failed to generate card data: {e}")
                        raise RuntimeError(f"Failed to generate card data: {e}")

        def format_card_number(self, card_number: str) -> str:
                """
                Format card number with spaces for readability.

                Args:
                    card_number: 16 digit card number

                Returns:
                    str: Formatted card number (XXXX XXXX XXXX XXXX)

                Raises:
                    ValueError: If card number is invalid
                """
                if not card_number.isdigit():
                        raise ValueError("Card number must contain only digits")

                if len(card_number) != self.CARD_LENGTH:
                        raise ValueError(f"Card number must be exactly {self.CARD_LENGTH} digits")

                return f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"

        def validate_luhn(self, card_number: str) -> bool:
                """
                Validate a card number using the Luhn algorithm.

                Args:
                    card_number: Card number to validate

                Returns:
                    bool: True if valid according to Luhn algorithm
                """
                if not card_number.isdigit() or len(card_number) != self.CARD_LENGTH:
                        return False

                total = 0
                reverse_digits = card_number[::-1]

                for i, digit in enumerate(reverse_digits):
                        digit_val = int(digit)

                        if i % 2 == 1:  # Every second digit from the right
                                doubled = digit_val * 2
                                if doubled > 9:
                                        doubled -= 9
                                total += doubled
                        else:
                                total += digit_val

                return total % 10 == 0

def main():
        """Main function to run the credit card generator"""
        print("=" * 60)
        print("Credit Card Generator")
        print("=" * 60)

        try:
                generator = CreditCardGenerator()

                #Generate card data
                card_data = generator.generate_complete_card_data()

                #Validate the generated card
                is_valid = generator.validate_luhn(card_data['card_number'])

                #Display results
                print("\n" + "=" * 50)
                print("GENERATED CARD DATA")
                print("=" * 50)
                print(f"BIN:              {card_data['bin']}")
                print(f"Card Number:      {generator.format_card_number(card_data['card_number'])}")
                print(f"Card Number:      {card_data['card_number']}")  #Unformatted for copying reasons
                print(f"CVV:              {card_data['cvv']}")
                print(f"Expiration:       {card_data['month']}/{card_data['year']}")
                print("=" * 50)

                if not is_valid:
                        logger.error("Generated card failed Luhn validation!")
                        print("WARNING: Generated card failed Luhn validation!")

        except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                logger.info("User cancelled operation")
                sys.exit(0)
        except Exception as e:
                print(f"\nError: {e}")
                logger.error(f"Application error: {e}")
                sys.exit(1)


if __name__ == "__main__":
        main()