    # Python Scripts for the Doomtown CCG definition for OCTGN
    # Copyright (C) 2012  Konstantine Thoukydides

    # This python script is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this script.  If not, see <http://www.gnu.org/licenses/>.

#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------

playerside = None # Variable to keep track on which side each player is
playeraxis = None # Variable to keep track on which axis the player is
strikeCount = 0 # Used to automatically place strikes
posSideCount = 0 # Used to automatically place in-town deeds 
negSideCount = 0 # Same as above
handsize = 5 # Used when automatically refilling your hand
playerOutfit = None # Variable to keep track of the player's outfit.
PlayerColor = "#" # Variable with the player's unique colour.
AttachingCard = None # Holds the card about to have other card attached. This needs to become a shared OCTGN variable when available.

wantedDudes = {} # A dictionaty to store which dude is wanted.
harrowedDudes = {} # Which dudes are harrowed
jailbrokenDeeds = {} # Which deeds are jailbroken
ValueMemory = {} # Which cards have amodified value
AttachedCards = {} # A dictionary which holds a coutner for each card, numbering how many attached cards each card has.
InfluenceRAM = {} # Which cards have extra influence
ControlRAM = {} # Which cards have extra cp

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

def goToShootout(group, x = 0, y = 0): # Start or End a Shootout Phase
   if getGlobalVariable('Shootout') == 'False': # The shootout phase just shows a nice notification when it starts and does nothing else.
      notify("A shootout has broken out.".format(me))
      setGlobalVariable('Shootout','True')
   else: # When the shootout ends however, any card.highlights for attacker and defender are quickly cleared.
      notify("The shootout has ended.".format(me))
      clearShootout()

def clearShootout():
   setGlobalVariable('Shootout','False')
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

def ace(card, x = 0, y = 0): # Ace a card. I.e. kill it and send it to the boot hill (i.e.graveyard)
   debugNotify(">>> ace()") #Debug
   mute()
   cardowner = card.owner # We need to save the card onwer for later
   if card.highlight != DrawHandColor: # We don't want to do anything else except move cards when they're not really in play.
      if (card.markers[HarrowedMarker] == 1 or re.search(r'\bHarrowed\b\.', card.Text)) and card.Type == 'Dude': 
         if not confirm("{} was harrowed! Did you remember to do a harrowed pull?".format(card.name)): return
         # if the dude is harrowed, remind the player about the harrowed pull. If they haven't done it, leave the dude in play.
         # In the future, I'll modify the option to perform the harrowed pull automatically.
      if card.markers[WantedMarker] == 1: notify("{} was wanted! Don't forget your bounty.".format(card)) # Remind the player to take a bounty for wanted dudes.
      cardRMsync(card) # This function removes any Influence and Control Points that card had from your total. 
                       # We need to do it before the card is moved to the boot hill because by then, the markers are removed.
      cardMemoryStore(card) # This function stores added effects likes being wanted or harrowed in card memory.
   # Remind the player to take a bounty for wanted dudes. In the future this will be automated.
   notify("{} has aced {}.".format(me, card))
   clearAttachLinks(card,'Ace')
   card.moveTo(cardowner.piles['Boot Hill']) # Cards aced need to be sent to their owner's boot hill
   debugNotify("<<< ace()") #Debug

def discard(card, x = 0, y = 0): # Discard a card.
   debugNotify(">>> discard()") #Debug
   mute()
   cardowner = card.owner
   if card.highlight != DrawHandColor and card.highlight != EventColor: # If the card being discarded was not part of a draw hand
      cardRMsync(card) # Then remove it's influence / CP from the player's pool
      cardMemoryStore(card) # And store it's memory.
      notify("{} has discarded {}.".format(me, card))
   clearAttachLinks(card,'Discard')
   if card.highlight == EventColor and re.search('Ace this card', card.Text): # If the card being discarded was an event in a lowball hand
                                                                              # And that event had instructions to be aced
      card.moveTo(cardowner.piles['Boot Hill'])                               # Then assume player error and ace it         
      notify("{} was the active event and has been aced as per card instructions.".format(card)) # And inform the players.
   else: card.moveTo(cardowner.piles['Discard Pile']) # Cards aced need to be sent to their owner's discard pile
   debugNotify("<<< discard()") #Debug

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
                 if (card.owner == me or card.highlight == me.color) # you cannot pay or produce from cards you do not own.
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
         concat_prod += '{} GR from {}. '.format(str(gr),card) # This is where the concatenation happens
      elif gr < 0: # Much like production, we only add the name to the string if it's having any upkeep
         upk += -gr # Add the negative gr as a positive amount to the variable, so that we can compare it later to  our remaining GR.
         concat_upk += '{} GR for {}. '.format(str(gr),card)
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
   confirm("{}".format(card.Text))

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
         concat_inf += '{} from {}'.format(str(count),card) # Add the count as a string to the concatenated list before the name, e.g. "3 from Black Jack"
         i += 1 # Once we have found at least one card with influence, we separate the rest with commas
         influence += count # We add this card's total influence to our tally.
      count = num(card.Control) + card.markers[ControlPlusMarker] - card.markers[ControlMinusMarker] # Put the card's total influence on a temp marker.
      if count > 0: # Same as influence but for control this time
         if c > 0: concat_cp += ', '
         concat_cp += '{} from {}'.format(str(count),card)
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
              if card.Type == 'Outfit')
   for outfit in outfits:
      if outfit.owner == winner: outfit.markers[WinnerMarker] = 1
      else: outfit.markers[WinnerMarker] = 0

#---------------------------------------------------------------------------
# Marker functions
#---------------------------------------------------------------------------

def plusControl(card, x = 0, y = 0, notification = 'loud', count = 1): # Adds an extra control marker to cards (usually deeds)
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
        
def minusControl(card, x = 0, y = 0, notification = 'loud', count = 1): # Similar to adding Control but we remove instead.
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

def plusInfluence(card, x = 0, y = 0, notification = 'loud', count = 1): # The same as pluControl but for influence
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
        
def minusInfluence(card, x = 0, y = 0, notification = 'loud', count = 1): # The same as minusContorl but for influence
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

def plusBullet(card, x = 0, y = 0): # Very much like plus Value
   mute()
   notify("{} marks that {}'s bullets have increased by 1.".format(me, card))
   if BulletMinusMarker in card.markers:
      card.markers[BulletMinusMarker] -= 1
   else:
      card.markers[BulletPlusMarker] += 1

def minusBullet(card, x = 0, y = 0):
   mute()
   notify("{} marks that {}'s bullets have decreased by 1.".format(me, card))
   if BulletPlusMarker in card.markers:
      card.markers[BulletPlusMarker] -= 1
   else:
      card.markers[BulletMinusMarker] += 1

def calcValue(card, type = 'poker'):
   numvalue = numrank(card.Rank) + card.markers[ValuePlusMarker] - card.markers[ValueMinusMarker]
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
      
def plusValue(card, x = 0, y = 0, notification = 'loud', valuemod = None): 
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
        
def minusValue(card, x = 0, y = 0, notification = 'loud', valuemod = None): 
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
         
def FlightOfAngels(card, x = 0, y = 0): # Add a flight of angels counter
   mute()
   if card.Type != 'Outfit':
      whisper("You can only place this marker on an outfit card")
      return
   notify("{}'s gang is now hounded by a Flight of Angels.".format(me))
   card.markers[FlightOfAngelsMarker] += 1
            
#---------------------------------------------------------------------------
# Deed actions
#---------------------------------------------------------------------------
      
def takeOver(card, x = 0, y = 0):
# Set a deed as taken over. This is marked via a card highlight. 
# Same process as doesNotUnboot but only for deeds.
# Taken over deeds are deeds who's ownership has been taken by another player. Since you cannot change owners naturally, we work around that.
   mute()
   if card.Type == "Deed":
      card.highlight = me.color
      notify("Ownership of {} has passed to {}".format(card, me))
         
def locationTarget(card, x = 0, y = 0): # A function to let others know where you are moving. 
                                        # Unfortunately one cannot initiate card actions on cards they do not control.
                                        # Which prevents us from doing much with this. 
                                        # At the future I'd like to automatically read the locations coordinates and move dudes to an appropriate.
                                        # location, but this requires that one can init actions on cards they do not control.
   mute()
   if card.Type == "Deed" or card.Type == "Outfit":
      notify("{} announces {} as the location.".format(me, card))
      card.target
        
def addJailbreakMarker(card, x = 0, y = 0): 
# Jailbreak is the result of a specific action card in the game that is permanent and wipes all the actions from the card so we need to keep track of it.
# It also reduces CP and production. For the reduction of CP we use the minusControl function silently, so that it works better with any +CP markers
# But for the reduced production, we simply take care of it during upkeep.
   mute()
   if card.Type == "Deed":
      notify("{} has been severely damaged.".format(card))
      card.markers[JailbreakMarker] += 1
      minusControl(card, x, y, silent)
#---------------------------------------------------------------------------
# Dude actions
#---------------------------------------------------------------------------

def modWantedMarker(card, x = 0, y = 0): # Similar to the doesNotUnboot function but with markers. Adds or removes the wanted marker from a dude.
   mute()
   if card.Type == "Dude":
      if card.markers[WantedMarker] == 0:
         notify("{} is now wanted by the law.".format(card))
         card.markers[WantedMarker] += 1
      else:
         notify("The name of {} is cleared.".format(card))
         card.markers[WantedMarker] -= 1	
         
def addHarrowedMarker(card, x = 0, y = 0): # Same as the modWantedMarker but you cannot remove it. You get a notification instead.
   mute()
   if card.Type == "Dude":
      if card.markers[HarrowedMarker] == 1 or re.search(r'\bHarrowed\b\.', card.Text):
         notify("{} is already harrowed! There's only space for one manitou in thar.".format(card))
      else:
         notify("{} has come back from the grave as one of the Harrowed.".format(card))
         card.markers[HarrowedMarker] += 1

def callout(card, x = 0, y = 0): # Notifies that this dude is calling someone out.
   mute()
   if getGlobalVariable('Called Out') != 'None' and not confirm(":::WARNING::: There seems to be another call out in progress. Override it?"): return
   if card.Type == "Dude":
      targetDudes = [c for c in table if c.Type == 'Dude' and c.targetedBy and c.targetedBy == me]
      if not len(targetDudes):
         whisper(":::ERROR::: You need to target the dude you're calling out.")
         return
      targetD = targetDudes[0]
      if targetD == card:
         whisper(":::ERROR::: You cannot call out yourself silly!")
         return         
      notify("{} is calling {} out.".format(card,targetD))
      setGlobalVariable('Called Out',str(targetD._id)) # We store the called out dude as a global variable so that the owner can easier select their answer.
      if card.orientation == Rot90: notify(":::WARNING::: Remember that you need a card effect to call out someone while booted)".format(card))
      card.highlight = AttackColor
   else: whisper(":::ERROR::: You can only initiate a call-out with a dude")

def move(card, x = 0, y = 0): # Notifies that this dude is moving without booting
   mute()
   if card.Type == "Dude":
      notify("{} is moving without booting.".format(card))
      if card.orientation == Rot90: notify("(Remember that you need a card effect to move while booted)".format(card))
      
def moveBoot(card, x = 0, y = 0): # Notifies that this dude is moving by booting
   mute()
   if card.orientation == Rot0 and card.Type == "Dude":
         notify("{} is booting to move.".format(card))
         card.orientation = Rot90

def goods(card, x = 0, y = 0): # Notifies that this dude is about to receive some goods, either by trading or by playing from your hand
                               # This function provides a "lock" for incoming goods, and then once you select the goods
                               # ...or play them from hand, they will are automatically moved below the dude with their title showing.
   global AttachingCard, AttachedCards
   mute()
   if card.Type == "Dude":
      notify("{} is receiving some goods.".format(card))
      if card.orientation == Rot90: notify("(Remember that you need a card effect to receive goods while booted)".format(card))         
      AttachingCard = card # This variable stores the card that is about to receive the goods. Once the goods are received, it is cleared.
      if AttachingCard not in AttachedCards: 
         AttachedCards[AttachingCard] = 1 # We set the dictionary AttachedCards to store an entry for the card which is about to receive goods, so as not to crash our scripts later on.

def tradeGoods(card, x = 0, y = 0): 
   mute()
   if card.Type != "Dude":
     whisper(":::ERROR::: You can only use this action on a dude")
     return
   newHost = findHost()
   if not newHost:
      whisper(":::ERROR::: You need to target a dude in the same location to receive the goods")
      return
   if newHost.orientation != Rot0 and not confirm("You can only trade goods to unbooted dudes. Bypass restriction?"): return
   hostCards = eval(getGlobalVariable('Host Cards'))
   attachedGoods = [Card(att_id) for att_id in hostCards if hostCards[att_id] == card._id and Card(att_id).Type == 'Goods']
   chosenGoods = []
   if len(attachedGoods) == 0: 
      whisper(":::ERROR::: This dude does not hold any goods they can trade.")
      return
   elif len(attachedGoods) == 1: 
      attachCard(attachedGoods[0],newHost)  #If there's only 1 goods attached, we assume that's the one that is going to be moved.
      chosenGoods.append(attachedGoods[0])
   else:
      notify("{} is trading goods some goods between their dudes...".format(me))
      choices = multiChoice("Choose goods to trade to {}".format(newHost.name), makeChoiceListfromCardList(attachedGoods))
      if choices == 'ABORT': 
         notify("{} has aborted the trading action.".format(me))
         return
      for choice in choices: 
         attachCard(attachedGoods[choice],newHost)
         chosenGoods.append(attachedGoods[choice])
   orgAttachments(card)
   notify("{} has traded {} to {}".format(card,[c.name for c in chosenGoods],newHost))
   
#---------------------------------------------------------------------------
# Posse actions
#---------------------------------------------------------------------------        

def joinAttack(card, x = 0, y = 0): # Informs that this dude joins an attack posse and highlights him accordingly. 
                                    # This is to help track who is shooting it out. The highlights are cleared by the goToShootout function.
   if card.Type == "Dude" : # This is something only dudes can do
       mute () 
       notify("{} is joining the attacking posse.".format(card))
       card.highlight = AttackColor

def joinDefence(card, x = 0, y = 0): # Same as above, but about defensive posse.
   if card.Type == "Dude" : 
      mute ()
      notify("{} is joining the defending posse.".format(card))
      card.highlight = DefendColor   

def acceptCallout(ignored, x = 0, y = 0): # Same as the defending posse but with diferent notification.
   mute ()
   if getGlobalVariable('Called Out') == 'None': whisper(":::ERROR::: There seems to be no callout in progress")
   else:
      dude = Card(num(getGlobalVariable('Called Out')))
      notify("{} has accepted the call out. A shootout is breaking out!".format(dude))
      dude.highlight = DefendColor
      setGlobalVariable('Shootout','True') 

def refuseCallout(ignored, x = 0, y = 0): # Boots the dude and moves him to your home or informs you if they cannot refuse.
   chooseSide()
   mute ()
   if getGlobalVariable('Called Out') == 'None': whisper(":::ERROR::: There seems to be no callout in progress")
   else:
      chickenDude = Card(num(getGlobalVariable('Called Out')))
      if chickenDude.orientation == Rot90 and not confirm(":::WARNING::: Normally booted dudes cannot refuse callouts. Bypass restriction and refuse anyway?"): 
         return # If the dude is booted, they cannot refuse without a card effect
      else:
         notify("{} has turned yella and run home to hide.".format(chickenDude))
         chickenDude.orientation = Rot90 # If they refure boot them...
         if playeraxis == Xaxis: chickenDude.moveToTable(homeDistance(chickenDude) + (playerside * cwidth(chickenDude,-4)), 0) # ...and move them where we expect the player's home to be.
         elif playeraxis == Yaxis: chickenDude.moveToTable(0,homeDistance(chickenDude) + (playerside * cheight(chickenDude,-4)))
         orgAttachments(chickenDude)
         setGlobalVariable('Called Out','None') # Finally we clear the Called Out variable
         clearShootout()

def runAway(card, x = 0, y = 0): # Same as above pretty much but also clears the shootout highlights.
   if card.Type == "Dude" : 
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
      
def playcard(card): 
# This is the function to play cards from your hand. It's one of the core functions
# It will automatically pay the cost of cards if you can, or inform you if you cannot.
# If the card being played has influence or Control points, those will automatically be added to the player's total.
# Dudes and deeds will be placed at default locations to facilitate quicker play.
   mute()
   chooseSide()
   chkcards = [] # Create an empty list to fill later with cards to check
   uniquecards = (tablecard for tablecard in table # Lets gather all the cards from the table that may prevent us from playing our card
                  if tablecard.name == card.name # First the card need to be the same as ours
                  and (tablecard.Type == 'Dude'  # But only dude or deeds...
                        or tablecard.Type == 'Deed' 
                        or (re.search('Unique.', tablecard.Text) # ...or cards with an explicit "Unique" in the text that are Goods, Improvements or Spells.
                           and (tablecard.Type == 'Goods'        # Because otherwise those types can be up to 4 per player.
                              or tablecard.Type == 'Improvement' 
                              or tablecard.Type == 'Spell')))) 
   for c in uniquecards: # Append the cards from the table and the cards from the boot hill into one list we can go through.
      chkcards.append(c)
   for player in players:
      acedcards = (acedcard for acedcard in player.piles['Boot Hill'] # Go through each player's Boot Hill looking for matches 
                     if acedcard.name == card.name
                     and (acedcard.Type == 'Dude' 
                           or acedcard.Type == 'Deed' 
                           or (re.search('Unique.', acedcard.Text) 
                              and (acedcard.Type == 'Goods' 
                                 or acedcard.Type == 'Improvement' 
                                 or acedcard.Type == 'Spell')))) 
      for c in acedcards:
         chkcards.append(c)
   for chkcard in chkcards: # Now we check the combined list to see if anything will block us from playing our card from the hand.
      if ((chkcard.controller == me and  # First lets see if this is an experienced version that we can play for free.
            chkcard.group == table and
            (re.search('Experienced', chkcard.Text) or re.search('Experienced', card.Text)))):
         if confirm("You seem to have another version of {} in play. Do you want to replace it with the version in your hand".format(card.name)):
            xp, yp = chkcard.position
            card.moveToTable(xp,yp)
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
   if card.Type == "Dude" : 
      if payCost(card.Cost, loud) == 'ABORT' : return # Check if the player can pay the cost. If not, abort.
      placeCard(card,'HireDude')
      notify("{} has hired {}.".format(me, card)) # Inform of the new hire      
   elif card.Type == "Deed" :   
      if payCost(card.Cost, loud) == 'ABORT' : return # Check if the player can pay the cost. If not, abort.
      placeCard(card,'BuyDeed')
      notify("{} has acquired the deed to {}.".format(me, card))
   elif card.Type == "Goods" or card.Type == "Spell" or card.Type == "Improvement": # If we're bringing in any goods, just remind the player to pull for gadgets.
      if card.Type == "Improvement": hostCard = findHost('Improvement')
      else: hostCard = findHost('Goods')
      if hostCard.orientation != Rot0 and not confirm("You can only purchase goods with unbooted dudes. Bypass restriction?"): return      
      if not hostCard:
         if card.Type == "Improvement": whisper("You need to target the deed which is going to be improved")
         else: whisper("You need to target the dude which is going to purchase the goods")
         return
      else:
         if hostCard.orientation != Rot0 and card.Type != "Improvement" and not confirm("You can only attach goods to unbooted dudes. Bypass restriction?"): return      
         if payCost(card.Cost, loud) == 'ABORT' : return # Check if the player can pay the cost. If not, abort.
         attachCard(card,hostCard)
         if re.search('Gadget', card.Text):
            if confirm("You are trying to create a gadget. Would you like to do a gadget pull at this point?"): 
               gadgetPull = pull(silent = True) # pull returns a tuple with the results of the pull
               hostCard.orientation = Rot90
               notify("{} attempted to manufacture a {} and pulled a {} {}".format(hostCard,card,fullrank(gadgetPull[0]), fullsuit(gadgetPull[1])))
            else: notify("{} has created a {} without a gadget pull.".format(hostCard, card))
         elif card.Type == "Spell": notify("{} has learned {}.".format(hostCard, card))
         elif card.Type == "Improvement": notify("{} has improved {} with {}.".format(me, hostCard, card))
         else : notify("{} has purchased {}.".format(hostCard, card))
   else: 
      if payCost(card.Cost, loud) == 'ABORT' : return # Check if the player can pay the cost. If not, abort.
      card.moveToTable(0,0) # For anything else, just say they play it.
      notify("{} plays {} from their hand.".format(me, card))
   cardMemoryRemember(card) # Remember the card's memory.
   if num(card.Control) + card.markers[ControlPlusMarker] - card.markers[ControlMinusMarker] > 0:
      # Increase control, if the new card provides is any.
      modControl(num(card.Control) + card.markers[ControlPlusMarker] - card.markers[ControlMinusMarker], loud) 
   if num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker] > 0:
      # Increase influence, if the new card provides is any.
      modInfluence(num(card.Influence) + card.markers[InfluencePlusMarker] - card.markers[InfluenceMinusMarker], loud) 
   # Increase influence, if the new card provides any or any influence markers are remembered

def setup(group,x=0,y=0):
# This function is usually the first one the player does. It will setup their home and cards on the left or right of the playfield 
# It will also setup the starting Ghost Rock for the player according to the cards they bring in play, as well as their influence and CP.
   global playerOutfit # Import some necessary variables we're using around the game.
   debugNotify(">>> setup()")
   mute()
   if table.isTwoSided(): 
      if not confirm("This game is NOT designed to be played on a two-sided table. Things will break!! Please start a new game and unckeck the appropriate button. Are you sure you want to continue?"): return
   if playerOutfit and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return # We make sure the player intended to start a new game
   resetAll()
   chooseSide() # The classic place where the players choose their side.
   me.Deck.shuffle() # First let's shuffle our deck now that we have the chance.
   if len([c for c in table if c.name == 'Town Square']) == 0: # Only create a Town Square token if there's not one in the table until now
      TSL = table.create("ac0b08ed-8f78-4cff-a63b-fa1010878af9",2 - cwidth(divisor = 0),0, 1, True) # Create a Left Town Square card in the middle of the table.
      TSR = table.create("72f6c0a9-e4f6-4b17-9777-185f88187ad7",-1,0, 1, True) # Create a Right Town Square card in the middle of the table.
   for card in me.hand: # For every card in the player's hand... (which should be an outfit and a bunch of dudes usually)
      if card.Type == "Outfit" :  # First we do a loop to find an play the outfit, (in case the player managed to mess the order somehow)
         placeCard(card,'SetupHome')
         me.GhostRock += num(card.properties['Ghost Rock']) # Then we add its starting Ghost Rock to the bank
         playerOutfit = card.Outfit # We make a note of the outfit the player is playing today (used later for upkeep)
         concat_home = '{}'.format(card) # And we save the name.
   if not playerOutfit: # If we haven't found an outfit in the player's hand, we assume they made some mistake and break out.
      whisper(":::ERROR:::  You need to have an outfit card in your hand before you try to setup the game. Please reset the board, load a valid deck and try again.")
      return
   debugNotify("About to place Dudes",2)
   dudecount = 0
   concat_dudes = 'and has the following starting dudes: ' # A string where we collect the names of the dudes we bring in
   concat_other = '' # A string to remember any other card (like sweetrock's mine)
   for card in me.hand: # For every card in the player's hand... (which should a bunch of dudes now)
      debugNotify("Placing {}".format(card),4)
      if card.Type == "Dude" : # If it's a dude...
         placeCard(card,'SetupDude',dudecount)
         dudecount += 1 # This counter increments per dude, ad we use it to move each other dude further back.
         payCost(card.Cost) # Pay the cost of the dude
         modInfluence(card.Influence, silent) # Add their influence to the total
         concat_dudes += '{}. '.format(card) # And prepare a concatenated string with all the names.
      else: # If it's any other card...
         placeCard(card,'SetupOther')
         payCost(card.Cost) # We pay the cost 
         modControl(card.Control) # Add any control to the total
         modInfluence(card.Influence) # Add any influence to the total
         concat_other = ', brings {} into play'.format(card) # And we create a special concat string to use later for the notification.
   if dudecount == 0: concat_dudes = 'and has no starting dudes. ' # In case the player has no starting dudes, we change the notification a bit.
   refill() # We fill the player's play hand to their hand size (usually 5)
   notify("{} is playing {} {} {}Starting Ghost Rock is {} and starting influence is {}.".format(me, concat_home, concat_other, concat_dudes, me.GhostRock, me.Influence))  
   # And finally we inform everyone of the player's outfit, starting dudes & other cards, starting ghost rock and influence.

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
   
def pull(group = me.Deck, x = 0, y = 0, silent = False): # Draws one card from the deck into the discard pile and announces its value.
   mute()
   Deck = me.Deck
   if len(Deck) == 0: # In case the deck is empty, invoke the reshuffle function.
      notify("{}'s Deck empty. Will reshuffle discard pile".format(me))
      reshuffle()
      rnd(1, 100) # Bug workaround. We wait a bit so that we are sure the cards are there.
   Deck.top().moveTo(me.piles['Discard Pile']) # Move the top card from the deck into the discard pile
   rnd(1, 100) # Wait a bit more, as in multiplayer games, things are slower.
   rank = me.piles['Discard Pile'].top().Rank # Save the card's rank
   suit = me.piles['Discard Pile'].top().Suit # Save the card's suit
   if not silent: notify("{} Pulled a {} {}.".format(me, fullrank(rank), fullsuit(suit)))  # Announce them nicely to everyone.
   return (rank,suit)

def drawMany(group, count = None, notification = 'loud'): # This function draws a variable number cards into the player's hand.
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
   
def drawhandMany(group, count = None, notification = 'loud'): #Same as drawMany, but puts the cards into the player's Draw Hand pile.
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
   
def revealHand(group = me.piles['Draw Hand'], type = 'lowball', event = None): 
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
         if playeraxis == Xaxis: card.moveToTable(homeDistance(card) - cardDistance(card) * 3 + i * (cwidth(card) / 4), cheight(card) * 2) 
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
         if playeraxis == Xaxis: card.moveToTable(homeDistance(card) - cardDistance(card) * 3 + i * (cwidth(card) / 4), cheight(card) * -2)
         elif playeraxis == Yaxis: card.moveToTable(cwidth(card) / -2 + i * (cwidth(card) / 4), homeDistance(card) - cardDistance(card))
         else: card.moveToTable(i * (cwidth(card) / 4) - cwidth(card), 0)
         if foundjoker == 'yes': random = rnd(100, 10000)
      card.highlight = DrawHandColor # Highlight them
      if type == 'lowball' and card == event: 
         card.highlight = EventColor # If this is the selected event, highlight it differently
         notify("{} reveals an event this turn: {}".format(me,card)) 
      rank[i] = card.Rank # save their rank into the table
      suit[i] = card.Suit # save their suit into the table
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
         notify("The winner is {} by {} ranks and {} must ace as many of their dudes in this shootout".format(player, (player.HandRank - me.HandRank), me))
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
      if card.Type == 'Event': # Check if the card is an event and save it's name.
         foundEvents[evCount] = card
         evCount += 1 # Count how many events we have in the hand
   if evCount > 1: # If we have more than one, select one at random
      eventPointer = rnd(0,evCount-1)
      revealHand(group, 'lowball',foundEvents[eventPointer]) # Then pass its name to the next function so that it can be highlighted and announced.
   elif evCount == 1: # If there's only one event, then just pass it's name on the revealHand function so that it can be highlighted and announced.
      revealHand(group, 'lowball',foundEvents[0])      
   else: revealHand(group, 'lowball')
   winner = lowballWinner()
   if type == 'quick': return winner  # If this function has been called from playLowball(), just return the winner.
   else: 
      try:
         if winner == 'tie': notify ("It's a tie! Y'all need to compare high cards to determine the lucky bastard.")
      except: # Otherwise the evuation will fail which means that the winner variable holds is a player class.
         notify ("The winner is {}".format(winner)) # Thus we can just announce them.
         setWinner(winner)

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
      if card.Type == 'Event': 
         card.moveTo(me.piles['Boot Hill'])
         notify("{} has aced {}".format(me,card))

def harrow(card):  # Returns the top dude card from boot hill, into the table with a harrowed marker.
   mute()
   if card.Type == 'Dude': 
      card.moveToTable(playerside * 200, 0)
      if not re.search(r'\bHarrowed\b\.', card.Text): 
         card.markers[HarrowedMarker] += 1
         notify("{} has brought {} back from the dead as one of the Harrowed".format(me,card))
      else: notify("{} has once again crawled out of a shallow grave.".format(card))
      modInfluence(card.Influence, loud)

def permRemove(card): # Takes a card from the boot hill and moves it to the shared "removed from play" pile.
   mute()
   card.moveTo(shared.piles['Removed from Play'])
   notify("{} has permanently removed {} from play".format(me, card))
