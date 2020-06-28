#!/usr/bin/python3
import random
from time import sleep

class Character:
	def __init__(self,identifier):
		self.hitpoints = 1000
		self.attack = random.randint(20,30)
		self.defense = random.randint(10,20)
		self.attacks = set()
		#self.itemlist = set()
		self.identifier = identifier
	def damage(self,hp):
		self.hitpoints -= hp
	def heal(self,h):
		self.hitpoints += h.hp
	#def additem(self,item):
		#self.itemlist.add(item)
	def taketurn(self):
		pass

class Heart:
	def __init__(self,hp=30):
		self.hp = hp

def validinput(commandstring,validlist):
	x = input(commandstring).upper()
	while x not in validlist:
			print(errormessage)
			sleep(1)
			x = input(commandstring).upper()
	return x

itemmasterlist = {"HEART":Heart(),"SUPER HEART":Heart(60),"ULTRA HEART":Heart(90),"MAX HEART":Heart(120)}

def playerattackprompt(promptstring,damagedealt,enemy):
	print(promptstring)
	sleep(2)
	print("...and inflicted", damagedealt, f"damage to ENEMY {enemy.identifier}!")
	enemy.damage(damagedealt)
	sleep(1)

def enemyattackprompt(promptstring,damagedealt,player):
	print(promptstring)
	sleep(2)
	print(f"...and thus PLAYER {player.identifier} received", damagedealt, "damage!")
	player.damage(damagedealt)
	sleep(1)

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
	itemlist = [i for i in itemmasterlist] * 5
	def __init__(self,identifier):
		super().__init__(identifier)
		self.attacks = {x:PlayerAttack(x,y) for (x,y) in [["SLASH","You swung your blade..."], ["FIREBALL","You hurled a fireball..."], ["ICE CRYSTAL","You chucked an icicle..."]]}
	def taketurn(self,defense):
		while True:
			string = f"Will PLAYER {self.identifier} ATTACK, use ITEMS, or FLEE? "
			command = validinput(string,("ATTACK", "ITEMS", "FLEE"))
			if command == "ATTACK":
				attack = validinput(attackstring,list(self.attacks.keys()) + ["BACK"])
				if attack in self.attacks:
					choice = validinput(whichenemy,[str(i.identifier) for i in enemies] + ["BACK"])
					if choice == "BACK":
						continue
					for enemy in enemies:
						if int(choice) == enemy.identifier:
							break
					playerattackprompt(self.attacks[attack].quote,self.attacks[attack].calcdamage(self.attack,enemy.defense),enemy)
					return True
				if attack == "BACK":
					continue
			elif command == "ITEMS":
				itemstring = f"Which item will PLAYER {self.identifier} choose: HEART (×{self.itemlist.count('HEART')}), SUPER HEART (×{self.itemlist.count('SUPER HEART')}), ULTRA HEART (×{self.itemlist.count('ULTRA HEART')}), or MAX HEART (×{self.itemlist.count('MAX HEART')})? (You can also type \"BACK\" to go back.) "
				items = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
				while items not in self.itemlist:
					if items in itemmasterlist:
						print(itemrelinquish)
						sleep(1)
						items = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
					elif items == "BACK":
						break
					else:
						print(errormessage)
						sleep(1)
						items = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
				if items == "BACK":
					continue
				if self.hitpoints == 1000:
					print("You're already at max HP!")
					sleep(1)
					continue
				self.heal(itemmasterlist[items])
				print(f"You restored {itemmasterlist[items].hp} HP!")
				sleep(1)
				self.itemlist.remove(items)
				self.hitpoints = min(self.hitpoints,1000)
				return True
			elif command == "FLEE":
				print("You ran away!")
				sleep(1)
				return False

class EnemyCharacter(Character):
	def __init__(self,identifier):
		super().__init__(identifier)
		self.attacks = {x:EnemyAttack(x,y) for (x,y) in [["BITE","ENEMY latches its jaws onto you..."], ["STOMP","ENEMY raises its foot onto you..."], ["SMASH","ENEMY charges up to ram into you..."]]}
	def taketurn(self,defense):
		enemystring = f"ENEMY {self.identifier} readies an attack!"
		print(enemystring)
		sleep(1)
		enemychoice = random.choice(list(self.attacks.keys()))
		if enemychoice in self.attacks:
			player = random.choice(players)
			enemyattackprompt(self.attacks[enemychoice].quote,self.attacks[enemychoice].calcdamage(self.attack,player.defense),player)
		return True

def hpstatistics():
	for character in characters:
		if character in players:
			beligerent = "PLAYER"
		else:
			beligerent = "ENEMY"
		print(f"{beligerent} {character.identifier} has {character.hitpoints}/1000 HP.")
		sleep(1)

def defeatstate():
	for character in characters:
		if character in players:
			beligerent = "PLAYER"
		else:
			beligerent = "ENEMY"
		if character.hitpoints <= 0:
			characters.remove(character)
			if character in players:
				players.remove(character)
			else:
				enemies.remove(character)
			print(f"{beligerent} {character.identifier} is defeated!")
			sleep(1)
	if len(enemies) == 0:
		print("All ENEMIES defeated!")
		sleep(1)
		print("YOU WIN!")
		sleep(2)
		print("Your team obtained 43 EXP.")
		sleep(1)
		return True
	elif len(players) == 0:
		print("Your team was defeated!")
		sleep(1)
		print("Your team lost the battle...")
		sleep(2)
		print("GAME OVER")
		sleep(1)
		return True
	else:
		return False

# Start battle
quantity = int(input("How many players? "))
print("ENEMY team attacks!")
#speedstats = [random.randint(0,360) for i in range(2*quantity)]
players = [PlayerCharacter(i+1) for i in range(quantity)]
enemies = [EnemyCharacter(i+1) for i in range(quantity)]
characters = players + enemies
random.shuffle(characters)
sleep(1)
hpstatistics()
errormessage = "Command not recognized. Try again."
itemrelinquish = "You're out of that particular item..."
attackstring = "Which attack will it be: SLASH, FIREBALL, or ICE CRYSTAL? (You can also type \"BACK\" to go back.) "
whichenemy = "Which enemy is to be targeted? (You can also type \"BACK\" to go back.) "
while len(players) != 0 and len(enemies) != 0:
	for character in characters:
		if character in players:
			opponents = enemies
		else:
			opponents = players
		if not character.taketurn([opponent.defense for opponent in opponents]):
			break
		if defeatstate():
			break
	hpstatistics()