from typing import List, Tuple, Dict


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.position: Tuple[int, int] = (row, column)
        self.is_alive: bool = is_alive


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: List[Deck] = self.make_ship()

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.position == (row, column):
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck:
            if not deck.is_alive:
                return "Miss!"

            deck.is_alive = False

            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"

        return "Miss!"

    def make_ship(self) -> List[Deck]:
        start_x, start_y = self.start
        end_x, end_y = self.end

        ship: List[Deck] = []

        while True:
            ship.append(Deck(start_x, start_y))

            if (start_x, start_y) == (end_x, end_y):
                break

            if start_x < end_x:
                start_x += 1
            elif start_x > end_x:
                start_x -= 1

            if start_y < end_y:
                start_y += 1
            elif start_y > end_y:
                start_y -= 1

        return ship


class Battleship:
    def __init__(
            self,
            ships: List[
                Tuple[Tuple[int, int], Tuple[int, int]]
            ]
    ) -> None:
        self.field:\
            Dict[Tuple[Tuple[int, int], ...], Ship] = self._add_ship(ships)

    @staticmethod
    def _add_ship(
        ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> Dict[Tuple[Tuple[int, int], ...], Ship]:
        ships_field: Dict[Tuple[Tuple[int, int], ...], Ship] = {}
        for item in ships:
            ship = Ship(item[0], item[1])
            ships_field[tuple(deck.position for deck in ship.decks)] = ship
        return ships_field

    def fire(self, location: Tuple[int, int]) -> str:
        for ship_decks, ship in self.field.items():
            if location in ship_decks:
                return ship.fire(*location)
        return "Miss!"
