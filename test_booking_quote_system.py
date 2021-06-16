#!/usr/bin/env python3

"""
Topic: Tests for Booking Quote System
Change_Log: IBRAR, Added tests for OrderProcessor class, 06/15/2021
"""

import sys
import pytest
import booking_quote_system


def test_add_new_order():
    order_dict = {'1': {'order_id': '1', 'shipment_priority': 'Urgent', 'customer_name': 'Xyz', 'package_description': 'Ipod', 'package_contents': 'Safe', 'package_weight': '0.5', 'package_volume': '0.5', 'delivery_date': '2021-06-18'}}
    test_dict = {}
    test_order_dict = booking_quote_system.OrderProcessor.add_new_order(test_dict,'1','Urgent','Xyz','Ipod','Safe','0.5','0.5','2021-06-18')[0]
    assert test_order_dict == order_dict

def test_add_new_order_2():
    order_dict = {'1': {'order_id': '1', 'shipment_priority': 'Urgent', 'customer_name': 'Xyz', 'package_description': 'Ipod', 'package_contents': 'Safe', 'package_weight': '0.5', 'package_volume': '0.5', 'delivery_date': '2021-06-18'}}
    test_order_dict = booking_quote_system.OrderProcessor.add_new_order(order_dict,'2','Normal','Abc','Iphone','Dangerous','1','1','2021-06-21')[0]
    assert len(test_order_dict.keys()) == 2

def test_compute_shipping_cost():
    order_dict = {'1': {'order_id': '1', 'shipment_priority': 'Urgent', 'customer_name': 'Xyz', 'package_description': 'Ipod', 'package_contents': 'Safe', 'package_weight': '0.5', 'package_volume': '0.5', 'delivery_date': '2021-06-18', 'air_shipment_cost': '$10.00', 'truck_shipment_cost': '$45', 'ocean_shipment_cost': 'NA'}}
    test_dict = {'1': {'order_id': '1', 'shipment_priority': 'Urgent', 'customer_name': 'Xyz', 'package_description': 'Ipod', 'package_contents': 'Safe', 'package_weight': '0.5', 'package_volume': '0.5', 'delivery_date': '2021-06-18'}}
    test_order_dict = booking_quote_system.OrderProcessor.compute_shipment_costs(test_dict,'1')
    assert test_order_dict == order_dict

def test_compute_shipping_cost_2():
    test_dict = {'1': {'order_id': '1', 'shipment_priority': 'Urgent', 'customer_name': 'Xyz', 'package_description': 'Ipod', 'package_contents': 'Safe', 'package_weight': '0.5', 'package_volume': '0.5', 'delivery_date': '2021-06-18'}}
    test_order_dict = booking_quote_system.OrderProcessor.compute_shipment_costs(test_dict,'1')
    assert test_order_dict['1']['ocean_shipment_cost'] == 'NA'