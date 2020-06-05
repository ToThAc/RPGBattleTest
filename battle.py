#!/usr/bin/python3
import random
import time

class Character:
	def __init__(self):
		self.hitpoints = 1000
		self.attack = random.randint(20,30)
		self.defense = random.randint(10,20)
		self.attacks = set()
		self.items = set()
	def damage(self,hp):
		self.hitpoints -= hp
	def heal(self,h):
		self.hitpoints += h.hp
	def additem(self,item):
		self.items.add(item)
	def taketurn(self):
		pass

class Heart:
	def __init__(self,hp=30):
		self.hp = hp

def validinput(commandstring,validlist):
    x = input(commandstring)
    while x not in validlist:
            print(errormessage)
            time.sleep(1)
            x = input(commandstring)
    return x

heart = Heart()
superheart = Heart(60)
ultraheart = Heart(90)
maxheart = Heart(120)

command = ''

def playerattackprompt(promptstring,damagedealt):
    print(promptstring)
    time.sleep(2)
    print("...and inflicted", damagedealt, "damage to ENEMY!")
    enemy.damage(damagedealt)
    time.sleep(1)

def playerhealprompt(item):
    player.heal(item)
    print(f"You restored {item.hp} HP!")
    time.sleep(1)

def enemyattackprompt(promptstring,damagedealt):
    print(promptstring)
    time.sleep(2)
    print("...and thus you received", damagedealt, "damage!")
    player.damage(damagedealt)
    time.sleep(1)

class PlayerCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attacks = ('SLASH', 'FIREBALL', 'ICE CRYSTAL')
    def taketurn(self):
        command = validinput(string,("ATTACK", "ITEMS", "FLEE"))
        if command == "ATTACK":
            attack = validinput(attackstring,self.attacks)
            if attack == "SLASH":
                playerattackprompt("You swung your blade...",damageslash)
            elif attack == "FIREBALL":
                playerattackprompt("You hurled a fireball...",damagefireball)
            elif attack == "ICE CRYSTAL":
                playerattackprompt("You chucked an icicle...",damageicecrystal)
            return True
        elif command == "ITEMS":
            itemstring = f"Which item will you choose: HEART (×{itemlist.count('HEART')}), SUPER HEART (×{itemlist.count('SUPER HEART')}), ULTRA HEART (×{itemlist.count('ULTRA HEART')}), or MAX HEART (×{itemlist.count('MAX HEART')})? "
            items = validinput(itemstring,itemmasterlist)
            while items not in itemlist:
                if items in itemmasterlist:
                    print(itemrelinquish)
                    time.sleep(1)
                    items = validinput(itemstring,itemmasterlist)
                else:
                    print(errormessage)
                    time.sleep(1)
                    items = validinput(itemstring,itemmasterlist)
            if items == "HEART":
                playerhealprompt(heart)
            elif items == "SUPER HEART":
                playerhealprompt(superheart)
            elif items == "ULTRA HEART":
                playerhealprompt(ultraheart)
            elif items == "MAX HEART":
                playerhealprompt(maxheart)
            if player.hitpoints > 1000:
                print("You're already at max HP!")
                player.hitpoints = 1000
                time.sleep(1)
            itemlist.remove(items)
            return True
        elif command == "FLEE":
            print("You ran away!")
            time.sleep(1)
            return False

class EnemyCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attacks = ('BITE', 'STOMP', 'SMASH')
    def taketurn(self):
        print("ENEMY readies an attack!")
        time.sleep(1)
        enemychoice = random.choice(self.attacks)
        if enemychoice == "BITE":
            enemyattackprompt("ENEMY latches its jaws onto you...",damagebite)
        elif enemychoice == "STOMP":
            enemyattackprompt("ENEMY raises its foot onto you...",damagestomp)
        elif enemychoice == "SMASH":
            enemyattackprompt("ENEMY charges up to ram into you...",damagesmash)

player = PlayerCharacter()
enemy = EnemyCharacter()
itemlist = ["HEART"] * 5 + ["SUPER HEART"] * 5 + ["ULTRA HEART"] * 5 + ["MAX HEART"] * 5
itemmasterlist = ("HEART", "SUPER HEART", "ULTRA HEART", "MAX HEART")
constantslash = random.randint(60, 100)
constantfireball = random.randint(60, 100)
constanticecrystal = random.randint(60, 100)
constantbite = random.randint(30, 70)
constantstomp = random.randint(30, 70)
constantsmash = random.randint(30, 70)
damageslash = int((0.1 * (player.attack - enemy.defense) * constantslash) + 0.5)
damagefireball = int((0.1 * (player.attack - enemy.defense) * constantfireball) + 0.5)
damageicecrystal = int((0.1 * (player.attack - enemy.defense) * constanticecrystal) + 0.5)
damagebite = int((0.1 * (enemy.attack - player.defense) * constantbite) + 0.5)
damagestomp = int((0.1 * (enemy.attack - player.defense) * constantstomp) + 0.5)
damagesmash = int((0.1 * (enemy.attack - player.defense) * constantsmash) + 0.5)

def hpstatistics():
    print(f"ENEMY has {enemy.hitpoints}/1000 HP.")
    time.sleep(1)
    print(f"You currently have {player.hitpoints}/1000 HP.")
    time.sleep(1)

def defeatstate():
    if enemy.hitpoints <= 0:
        print("ENEMY is defeated!")
        time.sleep(1)
        print("YOU WIN!")
        time.sleep(2)
        print("You obtained 43 EXP.")
        time.sleep(1)
        return True
    elif player.hitpoints <= 0:
        print("You were defeated!")
        time.sleep(1)
        print("You lost the battle...")
        time.sleep(2)
        print("GAME OVER")
        time.sleep(1)
        return True
    else:
        return False

# Start battle
print("ENEMY attacks!")
time.sleep(1)
hpstatistics()
string = "Will you ATTACK, use ITEMS, or FLEE? "
errormessage = "Command not recognized. Try again."
itemrelinquish = "You're out of that particular item..."
attackstring = "Which attack will it be: SLASH, FIREBALL, or ICE CRYSTAL? "
while True:
    if not player.taketurn():
        break
    if defeatstate():
        break
    enemy.taketurn()
    if defeatstate():
        break
    hpstatistics()