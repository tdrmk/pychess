from collections import defaultdict
from functools import wraps


class Memoize:
	def __init__(self):
		self._stored_values_ = dict()

	def memoize(self, _fn):
		@wraps(_fn)
		def wrapper(*args):
			key = (_fn.__name__, *args)
			if key in self._stored_values_:
				return_value = self._stored_values_[key]
				# print('Returning memoized value', _fn.__name__)
				return return_value
			return_value = _fn(*args)
			print('Memoizing', key)
			self._stored_values_[key] = return_value
			return return_value

		return wrapper

	def invalidate(self, _fn):
		@wraps(_fn)
		def wrapper(*args):
			# remove all entries
			print('Invalidate', _fn.__name__)
			self._stored_values_.clear()
			return _fn(*args)

		return wrapper
