"""
Topic: Booking quote system
Change_Log:
IBRAR, Created file, 06/14/2021
"""

# !/usr/bin/env python3
import sys
import csv
from datetime import datetime, date, timedelta

class IO:
    """  A class for performing booking input and output"""
    @staticmethod
    def print_welcome():
        print('''
        Welcome to the Booking Quote System
        ''')
    @staticmethod
    def menu_and_choice():
        while True:
            try:
                user_main_choice = int(input("""
        The menu options are:
              1 - View order history,
              2 - Input a new order,
              3 - Quit
        Please input your choice [1-3]: """))
            except ValueError:
                print("\tInvalid Input")
                continue

            if user_main_choice not in range(1, 3 + 1):
                print("\tInvalid Input")
                continue

            return user_main_choice

    @staticmethod
    def input_new_order():
        """ Gets data for a booking object

        :return: (booking) object with input data
        """
        customer_name = str(input("What is the customer name? - "))
        package_description = str(input("Describe the package - ").strip())
        while True:
            try:
                hazard_tag = str(input("Are the contents dangerous (Yes/No)? - ").strip())
                if hazard_tag.lower() in ("yes", "no"):
                    if hazard_tag.lower() == "yes":
                        package_contents = "Dangerous"
                        break
                    else:
                        package_contents = "Safe"
                        break
                else:
                    raise ValueError
            except ValueError:
                print("\nInvalid Input. Please try again.\n")
        while True:
            try:
                package_weight = float(input("Enter the package weight (in kilograms) - "))
                if package_weight <= 10.00:
                    break
                else:
                    print("\nPackage must weigh less than 10kg.\n")
            except ValueError:
                print("\nInvalid Input. Please try again.\n")
                continue
        while True:
            try:
                package_volume = float(input("Enter the package volume (in cubic meters) - "))
                if package_volume <= 125.00:
                    break
                else:
                    print("\nPackages must have a volume of less than 125 cubic meters.\n")
            except ValueError:
                print("\nInvalid Input. Please try again.\n")
                continue
        while True:
            try:
                urgent_tag = str(
                    input("Is the shipment urgent (i.e. delivery in less than 3 days)? (Yes/No): - ").strip())
                if urgent_tag.lower() in ("yes", "no"):
                    if urgent_tag.lower() == "yes":
                        shipment_priority = "Urgent"
                        break
                    else:
                        shipment_priority = "Normal"
                        break
                else:
                    raise ValueError
            except ValueError:
                print("\nInvalid Input. Please try again.\n")

        if shipment_priority == "Urgent":
            required_delivery_date = (datetime.now() + timedelta(days=3)).date()
        else:
            while True:
                try:
                    delivery_date = input("Enter required delivery date (YYYY-MM-DD): ").strip()
                    if datetime.strptime(delivery_date, "%Y-%m-%d").date() > (
                            datetime.now() + timedelta(days=3)).date():
                        required_delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()
                        break
                    else:
                        print("\nDelivery date must be after 3 days from today!\n")
                        continue
                except ValueError:
                    print("\nInvalid Input. Please try again.\n")
        order = DC.Booking(shipment_priority, customer_name, package_description,package_contents,package_weight,package_volume, required_delivery_date)
        return order

    @staticmethod
    def print_order_history(list_of_rows: list):
        """ Print the current items in the Order History

        :param list_of_rows: (list) of rows you want to display
        """