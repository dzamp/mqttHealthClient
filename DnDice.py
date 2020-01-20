import os, random, time
import struct

def throw_dice():
    data = os.urandom(4)
    dice = struct.unpack('I',data)[0]%6 +1 # range from 1 - 6
    print("Dice number is " + str(dice))
    return dice

def throw_dice_using_random():
    print("Rad int is " +str(random.randint(1,6)))

def throw_using_sys_random():
    print("system random is " + str(random.SystemRandom().random()* struct.unpack('I',os.urandom(4))[0]% 6 +1))


def main():
   txt = raw_input("Set number of dice throws: ")
   total_throws = int(txt)
   for i in range(0, total_throws):
       time.sleep(0.003)
       throw_dice_using_random()

   for i in range(0, total_throws):
       time.sleep(0.003)
       throw_using_sys_random()

   for i in range(0,total_throws):
        time.sleep(0.03)
        print("No." + str(i)),
        dice = throw_dice()
        if (dice < 3) :
            print "Rethrowing dice ... ",
            re_dice = throw_dice()

if __name__ == '__main__':
    main()