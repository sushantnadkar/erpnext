# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TourFlow(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_tour(tour_name=""):
	if not tour_name:
		return
	doc = frappe.get_doc("Tour Flow", tour_name)
	steps = []
	for row in doc.flow:
		step = {
			"title": row.name1,
			"element": row.css_selector,
			"content": row.description,
		}
		steps.append(step)
	print "steps", steps
	return {
		"steps": steps
	}
