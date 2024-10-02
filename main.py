import inquirer
import os
import random
import time
import toml


#init user data
currentHP = 100
maxHP = 100
currentXP = 0
levelupXP = 2000
rank = 1

#init enemy data
maxHP = 100
enemyHP = 100

#init player location
location = "home"
places = ["Cave", "Forest"]

#load from toml file
def loadSave():

  global currentHP, maxHP, currentXP, levelupXP, rank
  
  with open("config.toml", "r") as f:
    config = toml.load(f)

  currentHP = int(config['player']['currentHP'])
  maxHP = config['player']['maxHP']
  currentXP = config['player']['currentXP']
  levelupXP = config['player']['levelupXP']
  rank = config['player']['rank']

#write to toml file
def save():
  with open("config.toml", "r") as f:
    config = toml.load(f)

  config['player']['currentHP'] = currentHP
  config['player']['maxHP'] = maxHP
  config['player']['currentXP'] = currentXP
  config['player']['levelupXP'] = levelupXP
  config['player']['rank'] = rank

  with open('config.toml', 'w') as f:
    toml.dump(config, f)

#enemy class
class Enemy:
  def __init__(self, name, health, agility, strength):
    self.name = name
    self.health = health  #Value
    self.agility = agility  #Multiplier
    self.strength = strength  #Multiplier

troll = Enemy("Troll", 150, 1, 1.8)
wolf = Enemy("Wolf", 50, 8, 1.6)
bandit = Enemy("Bandit", 100, 5, 1.5)

#get xp reward from enemy
def getXP(enemyHP):
  os.system('clear')
  global currentXP, levelupXP, rank
  earntXP = enemyHP * 5
  currentXP += earntXP
  if currentXP >= levelupXP:
    rank += 1
    print("Your Rank has increased to", rank)
    levelupXP = levelupXP * 1.2
  print("Your XP is at", currentXP, "\n\nNext Rank at", levelupXP, "XP")
  time.sleep(3)
  match location:
    case "home":
      adventure()
    case "cave":
      cave()

#die used for game
def rollGenericDice():
  totalDie = 0
  for _ in range(0, 2):
    totalDie = totalDie + random.randint(1, 6)
  return totalDie

#regain all hp when resting
def rest():
  global currentHP
  print("Resting for 20 seconds")
  for x in range(20, 0, -1):
    if x == 1:
      print(x, "second left")
    else:
      print(x, "seconds left")
    time.sleep(1)
    os.system('clear')
  currentHP = maxHP
  print("HP back to", currentHP)
  adventure()

#on death
def death():
  os.system('clear')
  print("You died")

#flee from enemy, rolls die (not working sometimes)
def Flee(agilityOfEnemy):
  print("DEBUG; Flee Attempt")
  time.sleep(2)
  totalRoll = 0

  os.system('clear')
  print("Rolling two die.")

  if agilityOfEnemy >= 8:
    for _ in range(2):
      totalRoll += random.randint(1, 6)
    if totalRoll >= 10:
      time.sleep(2)
      print("\nTotal roll =", totalRoll, "\nNeeded = 10")
      return 1
    else:
      return 0

  else:
    for _ in range(2):
      totalRoll += random.randint(1, 6)
    if totalRoll >= 8:
      time.sleep(2)
      print("\nTotal roll =", totalRoll, "\nNeeded = 5")
      return 1
    else:
      return 0

#fight enemy
def Fight(enemyEncountered, first):

  totalRoll = 0
  os.system('clear')
  enemyName = enemyEncountered.name
  enemyHP = enemyEncountered.health
  enemyAgil = enemyEncountered.agility  #might implement enemies able to dodge
  enemyStr = enemyEncountered.strength

  if first == "enemy":
    tempHpLoss = rollGenericDice()
    print(enemyName, "attacked first")
    time.sleep(2)
    print("You lost", tempHpLoss)
    global currentHP
    currentHP -= tempHpLoss

  while currentHP > 0 and enemyHP > 0:
    if currentHP > 0:
      os.system('clear')
      print("You attack.\n\nRolling die")
      totalRoll = rollGenericDice()
      time.sleep(2)
      print("You rolled", totalRoll, "\n")
      time.sleep(2)
      healthLoss = totalRoll * 3
      enemyHP -= healthLoss
      if enemyHP < 0:
        enemyHP = 0
        os.system('clear')
        print("Enemy defeated.")
        getXP(enemyEncountered.health)
        break

      print(enemyName, "Lost", healthLoss, "HP\nThey are now on", enemyHP,
            "HP\n\n")
    if enemyHP > 0:
      time.sleep(4)
      print(enemyName, "is attacking.")
      totalRoll = rollGenericDice()
      healthLoss = totalRoll * enemyStr
      currentHP -= round(healthLoss)
      if currentHP < 0:
        currentHP = 0
        death()
        break
      print("You lost", healthLoss, "HP\nYou are now on", currentHP, "HP")
      time.sleep(4)

#asks user where to travel to
def adventure():
  decision = 0
  os.system('clear')
  questions = [
      inquirer.List(
          'place',
          message="Where do you want to go?",
          choices=['Cave', 'Forest', 'Home'],
      ),
  ]
  answers = inquirer.prompt(questions)
  decision = (answers["place"])
  time.sleep(1)

  while currentHP > 0:
    os.system('clear')

    if decision == 'Cave':
      print("You go into the Cave")
      cave()

    if decision == 'Forest':
      print("Forest Not Implemented Yet")

    if decision == 'Home':
      print("You go home to relax")
      rest()

    else:
      time.sleep(2)
      adventure()

#location cave
def cave():
  global location
  location = "cave"
  os.system('clear')
  time.sleep(1)
  tempEnemy = random.randint(1, 3)
  choice = [
      inquirer.List(
          'decision',
          message="What do you do?",
          choices=['Flee', 'Fight'],
      ),
  ]

  if tempEnemy == 1:
    print("You encounter a", troll.name, "\nThey have", troll.health,
          "health\n\n")
    answers = inquirer.prompt(choice)
    decision = (answers["decision"])

    if decision == "Flee" and Flee(troll.agility) == 1:
      print("\nYou escaped")
    elif decision == "Flee" and Flee(troll.agility) == 0:
      print("\nYour escape failed")
      Fight(troll, "enemy")
    time.sleep(2)
    if decision == "Fight":
      Fight(troll, "player")

  elif tempEnemy == 2:
    print("You encounter a", wolf.name, "\nThey have", wolf.health,
          "health\n\n")
    answers = inquirer.prompt(choice)
    decision = (answers["decision"])

    if decision == "Flee" and Flee(wolf.agility) == 1:
      print("\nYou escaped")
    elif decision == "Flee" and Flee(wolf.agility) == 0:
      print("\nYour escape failed")
      Fight(wolf, "enemy")
    time.sleep(2)

    if decision == "Fight":
      Fight(wolf, "player")

  elif tempEnemy == 3:
    print("You encounter a", bandit.name, "\nThey have", bandit.health,
          "health\n\n")
    answers = inquirer.prompt(choice)
    decision = (answers["decision"])

    if decision == "Flee" and Flee(bandit.agility) == 1:
      print("\nYou escaped")
    elif decision == "Flee" and Flee(bandit.agility) == 0:
      print("\nYour escape failed")
      Fight(bandit, "enemy")
    time.sleep(2)

    if decision == "Fight":
      Fight(bandit, "player")

#just for story
def space():
  time.sleep(5)
  os.system('clear')
  time.sleep(1)


def introStory():
  print(
      "In the ancient land of Eldoria, a realm once brimming with magic and prosperity."
  )

  space()

  print(
      "darkness has taken root. The once-glorious kingdom now lies in ruins, its "
      "people scattered and its lands overrun by monstrous creatures.")

  space()

  print(
      "At the heart of this chaos lies the Abyss, a network of ever-changing dungeons"
      " that stretch deep beneath the earth, rumored to be the source of the corruption"
  )

  space()

  print(
      "Guided by the spirit of an ancient Sentinel, you learn that the only way to "
      "cleanse the land is to delve into the Abyss, conquer its depths, and harness the"
      " power within.")

  space()

  print(
      "Each dungeon is a test of strength, wit, and courage, filled with deadly traps,"
      "fearsome beasts, and ancient relics that hold the key to your growth.")

  space()

  print("You wake up")
  time.sleep(3)
  adventure()

loadSave()
#introStory()
adventure()
