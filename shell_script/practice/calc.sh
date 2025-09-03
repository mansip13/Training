#!/bin/bash
# Advanced CLI Calculator

HISTORY_FILE="calc_history.txt"

# Colors
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
RESET="\e[0m"

# Function to perform calculation
calculate() {
    num1=$1
    op=$2
    num2=$3

    # Validate numeric input
    if ! [[ "$num1" =~ ^-?[0-9]*\.?[0-9]+$ && "$num2" =~ ^-?[0-9]*\.?[0-9]+$ ]]; then
        echo -e "${RED}Error: Both inputs must be numbers.${RESET}"
        return
    fi

    # Division check
    if [[ "$op" = "/" && "$num2" = "0" ]]; then
        echo -e "${RED}Error: Division by zero!${RESET}"
        return
    fi

    # Use bc for floating-point support
    result=$(echo "$num1 $op $num2" | bc -l)

    # Log the calculation
    echo "$num1 $op $num2 = $result" >> "$HISTORY_FILE"

    # Print result
    echo -e "${GREEN}Result:${RESET} $result"
}

# -----------------------
# Command-line mode
# -----------------------
if [ $# -eq 3 ]; then
    calculate "$1" "$2" "$3"
    exit 0
fi

# -----------------------
# Interactive mode
# -----------------------
echo -e "${YELLOW}Welcome to CLI Calculator! (type 'q' to quit)${RESET}"
while true; do
    read -p "Enter first number (or q to quit): " num1
    if [ "$num1" = "q" ]; then
        echo "Goodbye!"
        break
    fi

    read -p "Enter operator (+ - * /): " op
    read -p "Enter second number: " num2

    calculate "$num1" "$op" "$num2"
done

