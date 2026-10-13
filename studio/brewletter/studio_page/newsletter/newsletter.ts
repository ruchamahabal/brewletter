import { watch } from "vue"

export default function setup(context) {
	const { newsletter, formData, router, call, toast } = context

	watch(
		() => newsletter.doc,
		(doc) => {
			if (!doc) return
			formData.value = {
				subject: doc.subject,
				content: doc.content,
				schedule_sending: Boolean(doc.schedule_sending),
				send_email_at: doc.send_email_at,
			}
		},
		{ immediate: true },
	)

	async function save() {
		try {
			if (newsletter.doc) {
				await newsletter.setValue.submit({ ...formData.value })
				toast.success("Newsletter saved")
				return
			}
			const doc = await call("frappe.client.insert", { doc: { doctype: "SD Newsletter", ...formData.value } })
			toast.success("Newsletter created")
			router.push(`/newsletter/${doc.name}`)
		} catch {
			toast.error("Could not save the newsletter")
		}
	}

	async function sendNow() {
		try {
			await newsletter.send_newsletter.submit()
			await newsletter.reload()
			toast.success("Newsletter sent")
		} catch {
			toast.error("Could not send the newsletter")
		}
	}

	return { save, sendNow }
}
