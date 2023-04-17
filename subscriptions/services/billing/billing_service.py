class BillingService:
	"""
	This is just a sample of how could the billing service look like.
	No code implementation for this part.
	"""
	def call(self, subscription):
		if self._process_billing(subscription.customer.id, subscription.price):
			return print(f"Succesfully billed {subscription.customer.id} for subscription {subscription.id}")
		else:
			raise BillingError(f"Failed to bill {subscription.customer.id}")
	def _process_billing(self, customer_id, amount):
		"""
		Ideally this is the place which is responsible for processing the billing
		and also enqueueing a message that the billing is done. Then this message
		will be picked up by a Job that actually sends the invoice via email.
		"""
		if customer_id and amount:
			return True
		else:
			return False

class BillingError(Exception):
	pass