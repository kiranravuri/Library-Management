# Copyright (c) 2024, kiran and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Book(Document):
    def validate(self):
        self.calculate_available_quantity()

    def calculate_available_quantity(self):
        issued_books = frappe.get_all('Transactions', filters={'book': self.name, 'status': 'Issued'}, fields=['book_name'])
        self.available_quantity = self.quantity - len(issued_books)

