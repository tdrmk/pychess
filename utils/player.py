from enum import Enum


class Player(Enum):
	WHITE = 'WHITE'
	BLACK = 'BLACK'

	def __invert__(self):
		return Player.BLACK if self.value == 'WHITE' else Player.WHITE

	@property
	def enemy(self):
		# Returns the enemy of the current player,
		# also obtained if ~ operation is used
		return ~self

	def __str__(self):
		return f"{self.value}"

	def __repr__(self):
		return f"Player.{self.name}"

