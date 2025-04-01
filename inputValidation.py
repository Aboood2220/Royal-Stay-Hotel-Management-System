class Validation:

    def validate_text_input(input_text, min_value, max_value):
        """
        Validates if the input text can be converted to an integer within a given range.

        Parameters:
        - text (str): The input string to validate.
        - min_value (int): The minimum acceptable integer value.
        - max_value (int): The maximum acceptable integer value.

        Returns:
        - (bool, str): Tuple containing:
            - True and a success message if valid.
            - False and an error message otherwise.
        """
        try:
            number = float(input_text)
        except ValueError:
            return False, "Input is not a number."

        if not number.is_integer():
            return False, "Number is not a whole number."

        number = int(number)
        if number < min_value or number > max_value:
            return False, f"Number is not within the range {min_value} to {max_value}."

        return True, number
