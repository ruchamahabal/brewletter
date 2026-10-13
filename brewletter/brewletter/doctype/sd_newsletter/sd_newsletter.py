# Copyright (c) 2025, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class SDNewsletter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		content: DF.MarkdownEditor | None
		schedule_sending: DF.Check
		send_email_at: DF.Datetime | None
		status: DF.Literal["", "Sent", "Not Sent"]
		subject: DF.SmallText | None
		total_recipients: DF.Int
		total_views: DF.Int
		view_rate: DF.Percent
	# end: auto-generated types

	@frappe.whitelist()
	def send_newsletter(self):
		recipients = frappe.get_all("Subscriber", filters={"status": "Active"}, pluck="email")
		if not recipients:
			frappe.throw(_("There are no active subscribers"))

		frappe.sendmail(
			recipients=recipients,
			subject=self.subject,
			message=frappe.utils.md_to_html(self.content or ""),
			reference_doctype=self.doctype,
			reference_name=self.name,
		)
		self.db_set({"status": "Sent", "total_recipients": len(recipients)})
