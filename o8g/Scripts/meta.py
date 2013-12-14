    # Python Scripts for the Doomtown  CCG definition for OCTGN
    # Copyright (C) 2013  Konstantine Thoukydides

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


import re, time

debugVerbosity = -1 # At -1, means no debugging messages display

Automations = {'Play'      : True, # If True, game will automatically trigger card effects when playing or double-clicking on cards. Requires specific preparation in the sets.
               'Phase'     : True, # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.
               'WinForms'  : True} # If True, game will use the custom Windows Forms for displaying multiple-choice menus and information pop-ups


#---------------------------------------------------------------------------
# Misc
#---------------------------------------------------------------------------
               
def resetAll(): # Clears all the global variables in order to start a new game.
   # Import all our global variables and reset them.
   global playerside, strikeCount, posSideCount, negSideCount, handsize, playerOutfit 
   global wantedDudes, harrowedDudes, jailbrokenDeeds, ValueMemory, debugVerbosity
   debugNotify(">>> resetAll()") #Debug   
   setGlobalVariable('Shootout','False')
   playerside = None
   strikeCount = 0
   posSideCount = 0
   negSideCount = 0
   handsize = 5
   shared.Phase = 0
   me.GhostRock = 0 # Wipe the counters
   me.Influence = 0
   me.Control = 0
   me.VictoryPoints = 0
   me.HandRank = 0
   playerOutfit = None
   wantedDudes.clear() # Clear the dictionaries so that you don't remember card memory from the previous games
   harrowedDudes.clear()
   jailbrokenDeeds.clear()
   ValueMemory.clear()
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostCards.clear()
   setGlobalVariable('Host Cards',str(hostCards))
   setGlobalVariable('Called Out','None')
   setGlobalVariable('Shootout','False')
   if len(players) > 1: debugVerbosity = -1 # Reset means normal game.
   elif debugVerbosity != -1 and confirm("Reset Debug Verbosity?"): debugVerbosity = -1    
   debugNotify("<<< resetAll()") #Debug   

def chkHighNoon():
   if shared.Phase != 3 and confirm(":::WARNING::: You are normally only allowed to take this action during High Noon.\n\nDo you want to jump to High Noon now?"): goToHighNoon()
   
#---------------------------------------------------------------------------
# Card Memory
#---------------------------------------------------------------------------

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
      if harrowedDudes[card.name] == 1 and not re.search(r'\bHarrowed\b\.', card.Text):
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
# Counter Manipulation
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
   if count == 0 : return # If the card has 0 cost, there's nothing to do.
   if me.GhostRock < count: # If we don't have enough Ghost Rock in the bank, we assume card effects or mistake and notify the player that they need to do things manually.
      if notification == loud: 
         if not confirm("You do not seem to have enough Ghost Rock in your bank to play this card. Are you sure you want to proceed? \
         \n(If you do, your GR will go to the negative. You will need to increase it manually as required.)"): return 'ABORT'
         notify("{} was supposed to pay {} Ghost Rock but only has {} in their bank. They'll need to reduce the cost by {} with card effects.".format(me, count, me.GhostRock, count - me.GhostRock))   
         me.GhostRock -= num(count)
      else: me.GhostRock -= num(count) 
   else: # Otherwise, just take the money out and inform that we did if we're "loud".
      me.GhostRock -= num(count)
      if notification == 'loud': notify("{} has paid {} Ghost Rock. {} is left their bank".format(me, count, me.GhostRock))  

def cardRMsync(card, notification = 'loud'): # a function which removes influence and CP when a card which had them leaves play.
   if card.Type != 'Dude' and card.Type != 'Deed': return
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

#---------------------------------------------------------------------------
# Shootout/Lowball Scripts
#---------------------------------------------------------------------------

def lowballWinner():
# This is a function which evaluates the lowball poker hand ranks of all players on the table and determines the winner
# This works for an indefinite number of players and it works as follows
# It checks if all players have revealed a lowball hand. If they haven't then it aborts. 
# This means that the slowest player is always the one who will do the hand comparison
# Once all hands are on the table, it compares hand ranks one by one until it finds the highest 
# then passes the winning player's object to the function that called it (usually revealLowballHand)
   debugNotify(">>> lowballWinner()")
   i = 0
   j = 1
   handtie = False
   if len(players) == 1: winner = me # Code to allow me debug with just one player in the match
   tied = [] # A list which holds the player objects of players who are tied. Not used atm.
             # We will pass it later to a variable to determine high card winners.
   for player in players:
      if player.HandRank == 0: 
         debugNotify("<<< lowballWinner(). ABORTED")
         return 'aborted' # If one player hasn't revealed their hand yet, abort this function
   while i < len(players) - 1: # Go once through all the players except the last
      while j < len(players): # Then go through all the players except the starting one in the previous for loop.
         debugNotify("comp {} to {}. handtie {}.".format(players[i].name,players[j].name,handtie),4)
         if players[i].HandRank < players[j].HandRank: # If the player we're checking has a lower hand than the next player...
            if handtie: # If we have recorded a tie...
               if players[i].HandRank >= tied[0].HandRank: pass # ...and if the tie is lower/equal than the current player. Then do nothing
               else: 
                  handtie = False # If the tie is higher than the current player, then there's no more a tie.
                  winner = players[i]
            else: winner = players[i] # Else record the current player as the winner
         elif players[i].HandRank > players[j].HandRank: # If the primary player (players[i])has lost a hand comparison, 
                                                         # then we take him completely off the comparison and move to the next one.
            if handtie: # but if there is a tie...
               if players[j].HandRank >= tied[0].HandRank: pass # ...and if the winning player is not lower/equal than the tie. Then do nothing
               else: 
                  handtie = False # If the tie is higher than the current player, then there's no more a tie.               
                  winner = players[j]
            else: winner = players[j] # And the winner is the player who won the current player
            j += 1
            break # No more need to check this player anymore as he's lost.
         else: 
            handtie = True # If none of the player's won, it's a tie
            if len(tied) == 0: # If our list isn't populated yet, then add the first two tied players
               tied = [players[i], players[j]]
            else: # If we have some players in the list, only add the compared ones if they're not already in the list.
               if players[i] not in tied: tied.append(players[i])
               if players[j] not in tied: tied.append(players[j])
         j += 1
         if not handtie: 
            if winner ==  players[i] and j == len(players): # If the player we're currently comparing has won all other hands,
               clearHandRanks()                             # and there's no more players to compare with then there' no reason to compare more.
               debugNotify("<<< lowballWinner() with Winner = {}.".format(winner))
               return winner                                
      i += 1
      j = i + 1
   clearHandRanks()
   if handtie: 
      debugNotify("<<< lowballWinner() with a Hand Tie")
      return 'tie'
   else: 
      debugNotify("<<< lowballWinner() with Winner = {}.".format(winner))
      return winner # If the loop manages to finish and it's not a tie, then the winner is always the last player in the list.

def getPotCard(): # Checks if the Lowball Pot Card is on the table and creates it if it isn't.
   mute()
   potCard = None
   for c in table:
      if c.model == "c421c742-c920-4cad-9f72-032c3378191e": 
         potCard = c
         break
   if not potCard:
      potCard = table.create("c421c742-c920-4cad-9f72-032c3378191e",cwidth() / -2,-20, 1, False)
      potCard.orientation = Rot90
   return potCard # We return the card to the function that called us, so that it can use it.
      
#------------------------------------------------------------------------------
# Card Attachments scripts
#------------------------------------------------------------------------------

def findHost(type = 'Goods'):
   debugNotify(">>> findHost(){}".format(extraASDebug())) #Debug
   # Tries to find a host to attach the gear
   hostCards = eval(getGlobalVariable('Host Cards'))
   potentialHosts = [card for card in table  # Potential hosts are:
                     if card.targetedBy # Cards that are targeted by the player
                     and card.targetedBy == me 
                     and card.controller == me # Which the player control
                     and ((card.Type == 'Dude' and type == 'Goods') or (card.Type == 'Deed' and type == 'Improvement'))# That is a Dude or a Deed if we're installing improvements
                     ]
   debugNotify("Finished gatherting potential hosts",2)
   if len(potentialHosts) == 0:
      delayed_whisper(":::ERROR::: Please Target a valid dude for these goods")
      result = None
   else: result = potentialHosts[0] # If a propert host is targeted, then we return it to the calling function. We always return just the first result.
   debugNotify("<<< findHost() with result {}".format(result), 3)
   return result

def attachCard(attachment,host,facing = 'Same'):
   debugNotify(">>> attachCard(){}".format(extraASDebug())) #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostCards[attachment._id] = host._id
   setGlobalVariable('Host Cards',str(hostCards))
   orgAttachments(host,facing)
   debugNotify("<<< attachCard()", 3)
   
def clearAttachLinks(card,type = 'Discard'):
# This function takes care to discard any attachments of a card that left play
# It also clear the card from the host dictionary, if it was itself attached to another card
# If the card was hosted by a Daemon, it also returns the free MU token to that daemon
   debugNotify(">>> clearAttachLinks()") #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
   if cardAttachementsNR >= 1:
      hostCardSnapshot = dict(hostCards)
      for attachmentID in hostCardSnapshot:
         if hostCardSnapshot[attachmentID] == card._id:
            if Card(attachmentID) in table: 
               debugNotify("Attachment exists. Trying to remove.", 2)      
               if type == 'Discard': discard(Card(attachmentID))
               else: ace(Card(attachmentID))
            del hostCards[attachmentID]
   debugNotify("Checking if the card is attached to unlink.", 2)      
   if hostCards.has_key(card._id):
      hostCard = Card(hostCards[card._id])
      del hostCards[card._id] # If the card was an attachment, delete the link
      setGlobalVariable('Host Cards',str(hostCards)) # We store it before calling orgAttachments, so that it has the updated list of hostCards.
      orgAttachments(hostCard) 
   else: setGlobalVariable('Host Cards',str(hostCards))
   debugNotify("<<< clearAttachLinks()", 3) #Debug   


def orgAttachments(card,facing = 'Same'):
# This function takes all the cards attached to the current card and re-places them so that they are all visible
# xAlg, yAlg are the algorithsm which decide how the card is placed relative to its host and the other hosted cards. They are always multiplied by attNR
   debugNotify(">>> orgAttachments()") #Debug
   attNR = 1
   debugNotify(" Card Name : {}".format(card.name), 4)
   if specialHostPlacementAlgs.has_key(card.name):
      debugNotify("Found specialHostPlacementAlgs", 3)
      xAlg = specialHostPlacementAlgs[card.name][0]
      yAlg = specialHostPlacementAlgs[card.name][1]
      debugNotify("Found Special Placement Algs. xAlg = {}, yAlg = {}".format(xAlg,yAlg), 2)
   else: 
      debugNotify("No specialHostPlacementAlgs", 3)
      xAlg = 0 # The Default placement on the X axis, is to place the attachments at the same X as their parent
      yAlg = -(cwidth() / 4)
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachements = [Card(att_id) for att_id in hostCards if hostCards[att_id] == card._id]
   x,y = card.position
   for attachment in cardAttachements:
      if facing == 'Faceup': FaceDown = False
      elif facing == 'Facedown': FaceDown = True
      else: # else is the default of 'Same' and means the facing stays the same as before.
         if attachment.isFaceUp: FaceDown = False
         else: FaceDown = True
      attachment.moveToTable(x + (xAlg * attNR), y + (yAlg * attNR),FaceDown)
      if attachment.controller == me and FaceDown: attachment.peek()
      attachment.setIndex(len(cardAttachements) - attNR) # This whole thing has become unnecessary complicated because sendToBack() does not work reliably
      debugNotify("{} index = {}".format(attachment,attachment.getIndex), 4) # Debug
      attNR += 1
      debugNotify("Moving {}, Iter = {}".format(attachment,attNR), 4)
   card.sendToFront() # Because things don't work as they should :(
   if debugVerbosity >= 4: # Checking Final Indices
      for attachment in cardAttachements: notify("{} index = {}".format(attachment,attachment.getIndex)) # Debug
   debugNotify("<<< orgAttachments()", 3) #Debug      

def makeChoiceListfromCardList(cardList,includeText = False):
# A function that returns a list of strings suitable for a choice menu, out of a list of cards
# Each member of the list includes a card's name, traits, resources, markers and, if applicable, combat icons
   debugNotify(">>> makeChoiceListfromCardList()")
   debugNotify("cardList: {}".format([c.name for c in cardList]), 2)
   targetChoices = []
   debugNotify("About to prepare choices list.", 2)# Debug
   for T in cardList:
      debugNotify("Checking {}".format(T), 4)# Debug
      markers = 'Counters:'
      if T.markers[mdict['WantedMarker']] and T.markers[mdict['WantedMarker']] >= 1: markers += "Wanted,".format(T.markers[mdict['Advancement']])
      if T.markers[mdict['HarrowedMarker']] and T.markers[mdict['HarrowedMarker']] >= 1: markers += "Harrowed,".format(T.markers[mdict['Credits']])
      if markers != 'Counters:': markers += '\n'
      else: markers = ''
      debugNotify("Finished Adding Markers. Adding stats...", 4)# Debug               
      stats = ''
      stats += "Cost: {}. ".format(T.Cost)
      if num(T.Upkeep): stats += "Upkeep: {}.\n".format(T.Upkeep)
      if num(T.Production): stats += "Production: {}.\n".format(T.Production)
      if num(T.Bullets): stats += "Bullets: {}.".format(T.Bullets)
      if num(T.Influence): stats += "Influence: {}.".format(T.Influence)
      if num(T.Control): stats += "CP: {}.".format(T.Control)
      if includeText: cText = '\n' + T.Text
      else: cText = ''
      debugNotify("Finished Adding Stats. Going to choice...", 4)# Debug               
      choiceTXT = "{}\n{}\n{}{}{}".format(T.name,T.Type,markers,stats,cText)
      targetChoices.append(choiceTXT)
   debugNotify("<<< makeChoiceListfromCardList()", 3)
   return targetChoices
   
#------------------------------------------------------------------------------
# Debugging
#------------------------------------------------------------------------------
   
def TrialError(group, x=0, y=0): # Debugging
   global debugVerbosity
   mute()
   ######## Testing Corner ########
   #findTarget('Targeted-atVehicle_and_Fighter_or_Character_and_nonWookie')
   #BotD.moveToTable(0,0) 
   ###### End Testing Corner ######
   #notify("### Setting Debug Verbosity")
   if debugVerbosity >=0: 
      if debugVerbosity == 0: 
         debugVerbosity = 1
         #ImAProAtThis() # At debug level 1, we also disable all warnings
      elif debugVerbosity == 1: debugVerbosity = 2
      elif debugVerbosity == 2: debugVerbosity = 3
      elif debugVerbosity == 3: debugVerbosity = 4
      else: debugVerbosity = 0
      notify("Debug verbosity is now: {}".format(debugVerbosity))
      return
   notify("### Checking Players")
   for player in players:
      if player.name == 'db0' or player.name == 'dbzer0': debugVerbosity = 0
   notify("### Checking Debug Validity")
   if not (len(players) == 1 or debugVerbosity >= 0): 
      whisper("This function is only for development purposes")
      return
   notify("### Setting Table Side")
   if not playerside: chooseSide() # If we've already run this command once, don't recreate the cards.

def extraASDebug(Autoscript = None):
   if Autoscript and debugVerbosity >= 3: return ". Autoscript:{}".format(Autoscript)
   else: return ''
