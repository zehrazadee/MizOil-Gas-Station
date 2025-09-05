# print('''
# ********** GAME **********
# Rock = r
# Paper = p
# Scissors = s
# Spock = spock
# Lizard = l
# ''')
# player = input('Enter:')
# import random
# computer = random.choice(['r', 'p', 's', 'spock', 'l'])
# print('\nPlayer:', player)
# print('Computer:', computer,'\n\n')
# if(player==computer):
#     print('Draw')
# elif player == 'r' and computer == 'p':
#     print('Computer won')
# elif player == 'r' and computer == 's':
#     print('Player won')
# elif player == 'p' and computer == 'r':
#     print('Player won')
# elif player == 'p' and computer == 's':
#     print('Computer won')
# elif player == 's' and computer == 'r':
#     print('Computer won')
# elif player == 's' and computer == 'p':
#     print('Player won')
# elif player == 'l' and computer == 'spock':
#     print('Player won')
# elif player =='spock' and computer == 'l':
#     print('Computer won')
# elif player == 'spock' and computer =='s':
#     print('Player won')
# elif player == 's' and computer == 'spock':
#     print('Computer won')
# elif player == 'spock' and computer == 'p':
#     print('Computer won')
# elif player == 'p' and computer == 'spock':
#     print('Player won')
# elif player =='spock' and computer == 'r':
#     print('Player won')
# elif player == 'r' and computer == 'spock':
#     print('Computer won')
# elif player =='l' and computer == 'r':
#     print('Computer won')
# elif player =='r' and computer == 'l':
#     print('Player won')
# elif player == 'p' and computer == 'l':
#     print('Computer won')
# elif player == 'l' and computer == 'p':
#     print('Player won')
# elif player == 's' and computer == 'l':
#     print('Player won')
# elif player == 'l' and computer == 's':
#     print('Computer won')
# else:
#     print('Wrong')


#Homework
#Task1
eded = int(input("Bir ədəd daxil edin:"))
if eded % 2 == 0:
       print("Bu ədəd cütdür.")
else:
        print("Bu ədəd təkdir.")
#Task2
eded1 = int(input("Birinici ədədi daxil edin:"))
eded2 = int(input("Ikinci ədədi daxil edin:"))
if eded1 < eded2:
      print("Kiçik ədəd:", eded1)
else:
      print("Kiçik ədəd:", eded2)
#Task3
eded = int(input("Bir ədəd daxil edin:"))
if eded > 0:
      print("Bu ədəd müsbətdir.")
elif eded < 0:
     print("Bu ədəd mənfidir.")
else:
     print("Ədəd sıfırdır.")
#Task4
eded1 =float(input("Birinci ədədi daxil edin:"))
eded2 =float(input("Ikinci ədədi daxil edin:"))
if eded1 + eded2:
      print("Ədədlərin cəmi:",  eded1+eded2)
if eded1 - eded2:
      print("Ədədlərin fərqi:", eded1-eded2)
if eded1%eded2:
      print("Ədədlərin qisməti:", eded1%eded2)
if eded1*eded2:
    print("Ədədlərin hasili:", eded1*eded2)
#Task5
eded = int(input("Ədəd daxil edin:"))
if 1<= eded <= 50:
     print("Ədəd bu aralığa daxildir.")
else:
     print("Ədəd bu aralığa daxil deyil.")