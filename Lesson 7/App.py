# #Task 30
# say = 65
# for i in range(5):
#     for j in range(5):
#         print(chr(say), end=" ")
#         say+=1
#     print()
# #Task 31
# for i in range (5):
#     for j in range(5):
#         print(chr(65+ i + j), end=" ")
#     print( )
# #Task 32
# for i in range(5):
#     for j in range(5):
#         print(chr(65 + i + j *5), end=" ")
#     print( )
# #Task 33
# for i in range(4, -1, -1):
#     for j in range(5):
#         print(chr(65 + i + j *5), end=" ")
#     print( )
# #Task 34
# for i in range(1, 6):
#     print("*" * i )
# #Task 35
# for i in range(1, 6):
#     print((str(i) + " ")* i)

# #Task 1
# n = 5
# for i in range(n):
#     for space in range(n - 1 - i):
#         print(" ", end="")
#     for j in range(2*i+1):
#         print(chr(65+j), end="")

#     print()
# #Task 2
# n = 4
# for i in range(1, n+1):
#     for j in range(i):
#         print(chr(65+j), end=" ")
#     print()
# for i in range(n- 1, 0, -1):
#     for j in range(i):
#         print(chr(65+j), end=" ")
#     print()
# #Task 3
# n= 5
# for i in range(1, n+1):
#     for j in range(i):
#         print(chr(69-j), end=" ")
#     print()
# #Task 4
# for i in range(1, 5):
#     for j in range(1, 5):
#         print(str(i) + str(j), end=" ")
#     print()
# #Pattern 51
# start = 15
# for i in range(1, 6):
#     for j in range(i):
#         print(start, end=" ")
#         start -= 1
#     print()
# #Pattern 52
# for i in range(1, 6):
#     num = 6 - i      
#     row = []
#     for j in range(i):
#         row.append(num)
#         num+=4
#     row.reverse()
#     for number in row:
#         print(number, end=" ")
#     print()
# #Pattern 55
# for i in range(1, 5):
#     for j in range(i):
#         print(num*num, end=" ")
#         num+=1
#     print()
# #Pattern 60
# for i in range(6):
#     for j in range(i + 1):
#         print(i%2, end=" ")
#     print()
# #Pattern 61
# n= 5
# start = 1
# for i in range(1, n+1):
#     for j in range(i):
#         print(start % 2, end=" ")
#         start += 1
#     print()
# #Pattern 73
# for i in range(5, 0, -1):
#     for j in range(i):
#         print(i, end=" ") 
#     print()
# #Pattern 81
# num = 1
# for i in range(5, 0, -1):
#     for j in range(i):
#         print(num, end=" ")
#     print()
#     num = 1 - num
# #Pattern 171
# n = 4
# for i in range(1, n+1):
#     for j in range(i):
#         print(3-j, end=" ")
#     print()
# for i in range(n-1, 0, -1):
#     for j in range(i):
#         print(3-j, end=" ")
#     print()
#random kitabxanası


#Homework --- Tic Tac Toe

board = [' ' for _ in range(9)]
current_player = 'X'
game_over = False

print("Xanalar 1-dən 9-a qədər nömrələnib:")
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 ")
print("\n Oyun başlayır!")
while not game_over:
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

    move_index = -1
    while True:
        try:
            move_input = input(f"Oyunçu {current_player}, hərəkətini daxil et (1-9): ")
            move = int(move_input)
            if 1 <= move <= 9:
        
                index = move - 1
                if board[index] == ' ':
                    move_index = index
                    break 
                else:
                    print("Bu xana doludur. Zəhmət olmasa, başqa bir xana seçin.")
            else:
                print("Yanlış giriş. Zəhmət olmasa, 1 ilə 9 arasında bir rəqəm daxil edin.")
        except ValueError:
            print("Yanlış giriş. Zəhmət olmasa, bir rəqəm daxil edin.")

    board[move_index] = current_player

    
    winner_found = False
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == current_player:
            winner_found = True
            break
    if not winner_found:
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] == current_player:
                winner_found = True
                break
    if not winner_found:
        if board[0] == board[4] == board[8] == current_player:
            winner_found = True
        elif board[2] == board[4] == board[6] == current_player:
            winner_found = True
    
    if winner_found:
        print(f"\n {board[0]} | {board[1]} | {board[2]} ")
        print("---+---+---")
        print(f" {board[3]} | {board[4]} | {board[5]} ")
        print("---+---+---")
        print(f" {board[6]} | {board[7]} | {board[8]} ")
        print(f"\nTəbrik edirik! Oyunçu {current_player} qalib gəldi!")
        game_over = True
    else:
        draw_found = True
        for square in board:
            if square == ' ':
                draw_found = False
                break
        
        if draw_found:
            print(f"\n1{board[0]} | {board[1]} | {board[2]} ")
            print("---+---+---")
            print(f" {board[3]} | {board[4]} | {board[5]} ")
            print("---+---+---")
            print(f" {board[6]} | {board[7]} | {board[8]} ")
            print("\nOyun heç-heçə bitdi!")
            game_over = True
        else:
            if current_player == 'X':
                current_player = 'O'
            else:
                current_player = 'X'
