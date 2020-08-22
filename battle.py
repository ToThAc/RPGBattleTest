#!/usr/bin/python3
import random
import sys
from time import sleep
from tkinter import *
from tkinter import ttk
import tklayout as tkb

class Character:
	def __init__(self,identifier):
		self.hitpoints = IntVar(root,value=1000)
		self.attack = random.randint(20,30)
		self.defense = random.randint(10,20)
		self.attacks = set()
		#self.itemlist = set()
		self.identifier = identifier
	def damage(self,hp):
		self.hitpoints.set(self.hitpoints.get() - hp)
	def heal(self,h):
		self.hitpoints.set(self.hitpoints.get() + h.hp)
	#def additem(self,item):
		#self.itemlist.add(item)
	def taketurn(self):
		pass

class Heart:
	def __init__(self,hp=30):
		self.hp = hp

class Revive:
	def __init__(self,hp=1000):
		self.hp = hp

def validinput(commandstring,validlist):
	x = input(commandstring).upper()
	while x not in validlist:
			print(errormessage)
			sleep(1)
			x = input(commandstring).upper()
	return x

def playerchoice(beligerents,whichprompt):
	if len(beligerents) == 1:
		beligerent = beligerents[0]
	else:
		choiceprompt = validinput(whichprompt,[str(i.identifier) for i in beligerents] + ["BACK"])
		if choiceprompt == "BACK":
			return False
		for beligerent in beligerents:
			if int(choiceprompt) == beligerent.identifier:
				break
	return beligerent

heartlist = {"HEART":Heart(),"SUPER HEART":Heart(60),"ULTRA HEART":Heart(90),"MAX HEART":Heart(120)}
revivelist = {"REVIVE":Revive(500),"DELUXE REVIVE":Revive()}
itemmasterlist = {**heartlist, **revivelist}

def build_hpCount(parent):
	row = 0
	for character in characters:
		if character in players:
			beligerent = "PLAYER"
		else:
			beligerent = "ENEMY"
		LABEL = Label(parent)
		LABEL["text"] = f"{beligerent} {character.identifier}"
		LABEL.grid(row=row,column=0,padx=10,pady=5,sticky=NSEW)
		hp = ttk.Progressbar(parent)
		hp["orient"] = "horizontal"
		#hp["length"] = "1000"
		hp["mode"] = "determinate"
		hp["maximum"] = "1000"
		hp["variable"] = character.hitpoints
		hp.grid(row=row,column=1,padx=10,pady=5,sticky=NSEW)
		row += 1

nextplayer = 0
def app_idle(root):
	global nextplayer
	while characters[nextplayer] not in players:
		characters[nextplayer].taketurn()
		if defeatstate():
			root.quit()
		nextplayer = (nextplayer + 1) % len(characters)
	attackbutton["state"] = "active"
	itemsbutton["state"] = "active"
	fleebutton["state"] = "active"

attackbutton = None
itemsbutton = None
fleebutton = None

def mainapp():
	def build_attack(parent):
		global attackbutton
		attackbutton = Button(parent,text="ATTACK",justify=CENTER,fg="deepskyblue",state="disabled",command=attackapp)
		attackbutton.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_items(parent):
		global itemsbutton
		itemsbutton = Button(parent,text="ITEMS",justify=CENTER,fg="gold",state="disabled",command=itemsapp)
		itemsbutton.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_flee(parent):
		global fleebutton
		fleebutton = Button(parent,text="FLEE",justify=CENTER,fg="red",state="disabled")
		fleebutton.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	lo = tkb.AppLayout()
	config_opts = {"borderwidth":3,"relief":GROOVE}
	grid_opts = {"sticky": NSEW}
	aif = lo.row_elements(["A","I","F"],config_opts,grid_opts)
	app = lo.column_elements([aif,"H"],config_opts,grid_opts)
	lo.create_layout(root,app,row=0,column=0,row_weight=1,column_weight=1)
	lo.build_elements({"A":build_attack,"I":build_items,"F":build_flee,"H":build_hpCount})
	root.after_idle(app_idle,root)

def slashbutton():
	enemychoiceapp("SLASH")

def fireballbutton():
	enemychoiceapp("FIREBALL")

def icecrystalbutton():
	enemychoiceapp("ICE CRYSTAL")

def attackapp():
	def build_slash(parent):
		w = Button(parent,text="SLASH",justify=CENTER,fg="silver",command=slashbutton)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_fireball(parent):
		w = Button(parent,text="FIREBALL",justify=CENTER,fg="orangered",command=fireballbutton)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_icecrystal(parent):
		w = Button(parent,text="ICE CRYSTAL",justify=CENTER,fg="paleturquoise",command=icecrystalbutton)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_back(parent):
		w = Button(parent,text="BACK",justify=CENTER,fg="black",command=mainapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	lo = tkb.AppLayout()
	config_opts = {"borderwidth":3,"relief":GROOVE}
	grid_opts = {"sticky": NSEW}
	sfi = lo.row_elements(["SL","FB","IC"],config_opts,grid_opts)
	sfib = lo.column_elements([sfi,"B"],config_opts,grid_opts)
	app = lo.column_elements([sfib,"H"],config_opts,grid_opts)
	lo.create_layout(root,app,row=0,column=0,row_weight=1,column_weight=1)
	lo.build_elements({"SL":build_slash,"FB":build_fireball,"IC":build_icecrystal,"B":build_back,"H":build_hpCount})
	root.mainloop()

def itemsapp():
	def build_heart(parent):
		w = Button(parent,text="HEART",justify=CENTER,fg="magenta",command=playerchoiceapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_superheart(parent):
		w = Button(parent,text="SUPER HEART",justify=CENTER,fg="magenta",command=playerchoiceapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_ultraheart(parent):
		w = Button(parent,text="ULTRA HEART",justify=CENTER,fg="magenta",command=playerchoiceapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_maxheart(parent):
		w = Button(parent,text="MAX HEART",justify=CENTER,fg="magenta",command=playerchoiceapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_revive(parent):
		w = Button(parent,text="REVIVE",justify=CENTER,fg="darkorchid",command=playerchoiceapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_deluxerevive(parent):
		w = Button(parent,text="DELUXE REVIVE",justify=CENTER,fg="darkorchid",command=playerchoiceapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	def build_back(parent):
		w = Button(parent,text="BACK",justify=CENTER,fg="black",command=mainapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	lo = tkb.AppLayout()
	config_opts = {"borderwidth":3,"relief":GROOVE}
	grid_opts = {"sticky": NSEW}
	hsum = lo.row_elements(["H","SH","UH","MH"],config_opts,grid_opts)
	rd = lo.row_elements(["R","DR"],config_opts,grid_opts)
	hrb = lo.column_elements([hsum,rd,"B"],config_opts,grid_opts)
	app = lo.column_elements([hrb,"HP"],config_opts,grid_opts)
	lo.create_layout(root,app,row=0,column=0,row_weight=1,column_weight=1)
	lo.build_elements({"H":build_heart,"SH":build_superheart,"UH":build_ultraheart,"MH":build_maxheart,"R":build_revive,"DR":build_deluxerevive,"B":build_back,"HP":build_hpCount})
	root.mainloop()

enemy_index = 0

def enemychoiceapp(attack):
	global enemy_index
	enemy_index = 0
	def build_choice(parent):
		global enemy_index
		enemy = enemies[enemy_index]
		#print(f"{beligerent}x{enemy.identifier}")
		def handler(enemy=enemy):
			player = characters[nextplayer]
			print(player.attacks[attack].quote)
			sleep(2)
			print("...and inflicted", player.attacks[attack].calcdamage(player.attack,enemy.defense), f"damage to ENEMY {enemy.identifier}!")
			enemy.damage(player.attacks[attack].calcdamage(player.attack,enemy.defense))
			sleep(1)
		w = Button(parent,text=f"ENEMY {enemy.identifier}",justify=CENTER,fg="black",command=handler)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
		enemy_index += 1
	def build_back(parent):
		w = Button(parent,text="BACK",justify=CENTER,fg="black",command=mainapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	lo = tkb.AppLayout()
	config_opts = {"borderwidth":3,"relief":GROOVE}
	grid_opts = {"sticky": NSEW}
	enemy_dict = {}
	for enemy in enemies:
		enemy_dict.update({f"ENEMY {enemy.identifier}":build_choice})
	choiceplayer = lo.row_elements(list(enemy_dict),config_opts,grid_opts)
	cb = lo.column_elements([choiceplayer,"B"],config_opts,grid_opts)
	app = lo.column_elements([cb,"H"],config_opts,grid_opts)
	lo.create_layout(root,app,row=0,column=0,row_weight=1,column_weight=1)
	enemy_dict.update({"B":build_back,"H":build_hpCount})
	lo.build_elements(enemy_dict)

player_index = 0

def playerchoiceapp():
	global player_index
	player_index = 0
	def build_choice(parent):
		global player_index
		player = players[player_index]
		#print(f"{beligerent}x{player.identifier}")
		def handler(player=player):
			for item in player.itemlist:
				while item not in player.itemlist:
					if item in itemmasterlist:
						print(itemrelinquish)
						sleep(1)
					if item in heartlist:
						player = playerchoice(players,whichplayer)
						if player.hitpoints == 1000:
							print(f"PLAYER {player.identifier} is already at max HP!")
							sleep(1)
							continue
						player.heal(itemmasterlist[item])
						print(f"PLAYER {player.identifier} restored {itemmasterlist[item].hp} HP!")
						sleep(1)
						player.hitpoints = min(player.hitpoints,1000)
					elif item in revivelist:
						player = playerchoice(downedplayers,whichplayer)
						player.heal(itemmasterlist[item])
						print(f"PLAYER {player.identifier} was revived with {itemmasterlist[item].hp} HP!")
						sleep(1)
		w = Button(parent,text=f"PLAYER {player.identifier}",justify=CENTER,fg="black",command=handler)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
		player_index += 1
	def build_back(parent):
		w = Button(parent,text="BACK",justify=CENTER,fg="black",command=mainapp)
		w.grid(row=0,column=0,padx=10,pady=5,sticky=NSEW)
	lo = tkb.AppLayout()
	config_opts = {"borderwidth":3,"relief":GROOVE}
	grid_opts = {"sticky": NSEW}
	player_dict = {}
	for player in players:
		player_dict.update({f"PLAYER {player.identifier}":build_choice})
	choice = lo.row_elements(list(player_dict),config_opts,grid_opts)
	cb = lo.column_elements([choice,"B"],config_opts,grid_opts)
	app = lo.column_elements([cb,"H"],config_opts,grid_opts)
	lo.create_layout(root,app,row=0,column=0,row_weight=1,column_weight=1)
	player_dict.update({"B":build_back,"H":build_hpCount})
	lo.build_elements(player_dict)
	root.quit()

class Attack:
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
		self.attacks = {x:PlayerAttack(x,y) for (x,y) in [["SLASH",f"PLAYER {self.identifier} swung their blade..."], ["FIREBALL",f"PLAYER {self.identifier} hurled a fireball..."], ["ICE CRYSTAL",f"PLAYER {self.identifier} chucked an icicle..."]]}
	def taketurn(self):
		while True:
			string = f"Will PLAYER {self.identifier} ATTACK, use ITEMS, or FLEE? "
			command = validinput(string,("ATTACK", "ITEMS", "FLEE"))
			if command == "ATTACK":
				attack = validinput(attackstring,list(self.attacks.keys()) + ["BACK"])
				if attack in self.attacks:
					enemy = playerchoice(enemies,whichenemy)
					if not enemy:
						continue
					print(self.attacks[attack].quote)
					sleep(2)
					print("...and inflicted", self.attacks[attack].calcdamage(self.attack,enemy.defense), f"damage to ENEMY {enemy.identifier}!")
					enemy.damage(self.attacks[attack].calcdamage(self.attack,enemy.defense))
					sleep(1)
					return True
				if attack == "BACK":
					continue
			elif command == "ITEMS":
				itemstring = f"Which item will PLAYER {self.identifier} choose: HEART (×{self.itemlist.count('HEART')}), SUPER HEART (×{self.itemlist.count('SUPER HEART')}), ULTRA HEART (×{self.itemlist.count('ULTRA HEART')}), MAX HEART (×{self.itemlist.count('MAX HEART')}), REVIVE (×{self.itemlist.count('REVIVE')}), or DELUXE REVIVE (×{self.itemlist.count('DELUXE REVIVE')})? (You can also type \"BACK\" to go back.) "
				item = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
				while item not in self.itemlist:
					if item in itemmasterlist:
						print(itemrelinquish)
						sleep(1)
						item = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
					elif item == "BACK":
						break
					else:
						print(errormessage)
						sleep(1)
						item = validinput(itemstring,list(itemmasterlist.keys()) + ["BACK"])
				if item == "BACK":
					continue
				if item in heartlist:
					player = playerchoice(players,whichplayer)
					if not player:
						continue
					if player.hitpoints == 1000:
						print(f"PLAYER {player.identifier} is already at max HP!")
						sleep(1)
						continue
					player.heal(itemmasterlist[item])
					print(f"PLAYER {player.identifier} restored {itemmasterlist[item].hp} HP!")
					sleep(1)
					player.hitpoints = min(player.hitpoints,1000)
				elif item in revivelist:
					player = playerchoice(downedplayers,whichplayer)
					if not player:
						continue
					player.heal(itemmasterlist[item])
					print(f"PLAYER {player.identifier} was revived with {itemmasterlist[item].hp} HP!")
					sleep(1)
					players.append(player)
					characters.append(player)
					downedplayers.remove(player)
				self.itemlist.remove(item)
				return True
			elif command == "FLEE":
				print("You ran away!")
				sleep(1)
				return False

class EnemyCharacter(Character):
	def __init__(self,identifier):
		super().__init__(identifier)
		self.attacks = {x:EnemyAttack(x,y) for (x,y) in [["BITE",f"ENEMY {self.identifier} opens its jaws..."], ["STOMP",f"ENEMY {self.identifier} raises its foot..."], ["SMASH",f"ENEMY {self.identifier} charges up to ram into your team..."]]}
	def taketurn(self):
		enemystring = f"ENEMY {self.identifier} readies an attack!"
		print(enemystring)
		sleep(1)
		enemychoice = random.choice(list(self.attacks.keys()))
		if enemychoice in self.attacks:
			player = random.choice(players)
			print(self.attacks[enemychoice].quote)
			sleep(2)
			print(f"...and thus PLAYER {player.identifier} received", self.attacks[enemychoice].calcdamage(self.attack,player.defense), "damage!")
			player.damage(self.attacks[enemychoice].calcdamage(self.attack,player.defense))
			sleep(1)
		return True

def defeatstate():
	for character in characters:
		if character in players:
			beligerent = "PLAYER"
		else:
			beligerent = "ENEMY"
		if character.hitpoints.get() <= 0:
			characters.remove(character)
			if character in players:
				downedplayers.append(character)
				players.remove(character)
			else:
				enemies.remove(character)
			print(f"{beligerent} {character.identifier} is defeated!")
			sleep(1)
			character.hitpoints.set(0)
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

class PlayerCount(Frame):
	def createWidgets(self):
		self.LABEL = Label(self)
		self.LABEL["text"] = "How many players?"
		self.LABEL.pack({"side": "left"})
		self.COUNT = Spinbox(self)
		self.COUNT["to"] = "5"
		self.COUNT["from"] = "1"
		self.COUNT["increment"] = "1"
		self.COUNT.pack({"side": "left"})
		self.START = Button(self)
		self.START["text"] = "START",
		self.START["command"] = self.quit
		self.START.pack({"side": "left"})

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
root1 = Tk()
root1.protocol("WM_DELETE_WINDOW",sys.exit)
# Start battle
getCount = PlayerCount(master=root1)
getCount.mainloop()
quantity = getCount.COUNT.get()
root1.destroy()

whichenemy = "Which enemy is to be targeted? (You can also press \"BACK\" to go back.)"
whichplayer = "Which player should use this item? (You can also press \"BACK\" to go back.)"
itemrelinquish = "You're out of that particular item..."

root = Tk()
root.protocol("WM_DELETE_WINDOW",sys.exit)
print("ENEMY team attacks!")
#speedstats = [random.randint(0,360) for i in range(2*quantity)]
players = [PlayerCharacter(i+1) for i in range(int(quantity))]
enemies = [EnemyCharacter(i+1) for i in range(int(quantity))]
characters = players + enemies
downedplayers = []
random.shuffle(characters)
speed = 0
for character in characters:
	character.speed = speed
	speed += 1
sleep(1)
mainapp()
root.mainloop()
#errormessage = "Command not recognized. Try again."
#attackstring = "Which attack will it be: SLASH, FIREBALL, or ICE CRYSTAL? (You can also type \"BACK\" to go back.) "
#while len(players) != 0 and len(enemies) != 0:
	#for character in characters:
		#if character in players:
			#opponents = enemies
		#else:
			#opponents = players
		#if not character.taketurn():
			#break
		#if defeatstate():
			#break
