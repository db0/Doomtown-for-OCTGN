import re
import collections
import time

def chkTwoSided():
   mute()
   if table.isTwoSided(): information(":::WARNING::: This game is NOT designed to be played on a two-sided table. Things will not look right!! Please start a new game and unckeck the appropriate button.")
   
def chooseSide(): # Called from many functions to check if the player has chosen a side for this game.
   mute()
   global playerside, playeraxis
   plCount = 0
   for player in sorted(getPlayers()):
      if len(player.Deck) == 0: continue # We ignore spectators
      plCount += 1
      if player != me: continue # We only set our own side
      if plCount == 1: # First player is on the right
         playeraxis = Xaxis
         playerside = 1
         notify(":> {}'s gang arrives on the west side of town.".format(me))
      elif plCount == 2: # First player is on the left
         playeraxis = Xaxis
         playerside = -1
         notify(":> {}' dudes scout warily from the east.".format(me))
      elif plCount == 3: # Third player is on the bottom
         playeraxis = Yaxis
         playerside = 1
         notify(":> {}' outfit sets up on the south entrance.".format(me))
      elif plCount == 4: # Fourth player is on the top
         playeraxis = Yaxis
         playerside = -1
         notify(":> {}'s posse claims the north entrance.".format(me))
      else:
         playeraxis = None  # Fifth and upward players are unaligned
         playerside = 0
         notify(":> {}' arrive late to the party.".format(me))

def checkMovedCard(player,card,fromGroup,toGroup,oldIndex,index,oldX,oldY,x,y,isScriptMove):
   mute()
   debugNotify("isScriptMove = {}".format(isScriptMove))
   if isScriptMove: return # If the card move happened via a script, then all automations should have happened already.
   if fromGroup == me.hand and toGroup == table: 
      if card.Type == 'Outfit': 
         card.moveTo(me.hand)
         setup(group = table)
      else: playcard(card, retainPos = True)
   elif fromGroup != table and toGroup == table and card.owner == me: # If the player moves a card into the table from Deck or Trash, we assume they are installing it for free.
      modControl(num(card.Control))
      modInfluence(num(card.Influence))
   elif fromGroup == table and toGroup != table and card.owner == me: # If the player dragged a card manually from the table to their discard pile...
      if toGroup.name == 'Boot Hill': clearAttachLinks(card, type = 'Ace')
      else: clearAttachLinks(card) # If the card was manually uninstalled or moved elsewhere than trash, then we simply take care of the attachments
   elif fromGroup == table and toGroup == table and card.controller == me: # If the player dragged a card manually to a different location on the table, we want to re-arrange the attachments
      orgAttachments(card) 
