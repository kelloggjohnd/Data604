# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:38:27 2020

@author: x
"""

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# used during the build process
def print_board(board):
    print(np.flip(board,0))

def valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
    #will need function to ensure top row is not full

def place_piece(board, row, col, piece):
    board[row][col] = piece

def get_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def winning_move(board, piece):
  
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True
      
    # Check vertival locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True    

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

    

board = create_board()
game_over = False
turn = 0
game_round = 0  

while not game_over:
    
    if turn == 0:
        col = int(input("Player1 selection: "))
            
        if valid_location(board, col):
            row = get_open_row(board, col)
            place_piece(board, row, col, 1)
                
            if winning_move(board, 1):
                print("Player 1 wins")
                game_over = True
    
    else:
        col = int(input("Player2 selection: "))
            
        if valid_location(board, col):
            row = get_open_row(board, col)
            place_piece(board, row, col, 2)
                
    print_board(board)  
        
    turn += 1
    turn = turn % 2
    game_round += 1
        


      

    