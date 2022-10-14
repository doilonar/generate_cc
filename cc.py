import random
import datetime

sum = 0
card = input("bin:")
current_time = datetime.datetime.now()

#
#verify if card has 6 characters
#

while card.isdigit() != True or len(card) != 6 :
        print("bin error")
        card = input("bin(6 numbers):")

#
#generate card
#

for i in range(6):
        if i%2 == 0:
                y=int(card[i])*2
                if y >= 10:
                        y = y%10+1
                sum += y
        else:
                sum += int(card[i])

for i in range(9):
        x = random.randint(0,9)
        if i%2 == 0:
                y = x*2
                if y >= 10:
                        y = y%10+1
                sum += y
        else:
                sum += x
        card = card + str(x)
sum *= 9

card = card + str(sum%10)
print("card:" + card)

#
#generate bin, year and month
#

cvv = random.randint(0,999)
if cvv <= 9:
    cvv = "00" + str(cvv)
elif cvv <= 99:
    cvv="0" + str(cvv)
month = random.randint(1,12)

year = random.randint(22,26)

while current_time.year%100 == year and current_time.month > month :
    month = random.randint(1,12)

if month <= 9:
        month = "0" + str(month)


print("cvv" + str(cvv))
print("month:" + str(month))
print("year:" + str(year))
