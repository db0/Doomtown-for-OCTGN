#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------
import re

phases = [
    '{} is currently in the Pre-game Setup Phase'.format(me),
    "It is now GAMBLIN' time. Play Lowball!",
    "The time has come to pay your UPKEEP",
    "It is now HIGH NOON",
    "NIGHTFALL has come."]

### Highlight Colours ###
DoesntUnbootColor = "#ffffff"
AttackColor = "#ff0000"
DefendColor = "#0000ff"
DrawHandColor = "#000000"
EventColor = "#00ff00"


### Markers ###
WantedMarker = ("wanted", "0a5fabc8-fe56-481a-b45a-a9ad6917d0d9")
HarrowedMarker = ("harrowed", "661f2771-6b73-414b-b0b1-3e2b50386b71")
HNActivatedMarker = ("High Noon Ability", "836dfd81-805b-489a-a3d6-b55d68ff5a71")
SHActivatedMarker = ("Shootout Ability", "197d8de5-d63f-4455-9144-7a106b192a02")
InfluencePlusMarker = ("+1 Influence", "43a4a6ba-d63b-46fd-8305-f9ffedf74f6d")
InfluenceMinusMarker = ("-1 Influence", "b59df5b4-708b-481a-8b38-2d50eac48465")
ControlPlusMarker = ("+1 Control", "6dbe2df7-4e9f-4e52-ab7d-c80afd7356ae")
ControlMinusMarker = ("-1 Control", "474f95a6-f1a9-4e23-ba4a-8eaba8b7cc0b")
ProdPlusMarker = ("+1 Production", "ddba0f0a-0c34-48b5-b7ea-ad1e1ab07c12")
ProdMinusMarker = ("-1 Production", "869eebe2-f503-4d9f-8fa3-af708c7ad70c")
ValuePlusMarker = ("+1 Value", "baff5422-3654-4f74-86fa-782805082fab")
ValueMinusMarker = ("-1 Value", "7fa426df-689e-41f5-91b8-5d06cbc46463")
JailbreakMarker = ("jailbroken", "692a1ab1-9aa9-49da-aff5-114644da921f")
WinnerMarker = ("Winner", "eeb5f447-f9fc-46b4-846a-a9a40e575cbc")

### Misc ###

loud = 'loud' # So that I don't have to use the quotes all the time in my function calls
silent = 'silent' # Same as above
lowball = 'lowball' # Same as above
shootout = 'shootout' # Same as above
Xaxis = 'x'  # Same as above
Yaxis = 'y'	 # Same as above

#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------

ShootoutActive = 0 # A variable to keep track if we are in a shootout phase
playerside = None # Variable to keep track on which side each player is
playeraxis = None # Variable to keep track on which axis the player is
strikeCount = 0 # Used to automatically place strikes
posSideCount = 0 # Used to automatically place in-town deeds 
negSideCount = 0 # Same as above
handsize = 5 # Used when automatically refilling your hand
playerOutfit = None # Variable to keep track of the player's outfit.
PlayerColor = "#" # Variable with the player's unique colour.


wantedDudes = {} # A dictionaty to store which dude is wanted.
harrowedDudes = {} # Which dudes are harrowed
jailbrokenDeeds = {} # Which deeds are jailbroken
ValueMemory = {} # Which cards have amodified value
AttachedCards = {} # Not used atm
InfluenceRAM = {} # Which cards have extra influence
ControlRAM = {} # Which cards have extra cp

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

def defPlayerColor():
# Provide a random highlight colour for the player which we use to simulate ownership
   global PlayerColor
   if len(PlayerColor) == 7 : return
   RGB = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
   for i in range(6): PlayerColor += RGB[rnd(0,15)]

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
   
def test(group, x = 0, y = 0): # Testing function.  
   global playerside, playeraxis
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
      playerside = 9
   notify("{} has selected side {}-{}".format(me,playerside,playeraxis))

def test2(card, x, y): # Testing function.
   notify("x = {} y = {}".format(x,y))   
   
#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def Pass(group, x = 0, y = 0): # Player says pass. A very common action.
   notify('{} Passes.'.format(me))

def showCurrentPhase(): # Just say a nice notification about which phase you're on.
   notify(phases[shared.Phase].format(me))
   
def nextPhase(group, x = 0, y = 0):  
# Function to take you to the next phase. 
   mute()
   if shared.Phase == 4: 
      shared.Phase = 1 # In case we're on the last phase (Nightfall), go back to the first game phase (Gamblin')
      clearHandRanks() # Clear the Hand Ranks, in case one is leftover from last High Noon.
   else: shared.Phase += 1 # Otherwise, just move up one phase
   showCurrentPhase()
	
def goToGamblin(group, x = 0, y = 0): # Go directly to the gamblin' phase
   mute()
   shared.Phase = 1
   showCurrentPhase()
   clearHandRanks() # Clear the Hand Ranks, in case one is leftover from last High Noon.

def goToUpkeep(group, x = 0, y = 0): # Go directly to the Upkeep phase
   mute()
   shared.Phase = 2
   showCurrentPhase()
	
def goToHighNoon(group, x = 0, y = 0): # Go directly to the High Noon phase
   mute()
   shared.Phase = 3
   showCurrentPhase()

def goToNightfall(group, x = 0, y = 0): # Go directly to the Nightfall phase
   mute()
   shared.Phase = 4
   showCurrentPhase()   

def goToSetup(group, x = 0, y = 0):  # Go back to the Pre-Game Setup phase.
# This phase is not rotated with the nextPhase function as it is a way to basically restart the game.
# It also serves as a control, so as to avoid a player by mistake using the setup function during play.
   mute()
   global ShootoutActive, playerside, strikeCount, posSideCount, negSideCount, handsize, playerOutfit 
   global wantedDudes, harrowedDudes, jailbrokenDeeds, ValueMemory
   # Import all our global variables and reset them.
   ShootoutActive = 0
   playerside = None
   strikeCount = 0
   posSideCount = 0
   negSideCount = 0
   handsize = 5
   shared.Phase = 0
   playerOutfit = None
   wantedDudes.clear() # Clear the dictionaries so that you don't remember card memory from the previous games
   harrowedDudes.clear()
   jailbrokenDeeds.clear()
   ValueMemory.clear()
   AttachedCards.clear()
   showCurrentPhase() # Remind the players which phase it is now
	
def goToShootout(group, x = 0, y = 0): # Start or End a Shootout Phase
   global ShootoutActive
   if ShootoutActive == 0: # The shootout phase just shows a nice notification when it starts and does nothing else.
      notify("A shootout has broken out.".format(me))
      ShootoutActive = 1
   else: # When the shootout ends however, any card.highlights for attacker and defender are quickly cleared.
      notify("The shootout has ended.".format(me))
      ShootoutActive = 0
      cards = (card for card in table
                     if card.highlight == DefendColor
                     or card.highlight == AttackColor)
      for card in cards: card.highlight = None
      clearHandRanks()  # Clear the Hand Ranks, in case one is leftover.
      
def boot(card, x = 0, y = 0): # Boot or Unboot a card. I.e. turn it 90 degrees sideways or set it straight.
   mute()
   card.orientation ^= Rot90 # This function rotates the card +90 or -90 degrees depending on where it was.
   if card.orientation & Rot90 == Rot90: # if the card is now at 90 degrees, then announce the card was booted
      notify('{} boots {}'.format(me, card))
   else: # if the card is now at 0 degrees (i.e. straight up), then announce the card was unbooted
      notify('{} unboots {}'.format(me, card))
		
def ace(cards, x = 0, y = 0): # Ace a card. I.e. kill it and send it to the boot hill (i.e.graveyard)
   mute()
   for card in cards:	# This function can be used at more than one card as the same time. Useful for sending dudes and attached cards to the boot hill quickly.
      cardowner = card.owner # We need to save the card onwer for later
      if card.highlight != DrawHandColor: # We don't want to do anything else except move cards when they're not really in play.
         if (card.markers[HarrowedMarker] == 1 or re.search(r'\bHarrowed.\b', card.text)) and card.Type == 'Dude': 
            if not confirm("{} was harrowed! Did you remember to do a harrowed pull?".format(card.name)): continue
            # if the dude is harrowed, remind the player about the harrowed pull. If they haven't done it, leave the dude in play.
            # In the future, I'll modify the option to perform the harrowed pull automatically.
         if card.markers[WantedMarker] == 1: notify("{} was wanted! Don't forget your bounty.".format(card)) # Remind the player to take a bounty for wanted dudes.
         cardRMsync(card) # This function removes any Influence and Control Points that card had from your total. 
                          # We need to do it before the card is moved to the boot hill because by then, the markers are removed.
         cardMemoryStore(card) # This function stores added effects likes being wanted or harrowed in card memory.
      # Remind the player to take a bounty for wanted dudes. In the future this will be automated.
      card.moveTo(cardowner.piles['Boot Hill']) # Cards aced need to be sent to their owner's boot hill
      notify("{} has aced {}.".format(me, card))

def discard(cards, x = 0, y = 0): # Discard a card.
   mute()
   for card in cards:	# Can be done at more than one card at the same time, since attached cards follow their parent always.
      cardowner = card.owner
      if card.highlight != DrawHandColor and card.highlight != EventColor: # If the card being discarded was not part of a draw hand
         cardRMsync(card) # Then remove it's influence / CP from the player's pool
         cardMemoryStore(card) # And store it's memory.
         notify("{} has discarded {}.".format(me, card))
      if card.highlight == EventColor and re.search('Ace this card', card.Text): # If the card being discarded was an event in a lowball hand
                                                                                 # And that event had instructions to be aced
         card.moveTo(cardowner.piles['Boot Hill'])                               # Then assume player error and ace it         
         notify("{} was the active event and has been aced as per card instructions.".format(card)) # And inform the players.
      else: card.moveTo(cardowner.piles['Discard Pile']) # Cards aced need to be sent to their owner's discard pile

def upkeep(group, x = 0, y = 0): # Automatically receive production and pay upkeep costs
# This function goes through each of your cards and checks if it provides production or requires upkeep, then automatically removes it from your bank.
   if shared.Phase != 2: #One can only call for upkeep during the upkeep phase
      whisper("You can only call pay upkeep and receive production during the upkeep phase")
      return
   mute()
   gr = 0 # Variable used to track each cards production/upkeep
   concat_prod = '' # A string which we will use to provide a succint notification at the end
   concat_upk = '' # Same as above
   prod = 0 # Variable to track total production received.
   upk = 0 # Variable to track total upkeep paid.
   cards = (card for card in table # Create a group with all the cards you own and control on the table.
                 if (card.owner == me or card.highlight == PlayerColor) # you cannot pay or produce from cards you do not own.
                 and card.controller == me  # you cannot pay or produce from cards you do not control.
                 and card.highlight != DrawHandColor) # And avoid counting lowball cards
   for card in cards: # For each card...
      gr = num(card.Production) - num(card.Upkeep) + card.markers[ProdPlusMarker] - card.markers[ProdMinusMarker]
      # Grab its production value (usually 0 for most non-deeds) then 
      # add the amount of any +production markers you have on the card and remove the amount of any -production markers you have on the card.
      if (card.Outfit != playerOutfit and # If a non-drifter dude is not from the player's outfit, 
         card.Outfit != 'Drifter' and     # they need to play an extra GR upkeep per influence.
         card.Type == 'Dude' and
         num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker] > 0): 
         gr -= (num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker])
      if gr - (2 * card.markers[JailbreakMarker]) > 0: # If we still have any production left after removing jailbroken penalties, 
                 # then we increment the total production we have for this turn 
                 # and add the name of the card to our concatenated string of all the cards that produced this turn
         prod += gr
         concat_prod += str(gr) # This is where the concatenation happens
         concat_prod += ' GR from '
         concat_prod += card.name
         concat_prod += '. '
      elif gr < 0: # Much like production, we only add the name to the string if it's having any upkeep
         upk += -gr # Add the negative gr as a positive amount to the variable, so that we can compare it later to  our remaining GR.
         concat_upk += str(gr)
         concat_upk += ' GR for '
         concat_upk += card.name
         concat_upk += '. '
   notify("{} has produced {} ghost rock this turn: {}".format(me, prod, concat_prod)) # Inform the players how much they produced and from where.
   me.GhostRock += prod # Then add the money to their Ghost Rock counter.
                        # Note that you can only modify counters with a single-string name due to bug 372
                        # See https://octgn.16bugs.com/projects/3602/bugs/188803
   if upk > 0: # If we need to pay any upkeep, we do it after receiving production for the turn.
      if me.GhostRock < upk: # If we cannot pay with the money we have, then let the player decide what to do.
                             # I could have made their bank account negative and let them modify it manually, but I think this way is better.
         notify("{} has {}GR in their bank but needs to pay {}GR for upkeep ({}). No GR has been taken but please discard enough cards with upkeep and reduce your remaining Ghost Rock manually.".format(me, me.GhostRock, upk, concat_upk))
      else: # If we can pay the upkeep, do so.
         notify("{} has paid {} upkeed in total this turn. {}".format(me, upk, concat_upk)) #Inform the players how much they paid and for what.
         me.GhostRock -= upk # Finally take the money out of their bank
         
def HNActivate(card, x = 0, y = 0): # A function to add or remove High Noon (HN) markers. 
                                    # Those markers are used to signify when a high noon ability has been used, 
                                    # as printed abilities can only ever be used once per turn, even if they do not require booting.
                                    # These markers are only removed at the end of the turn.
   mute()
   if card.markers[HNActivatedMarker] == 0: # If we have no HN markers, add one
      notify("{} uses {}'s High Noon ability.".format(me, card))
      card.markers[HNActivatedMarker] += 1
   else: # If we have have such a marker, assume the player did it by mistake and inform everyone.
      notify("{} Wanted to use {}'s High Noon ability but it has already been used this turn. Did they use a card effect?".format(me, card))
	  
def SHActivate(card, x = 0, y = 0): # Same process as the HN markers above
   mute()
   if card.markers[SHActivatedMarker] == 0:
      notify("{} uses {}'s Shootout ability.".format(me, card))
      card.markers[SHActivatedMarker] += 1
   else:
      notify("{} Wanted to use {}'s Shootout ability but it has already been used this turn.".format(me, card))		

def nightfall(card, x = 0, y = 0): # This function "refreshes" each card for nightfall.
                                   # This practically means that we remove any High Noon and Shootout ability markers and unboot the card
                                   # But only if it's not marked as a card that does not unboot
   mute()
   card.markers[HNActivatedMarker] -= 1 # Remove the markers.
   card.markers[SHActivatedMarker] -= 1
   if card.highlight != DoesntUnbootColor and card.name != 'Town Square' : # We do not unboot the Town Square card.
      card.orientation = Rot0 # And if we can unboot the card, turn it to 0 degrees.

def NightfallUnboot(group, x = 0, y = 0): # This function simply runs all the cards the player controls through the nigtfall function.
   mute()
   if shared.Phase != 4: #One can only call for refresh during the Nighfall phase
      whisper("You can only call this action during the nighfall phase")
      return   
   if not confirm("Have you remembered to discard any cards you don't want from your play hand?"): return
   refill()
   cards = (card for card in table
                 if card.controller == me)
   for card in cards: nightfall(card)
   notify("Nightfall refreshes {} cards and refills their hand back to {}.".format(me, handsize))
   
def doesNotUnboot(card, x = 0, y = 0): # Mark a card as "Does not unboot" or unmark it. We use a card highlight to do this.
   if card.highlight == DoesntUnbootColor: # If it's already marked, remove highlight from it and inform.
      card.highlight = None
      notify("{}'s {} can now unboot during Nightfall.".format(me, card))
   else:
      card.highlight = DoesntUnbootColor # Otherwise highlight it and inform. 
      notify("{}'s {} will not unboot during Nightfall.".format(me, card))
      
def spawnTokenDude(group, x = 0, y = 0): # Simply put a fake card in the game.
   table.create("88e598eb-65e0-4ae3-8416-52df58a5538f", x, y, 1)

def HandRankGuide(group, x = 0, y = 0): # Put the Hand Rank guide onto the table, in case player need help to remember.
   HRG = table.create("851b726b-3b0c-43df-bbd7-710b5a0ffbf6", x, y, 1)   
    
def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   confirm("{}".format(card.text)) 
   
def reCalculate(group = table, x = 0, y = 0, notification = 'loud'): 
# This function will calculate the amount of influence and Control you have on the table and update your counters. 
   mute()
   influence = 0 
   control = 0
   count = 0
   i = 0
   c = 0
   concat_inf = ' (' # We start our concatenated list of the cards with influence. We're going to put them in parenthesis for easy reading.
   concat_cp = ' ('
   cards = (card for card in table # We only care for cards we control. 
            if card.controller == me)
   for card in cards:
      count = num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker] # Put the card's total influence on a temp marker.
      if count > 0: # We only care to do anything if the card had any influence
         if i > 0: concat_inf += ', ' # We separate with comma only after we have at least 1 card in the list
         concat_inf += str(count) # Add the count as a string to the concatenated list before the name, e.g. "3 from Black Jack"
         concat_inf += ' from ' 
         concat_inf += card.name
         i += 1 # Once we have found at least one card with influence, we separate the rest with commas
         influence += count # We add this card's total influence to our tally.
      count = num(card.Control) + card.markers[ControlPlusMarker] - card.markers[ControlMinusMarker] # Put the card's total influence on a temp marker.
      if count > 0: # Same as influence but for control this time
         if c > 0: concat_cp += ', '
         concat_cp += str(count)
         concat_cp += ' from '
         concat_cp += card.name
         c += 1
         control += count
   concat_inf += ')' # We close our concatenated list
   if concat_inf == ' ()': concat_inf = '' # To avoid opening an empty parethesis if the player has no influence.
   concat_cp += ')'
   if concat_cp == ' ()': concat_cp = '' # To avoid opening an empty parethesis if the player has no control points.
   if notification == 'loud': # We only want to say the result if we're not explicitly asked to be silent (i.e. from the table action)
      notify('{} has recalculated and found their influence to to be {}{}, and their Control Points to be {}{}.'.format(me, influence, concat_inf, control, concat_cp))
   me.Influence = influence # Make the player's total influence and control equal to the sum we've just calculated.
   me.Control = control

def setWinner(winner):
   outfits = (card for card in table
              if card.type == 'Outfit')
   for outfit in outfits:
      if outfit.owner == winner: outfit.markers[WinnerMarker] = 1
      else: outfit.markers[WinnerMarker] = 0

#---------------------------------------------------------------------------
# Marker functions
#---------------------------------------------------------------------------

def plusControl(card, x = 0, y = 0, notification = loud, count = 1): # Adds an extra control marker to cards (usually deeds)
   mute()
   if notification == loud:
      notify("{} marks that {} provides {}  more control (Their total has been adjusted accordingly).".format(me, card, count))
   for i in range(0,count):
      if ControlMinusMarker in card.markers: # If we have a -CP counter already, just remove one of those.
         if num(card.Control) - card.markers[ControlMinusMarker] >= 0: 
            modControl() # This function takes care of modifying the player's control counter. In this case it increases it by 1.
                           # But we only go through with it if the -CP markers didn't actually take the cards' CP below 0.
         card.markers[ControlMinusMarker] -= 1
      else: # Otherwise just add an extra +CP
         card.markers[ControlPlusMarker] += 1
         modControl() 
        
def minusControl(card, x = 0, y = 0, notification = loud, count = 1): # Similar to adding Control but we remove instead.
   mute()
   if notification == loud:
      notify("{} marks that {} provides {} less control (Their total has been adjusted accordingly).".format(me, card, count))
   for i in range(0,count):
      if ControlPlusMarker in card.markers:
         card.markers[ControlPlusMarker] -= 1
         modControl(-1)
      else:
         if num(card.Control) - card.markers[ControlMinusMarker] > 0: modControl(-1) # We only reduce a players totals if the control was above 0
                                                                                     # As the minimum CP on a card is always 0.
         card.markers[ControlMinusMarker] += 1     

def plusInfluence(card, x = 0, y = 0, notification = loud, count = 1): # The same as pluControl but for influence
   mute()
   if notification == loud:
      notify("{} marks that {}'s influence has increased by {} ({}'s total has been adjusted automatically)".format(me, card, count, me))
   for i in range(0,count):
      if InfluenceMinusMarker in card.markers:
         if num(card.Influence) - card.markers[InfluenceMinusMarker] >= 0:
                modInfluence()
         card.markers[InfluenceMinusMarker] -= 1
      else:
         card.markers[InfluencePlusMarker] += 1         
         modInfluence()
        
def minusInfluence(card, x = 0, y = 0, notification = loud, count = 1): # The same as minusContorl but for influence
   mute()
   if notification == loud:
      notify("{} marks that {}'s influence has decreased by {} ({}'s total has been adjusted automatically).".format(me, card, count, me))
   for i in range(0,count):
      if InfluencePlusMarker in card.markers:
         card.markers[InfluencePlusMarker] -= 1
         modInfluence(-1)
      else:
         if num(card.Influence) - card.markers[InfluenceMinusMarker] > 0: modInfluence(-1)
         card.markers[InfluenceMinusMarker] += 1 

        
def plusProd(card, x = 0, y = 0): # Very much like plus Influence and control, but we don't have to worry about modifying the player's totals
   mute()
   if ProdPlusMarker in card.markers or ProdMinusMarker in card.markers: # Putting the clarification about upkeep 
                                                                         # only the first time this is changed
                                                                         # to make the message more readable
      notify("{} marks that {}'s production has increased by 1 GR.".format(me, card)) 
   else: 
      notify("{} marks that {}'s production has increased by 1 GR (This will be automatically taken into account during upkeep).".format(me, card))
   if ProdMinusMarker in card.markers:
      card.markers[ProdMinusMarker] -= 1
   else:
      card.markers[ProdPlusMarker] += 1         
        
def minusProd(card, x = 0, y = 0): 
   mute()
   if ProdPlusMarker in card.markers or ProdMinusMarker in card.markers:
      notify("{} marks that {}'s production has decreased by 1 GR.".format(me, card))
   else:
      notify("{} marks that {}'s production has decreased by 1 GR (This will be automatically taken into account during upkeep).".format(me, card))
   if ProdPlusMarker in card.markers:
      card.markers[ProdPlusMarker] -= 1
   else:
      card.markers[ProdMinusMarker] += 1  

def calcValue(card, type = 'poker'):
   numvalue = numrank(card.rank) + card.markers[ValuePlusMarker] - card.markers[ValueMinusMarker]
   if type == 'raw': return numvalue
   if numvalue > 12 and type == 'numeral': return 13
   if numvalue > 12: return 'K'
   if numvalue == 12 and type == 'numeral': return 12
   if numvalue == 12: return 'Q'
   if numvalue == 11 and type == 'numeral': return 11
   if numvalue == 11: return 'J'
   if numvalue == 1 and type == 'numeral': return 1
   if numvalue == 1: return 'A'
   if numvalue < 1: return 0
   return numvalue
      
def plusValue(card, x = 0, y = 0, notification = loud, valuemod = None): 
# Very much like plus Influence and control, but we don't have to worry about modifying the player's totals
   mute()
   if valuemod == None: valuemod = askInteger("Increase {}'s value by how much? (Current value is: {})".format(card.name,calcValue(card)), 3)
   if ValueMinusMarker in card.markers:
      if valuemod <= card.markers[ValueMinusMarker]:
         card.markers[ValueMinusMarker] -= valuemod
      else:
         card.markers[ValuePlusMarker] += valuemod - card.markers[ValueMinusMarker]
         card.markers[ValueMinusMarker] = 0
   else:
      card.markers[ValuePlusMarker] += valuemod 
   if calcValue(card,'raw') > 13: card.markers[ValuePlusMarker] = 13 - numrank(card.Rank) # Max value is 13 (King)
   if notification == loud:
      notify("{} marks that {}'s value has increased by {} and is now {}.".format(me, card, valuemod, calcValue(card)))
        
def minusValue(card, x = 0, y = 0, notification = loud, valuemod = None): 
   mute()
   if valuemod == None: valuemod = askInteger("Decrease {}'s value by how much? (Current value is: {})".format(card.name,calcValue(card)), 3)
   if ValuePlusMarker in card.markers:
      if valuemod <= card.markers[ValuePlusMarker]:
         card.markers[ValuePlusMarker] -= valuemod
      else:
         card.markers[ValueMinusMarker] += valuemod - card.markers[ValuePlusMarker]
         card.markers[ValuePlusMarker] = 0
   else:
      card.markers[ValueMinusMarker] += valuemod         
   if calcValue(card,'raw') < 1: card.markers[ValueMinusMarker] = numrank(card.Rank)
   if notification == loud:
      notify("{} marks that {}'s value has decreased by {} and is now {}.".format(me, card, valuemod, calcValue(card)))

def setValue(card, x = 0, y = 0):
   mute()
   currentValue = calcValue(card,'raw')
   newValue = askInteger("What should the new value be? (use direct number format: 1 - 13)", calcValue(card,'numeral'))
   if newValue > currentValue: plusValue(card,0,0,silent,(newValue - currentValue))
   if newValue < currentValue: minusValue(card,0,0,silent,(currentValue - newValue))
   notify("{} has set the value of {} to {}".format(me,card,calcValue(card)))
    
def addMarker(cards, x = 0, y = 0): # A simple function to manually add any of the available markers.
   mute()
   marker, quantity = askMarker() # Ask the player how many of the same type they want.
   if quantity == 0: return
   for card in cards: # Then go through their cards and add those markers to each.
      card.markers[marker] += quantity
      notify("{} adds {} {} counter to {}.".format(me, quantity, marker[0], card))	

def cardMemoryStore(card): # Stores markers that card have when they leave play
   global wantedDudes, harrowedDudes, jailbrokenDeeds, ValueMemory, InfluenceRAM, ControlRAM
   # The above are the dictionaries for the markers remembered in the game.
   mute()
   # Lets check if we have any wanted markers to remember
   if re.search(r'Card [mM]emory does not apply to', card.Text): 
      return # If the card does not have card memory, don't store anything.
   if card.markers[WantedMarker] == 1: # If we have a wanted marker, add to the card memory that this dude is wanted
      wantedDudes[card.name] = 1 
   else: 
      try: # We use a try because if the dictionary does not contain an entry, the script will crash
         if wantedDudes[card.name] == 1:  # If we have no wanted marker and the card memory remember them being wanted
            del wantedDudes[card.name] # remove the wanted memory
      except KeyError: pass  # This means that no card was found, so we can just continue.
   # Checking for Harrowed markers to remember
   if card.markers[HarrowedMarker] == 1: # Same as wanted, but once a dude is harrowed, they can never be cleared.
      harrowedDudes[card.name] = 1
   # Checking for Jailbreak markers to remember
   if card.markers[JailbreakMarker] >= 1: # Same as wanted, but we can have more than one counter. So we store how many as well.
      jailbrokenDeeds[card.name] = card.markers[JailbreakMarker]
   # Checking for Value modification markers to remember
   if card.markers[ValuePlusMarker] >= 1 or card.markers[ValueMinusMarker] >= 1: # If our card has its value modified in any way...
      ValueMemory[card.name] = calcValue(card,'numeral') # ...we store the end value.
   else: 
      try:
         if calcValue(card,'numeral') - ValueMemory[card.name] != 0:  
         # If we have no value markers and the card memory remember a different value than the printed one.
            del ValueMemory[card.name] # delete the value memory   
      except KeyError: pass               
   # Checking for Influence markers to remember
   if card.markers[InfluencePlusMarker] > 0: # If we have +influence markers, store how many
      InfluenceRAM[card.name] = card.markers[InfluencePlusMarker] 
   elif card.markers[InfluenceMinusMarker] > 0: # If we have -influence markers, store negative as many.
      InfluenceRAM[card.name] = -card.markers[InfluenceMinusMarker]
   else: # If we have no markers, clear the key for this card if it existed
      try: del InfluenceRAM[card.name]
      except KeyError: pass
   # Checking for Control markers to remember. Same as influence really.
   if card.markers[ControlPlusMarker] > 0:
      ControlRAM[card.name] = card.markers[ControlPlusMarker] 
   elif card.markers[ControlMinusMarker] > 0:
      ControlRAM[card.name] = -card.markers[ControlMinusMarker]
   else:
      try: del ControlRAM[card.name]
      except KeyError: pass
      
def cardMemoryRemember(card): # Checks if the card that just came into play has any markers remembered.
   global wantedDudes, harrowedDudes, jailbrokenDeeds, ValueMemory, InfluenceRAM, ControlRAM
   mute()
   try: # Check if there such a wanted key for this card, to avoid crashing the function by looking for something that doesn't exist.
      if wantedDudes[card.name] == 1: # If we remember the dude being wanted, add a marker
         card.markers[WantedMarker] += 1
   except KeyError: pass # If we don't have a value stored, an exception will be returned, which we we use to pass.
   try: # Same as wanted, but in this case we also make sure that we didn't bring an experienced version that's already harrowed
      if harrowedDudes[card.name] == 1 and not re.search(r'\bHarrowed\b', card.text):
         card.markers[HarrowedMarker] += 1
   except KeyError: pass    
   try: # Similar to the above, but a Deed can have more than one jailbreak marker.
      if jailbrokenDeeds[card.name] >= 1:
         card.markers[JailbreakMarker] = jailbrokenDeeds[card.name]
         for i in range(0, jailbrokenDeeds[card.name]):
            minusControl(card, silent)
   except KeyError: pass    
   try: # Check if any value modification is stored for this card.
      cardValue = calcValue(card,'numeral')
      if  cardValue > ValueMemory[card.name]: # If the value in memory is smaller than the printed value.
         card.markers[ValueMinusMarker] = cardValue - ValueMemory[card.name] # Add some -value tokens until the same level is reached.
      else: 
         card.markers[ValuePlusMarker] = ValueMemory[card.name] - cardValue# Add some +value tokens until the same level is reached.      
   except KeyError: pass       
   try: # Check if any influence modification is stored for this card.
      if InfluenceRAM[card.name] > 0: # If the value is positive, add +influence markers
         card.markers[InfluencePlusMarker] = InfluenceRAM[card.name]
      elif InfluenceRAM[card.name] < 0: # if the value is negative, reverse it and add it as -Influence markers
         card.markers[InfluenceMinusMarker] = -InfluenceRAM[card.name]
   except KeyError: pass # If no key for the card is found, do nothing
   try: # Same as the procedure for influence above
      if ControlRAM[card.name] > 0:
         card.markers[ControlPlusMarker] = ControlRAM[card.name]
      elif ControlRAM[card.name] < 0:
         card.markers[ControlMinusMarker] = -ControlRAM[card.name]
   except KeyError: pass    

         
            
#---------------------------------------------------------------------------
# Deed actions
#---------------------------------------------------------------------------
      
def takeOver(card, x = 0, y = 0): 
# Set a deed as taken over. This is marked via a card highlight. 
# Same process as doesNotUnboot but only for deeds.
# Taken over deeds are deeds who's ownership has been taken by another player. Since you cannot change owners naturally, we work around that.
   mute()
   if card.type == "Deed":
      card.highlight = PlayerColor
      notify("Ownership of {} has passed to {}".format(card, me))
         
def locationTarget(card, x = 0, y = 0): # A function to let others know where you are moving. 
                                        # Unfortunately one cannot initiate card actions on cards they do not control.
                                        # Which prevents us from doing much with this. 
                                        # At the future I'd like to automatically read the locations coordinates and move dudes to an appropriate.
                                        # location, but this requires that one can init actions on cards they do not control.
   mute()
   if card.type == "Deed" or card.type == "Outfit":    
      notify("{} announces {} as the location.".format(me, card))
      card.target
        
def addJailbreakMarker(card, x = 0, y = 0): 
# Jailbreak is the result of a specific action card in the game that is permanent and wipes all the actions from the card so we need to keep track of it.
# It also reduces CP and production. For the reduction of CP we use the minusControl function silently, so that it works better with any +CP markers
# But for the reduced production, we simply take care of it during upkeep.
   mute()
   if card.type == "Deed":
      notify("{} has been severely damaged.".format(card))
      card.markers[JailbreakMarker] += 1
      minusControl(card, x, y, silent)
#---------------------------------------------------------------------------
# Dude actions
#---------------------------------------------------------------------------

def modWantedMarker(card, x = 0, y = 0): # Similar to the doesNotUnboot function but with markers. Adds or removes the wanted marker from a dude.
   mute()
   if card.type == "Dude":
      if card.markers[WantedMarker] == 0:
         notify("{} is now wanted by the law.".format(card))
         card.markers[WantedMarker] += 1
      else:
         notify("The name of {} is cleared.".format(card))
         card.markers[WantedMarker] -= 1	
         
def addHarrowedMarker(card, x = 0, y = 0): # Same as the modWantedMarker but you cannot remove it. You get a notification instead.
   mute()
   if card.type == "Dude":
      if card.markers[HarrowedMarker] == 1 or re.search(r'\bHarrowed.\b', card.text):
         notify("{} is already harrowed! There's only space for one manitou in thar.".format(card))
      else:
         notify("{} has come back from the grave as one of the Harrowed.".format(card))
         card.markers[HarrowedMarker] += 1

def callout(card, x = 0, y = 0): # Notifies that this dude is calling someone out.
   mute()
   if card.type == "Dude":
      notify("{} is calling someone out.".format(card))
      if card.orientation == Rot90: notify("(Remember that you need a card effect to call out someone while booted)".format(card))

def move(card, x = 0, y = 0): # Notifies that this dude is moving without booting
   mute()
   if card.type == "Dude":
      notify("{} is moving without booting.".format(card))
      if card.orientation == Rot90: notify("(Remember that you need a card effect to move while booted)".format(card))
      
def moveBoot(card, x = 0, y = 0): # Notifies that this dude is moving by booting
   mute()
   if card.orientation == Rot0 and card.type == "Dude":
         notify("{} is booting to move.".format(card))
         card.orientation = Rot90

def goods(card, x = 0, y = 0): # Notifies that this dude is about to receive some goods, either by trading or by playing from your hand
                               # In the future, I want to make this function provide a "lock" for incoming goods, and then once you select the goods
                               # ...or play them from hand, they will be automatically moved below the dude with their title showing.
   global AttachingCard
   mute()
   if card.type == "Dude":
      notify("{} is receiving some goods.".format(card))
      if card.orientation == Rot90: notify("(Remember that you need a card effect to receive goods while booted)".format(card))         
      AttachingCard = card
      
def tradeGoods(cards, x = 0, y = 0): # Notified that this dude is giving away some goods. 
                                     # Allows one to target dude and goods at the same time for quick use.
   mute()
   for card in cards:	
      if card.type == "Dude":
         notify("{} is trading away some of their goods.".format(card))
      if card.type == "Goods":
         notify("{} is being traded.".format(card))


   
#---------------------------------------------------------------------------
# Posse actions
#---------------------------------------------------------------------------        

def joinAttack(card, x = 0, y = 0): # Informs that this dude joins an attack posse and highlights him accordingly. 
                                    # This is to help track who is shooting it out. The highlights are cleared by the goToShootout function.
   if card.type == "Dude" : # This is something only dudes can do
       mute () 
       notify("{} is joining the attacking posse.".format(card))
       card.highlight = AttackColor

def joinDefence(card, x = 0, y = 0): # Same as above, but about defensive posse.
   if card.type == "Dude" : 
      mute ()
      notify("{} is joining the defending posse.".format(card))
      card.highlight = DefendColor   

def acceptCallout(card, x = 0, y = 0): # Same as the defending posse but with diferent notification.
   if card.type == "Dude" : 
      mute ()
      notify("{} has accepted the call out.".format(card))
      card.highlight = DefendColor   

def refuseCallout(card, x = 0, y = 0): # Boots the dude and moves him to your home or informs you if they cannot refuse.
   if card.type == "Dude" : 
      chooseSide()
      mute ()
      if card.orientation == Rot90: # If the dude is booted, they cannot refuse without a card effect
         notify ("Booted Dudes cannot refuse a Call Out!")
      else:
         notify("{} has turned yella and run home to hide.".format(card))
         card.orientation = Rot90 # If they refure boot them...
         if playeraxis == Xaxis: card.moveToTable(homeDistance(card) + (playerside * cwidth(card,-4)), 0) # ...and move them where we expect the player's home to be.
         elif playeraxis == Yaxis: card.moveToTable(0,homeDistance(card) + (playerside * cheight(card,-4)))

def runAway(card, x = 0, y = 0): # Same as above pretty much but also clears the shootout highlights.
   if card.type == "Dude" : 
      chooseSide()
      mute ()
      notify("{} is running away from the shootout.".format(card))
      card.orientation = Rot90
      if playeraxis == Xaxis: card.moveToTable(homeDistance(card) + (playerside * cwidth(card,-4)), 0)
      elif playeraxis == Yaxis: card.moveToTable(0,homeDistance(card) + (playerside * cheight(card,-4)))
      card.highlight = None
      
def posseReady (group, x = 0, y = 0):
   notify("{}'s Posse is Ready to throw down!".format(me))     

#---------------------------------------------------------------------------
# Hand and Deck actions
#---------------------------------------------------------------------------

def modInfluence(count = 1, notification = silent): # A function to modify the players influence counter. Can also notify.
   count = num(count) # We need to make sure we get an integer or we will fail horribly. OCTGN doesn't seem to respect its own definitions.
   me.Influence += count # Now increase the influence by the amount passed to us.
   if notification == 'loud' and count > 0: notify("{}'s influence has increased by {}. New total is {}".format(me, count, me.Influence))  
   # We only notify if the function is called as "loud" and we actually modify anything.

def modControl(count = 1, notification = silent): # Same as above but for Control Points
   count = num(count)
   me.Control += count
   if notification == 'loud' and count > 0: notify("{}'s control points have increased by {}. New total is {}".format(me, count, me.Control))         

def payCost(count = 1, notification = silent): # Same as above for Ghost Rock. However we also check if the cost can actually be paid.
   count = num(count)
   if me.GhostRock < count: # If we don't have enough Ghost Rock in the bank, we assume card effects or mistake and notify the player that they need to do things manually.
      if notification == 'loud' and count > 0: notify("{} was supposed to pay {} Ghost Rock but only has {} in their bank. Assuming card effect used. **No GR has been taken!** Please modify your bank manually as necessary".format(me, count, me.GhostRock))   
   else: # Otherwise, just take the money out and inform that we did if we're "loud".
      me.GhostRock -= num(count)
      if notification == 'loud' and count > 0: notify("{} has paid {} Ghost Rock. {} is left their bank".format(me, count, me.GhostRock))  

def cardRMsync(card, notification = loud): # a function which removes influence and CP when a card which had them leaves play.
   if card.type != 'Dude' and card.type != 'Deed': return
   influence = 0
   control = 0
   count = num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker]
   if count > 0: 
      modInfluence(-1 * count)
      if notification == 'loud': notify("{}'s influence is reduced by {}".format(me,count))
   count = num(card.Control) + card.markers[ControlPlusMarker] - card.markers[ControlMinusMarker]
   if count > 0: 
      modControl(-1 * count)
      if notification == 'loud': notify("{}'s control points are reduced by {}".format(me,count))
   
      
def playcard(card): 
# This is the function to play cards from your hand. It's one of the core functions
# It will automatically pay the cost of cards if you can, or inform you if you cannot.
# If the card being played has influence or Control points, those will automatically be added to the player's total.
# Dudes and deeds will be placed at default locations to facilitate quicker play.
   global AttachingCard, AttachedCards
   # Import some variables to know where the player is seated, how much they've built and any cards targets that are receiving attachments.
   mute()
   chooseSide()
   chkcards = [] # Create an empty list to fill later with cards to check
   uniquecards = (tablecard for tablecard in table # Lets gather all the cards from the table that may prevent us from playing our card
                  if tablecard.name == card.name # First the card need to be the same as ours
                  and (tablecard.type == 'Dude'  # But only dude or deeds...
                        or tablecard.type == 'Deed' 
                        or (re.search('Unique.', tablecard.Text) # ...or cards with an explicit "Unique" in the text that are Goods, Improvements or Spells.
                           and (tablecard.type == 'Goods'        # Because otherwise those types can be up to 4 per player.
                              or tablecard.type == 'Improvement' 
                              or tablecard.type == 'Spell')))) 
   for c in uniquecards: # Append the cards from the table and the cards from the boot hill into one list we can go through.
      chkcards.append(c)
   for player in players:
      acedcards = (acedcard for acedcard in player.piles['Boot Hill'] # Go through each player's Boot Hill looking for matches 
                     if acedcard.name == card.name
                     and (acedcard.type == 'Dude' 
                           or acedcard.type == 'Deed' 
                           or (re.search('Unique.', acedcard.Text) 
                              and (acedcard.type == 'Goods' 
                                 or acedcard.type == 'Improvement' 
                                 or acedcard.type == 'Spell')))) 
      for c in acedcards:
         chkcards.append(c)
   for chkcard in chkcards: # Now we check the combined list to see if anything will block us from playing our card from the hand.
      if ((chkcard.controller == me and  # First lets see if this is an experienced version that we can play for free.
            chkcard.group == table and
            (re.search('Experienced', chkcard.Text) or re.search('Experienced', card.Text)))):
         if confirm("You seem to have another version of {} in play. Do you want to replace it with the version in your hand".format(card.name)):
            card.moveToTable(0,0) # I need to replace 0,0 with chkcard.position but it doesn't work!
            chkcard.moveTo(me.piles['Discard Pile'])
            cardRMsync(chkcard, silent)
            modInfluence(card.Influence, silent)
            modControl(card.Control, silent)      
            cardMemoryRemember(card)
            notify ("{} replaced {} with an different experience version".format(me,card))
            return
         else: return
      elif ((re.search('Non-Unique', chkcard.Text) and chkcard.owner != me) or
            re.search('There is no limit', chkcard.Text)): continue 
            # We can still play our own non-unique cards that other players have in play.
      elif chkcard.owner == me: 
            notify ("{} wanted to bring {} into play they but already have a copy of it in play".format(me,card))     
            return
      else: 
         if chkcard.group == table:
            notify ("{} wanted to bring {} in play but it is already on the table and owned by {}".format(me,card,chkcard.owner))
         else: # if they're not on the table, they're in someone's boothill
            notify ("{} wanted to bring {} in play but it currently RIP in {}'s Boot Hill".format(me,card,chkcard.owner))
         return
   if card.type == "Dude" : 
      placeCard(card,'HireDude')
      notify("{} has hired {}.".format(me, card)) # Inform of the new hire      
   elif card.type == "Deed" :   
      placeCard(card,'BuyDeed')
      notify("{} has acquired the deed to {}.".format(me, card))
   elif card.type == "Goods" : # If we're bringing in any goods, just remind the player to pull for gadgets.
      if re.search('Gadget', card.Text): notify("{} is trying to create a {}. Don't forget to pull!".format(me, card))
      else: notify("{} has purchased {}.".format(me, card))
      card.moveToTable(0,0)
   elif card.type == "Spell" : # For spells, just change the notification text.
      card.moveToTable(0,0)
      notify("One of {}'s dudes has learned {}.".format(me, card))      
   elif card.type == "Improvement" : # For improvements, just change the notification text.
      card.moveToTable(0,0)
      notify("{} is improving one of their Deeds with {}.".format(me, card))      
   else: 
      card.moveToTable(0,0) # For anything else, just say they play it.
      notify("{} plays {} from their hand.".format(me, card))
   payCost(card.Cost, loud) # Take cost out of the bank, if there is any.
   cardMemoryRemember(card) # Remember the card's memory.
   if num(card.Control) + card.markers[ControlPlusMarker] - card.markers[ControlMinusMarker] > 0:
      # Increase control, if the new card provides is any.
      modControl(num(card.Control) + card.markers[ControlPlusMarker] - card.markers[ControlMinusMarker], loud) 
   if num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker] > 0:
      # Increase influence, if the new card provides is any.
      modInfluence(num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker], loud) 
   # Increase influence, if the new card provides any or any influence markers are remembered

def setup(group):
# This function is usually the first one the player does. It will setup their home and cards on the left or right of the playfield 
# It will also setup the starting Ghost Rock for the player according to the cards they bring in play, as well as their influence and CP.
   if shared.Phase == 0: # First check if we're on the pre-setup game phase. 
                     # As this function will play your whole hand and wipe your counters, we don't want any accidents.
      global playerside, playerOutfit # Import some necessary variables we're using around the game.
      mute()
      chooseSide() # The classic place where the players choose their side.
      dudecount = 0
      concat_dudes = 'and has the following starting dudes: ' # A string where we collect the names of the dudes we bring in
      concat_home = '' # A string to remember our home's name
      concat_other = '' # A string to remember any other card (like sweetrock's mine)
      me.Deck.shuffle() # First let's shuffle our deck now that we have the chance.
      me.GhostRock = 0 # Wipe the counters
      me.Influence = 0
      me.Control = 0
      defPlayerColor() # Randomize the player's unique colour.       
      if len(table) == 0: # Only create a Town Square token if nobody has setup their side yet.
         TSL = table.create("ac0b08ed-8f78-4cff-a63b-fa1010878af9", 0, 0, 1, True) # Create a Left Town Square card in the middle of the table.
         TSL.moveToTable(2 - cwidth(TSL,0) ,0) # Move the left TS part to the left
         TSR = table.create("72f6c0a9-e4f6-4b17-9777-185f88187ad7", 0, 0, 1, True) # Create a Right Town Square card in the middle of the table.
         TSR.moveToTable(-1,0) 
      for card in group: # For every card in the player's hand... (which should be an outfit and a bunch of dudes usually)
         if card.type == "Outfit" :  # If it's the outfit...
            placeCard(card,'SetupHome')
            me.GhostRock += num(card.properties['Ghost Rock']) # Then we add its starting Ghost Rock to the bank
            playerOutfit = card.Outfit # We make a note of the outfit the player is playing today (used later for upkeep)
            concat_home += card.name # And we save the name.
         elif card.type == "Dude" : # If it's a dude...
            placeCard(card,'SetupDude',dudecount)
            dudecount += 1 # This counter increments per dude, ad we use it to move each other dude further back.
            payCost(card.Cost) # Pay the cost of the dude
            modInfluence(card.Influence, silent) # Add their influence to the total
            concat_dudes += card.name # And prepare a concatenated string with all the names.
            concat_dudes += '. '
         else: # If it's any other card...
            placeCard(card,'SetupOther')
            payCost(card.Cost) # We pay the cost 
            modControl(card.Control) # Add any control to the total
            modInfluence(card.Influence) # Add any influence to the total
            concat_other = ', brings ' # And we create a special concat string to use later for the notification.
            concat_other += card.name # 
            concat_other += ' into play'   
      if dudecount == 0: concat_dudes = 'and has no starting dudes. ' # In case the player has no starting dudes, we change the notification a bit.
      refill() # We fill the player's play hand to their hand size (usually 5)
      notify("{} is playing {} {} {}Starting Ghost Rock is {} and starting influence is {}.".format(me, concat_home, concat_other, concat_dudes, me.GhostRock, me.Influence))  
      # And finally we inform everyone of the player's outfit, starting dudes & other cards, starting ghost rock and influence.
   else: whisper('You can only setup your starting cards during the Pre-Game setup phase') # If this function was called outside the pre-game setup phase
                                                                                           # We assume a mistake and stop.

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
      
def shuffle(group): # A simple function to shuffle piles
   group.shuffle()

def reshuffle(group = me.piles['Discard Pile']): # This function reshuffles the player's discard pile into their deck.
   mute()
   Deck = me.Deck # Just to save us some repetition
   for card in group: card.moveTo(Deck) # Move the player's cards from the discard to their deck one-by-one.
   random = rnd(100, 10000) # Bug 105 workaround. This delays the next action until all animation is done. 
                           # see https://octgn.16bugs.com/projects/3602/bugs/102681
   Deck.shuffle() # Then use the built-in shuffle action
   notify("{} reshuffled their {} into their Deck.".format(me, group.name)) # And inform everyone.

def draw(group = me.Deck): # Draws one card from the deck into the player's hand.
   mute()
   if len(group) == 0: # In case the deck is empty, invoke the reshuffle function.
      notify("{}'s Deck empty. Will reshuffle discard pile".format(me))
      reshuffle()
   group.top().moveTo(me.hand)
   notify("{} draws a card.".format(me))   
   
def Pull(group = me.Deck, x = 0, y = 0): # Draws one card from the deck into the discard pile and announces its value.
   mute()
   Deck = me.Deck
   if len(Deck) == 0: # In case the deck is empty, invoke the reshuffle function.
      notify("{}'s Deck empty. Will reshuffle discard pile".format(me))
      reshuffle()
      random = rnd(100, 10000) # Bug workaround. We wait a bit so that we are sure the cards are there.
   Deck.top().moveTo(me.piles['Discard Pile']) # Move the top card from the deck into the discard pile
   random = rnd(100, 10000) # Wait a bit more, as in multiplayer games, things are slower.
   rank = fullrank(me.piles['Discard Pile'].top().rank) # Save the card's rank
   suit = fullsuit(me.piles['Discard Pile'].top().suit) # Save the card's suit
   notify("{} Pulled a {} {}.".format(me, rank, suit))  # Announce them nicely to everyone.

def drawMany(group, count = None, notification = loud): # This function draws a variable number cards into the player's hand.
   mute()
   if count == None: count = askInteger("Draw how many cards to your Play Hand?", 5) # Ask the player how many cards they want.
   for i in range(0, count): 
      if len(group) == 0: reshuffle() # If before moving a card the deck is empty, reshuffle.
      group.top().moveTo(me.hand) # Then move them one by one into their play hand.
   if notification == loud : notify("{} draws {} cards to their play hand.".format(me, count)) # And if we're "loud", notify what happened.

def setHandSize(group): # A function to modify a player's hand size. This is used during nighfall when refilling the player's hand automatically.
   global handsize
   handsize = askInteger("What is your current hand size?", handsize)
   if handsize == None: handsize = 5
   notify("{} sets their hand size to {}".format(me, handsize))
   
def refill(group = me.hand): # Refill the player's hand to its hand size.
   global handsize
   playhand = len(me.hand) # count how many cards there are currently there.
   if playhand < handsize: drawMany(me.Deck, handsize - playhand, silent) # If there's less cards than the handsize, draw from the deck until it's full.
	
def handDiscard(card, x = 0, y = 0): # Discard a card from your hand.
   mute()
   card.moveTo(me.piles['Discard Pile'])
   notify("{} has discarded {}.".format(me, card))  

def randomDiscard(group): # Discard a card from your hand randomly.
   mute()
   card = group.random() # Select a random card
   if card == None: return # If hand is empty, do nothing.
   notify("{} randomly discards a card.".format(me)) # Inform that a random card was discarded
   card.moveTo(me.piles['Discard Pile']) # Move the card in the discard pile.
	
def moveIntoDeck(group): 
   mute()
   Deck = me.Deck
   for card in group: card.moveTo(Deck)
   notify("{} moves their {} into their Deck.".format(me, group.name))
   
def drawhandMany(group, count = None, notification = loud): #Same as drawMany, but puts the cards into the player's Draw Hand pile.
   mute()
   if count == None: count = askInteger("Draw how many cards to your Draw Hand?", 5)
   for i in range(0, count): 
      if len(group) == 0: reshuffle()
      group.top().moveTo(me.piles['Draw Hand'])
   if notification == loud : notify("{} draws {} cards to their draw hand.".format(me, count))   

def discardDrawHand(group = me.piles['Draw Hand']): # Discards the player's whole Draw Hand.
   mute()
   Discard = me.piles['Discard Pile']
   notify("{} moved their {} ({} cards) to their discard pile.".format(me, group.name, len(group)))    
   for card in group: card.moveTo(Discard)
   
def revealHand(group = me.piles['Draw Hand'], type = lowball, event = None): 
# This function moves 5 cards from the player's Draw Hand pile into the table (normally there should be only 5 there when this function is invoked)
# It also highlights those cards, so that they are not confused with the cards in play
# The cards are moved to the table relevant to the player's side and they are placed next to each other so that their suit&ranks are read easily
# Finally their suit and rank are announced
   chooseSide() # Just in case no side was chosen.
   mute()
   i = 0 
   rank = ['','','','',''] # We create some empty lists for the suits and ranks.
   suit = ['','','','','']
   for card in group: # For each card in the Draw Hand pile...
      foundjoker = 'no'
      if type == 'shootout':
         if card.name == "Fool's Joker": # Check if the card is a joker that is invalid for shootouts. If so, replace it
            card.moveTo(me.piles['Discard Pile'])
            notify ("A {} was revealed in {}'s shootout hand and has been discarded and replaced with a card from the top of the deck".format(card,me))
            if len(me.Deck) == 0: reshuffle()
            card = me.Deck.top() # Replace the card being processed with the top card of the player's deck.
            foundjoker = 'yes' #If we found a joker, make sure we delay the card suit/rank polling a bit.
         if playeraxis == Xaxis: card.moveToTable(homeDistance(card) - cardDistance(card) + i * (cwidth(card) / 4), cheight(card) * 2) 
         elif playeraxis == Yaxis: card.moveToTable(cwidth(card) / -2 + i * (cwidth(card) / 4), homeDistance(card) - cardDistance(card))
         else: card.moveToTable(i * (cwidth(card) / 4) - cwidth(card), 0) # If the player is not on any side, put the cards in the middle.
         # Move the card to the table, slightly to the right of any other cards from this hand
         if foundjoker == 'yes': # We only delay if we exchanged a joker, otherwise reveal gets too slow.
            random = rnd(100, 10000) # Wait a bit more, as in multiplayer games, things are slower.
      else: 
         if card.name == "Death's Head Joker" or card.name == "Fool's Joker": # Same as in shootouts above, but we don't want Death's Heads either
            if card.name == "Death's Head Joker":card.moveTo(me.piles['Boot Hill']) # Death's Head Jokers are aced
            else: card.moveTo(me.piles['Discard Pile']) # Fool's Jokers are discarded
            notify ("A {} was revealed in {}'s lowball hand and has been replaced with a card from the top of the deck".format(card,me))
            if len(me.Deck) == 0: reshuffle()
            card = me.Deck.top() # Put a new card in the draw hand and process that instead.
            foundjoker = 'yes'
         if playeraxis == Xaxis: card.moveToTable(homeDistance(card) - cardDistance(card) + i * (cwidth(card) / 4), cheight(card) * -2)
         elif playeraxis == Yaxis: card.moveToTable(cwidth(card) / -2 + i * (cwidth(card) / 4), homeDistance(card) - cardDistance(card))
         else: card.moveToTable(i * (cwidth(card) / 4) - cwidth(card), 0)
         if foundjoker == 'yes': random = rnd(100, 10000)
      card.highlight = DrawHandColor # Highlight them
      if type == lowball and card == event: card.highlight = EventColor # If this is the selected event, highlight it differently
      rank[i] = card.rank # save their rank into the table
      suit[i] = card.suit # save their suit into the table
      i += 1 # prepare for the next card.
   if type == 'shootout': # Finally, inform the players on what the hand is.
      notify("{}'s Shootout hand is {}{} ({} {}, {} {}, {} {}, {} {}, {} {}). ".format(me, PokerHand(rank,suit,type), cheatinchk(rank,suit), fullrank(rank[0]), fullsuit(suit[0]), fullrank(rank[1]), fullsuit(suit[1]), fullrank(rank[2]), fullsuit(suit[2]), fullrank(rank[3]), fullsuit(suit[3]), fullrank(rank[4]), fullsuit(suit[4])))
   else:
      notify("{}'s Lowball Hand is {}{} ({} {}, {} {}, {} {}, {} {}, {} {}). ".format(me, PokerHand(rank,suit,type), cheatinchk(rank,suit), fullrank(rank[0]), fullsuit(suit[0]), fullrank(rank[1]), fullsuit(suit[1]), fullrank(rank[2]), fullsuit(suit[2]), fullrank(rank[3]), fullsuit(suit[3]), fullrank(rank[4]), fullsuit(suit[4])))
   me.HandRank = PokerHand(rank,suit,type,'comparison')
      
def revealShootoutHand(group): 
# Simply call the procedure above and then compares hands to see who won. 
# The evaluation works only for 2 players but there can never be more than 2 players shooting it out anyway.
   revealHand(group, shootout)
   for player in players:
      if player == me or player.HandRank == 0: continue
      if player.HandRank < me.HandRank: 
         notify("The winner is {} by {} ranks and {} must ace as many of their dudes in this shootout".format(me, (me.HandRank - player.HandRank), player))
         clearHandRanks()
      elif player.HandRank > me.HandRank: 
         notify("The winner is {} by {} ranks and {} must ace as many of their dudes in this shootout".format(player, (me.HandRank - player.HandRank), me))
         clearHandRanks()
      else: 
         notify ("The Shootout is a tie. Both player suffer one casualty")
         clearHandRanks()
   
def revealLowballHand(group = me.piles['Draw Hand'], type = 'normal'): 
   mute()
   # Checking for events before passing on to the reveal function
   evCount = 0
   foundEvents = ['','','','',''] # We need to declare the list because it will not work if it doesn't exist.
   for card in group:
      if card.type == 'Event': # Check if the card is an event and save it's name.
         foundEvents[evCount] = card
         evCount += 1 # Count how many events we have in the hand
   if evCount > 1: # If we have more than one, select one at random and announce it
      eventPointer = rnd(0,evCount-1)
      notify("{} Reveals {} events this turn. The one selected at random to be active is {}".format(me,evCount,foundEvents[eventPointer]))
      revealHand(group, lowball,foundEvents[eventPointer]) # Then pass its name to the next function so that it can be highlighted.
   elif evCount == 1: # If there's only one event, then just pass it's name on the revealHand function so that it can be highlighted.
      notify("{} reveals an event this turn: {}".format(me,foundEvents[0]))
      revealHand(group, lowball,foundEvents[0])      
   else: revealHand(group, lowball)
   winner = lowballWinner()
   if type == 'quick': return winner  # If this function has been called from playLowball(), just return the winner.
   else: 
      try:
         if winner == 'tie': notify ("It's a tie! Y'all need to compare high cards to determine the lucky bastard.")
      except: # Otherwise the evuation will fail which means that the winner variable holds is a player class.
         notify ("The winner is {}".format(winner)) # Thus we can just announce them.
         setWinner(winner)

def lowballWinner():
# This is a function which evaluates the lowball poker hand ranks of all players on the table and determines the winner
# This works for an indefinite number of players and it works as follows
# It checks if all players have revealed a lowball hand. If they haven't then it aborts. 
# This means that the slowest player is always the one who will do the hand comparison
# Once all hands are on the table, it compares hand ranks one by one until it finds the highest 
# then passes the winning player's object to the function that called it (usually revealLowballHand)
   i = 0
   j = 1
   handtie = 'no'
   tied = [] # A list which holds the player objects of players who are tied. Not used atm.
             # We will pass it later to a variable to determine high card winners.
   for player in players:
      if player.HandRank == 0: return 'aborted' # If one player hasn't revealed their hand yet, abort this function
   while i < len(players) -1: # Go once through all the players except the last
      while j < len(players): # Then go through all the players except the starting one in the previous for loop.
#         notify("comp {} to {}. handtie {}.".format(players[i].name,players[j].name,handtie))
         if players[i].HandRank < players[j].HandRank: # If the player we're checking has a lower hand than the next player...
            if handtie == 'yes': # If we have recorded a tie...
               if players[i].HandRank >= tied[0].HandRank: pass # ...and if the tie is lower/equal than the current player. Then do nothing
               else: 
                  handtie = 'no' # If the tie is higher than the current player, then there's no more a tie.
                  winner = players[i]
            else: winner = players[i] # Else record the current player as the winner
         elif players[i].HandRank > players[j].Handrank: # If the primary player (players[i])has lost a hand comparison, 
                                                         # then we take him completely off the comparison and move to the next one.
            if handtie == 'yes': # but if there is a tie...
               if players[j].HandRank >= tied[0].HandRank: pass # ...and if the winning player is not lower/equal than the tie. Then do nothing
               else: 
                  handtie = 'no' # If the tie is higher than the current player, then there's no more a tie.               
                  winner = players[j]
            else: winner = players[j] # And the winner is the player who won the current player
            j += 1
            break # No more need to check this player anymore as he's lost.
         else: 
            handtie = 'yes' # If none of the player's won, it's a tie
            if len(tied) == 0: # If our list isn't populated yet, then add the first two tied players
               tied = [players[i], players[j]]
            else: # If we have some players in the list, only add the compared ones if they're not already in the list.
               if players[i] not in tied: tied.append(players[i])
               if players[j] not in tied: tied.append(players[j])
         j += 1
         if handtie == 'no': 
            if winner ==  players[i] and j == len(players): # If the player we're currently comparing has won all other hands,
               clearHandRanks()                             # and there's no more players to compare with then there' no reason to compare more.
               return winner                                
      i += 1
      j = i + 1
#   notify("winner {}".format(winner))
   clearHandRanks()
   if handtie == 'yes': return 'tie'
   else: return winner # If the loop manages to finish and it's not a tie, then the winner is always the last player in the list.

def playLowball(group = me.Deck):
# This function does the following. 
# * It takes one Ghost Rock from the player and adds it to the shared Lowball pot.
# * It draws 5 cards from the deck with the drawHandMany() function
# * It reveals those 5 with the revealLowballHand() function
# * It receives the winner result of the lowball and announces it
# * If there isn't a tie, then uses it gives the winner all the GR from the shared lowball pot
# * It assigns a "Winner" counter to the winner's outfit and wipes the previous winner's marker.
   mute()
   if shared.Phase != 1:
      whisper("You can use this action during the lowball phase")
      return
   notify ("{} has put their bet in their pot and is playing Lowball".format(me))
   drawhandMany(me.Deck, 5, silent)
   random = rnd(100, 1000) # Bug Workaround
   me.GhostRock -= 1
   shared.counters['Lowball Pot'].value += 1
   winner = revealLowballHand( type='quick')
   try:
      if winner == 'tie': notify ("It's a tie! Y'all need to compare high cards to determine the lucky bastard.")
   except:
      winner.GhostRock += shared.counters['Lowball Pot'].value
      notify("{} is the winner has received {} Ghost Rock from the pot".format(winner, shared.counters['Lowball Pot'].value))
      shared.counters['Lowball Pot'].value = 0
      setWinner(winner)
      
def aceevents(group = me.piles['Discard Pile']): # Goes through your discard pile and moves all events to the boot hill
   mute()
   notify("{} is going through their discard pile and acing all events".format(me))
   for card in group:
      if card.type == 'Event': 
         card.moveTo(me.piles['Boot Hill'])
         notify("{} has aced {}".format(me,card))

def harrow(card):  # Returns the top dude card from boot hill, into the table with a harrowed marker.
   mute()
   if card.type == 'Dude': 
      card.moveToTable(playerside * 200, 0)
      if not re.search(r'\bHarrowed\b', card.text): 
         card.markers[HarrowedMarker] += 1
         notify("{} has brought {} back from the dead as one of the Harrowed".format(me,card))
      else: notify("{} has once again dug themselves out of a shallow grave.".format(card))
      modInfluence(card.Influence, loud)

def permRemove(card): # Takes a card from the boot hill and moves it to the shared "removed from play" pile.
   mute()
   card.moveTo(shared.piles['Removed from Play'])
   notify("{} has permanently removed {} from play".format(me, card))
#---------------------------------------------------------------------------
# Poker Hand Evaluation scripts
#---------------------------------------------------------------------------
   
def PokerHand(rank,suit,type = shootout, result = 'normal'): # Evaluates 5 cards to find which poker hand they create.
   W = 'W'
   jokers = 0 # A counter to remember how many jokers we have in our hand
   for value in rank: 
      if value == W: jokers += 1 # Go through the hand and count the jokers available.
   numranks = [numrank(rank[0]), numrank(rank[1]), numrank(rank[2]), numrank(rank[3]), numrank(rank[4])] # Convert the hand into strict integers
   srank = sorted(numranks) # Sort the integers ascending. This is useful for checking for straights
   chkpairs = pairschk(rank,jokers,type) # So that we don't run the procedure 6 times unnecessarily.
# Look for Dead Man's Hand
   if checkDMH(rank,suit,jokers,type) == 1: 
      if result == 'comparison': return 11
      else: return "11 - Dead Man's Hand!"
# Look for five of a kind
   if chkpairs == 5:  
      if result == 'comparison': return 10
      else: return "10 - Five of a Kind"
# Look for four of a kind
   elif chkpairs == 4:  
      if result == 'comparison': return 8
      else: return "8 - Four of a Kind"
# Look for Full House
   elif chkpairs == 32:  
      if result == 'comparison': return 7
      else: return '7 - Full House'
# Look for a Flush
   elif flushchk(suit,jokers,type) == 1: 
      if straightchk(srank,jokers,type) == 1:  
         if result == 'comparison': return 9
         else: return "9 - Straight Flush"
      else:  
         if result == 'comparison': return 6
         else: return "6 - Flush"
# Look for a straight
   elif straightchk(srank,jokers,type) == 1:  
      if result == 'comparison': return 5
      else: return "5 - Straight"
# Look for Three of a Kind
   elif chkpairs == 3:  
      if result == 'comparison': return 4
      else: return '4 - Three of a kind'
# Look for Two Pairs
   elif chkpairs == 2:  
      if result == 'comparison': return 3
      else: return '3 - Two Pairs'
# Look for One Pair
   elif chkpairs == 1:  
      if result == 'comparison': return 2
      else: return '2 - One Pair'
# If none of the above is true, return a high card result.   
   else:  
      if result == 'comparison': return 1
      else: return '1 - High Card'

def numrank(rank): # Convert card ranks into pure integers for comparison
   if rank == 'W': return 20
   elif rank == 'A': return 1
   elif rank == 'J': return 11
   elif rank == 'Q': return 12
   elif rank == 'K': return 13
   else: return num(rank)
   
def pairschk(rank,jokers = 0,type = shootout): 
# This function checks the hand for similar ranks and depending on how many it finds, it returns the appropriate hand code.
   i = 0
   j = 1
   pairs = [0,0,0,0,0] 
# The above variable is where we'll be storing the matches we find for each hand. 
# The first pair we find will be labeled 1 and the second 2 as long as it's not the same rank as 1.
# This is for prevent us from counting the same pairing more than once. 
# In the end, we'll have a list where each digit is either 0, 1 or 2. 0 means this card's rank matches no other card in the hand
# 1 and 2 means that this card's rank is the same as all the others which are labeled with the same number
# So for example [1,0,1,2,2] is two pairs and [1,1,2,1,2] is full house.
   match1 = 0 # These will count in the end how many matches per rank we have. 
   match2 = 0
   op1 = 5 # These are used to point which was the first card where we found a match of this number.
   op2 = 5
   while i < 4: 
      while j < 5: # We start a nested while. First we check the first card with all the others. 
                   # Then the second one with the 3rd, 4th and 5th.
                   # Then 3rd with 4th and 5th and finally 4th and 5th.
         if rank[i] == rank[j] and rank[i] != 'W': # If we find a match (but we don't care about matching jokers)
#            notify("comparing rank[{}] = {} with rank[{}] = {}".format(i,rank[i],j,rank[j])) # Used for testing
            if op1 == 5: # If our first pointer has not been set
               op1 = i # Put our pointer on the first card of the match
               pairs[i] = 1 # Set the position of those cards to belong to the first matching.
               pairs[j] = 1
            elif rank[op1] == rank[j]: #If the pointer shows that the match belongs to the first group.
               pairs[j] = 1 # set the currently checked card's position to belong to the first group.
            elif op2 == 5: # If there is no match with the first pointer, then use the second one
               op2 = i
               pairs[i] = 2
               pairs[j] = 2
            elif rank[op2] == rank[j]: # Same process
               pairs[j]=2
#            notify("pairs[{},{},{},{},{}]".format(pairs[0],pairs[1],pairs[2],pairs[3],pairs[4])) # Used for testing
         j += 1 
      i += 1 # here we increment the parent loop by one
      j = i+1 # And we set the second loop's iterator to start at one position further.
   for pair in pairs: # Now we count how many matching cards we have for each group
      if pair == 1: match1 += 1
      elif pair == 2: match2 += 1
#   notify("match1 = {}, match2 = {}, type == {}".format(match1, match2, type)) # Used for testing
   if match1 == 5 or (match1 + jokers == 5 and type == shootout): return 5 # Finally we check for hand ranks. 5 sames are Five of a Kind
                                                                           # (Jokers count only in non-lowball hands)
   if match1 == 4 or (match1 + jokers == 4 and type == shootout): return 4 # 4 Sames are Four of a Kind.
   if ((match1 == 3 and match2 == 2) or 
         (match1 == 2 and match2 == 3) or
         (match1 + jokers == 3 and match2 == 2 and type == shootout) or
         (match1 == 2 and match2 + jokers == 3 and type == shootout)): return 32 # Thee of a kind plus one pair is a Full House
   if (match1 == 3 or # 3 sames is a Thee of a Kind
      (match1 + jokers == 3 and type == shootout) or # 1 pair and one joker is also a Three of a Kind
      (jokers == 2 and type == shootout)): return 3 # Also 2 jokers and nothing else is always at the least a Three of a Kind
   if match1 == 2 and match2 == 2: return 2 # 2 of each is Two Pairs 
   if match1 == 2 or (jokers == 1 and type == shootout): return 1 # 2 matching cards is One Pair
                                                                    # And one joker with nothing else is always at least a pair.
   else: return 0
   
def checkDMH(rank,suit,jokers,type = shootout): # This function checks whether the player has a Dead Man's Hand
# A DMH is 2 black Aces (clubs & spades), 2 black eights (clubs & spades) and one Diamond Jack.
   i = 0
   count = 0
   DMH = [0,0,0,0,0] # Create a list. Each digit will become 1 if the corresponding card has been found for DMH.
   while i < 5:
      if rank[i] == '8' and suit[i] == 'S': DMH[0] = 1
      if rank[i] == '8' and suit[i] == 'C': DMH[1] = 1
      if rank[i] == 'A' and suit[i] == 'S': DMH[2] = 1
      if rank[i] == 'A' and suit[i] == 'C': DMH[3] = 1
      if rank[i] == 'J' and suit[i] == 'D': DMH[4] = 1
      i += 1
   for card in DMH:
      if card == 1: count += 1
   if count == 5 or (count + jokers == 5 and type == shootout): return 1
   else: return 0

def flushchk(suit,jokers,type = shootout): # Check if the player's hand is a flush.
   i = 0
   sames = 0 # A variable to count how many pairs of matching suits we find.
   match = '' # A Variable to note which is the first matching suit we've found
   while i < 4:
      if suit[i] == '': suit[i] = 'W' # Jokers have empty suits, so lets give them something to make this easier to read.
      if suit[i] == suit[i+1]: # Check if the suit of cards adjacent to each other is the same
         if match == '' and suit != 'W':  # If we haven't found matching suits yet and and the cards are not jokers...
            match = suit[i] # Mark which is the first matching suit we found (otherwise 2 pairs of different suits will also increase our count.)
            sames += 1 # Increase our count.
         elif suit[i] == match and suit != 'W': sames+=1 # If we have already found a matching suit, check that what we matched now is the same.
      elif jokers >= 1 and i < 3:  # If the cards do not match, but we have at least joker, skip one card and compare with the next as above
         if suit[i] == suit[i+2]:
            if match == '' and suit != 'W': 
               match = suit[i]
               sames += 1
            elif suit[i] == match and suit != 'W': sames+=1
         elif jokers == 2 and i < 2: # If the cards do not match, but we have two jokers, skip two cards and compare with the next as above
            if suit[i] == suit[i+3]: 
               if match == '' and suit != 'W': 
                  match = suit[i]
                  sames += 1
               elif suit[i] == match and suit != 'W': sames+=1
      i += 1
   if sames == 4 or (sames + jokers == 4 and type == shootout): return 1 # Four pairs of matching adjacent cards means all cards are of the same suit
                                                                         # If we have less pairs and enough jokers, it can also be a flush.
   else: return 0

def straightchk(rank,jokers,type = shootout): # Check if the player's hand is a straight.
   i = 0
   straight = 0 # A counter to see how many serial numbers the player has
   while i < 4: 
      if (rank[i] + 1 == rank[i+1] or # We increment our counter if the pair is serial or...
         (rank[i] + 2 == rank[i+1] and jokers >= 1 and type == shootout) or # If the pair is two numbers away 
                                                                            # and the player has at least 1 joker to cover the gap
                                                                            # and this is a non-lowball hand or...
                                                                            # (because in lowball you don't want the jokers to be helping you get a higher hand)
         (rank[i] + 3 == rank[i+1] and jokers == 2 and type == shootout)):  # If the pair is three numbers away 
                                                                            # and the player has 2 jokers to cover the gap
                                                                            # and this is not a lowball hand...
         straight +=1 # Then increase the counter marking how many straight pairs we have by 1.
      i += 1
   if straight == 4 or (straight + jokers == 4 and type == shootout): return 1 # If we have 4 straight pairs (including the jokers), then it's a straight.
   else: return 0

def cheatinchk(rank,suit): # Check if the player is cheating (i.e. has 2 or more cards of the same suit & rank)
   i = 0
   j = 1
   while i < 4:
      while j < 5:
         if rank[i] == rank[j] and suit[i] == suit[j] and rank[i] != 'W': return " (Cheatin'!)"
         j += 1
      i += 1
      j = i + 1
   return ''
   
def fullsuit(suit): # This function simply returns the full suit of the various cards so that notifications read easily.
   if suit == "C": return "Clubs"
   elif suit == "S": return "Spades"
   elif suit == "D": return "Diamonds"
   elif suit == "H": return "Hearts"
   else: return ""
   
def fullrank(rank): # This function simply returns the full rank of non-numeral cards so that notifications read easily
   if rank == "Q": return "Queen of"
   elif rank == "J": return "Jack of"
   elif rank == "K": return "King of"
   elif rank == "A": return "Ace of"
   elif rank == "W": return "Joker"
   else: return rank
 
def clearHandRanks(): # Cleas player hand ranks so that comparisons can start anew
   for player in players:
      player.HandRank = 0 # Make sure that all shootout handrank counters are cleared.