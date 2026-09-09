import streamlit as st
import copy
import sys

# Increase recursion depth for deep backtracking trees
sys.setrecursionlimit(5000)

# --- Core Solver Logic ---
def is_valid_move(grid, row, col, number):
    for x in range(9):
        if grid[row][x] == number:
            return False

    for x in range(9):
        if grid[x][col] == number:
            return False

    corner_row = row - row % 3
    corner_col = col - col % 3
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == number:
                return False
    return True

def solve(grid, row, col):
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if grid[row][col] > 0:
        return solve(grid, row, col + 1)

    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve(grid, row, col + 1):
                return True
            grid[row][col] = 0
    return False

# --- App UI Configuration ---
st.set_page_config(page_title="Sudoku Solver", layout="centered")

st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] input {
        text-align: center;
        font-size: 20px;
        font-weight: 600;
        height: 48px;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Sudoku Solver")
st.info("Instructions: Enter given numbers (1-9) in their cells. Enter 0 or leave empty for blank cells, then click Solve.")

SAMPLE_GRID = [
    [4, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 8, 1, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 8, 4, 0, 0, 0, 3],
    [2, 0, 1, 0, 0, 0, 8, 0, 0],
    [0, 0, 5, 9, 0, 0, 0, 0, 0],
    [6, 0, 0, 4, 1, 8, 0, 0, 0],
    [0, 1, 0, 0, 0, 5, 2, 7, 0]
]

# Helper to sync cell keys
def update_board_state(new_board):
    for r in range(9):
        for c in range(9):
            val = new_board[r][c]
            st.session_state[f"cell_{r}_{c}"] = str(val) if val != 0 else ""

# Initialize keys if first load
for r in range(9):
    for c in range(9):
        if f"cell_{r}_{c}" not in st.session_state:
            st.session_state[f"cell_{r}_{c}"] = ""

# --- 9x9 Input Grid ---
current_inputs = [[0 for _ in range(9)] for _ in range(9)]

for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        user_input = cols[c].text_input(
            label=f"r{r}c{c}",
            max_chars=1,
            key=f"cell_{r}_{c}",
            label_visibility="collapsed"
        )
        if user_input.isdigit() and 1 <= int(user_input) <= 9:
            current_inputs[r][c] = int(user_input)
        else:
            current_inputs[r][c] = 0

st.write("")

# --- Control Buttons ---
b_col1, b_col2, b_col3 = st.columns(3)

if b_col1.button("Solve", use_container_width=True, type="primary"):
    grid_copy = copy.deepcopy(current_inputs)

    # Check for empty grid
    if all(grid_copy[r][c] == 0 for r in range(9) for c in range(9)):
        st.warning("Please enter some numbers or click 'Load Sample' first.")
    else:
        # Check for initial contradictions
        valid_board = True
        for r in range(9):
            for c in range(9):
                num = grid_copy[r][c]
                if num != 0:
                    grid_copy[r][c] = 0
                    if not is_valid_move(grid_copy, r, c, num):
                        valid_board = False
                        break
                    grid_copy[r][c] = num
            if not valid_board:
                break

        if not valid_board:
            st.error("The board contains conflicting numbers!")
        else:
            with st.spinner("Solving..."):
                if solve(grid_copy, 0, 0):
                    update_board_state(grid_copy)
                    st.rerun()
                else:
                    st.error("No valid solution exists for this Sudoku board.")

if b_col2.button("Load Sample", use_container_width=True):
    update_board_state(SAMPLE_GRID)
    st.rerun()

if b_col3.button("Clear Board", use_container_width=True):
    empty_grid = [[0 for _ in range(9)] for _ in range(9)]
    update_board_state(empty_grid)
    st.rerun()
    
