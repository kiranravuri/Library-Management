# Copyright (c) 2024, kiran and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Transactions(Document):
    def validate(self):
        if self.status == "Returned":
            self.calculate_fees()

    def calculate_fees(self):
        if self.return_date and self.issue_date:
            # Calculate the number of days the book was issued
            days_issued = (self.return_date - self.issue_date).days
            rent_fee = 50 if days_issued <= 7 else 50 + (days_issued - 7) * 10  # Rs.50 base + Rs.10/day for overdue
            self.fee = rent_fee

            # Update member's outstanding debt
            member = frappe.get_doc('Library Member', self.library_member)
            member.outstanding_debt += rent_fee
            member.save()

            # Update the book status to 'Available' after return
            book = frappe.get_doc('Book', self.book)
            book.status = 'Available'
            book.save()

