"""
Topic: Booking quote system
Change_Log:
IBRAR, Created file, 06/14/2021
"""

# !/usr/bin/env python3
import sys
import csv
from collections import defaultdict
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
    def print_report(dict_to_be_printed):
        headers = list(dict_to_be_printed["1"].keys())
        order_table = [headers]
        for keys, values in dict_to_be_printed.items():
            order_table.append([values[header] for header in headers])
        column_width = [max(map(len, column)) for column in zip(*order_table)]
        table_format = " ".join(["{{:<{}}}".format(i) for i in column_width])
        for row in order_table:
            print(table_format.format(*row))


class FileProcessor:
    """Processes data to and from a file and a dictionary of objects:"""

    @staticmethod
    def save_data_to_file(file_name, dict_of_orders):
        """ Write data to a file from a dictionary of orders """
        try:
            headings = list(dict_of_orders["1"].keys())
            with open(file_name, 'w', newline='') as file:
                w = csv.DictWriter(file, fieldnames = headings)
                w.writeheader()
                for k, v in dict_of_orders.items():
                    w.writerow(v)
        except KeyError:
            print("There are no orders currently!")
        return "Data saved successfully!"

    @staticmethod
    def read_data_from_file(file_name):
        """ Write data to a file from a dictionary of orders """
        order_dict = {}
        with open(file_name, 'r') as file:
            data = csv.reader(file, delimiter=",")
            headers = next(data)[0:]
            for row in data:
                temp_dict = {}
                order_id = row[0]
                values = []
                for x in row[0:]:
                    values.append(x)
                for i in range(len(values)):
                    temp_dict[headers[i]] = values[i]
                order_dict[order_id] = temp_dict
        return order_dict