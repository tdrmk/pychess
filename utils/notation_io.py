from __future__ import annotations

from typing import List

from .move import Move

"""
Notation file format:
Numbered pair of moves separated by spaces. (Look at sample)
Note: Number is necessary, however ignored while reading the moves.
It is not necessary to indicate en-passant. In case necessary, use `(ep)` to indicate (NOTE no spaces).

Sample:
1. e4 e5
2. f4 exf4
3. Bc4 Qh4+
4. Kf1 b5
5. Bxb5 Nf6
6. Nf3 Qh6
7. d3 Nh5
8. Nh4 Qg5
9. Nf5 c6
10. g4 Nf6
11. Rg1 cxb5
12. h4 Qg6
13. h5 Qg5
14. Qf3 Ng8
15. Bxf4 Qf6
16. Nc3 Bc5
17. Nd5 Qxb2
18. Bd6 Bxg1
19. e5 Qxa1+
20. Ke2 Na6
21. Nxg7+ Kd8
22. Qf6+ Nxf6
23. Be7#	
	
"""


def write_notations(moves: List[Move], file: str = 'moves.txt'):
	# Takes in the sequence of moves from the start (first move being white)
	# And writes the notations of the moves to the specified file.
	with open(file, 'w') as f:
		for idx, move in enumerate(moves, start=1):
			if idx % 2:
				f.write(f"{idx//2} {move.notation}")
			else:
				f.write(f" {move.notation}\n")


def read_notations(file: str = 'moves.txt') -> List[str]:
	# Reads file and returns array of notation (string).
	move_notations = []
	with open(file) as f:
		for line in f:
			_, *moves = line.split()
			move_notations.extend(moves)
	return move_notations
