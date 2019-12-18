import random
answer = random.randint(1,1000)
guess=int(input("Guess the number"))
if guess!=answer:
    difference = abs(guess-answer)
    guess=int(input("Good try. But wrong answer.Try Again"))
    while guess!=answer:
        temp = abs(guess-answer)
        message =""
        if difference>100:
            message = "Far far away in a distance galaxy and "
        elif difference>10:
            message = "You're closer now and "
        else:
            message = "Very, very close and "
            
        if temp>difference:
            guess = int(input(message + "going further"))
        else:
            guess = int(input(message + "getting close"))
        difference = temp
        

print("Yes!! Thats it! Correct Answer.")
