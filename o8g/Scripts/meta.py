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

def cardRMsync(card, notification = loud): # a function which removes influence and CP when a card which had them leaves play.
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
         elif players[i].HandRank > players[j].HandRank: # If the primary player (players[i])has lost a hand comparison, 
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
      