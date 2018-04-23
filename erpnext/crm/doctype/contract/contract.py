# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class Contract(Document):
	def validate(self):
		self.validate_dates()
		self.update_status()

	def on_update_after_submit(self):
		self.update_status()

	def validate_dates(self):
		if self.end_date < self.start_date:
			frappe.throw("End Date cannot be before Start Date!")


	def update_status(self):
		if self.is_signed:
			self.status = get_status(self.start_date, self.end_date)
		else:
			self.status = "Unsigned"


def get_status(start_date, end_date):
	if not end_date:
		return "Active"
	now_date = getdate(nowdate())
	status = "Active" if start_date < now_date < end_date else "Inactive"
	return status


def update_status_for_contracts():
	contracts = frappe.get_all("Contract", filters={"is_signed": True, "docstatus": 1}, fields=["name", "start_date", "end_date"])
	for contract in contracts:
		status = get_status(contract.get("start_date"),
							contract.get("end_date"))
		frappe.db.set_value("Contract", contract.get("name"), "status", status)
