import streamlit as st
import copy

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

st.title("🧩 Sudoku Solver")

# Clear instructions for the user
st.info("💡 **Instructions:** Enter the given numbers (1–9) into their respective cells. For any empty cells, enter **0** (or leave them empty), then click **Solve**.")

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

if "grid" not in st.session_state:
    st.session_state.grid = [[0 for _ in range(9)] for _ in range(9)]

# --- 9x9 Input Grid ---
current_inputs = [[0 for _ in range(9)] for _ in range(9)]

for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        val = st.session_state.grid[r][c]
        display_val = str(val) if val != 0 else ""
        user_input = cols[c].text_input(
            label=f"r{r}c{c}",
            value=display_val,
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

if b_col1.button("⚡ Solve", use_container_width=True, type="primary"):
    grid_copy = copy.deepcopy(current_inputs)
    
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
        st.error("The initial board contains conflicting numbers!")
    else:
        with st.spinner("Solving puzzle..."):
            if solve(grid_copy, 0, 0):
                st.session_state.grid = grid_copy
                st.rerun()
            else:
                st.error("No valid solution exists for this Sudoku board.")

if b_col2.button("📋 Load Sample", use_container_width=True):
    st.session_state.grid = copy.deepcopy(SAMPLE_GRID)
    st.rerun()

if b_col3.button("🗑️ Clear Board", use_container_width=True):
    st.session_state.grid = [[0 for _ in range(9)] for _ in range(9)]
    st.rerun()