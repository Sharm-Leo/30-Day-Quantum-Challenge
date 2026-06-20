from qiskit import QuantumCircuit
from qiskit import Aer, execute



class TicTacToe:
    def __init__(self):
        super().__init__()
        self.board = [[] for _ in range(9)]
        self.backend = QuantumBackend()
        self.current_player = "X"

    def display_board(self):
        print("\nBoard:")
        for i in range(3):
            row = []
            for j in range(3):
                cell = self.board[i*3 + j]
                row.append(",".join(cell) if cell else " ")
            print(" | ".join(row))
        print()

    def make_move(self, position):
        if self.board[position] == []:
            self.board[position] = self.current_player
            return True
        return False
    
    def get_quantum_move(self):
        move = input(f"Player {self.current_player}, choose two squares (e.g. 1 4): ")
        a, b = [int(x) - 1 for x in move.split()]
        return a, b
    
    def apply_quantum_move(self, a, b, move_id):
        qc = self.backend.qc

        # Put first qubit into superposition
        qc.h(a)

        # Entangle with second qubit
        qc.cx(a, b)

        # Mark board with label (e.g., X1, O2)
        label = f"{self.current_player}{move_id}"
        self.board[a].append(label)
        self.board[b].append(label)

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    

    def game_loop(self):
        # while True:
        #     self.display_board()
        #     move = int(input(f"Player {self.current_player}, choose (1-9): ")) - 1
        #     if self.make_move(move):
        #         self.switch_player()
        #     else:
        #         print("Invalid move!")
        move_id = 1

        while True:
            self.display_board()
            command = input("Enter move (e.g. 1 4) or 'collapse': ")
            if command == "collapse":
                self.collapse_board()
                self.display_board()
                self.evaluate_game()
                print(self.backend.qc.draw())
                break

            a, b = [int(x) - 1 for x in command.split()]

            if self.board[a] == [] and self.board[b] == []:
                self.apply_quantum_move(a, b, move_id)
                move_id += 1
                print(self.backend.qc.draw())
                self.switch_player()
            else:
                print("Invalid quantum move!")
    

    def collapse_board(self):
        qc = self.backend.qc

        # Measure all qubits
        qc.measure(range(9), range(9))

        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1).result()

        counts = result.get_counts()
        bitstring = list(counts.keys())[0]

        print("Collapsed state:", bitstring)

        # Update board
        for i in range(9):
            if bitstring[8 - i] == "1":
                self.board[i] = "X"
            else:
                self.board[i] = "O"
    def check_winner(self):
        win_patterns = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        winners = []

        for pattern in win_patterns:
            values = [self.board[i] for i in pattern]
            if values[0] == values[1] == values[2]:
                winners.append(values[0])

        return winners

    def evaluate_game(self):
        winners = self.check_winner()

        if not winners:
            print("No winner.")
        elif len(set(winners)) == 1:
            print(f"Winner: {winners[0]}")
        else:
            print("Quantum tie! Both players win (fractional score).")

class QuantumBackend:
    def __init__(self):
        self.qc = QuantumCircuit(9, 9)

    def reset(self):
        self.qc = QuantumCircuit(9, 9)

if __name__ == "__main__":
    game = TicTacToe()
    game.game_loop()