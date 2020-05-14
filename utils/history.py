from typing import TypeVar, Generic, List

T = TypeVar('T')


class History(Generic[T]):
	def __init__(self):
		self._entries_: List[T] = []
		self._index_ = 0

	def push(self, item: T):
		self._entries_ = self._entries_[:self._index_]
		self._entries_.append(item)
		self._index_ += 1

	def back(self) -> T:
		if self._index_ > 0:
			self._index_ -= 1
			return self._entries_[self._index_]

	def forward(self) -> T:
		if self._index_ < len(self._entries_):
			item = self._entries_[self._index_]
			self._index_ += 1
			return item

	def top(self) -> T:
		if self._index_ > 0:
			return self._entries_[self._index_ - 1]
