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

itemmasterlist = {"HEART":Heart(),"SUPER HEART":Heart(60),"ULTRA HEART":Heart(90),"MAX HEART":Heart(120)}
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

class Attack():
    def __init__(self,name,quote):
        self.name = name
        self.quote = quote
        self.constant = 0
    def calcdamage(self,attacker,defender):
        return int((0.1 * (attacker - defender) * self.constant) + 0.5)

class PlayerAttack(Attack):
    def __init__(self,name,quote):
        super().__init__(name,quote)
        self.constant = random.randint(60, 100)

class EnemyAttack(Attack):
    def __init__(self,name,quote):
        super().__init__(name,quote)
        self.constant = random.randint(30, 70)

class PlayerCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attacks = {x:PlayerAttack(x,y) for (x,y) in [["SLASH","You swung your blade..."], ["FIREBALL","You hurled a fireball..."], ["ICE CRYSTAL","You chucked an icicle..."]]}
        self.items = [i for i in itemmasterlist] * 5
    def taketurn(self,defense):
        while True:
            command = validinput(string,("ATTACK", "ITEMS", "FLEE"))
            if command == "ATTACK":
                attack = validinput(attackstring,list(self.attacks.keys()) + ["BACK"])
                if attack in self.attacks:
                    playerattackprompt(self.attacks[attack].quote,self.attacks[attack].calcdamage(self.attack,defense))
                    return True
                if attack == "BACK":
                    continue
            elif command == "ITEMS":
                itemstring = f"Which item will you choose: HEART (×{self.items.count('HEART')}), SUPER HEART (×{self.items.count('SUPER HEART')}), ULTRA HEART (×{self.items.count('ULTRA HEART')}), or MAX HEART (×{self.items.count('MAX HEART')})? (You can also type \"BACK\" to go back.) "
                items = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
                while items not in self.items:
                    if items in itemmasterlist:
                        print(itemrelinquish)
                        time.sleep(1)
                        items = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
                    elif items == "BACK":
                        break
                    else:
                        print(errormessage)
                        time.sleep(1)
                        items = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
                if items == "BACK":
                    continue
                if player.hitpoints == 1000:
                    print("You're already at max HP!")
                    time.sleep(1)
                    continue
                playerhealprompt(itemmasterlist[items])
                self.items.remove(items)
                player.hitpoints = min(player.hitpoints,1000)
                return True
            elif command == "FLEE":
                print("You ran away!")
                time.sleep(1)
                return False

class EnemyCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attacks = {x:EnemyAttack(x,y) for (x,y) in [["BITE","ENEMY latches its jaws onto you..."], ["STOMP","ENEMY raises its foot onto you..."], ["SMASH","ENEMY charges up to ram into you..."]]}
    def taketurn(self,defense):
        print("ENEMY readies an attack!")
        time.sleep(1)
        enemychoice = random.choice(list(self.attacks.keys()))
        if enemychoice in self.attacks:
            enemyattackprompt(self.attacks[enemychoice].quote,self.attacks[enemychoice].calcdamage(self.attack,defense))

player = PlayerCharacter()
enemy = EnemyCharacter()

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
attackstring = "Which attack will it be: SLASH, FIREBALL, or ICE CRYSTAL? (You can also type \"BACK\" to go back.) "
while True:
    if not player.taketurn(enemy.defense):
        break
    if defeatstate():
        break
    enemy.taketurn(player.defense)
    if defeatstate():
        break
    hpstatistics()