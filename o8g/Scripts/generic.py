#---------------------------------------------------------------------------
# General functions
#---------------------------------------------------------------------------
   
def chooseSide(): # Called from many functions to check if the player has chosen a side for this game.
   mute()
   global playerside, playeraxis
   if playerside == None:  # Has the player selected a side yet? If not, then...
      if len(players) < 3:
         playeraxis = Xaxis
         if confirm("Will you play on the right side?"): # Ask which side they want
            playerside = 1 # This is used to swap between the two halves of the X axis of the play field. Positive is on the right.
         else:
            playerside = -1 # Negative is on the left.
      else:
         askside = askInteger("On which side do you want to setup?: 1 = Right, 2 = Left, 3 = Bottom, 4 = Top, 0 = None (All your cards will be put in the middle of the table and you'll have to arrange them yourself", 1) # Ask which axis they want,
         if askside == 1:
            playeraxis = Xaxis
            playerside = 1
         elif askside == 2:
            playeraxis = Xaxis
            playerside = -1
         elif askside == 3:
            playeraxis = Yaxis
            playerside = 1
         elif askside == 4:
            playeraxis = Yaxis
            playerside = -1
         else:
            playeraxis = None  
            playerside = 0
         
def num (s): 
# This function reads the value of a card and returns an integer. For some reason integer values of cards are not processed correctly
# see bug 373 https://octgn.16bugs.com/projects/3602/bugs/188805
# This function will also return 0 if a non-integer or an empty value is provided to it as it is required to avoid crashing your functions.
#   if s == '+*' or s == '*': return 0
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

def defPlayerColor(): # Obsolete in OCTGN 3 but leaving it here in case I find another use for it.
# Provide a random highlight colour for the player which we use to simulate ownership
   global PlayerColor
   if len(PlayerColor) == 7 : return
   RGB = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
   for i in range(6): PlayerColor += RGB[rnd(0,15)]

def download_o8c(group,x=0,y=0):
   openUrl("http://dbzer0.com/pub/Doomtown/sets/Doomtown-Sets-Bundle.o8c")
     
#---------------------------------------------------------------------------
# Card Placement functions
#---------------------------------------------------------------------------

def cwidth(card, divisor = 10): 
# This function is used to always return the width of the card plus an offset that is based on the percentage of the width of the card used.
# The smaller the number given, the less the card is divided into pieces and thus the larger the offset added.
# For example if a card is 80px wide, a divisor of 4 will means that we will offset the card's size by 80/4 = 20.
# In other words, we will return 1 + 1/4 of the card width. 
# Thus, no matter what the size of the table and cards becomes, the distances used will be relatively the same.
# The default is to return an offset equal to 1/10 of the card width. A divisor of 0 means no offset.
   if divisor == 0: offset = 0
   else: offset = card.width() / divisor
   return (card.width() + offset)

def cheight(card, divisor = 10):
   if divisor == 0: offset = 0
   else: offset = card.height() / divisor
   return (card.height() + offset)

def placeCard(card,type = None, dudecount = 0):
# This function automatically places a card on the table according to what type of card is being placed
# It is called by one of the various custom types and each type has a different value depending on if the player is on the X or Y axis.
   global strikeCount, posSideCount, negSideCount
   if playeraxis == Xaxis:
      if type == 'HireDude':
         # Move the dude next to where we expect the player's home card to be.
         card.moveToTable(homeDistance(card) + (playerside * cwidth(card,-4)), 0)
      if type == 'BuyDeed':
         if re.search('Strike', card.Text) or re.search('Out of Town', card.Text): # Check if we're bringing out an out of town deed
            card.moveToTable(homeDistance(card) + 2 * cardDistance(card), (-1 * cheight(card,4) * 2) + strikeCount * cheight(card))
            strikeCount += 1 # Increment this counter. Extra out of town deeds will be placed below the previous ones.
         else:
            if confirm("Do you want to place this deed on the bottom side of your street?"): # If it's a city deed, then ask the player where they want it.
               negSideCount += 1 #If it's on the bottom, increment the counter...
               card.moveToTable(homeDistance(card), negSideCount * cheight(card)) # ...and put the deed below all other deeds already there.
            else:
               posSideCount += 1 # Same as above but going upwards from home.
               card.moveToTable(homeDistance(card), -1 * (posSideCount * cheight(card)))     
      if type == 'SetupHome':
         card.moveToTable(homeDistance(card), 0) # We move it to one side depending on what side the player chose.
      if type == 'SetupDude':
         card.moveToTable(homeDistance(card) + cardDistance(card) + playerside * (dudecount * cwidth(card)), 0) 
         # We move them behind the house
      if type == 'SetupOther':
         card.moveToTable(playerside * (cwidth(card,4) * 3), playerside * -1 * cheight(card)) # We move the card around the player's area.      
   elif playeraxis == Yaxis:
      if type == 'HireDude':# Hire dudes on your home + one card height - 20% of a card height
         card.moveToTable(0,homeDistance(card) + (playerside * cheight(card,-4)))
      if type == 'BuyDeed': 
         if re.search('Strike', card.Text) or re.search('Out of Town', card.Text): # Check if we're bringing out an out of town deed
            card.moveToTable((playerside * cwidth(card,4) * 5) + strikeCount * cwidth(card) * playerside, homeDistance(card) + cardDistance(card))
            strikeCount += 1 
         else:
            if confirm("Do you want to place this deed on the right side of your street?"): # If it's a city deed, then ask the player where they want it.
               negSideCount += 1 #If it's on the right, increment the counter...
               card.moveToTable(negSideCount * cwidth(card),homeDistance(card)) # ...and put the deed below all other deeds already there.
            else:
               posSideCount += 1 # Same as above but going leftwards from home.
               card.moveToTable(-1 * (posSideCount * cwidth(card)),homeDistance(card))       
      if type == 'SetupHome':
         card.moveToTable(0,homeDistance(card)) 
      if type == 'SetupDude': # Setup your dudes one card height behind your home and in a horizontal line
         card.moveToTable(-cwidth(card) + (dudecount * cwidth(card)),homeDistance(card) + cardDistance(card)) 
      if type == 'SetupOther':
         card.moveToTable(playerside * -3 * cwidth(card), playerside * (cheight(card,4) * 3)) 
   else: card.moveToTable(0,0)
   
def homeDistance(card):
# This function retusn the distance from the middle each player's home will be setup towards their playerSide. 
# This makes the code more readable and allows me to tweak these values from one place
   if playeraxis == Xaxis:
      return (playerside * cwidth(card) * 5) # players on the X axis, are placed 5 times a card's width towards their side (left or right)
   elif playeraxis == Yaxis:
      return (playerside * cheight(card) * 3) # players on the Y axis, are placed 3 times a card's height towards their side (top or bottom)

def cardDistance(card):
# This function returns the size of the card towards a player's side. 
# This is useful when playing cards on the table, as you can always manipulate the location
#   by multiples of the card distance towards your side
# So for example, if a player is playing on the bottom side. This function will always return a positive cardheight.
#   Thus by adding this in a moveToTable's y integer, the card being placed will be moved towards your side by one multiple of card height
#   While if you remove it from the y integer, the card being placed will be moved towards the centre of the table by one multiple of card height.
   if playeraxis == Xaxis:
      return (playerside * cwidth(card))
   elif playeraxis == Yaxis:
      return (playerside * cheight(card))
         