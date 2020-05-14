import re
from collections import namedtuple


class Square(namedtuple('Square', ['x', 'y'])):
	__slots__ = ()

	def __bool__(self):
		# Checks if square is in bounds of the board
		# Used to check if square is valid
		return 0 <= self.x < 8 and 0 <= self.y < 8

	def __str__(self):
		return f"[{self.x}, {self.y}]"

	def __repr__(self):
		return f'Square(x={self.x}, y={self.y})'

	@property
	def notation(self):
		return f"{chr(97 + self.x)}{8 - self.y}"
		pass

	@classmethod
	def from_notation(cls, notation: str):
		if re.match("&[a-h][1-8]$", notation):
			x, y = ord(notation[0]) - 97, 8 - int(notation[1])
			return cls(x=x, y=y)
