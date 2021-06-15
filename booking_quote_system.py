"""
Topic: Booking quote system
Change_Log:
IBRAR, Created file, 06/14/2021
IBRAR, Modified code, 06/15/2021
"""

# !/usr/bin/env python3
import sys
import csv
from datetime import datetime, date, timedelta


class Order(object):

    def __init__(self, order_id, shipment_priority, customer_name, package_description, package_contents, package_weight,
                 package_volume, delivery_date):
        self.order_id = str(order_id)
        self.shipment_priority = shipment_priority
        self.customer_name = customer_name
        self.package_description = package_description
        self.package_contents = package_contents
        self.package_weight = package_weight
        self.package_volume = package_volume
        self.delivery_date = delivery_date


class Quote(object):
    def __init__(self, air_shipment_cost="", truck_shipment_cost="", ocean_shipment_cost=""):
        self.air_shipment_cost = air_shipment_cost
        self.truck_shipment_cost = truck_shipment_cost
        self.ocean_shipment_cost = ocean_shipment_cost


class IO:
    """  A class for performing booking input and output"""

    @staticmethod
    def print_welcome():
        print('''
        Welcome to the Booking Quote System''')

    @staticmethod
    def menu_and_choice():
        while True:
            try:
                user_main_choice = int(input("""
        The menu options are:
              1 - View past order history,
              2 - Input a new order,
              3 - Save new orders to the file,
              4 - Quit
        Please input your choice [1-4]: """))
            except ValueError:
                print("\n\t\tInvalid Input. Please try again.")
                continue

            if user_main_choice not in range(1, 4 + 1):
                print("\n\t\tInvalid Input. Please try again.")
                continue

            return user_main_choice

    @staticmethod
    def input_new_order():
        """ Gets data for a booking object

        :return: (booking) object with input data
        """
        print()
        customer_name_entry = str(input("What is the customer name? - ")).title()
        package_description_entry = str(input("Describe the package - ").strip()).title()
        while True:
            try:
                hazard_tag = str(input("Are the contents dangerous (Yes/No)? - ").strip())
                if hazard_tag.lower() in ("yes", "no"):
                    if hazard_tag.lower() == "yes":
                        package_contents_entry = "Dangerous"
                        break
                    else:
                        package_contents_entry = "Safe"
                        break
                else:
                    raise ValueError
            except ValueError:
                print("\nInvalid Input. Please try again.\n")
        while True:
            try:
                package_weight_entry = float(input("Enter the package weight (in kilograms) - "))
                if package_weight_entry <= 10.00:
                    break
                else:
                    print("\nPackage must weigh less than 10kg.\n")
            except ValueError:
                print("\nInvalid Input. Please try again.\n")
                continue
        while True:
            try:
                package_volume_entry = float(input("Enter the package volume (in cubic meters) - "))
                if package_volume_entry <= 125.00:
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
                        shipment_priority_entry = "Urgent"
                        break
                    else:
                        shipment_priority_entry = "Normal"
                        break
                else:
                    raise ValueError
            except ValueError:
                print("\nInvalid Input. Please try again.\n")

        if shipment_priority_entry == "Urgent":
            required_delivery_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        else:
            while True:
                try:
                    delivery_date_entry = input("Enter required delivery date (YYYY-MM-DD): ").strip()
                    if datetime.strptime(delivery_date_entry, "%Y-%m-%d").date() > (
                            datetime.now() + timedelta(days=3)).date():
                        required_delivery_date = datetime.strptime(delivery_date_entry, "%Y-%m-%d").date().strftime('%Y-%m-%d')
                        break
                    else:
                        print("\nDelivery date must be after 3 days from today!\n")
                        continue
                except ValueError:
                    print("\nInvalid Input. Please try again.\n")
        return shipment_priority_entry, customer_name_entry, package_description_entry, package_contents_entry, str(package_weight_entry), str(package_volume_entry), required_delivery_date

    @staticmethod
    def print_report(dict_to_be_printed):
        try:
            headers = list(dict_to_be_printed["1"].keys())
            order_table = [headers]
            for keys, values in dict_to_be_printed.items():
                order_table.append([values[header] for header in headers])
            column_width = [max(map(len, column)) for column in zip(*order_table)]
            table_format = " ".join(["{{:<{}}}".format(i) for i in column_width])
            for row in order_table:
                print(table_format.format(*row))
        except KeyError:
            print("\n\t\tThere are no orders to view.\n")


class OrderProcessor:
    @staticmethod
    def add_new_order(order_dict_to_update, new_order_id, new_shipment_priority, new_customer_name, new_package_description,
                      new_package_contents, new_package_weight, new_package_volume, new_delivery_date):
        updated_order_dict = {}
        new_order = Order(new_order_id, new_shipment_priority, new_customer_name, new_package_description, new_package_contents,
                          new_package_weight, new_package_volume, new_delivery_date)
        new_order_dict = vars(new_order)
        updated_order_dict[new_order.order_id] = new_order_dict
        order_dict_to_update.update(updated_order_dict)
        return order_dict_to_update, new_order.order_id

    @staticmethod
    def compute_shipment_costs(order_dict_to_process, order_id_to_process):
        order_shipment_computation = order_dict_to_process.get(order_id_to_process)
        order_air_weight_price = 10 * float(order_shipment_computation["package_weight"])
        order_air_volume_price = 20 * float(order_shipment_computation["package_volume"])
        order_air_price = max(order_air_volume_price, order_air_weight_price)

        shipment_costs = vars(Quote())

        if order_shipment_computation["shipment_priority"] == "Urgent" and order_shipment_computation[
            "package_contents"] == "Dangerous":
            shipment_costs["air_shipment_cost"] = "NA"
            shipment_costs["truck_shipment_cost"] = "$45"
            shipment_costs["ocean_shipment_cost"] = "NA"

        elif order_shipment_computation["shipment_priority"] == "Urgent":
            shipment_costs["air_shipment_cost"] = "${:.2f}".format(order_air_price)
            shipment_costs["truck_shipment_cost"] = "$45"
            shipment_costs["ocean_shipment_cost"] = "NA"

        elif order_shipment_computation["package_contents"] == "Dangerous":
            shipment_costs["air_shipment_cost"] = "NA"
            shipment_costs["truck_shipment_cost"] = "$25"
            shipment_costs["ocean_shipment_cost"] = "$30"

        else:
            shipment_costs["air_shipment_cost"] = "${:.2f}".format(order_air_price)
            shipment_costs["truck_shipment_cost"] = "$25"
            shipment_costs["ocean_shipment_cost"] = "$30"

        order_dict_to_process[order_id_to_process].update(shipment_costs)
        return order_dict_to_process


class FileProcessor:
    """Processes data to and from a file and a dictionary of objects:"""

    @staticmethod
    def save_data_to_file(file_name, dict_of_orders):
        """ Write data to a file from a dictionary of orders """
        try:
            headings = list(dict_of_orders["1"].keys())
            with open(file_name, 'w', newline='') as file:
                w = csv.DictWriter(file, fieldnames=headings)
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
        try:
            with open(file_name, "r") as file:
                data = csv.reader(file, delimiter=",")
                headers = next(data)
                for row in data:
                    temp_dict = {}
                    order_id = row[0]
                    values = []
                    for x in row:
                        values.append(x)
                    for i in range(len(values)):
                        temp_dict[headers[i]] = values[i]
                    order_dict[order_id] = temp_dict
        except FileNotFoundError:
            open(file_name, "w")
        return order_dict


class Exit:
    @staticmethod
    def exit_program():
        print("\nGood Bye!")
        sys.exit()


class Main:
    @staticmethod
    def main():
        IO.print_welcome()
        order_csv_file = "Order_History.csv"
        order_number = 0
        order_dictionary = FileProcessor.read_data_from_file(order_csv_file)
        order_number += len(order_dictionary.keys())
        while True:
            response = IO.menu_and_choice()
            if response == 1:
                print()
                IO.print_report(order_dictionary)
            elif response == 2:
                order_number +=1
                order_Shipment_Priority, order_Customer_Name, order_Package_Description, order_Package_Contents, order_Package_Weight, order_Package_Volume, order_Delivery_Date = IO.input_new_order()
                updated_order_dictionary, order_id = OrderProcessor.add_new_order(order_dictionary,order_number,order_Shipment_Priority,order_Customer_Name,order_Package_Description,order_Package_Contents,order_Package_Weight,order_Package_Volume,order_Delivery_Date)
                new_order_dictionary = OrderProcessor.compute_shipment_costs(updated_order_dictionary, order_id)
                print("\nBelow is the updated order list:\n")
                IO.print_report(new_order_dictionary)
            elif response == 3:
                print(FileProcessor.save_data_to_file(order_csv_file, new_order_dictionary))
            elif response == 4:
                Exit.exit_program()


if __name__ == "__main__":
    Main.main()
