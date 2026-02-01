# main.py
# main program that converts a given expression into base units and display

import parse
import re

def group_exponents(parsed_expr):
    """
    Groups exponents to evaluate them before multiplication
    Returns a list, in the same format as parsed_expr
    """

    i = 0
    while i < len(parsed_expr):
        if parsed_expr[i] == "^":
            if i == 0 or i + 2 > len(parsed_expr):
                raise ValueError(f"Lone operator: ^")
            replacement = parsed_expr[i-1: i+2]
            parsed_expr[i-1: i+2] = [replacement,]
        else:
            i += 1

    return parsed_expr

def calculate_base_units(parsed_expr, units_data):
    """
    Recursively calculate the base units for a parsed expression
    Returns a dictionary with base units and coefficient
    """
    # Base case: if the expression is a string (number or unit)
    if isinstance(parsed_expr, str):
        # If it's a number
        if re.match(parse.NUM, parsed_expr):
            return {
                's': 0, 'm': 0, 'kg': 0, 'mol': 0, 'C': 0, 'K': 0, 'cd': 0,
                'COEFF': float(parsed_expr)
            }
        # If it's a unit
        elif re.match(parse.UNIT, parsed_expr):
            for unit in units_data:
                if unit['Symbol'] == parsed_expr or unit['Alternate Symbol'] == parsed_expr:
                    return {
                        's': unit['s'], 'm': unit['m'], 'kg': unit['kg'], 
                        'mol': unit['mol'], 'C': unit['C'], 'K': unit['K'], 
                        'cd': unit['cd'], 'COEFF': unit['COEFF']
                    }
            # Unit not found
            raise ValueError(f"Unknown unit: {parsed_expr}")
        elif re.match(parse.OP, parsed_expr):
            raise ValueError(f"Lone operator: {parsed_expr}")
    
    # Recursive case: if the expression is a list (compound expression)
    elif isinstance(parsed_expr, list):
        if len(parsed_expr) == 1:
            return calculate_base_units(parsed_expr[0], units_data)
        
        result = None
        current_op = '*' # multiply by default
        
        for item in parsed_expr:
            if not isinstance(item, list) and re.match(parse.OP, item):
                current_op = item
                continue
                
            current_result = calculate_base_units(item, units_data)
            
            if result is None:
                result = current_result
            else:
                # Apply operation
                if current_op == '*':
                    # Multiplication: add exponents, multiply coefficients
                    for key in result:
                        if key == 'COEFF':
                            result[key] *= current_result[key]
                        else:
                            result[key] += current_result[key]
                elif current_op == '/':
                    # Division: subtract exponents, divide coefficients
                    for key in result:
                        if key == 'COEFF':
                            result[key] /= current_result[key]
                        else:
                            result[key] -= current_result[key]
                    current_op = '*' # multiply by default
                elif current_op == '^':
                    # Exponentiation: multiply exponents, raise coefficient
                    
                    # if exponent is a unit, raise an error
                    for unit in ['s', 'm', 'kg', 'mol', 'C', 'K', 'cd']:
                        if current_result[unit] != 0:
                            raise ValueError(f"raising to an exponent: {item}")

                    exponent = current_result['COEFF']
                    for key in result:
                        if key == 'COEFF':
                            result[key] = result[key] ** exponent
                        else:
                            result[key] *= exponent
                    current_op = '*'
        
        return result
    
    return None

def format_result(base_units):
    """Format the base units into a readable string"""
    result = f"Coefficient: {base_units['COEFF']}\n"
    result += "Base Units:\n"
    
    # Filter out zero exponents
    base_units_str = []
    for unit in ['s', 'm', 'kg', 'mol', 'C', 'K', 'cd']:
        if base_units[unit] != 0:
            if base_units[unit] == 1:
                base_units_str.append(f"{unit}")
            else:
                base_units_str.append(f"{unit}^{base_units[unit]}")
    
    if base_units_str:
        result += " * ".join(base_units_str)
    else:
        result += "Dimensionless"
    
    return result

def convert_expression(expression):
    """
    Convert a given expression to its base units
    """
    # Load unit database
    _, units_data = parse.readfile("Unit_database.csv")
 
    try:
        parsed_expr = parse.parse(expression)
        grouped_expr = group_exponents(parsed_expr)

        # Calculate base units
        base_units = calculate_base_units(grouped_expr, units_data)
        
        # Format and return the result
        return format_result(base_units)
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def main():
    print("Unit Converter - Enter 'q' to quit")
    while True:
        expression = input("Enter expression: ").strip()
        if expression.lower() == 'q':
            break
        
        result = convert_expression(expression)
        print(result)
        print()

if __name__ == "__main__":
    main()
