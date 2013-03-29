Doomtown CCG plugin for OCTGN
=============================

The Doomtown Card Game arrives in OCTGN. A Brilliant mix of poker, collectible card games and even elements of chess-like tactics, all set in the Weird West (AKA Deadlands) in the boomtown of Gomorra, out in the pacific maze.

This is the code repository for the game definition. Downloading and installing this in OCTGN is not enough, you'll also need to download the [Markers](http://dbzer0.com/pub/Doomtown/markers.o8s) and the [sets](http://octgn.gamersjudgement.com/viewtopic.php?f=9&t=15). If this is the first time downloading Doomtown for OCTGN, you should just grab [the whole bundle](http://octgn.gamersjudgement.com/viewtopic.php?f=9&t=18) or check out the [step-by-step instructions](http://dbzer0.com/blog/doomtown-on-octgn).

Screenshots
-----------

(Click images for larger versions)

Shootout at High Noon

[![Shootout at High Noon](http://i.imgur.com/JRwLhl.jpg)](http://imgur.com/JRwLh.jpg)

A late-game with 3 players

[![](http://i.imgur.com/Er572l.jpg)](http://i.imgur.com/Er572.jpg)

A two player game in process

[![](http://img.imgur.com/ZqsJel.jpg)](http://i.imgur.com/ZqsJe.jpg)

About the Game
--------------

First of all, lets start with an introduction [From Wikipedia](http://en.wikipedia.org/wiki/Doomtown)

>Doomtown (originally Deadlands:Doomtown) is a collectible card game, a companion to the Deadlands roleplaying setting.

>The game sets itself apart from other CCGs by having each card also serve as a playing card and resolving certain in-game situations with a hand of poker, thus accentuating the Old West atmosphere of the game. The game involves complex deck construction and deep strategies, and was designed with multiplayer (three or more players) in mind. The sheer amount of card draw in the game makes luck much less of a factor, while the movement rules (in the style of board games such as chess) reward intelligent strategy.

>Doomtown was heavily story-driven as well, with a detailed and intriguing storyline that affected cards and play styles. An example was the Fear Level that changed with each expansion and improved or disrupted play styles. Doomtown also held storyline tournaments in which players could directly influence the storyline. For instance, in the finals of a major storyline tournament, Sheriff Coleman was killed by a Sweetrock hired gunman; the sheriff was subsequently killed in the storyline, resulting in new events and action cards, and a later experienced version was Harrowed (revived as a living dead) to avenge his own death.

>As of 2000, Doomtown is officially defunct.

Quite sad indeed. Doomtown is for me one of the most brilliant card games ever designed. It's a sad case that due to licensing, this game cannot be brought back to life, even while the "western" theme is becoming more popular due to recent movies.

One of the great things about Doomtown was indeed how story driven it was and how good the actual storyline was. I wholly suggest that you read [The Big Setup](http://gamesmeister.com/doomtown/viewtopic.php?t=106), which will introduce you to some of the main players in Gommorah and get you in the right mood for the game and if you crave for more, I can't recomment enough the excellent official fiction surrounding the events of the game. [Use this link](http://gamesmeister.com/doomtown/viewtopic.php?p=2554) to read it in the correct chronological order

Linkage
-------

There's [one surviving doomtown forum](http://gamesmeister.com/doomtown/) left, run by Gerry Crowe. Not very active, but there's a few people still interested in the game hanging around there.

You should also check and "Like" the [Deadlands Facebook page](http://www.facebook.com/pages/Deadlands/7361311946). There's also [a Doomtown facebook group](http://www.facebook.com/group.php?gid=129849126180) but it's mostly inactive

[BoardGameGeek has a nice section on Doomtown](http://boardgamegeek.com/boardgame/1037/deadlands-doomtown) as well.


Changelog
---------

### 3.0.7

* Some better concatenation. 

### 3.0.6

* Added the [pixel-western fonts]9http://fav.me/d37tc80) as custom ones for chat and menu.

### 3.0.5

* Modified the placement of revealed draw hands, so that they're not so likely to fall on top of your own deeds.
* Now shootout result announcement should be accurate when your opponent wins.
* Added new "Flight of Angels" marker and accompanying action. The marker can only be placed on outfit cards and is just there to remind you of how many have been played against a player. You will need to download the markers set v3.0.2


### 3.0.4

 * Changed some card properties capitalization to work with the new Python checking in the betas. 
 * Modified the search for the word Harrowed to more correctly understand which dudes have Harrowed as a printed trait
 * Moved the announcement of the event name revealed in lowball to after the card is on the table, to avoid the game announcing that the Event "Card" was revealed.
 * Pre-Game Setup Phase will now also wipe your counters
 * Added an "Add/Reduce Bullets" Markers action. 

### 3.0.3

 * (Hopefully) Fixed bug where other player's wouldn't see the name of goods being played from your hand.

### 3.0.2

 * I've implemented the functions which allow goods to be automatically placed in the right location on their parents. This also works robustly when trading goods between characters, as long as the "Receive Goods" and "Trade goods away" have been used correctly. I.e. first mark the dude with "Receive Goods" and then select all the card you need to move *as well as the dude that is holding them* and use the Trade action.

### 3.0.1

* If you bring a card in that you cannot pay for, your Ghost Rock counter will go to the negative.

### 3.0.0

Jumping Cheezus! A version that does not start with 0! What is the world coming to?

I've finally got the opportunity to mark the definition with a better working number, now that OCTGN 3 is out. I always wanted to move to a "full version" but it would break compatibility with all existing sets, and I couldn't be bothered. Now however that OCTGN 3 is out, I got the opportunity I wanted to.

So starting from this update on, we're on version 3 as well! All sets have also been upgraded in this way which means they break compatibility with the old OCTGN. To avoid you having to redownload all of them, I've created a patch file which you can find in the downloads section. Just download it and if you already have the sets installed, patch them in the game, or if not, put them in a directory and patch that (there's an option during the patching procedure) and then install the sets (Otherwise they will complain about not being a compatible version with the definition). Unfortunately I couldn't make the markers set patchable, so if it gives you an error during patching, just remove and reinstall it (new version also available in the downloads section)

I'm also leaving Doomtown 0.2.23 available, in case someone really wants to use OCTGN2.

Finally, I've made some changes in the code (which make the game incompatible with OCTGN 2), some reorganizing and also some presentation improvements.

* Game will now use the player's color to mark deeds that have been "Taken over"
* Game will now ask the player to confirm before bringing in a card they cannot pay for.
* Changed the draw hand group icon. Now it shows a Dead Man's Hand instead of 3 M:TG cards.
* Card now have a front-side showing an empty Action card with a question mark as an image.
* Game will warn the players if they've started a game with a two-sided table and advise them to start again using a normal one.

### 0.2.23


* Fixed typo when decreasing production on a card. Also increasing and decreasing production will only remind that it's taken into account during upkeep on the first time you do it on a card.
* Moved the Town Centre Token slightly to the left of the table, so as to appear centered between left and right side
* Town Centre will now only spawn once on the table (i.e. you won't see multiple TS' under each other)
* Cards put on the table via lowball are now not counted in automated upkeep (helps for when people forget to discard them first)
* When discarding a lowball hand, if there was an active event inside that needs to be aced afterwards, it will now be automatically aced.
* Fixed bug where two events of the same name, in the same lowball hand, would be highlighted as active at the same time.
* HandRank counters are now reset at the start of each turn and at the end of each Shootout. This is to avoid someone having a leftover handrank (say after a jackelope stampede) which would lead to the future lowball/shootout hands evaluating against it by mistake.

### 0.2.22

Now upkeep and production are mutually exclusive during automated upkeep calculations. That means that a card with 2 upl and 2 prod will not show at all in the turns production and upkeep (in the past you would see that the card produced 2 GR and that you paid 2 GR). This means that you can use +production markers to "nullify" upkeep that you don't need (say because it's cancelled by your home's ability) and -production to signify increased upkeep on a card.

### 0.2.21


* Fixed Bug where in multiplayer, having an invalid Joker autoswapped out of your revealed hand would make the replacement card show as a question mark and not taken into account during eval.
* Fixed a bug during lowbal where if the first two players tie and the last one has a higher rank than the first players, then the first player would be considered to have won, even though they were tied.
* Because of the above bugfix, the Lowball comparison is now tighter and I'm fairly certain it should work correctly for an unlimited amount of players.
* Now Revealed Draw hands are moved to the appropriate locations when there are more than 2 players. They should also be more out of the way
* After a cramped 3-player game, have now spread the starting locations so that homes are farther apart. Should help with location but it means that the table will be initially more zoomed out.
* Tweaked a lot of card placement stuff so that cards are placed in intuitive locations without overlapping with other player's cards (hopefully)
* Made some under-the-hood changes which allow me to tweak the starting location of the players and modify the location of all the rest of their cards easily.


### 0.2.20


* Fixed a bug where cancelling a hand size change would not allow you to change hand size again and would set it to None
* Game setup now usable up to 4 players  (top/bot/left/right). Cards will be setup and played at the appropriate locations

### 0.2.19


* Added a new token showing the Hand Rank Guide. **Update your markers file**
* Added a new function to add said token to the table. You can also "inspect" it.
* Non-valid jokers for draw hands (eg a Death's Head Joker in a lowball hand) will be automatically replaced with the top card of the game and either aced or discarded as they require


### 0.2.18


* When setting up the deck a Town Square composed of two tokens will be created in the middle. This should now be visible for all players. This also means that no shared deck is required. **Don't forget to update your markers file**.


### 0.2.17


* Fixed bug where dudes were not being sent to the right location when going home booted or hired from the left side of the table.
* Fixed bug introduced when working on 0.2.16. Your HandRank counter won't increase to 20 when finishing your posse.
* Fixed bug where drawing cards once your deck was empty wouldn't work. This affected quick lowball and nightfall as well.
* The Lowball winner will now receive a little marker on their outfit to make it easy to remember. **Remember the update your markers file**.
* Card Memory now stores influence and Control, because it's easier to remember to remove counters that do not apply, than it is to remember to put permanent counters that should be there.
* Markers for Influence, Control, production and value have been modified to only has +/- rather than +/-1 as at the size they have now that the card size has been increased, you couldn't see if it was minus or plus anymore without zooming.

### 0.2.16


* *Hand Comparison is finally here*! 
* Game will now compare shootout hands and tell you who won and how many casualties the loser must suffer.
* Game will now compare the lowball hands of all player, determine (and announce) the winner and give them the pot. If there is a tie, high card needs to be determined manually (but this evaluation too is coming on the next version)
* Made everything (i.e table & card) 50% bigger. You will not see any difference as everything scales with your window size, but now each card can fit more markers vertically it and can have up to 2 rows or markers visible. I.e. you can have about 8 more different markers on your card without running into space limits..
* As part of the above, I've set the automatic card placements to be dynamic and dependent on your card sized. This means that in the future I can just change the values of the card size around and things will be automatically scaled.
* Fixed bug where influence on items was counted in upkeep
* Fixed bug where if your deck had less cards than what you tried to draw into your draw hand, you would only draw as many cards your deck had even if you still had cards in your discard pile.
* Added a new function to set value on cards directly
* Now you can never have more +Value markers that would take you over K (unless you add them manually)
* Now checking if a Dude has the printed harrowed trait should be more accurate. 
* Added a new counter per player which records your hand rank. This is going to be used to compare hands after shootouts and lowballs. Do not modify it manually!


### 0.2.15


* You will have to play 1 GR per influence of any Non-drifter Dudes that don't belong to your outfit you've hired.
* At the start of the game now each player will be assigned a random unique highlight color to be used to show "soft" ownership (i.e. not actual ownership of card but just allow the game to know which cards you've taken over with actions like "Hostile Takeover". The player color will not change during game reset to allow consistency between games.
* Replaced the "(Un)Mod Disputed" action with a "Take Over" action, which will mark a deed as if you are the owner. Automated Upkeep will now give you GR for each deed you control and either are the owner or have marked with your colour via "Take Over"
* Added a new token to the markers set which is a little "Town Square" card. **Remember to update your markers set**
* Shared area can now be given some starting cards via shared decks (See new download above). For example, the "Town Square" card
* If a "Town Square" card has been loaded in the "Common" deck of the shared area, it will be automatically be put into play in the middle of the table during setup.
* Implemented a "Remove from Play" function for the Boot Hill which will move these cards to the shared deck's "Removed from Play" pile.

### 0.2.14


* Phases are now global. When you change the phase, you change the phase for every player.
* Some action control on important actions such as Automatic Upkeep/Production, Nightfall Refresh and so on. This means that you will not be able to play those actions unless you're in the right phase. The game will whisper to you in case you used them outside the proper phase. This should prevent accidents such as receiving production during high noon.
* Implemented *Card Memory*! Now any permanent effects, such as becoming wanted or harrowed, will be remembered in case that card leaves play and later comes back in. Unfortunately this will only be remembered for the person who aced/discarded the card from the table. At the moment only wanted, harrowed, jailbreak and value modifications are remembered. In the future I hope to figure out a way to remember harrowed and kung-fu actions as well.
* Implemented the "QuickPlay Lowball" action. This will bet to the shared pot and immediately play a lowball hand of 5 cards and announce their rank. In the future, perhaps this will be modified to compare ranks and tell who won.
* Fixed a bug that prevented you from revealing a lowball hand that had no events.
* Now checking for existing unique cards in play will go through all players' Boot Hills to check if it already exists.
* Given the implementation of card memory, now it's extra imperative that you remember to go back to the pre-game setup phase after a reset, as this will clear all the variables.

### 0.2.13


* Modified the "Play Card" function to check for uniqueness and existing cards. If a unique card is already in play by any player or in your boot hill, the game will prevent you from playing it and notify everyone that you tried to do so. The game will take into account unique goods, spells and improvements as well but not cards where there is no limit to the amount you can have in play. If the unique card is an experienced version of a card you have in play, the game will allow you to replace it at no cost instead.
* Implemented a "Harrow" action for Boot Hill, which will bring the specified dude into play as harrowed.
* When you ace a harrowed dude, the game will ask you to confirm if you've done the harrowed pull already or not.
* Added two new markers for increasing/decreasing card value and two new actions to add those markers. Those actions will also inform you of the value that card has after the modification. **Remember to update your markers file as well**

### 0.2.12


* When revealing a lowball hand, it will now announce if you have any event and highlight it differently. If you have more than one event, it will pick one at random for you.
* Implemented the "Ace all events from discard pile" function


### 0.2.11

Found a bug that was invisible until one tried to install the game for the first time. Then the sets wouldn't install. This should work now.

### 0.2.10


* **Poker Hand evaluation is finally here. W00t!** After a hard weekened of work, I've finally figured how to evaluate all the hands when you reveal them on the table. Not only that, but the hand will take into account any jokers you have to make a better rank *but will ignore the jokers during lowball hands*! It will also tell you if you are a Cheatin' sonnova.
* Acing and Discarding Revealed Draw Hands (from shootout and Lowball) from the table will not longer affect your influence and CPs
* Fixed bunch of other bugs that I've forgotten by now

### 0.2.9


* Standarized the shortcuts
* Implemented the Re-Calculate action. Now if ever you think you have the wrong totals, just hit Ctrl+C and you'll get updated verbosely.
* Now acing and discarding cards reduces your Influence and CP totals according to the amount on the cards that just left play.
* Added some warning when acing wanted and harrowed dudes to make sure you didn't forget the bounty or the pull.
* Minor spelling changes.


### 0.2.8


* Added *Mad Comments* everywhere. Now most functions are explained exquisitively.
* Added phase option to return to the pre-game setup phase. **Use this with caution** as it will reset all global variables (eg which side you're one, how many building your have and so on). Once you are back on the pre-game setup phase, you can then use the the "Setup Starting cards & Hand" function. In general, you should only ever go back to this phase once you've reset the game.
* the "Setup Starting cards & Hand" function has been restricted to only when you are in the pre-game setup phase to avoid nasty accidents.
* Moved Plus/Minus Control/Influence/Production markers, plus High Noon and Shootout ability markers and "Add new marker" into their own subgroup of table card actions.
* Adding plus Influence/Control markers on cards now increases your totals. Adding minus Influence/Control markers on cards reduced your totals but only if the card has any to begin with.
* The "Mark as Jailbroken" now adds a -Control marker, so it synergizes better in case the deed had a +control marker already or gets one in the future.
* Fixed the "Run Away" and "Refuse Call out" actions to now move you left /right instead of top/bottom

### 0.2.7


* Fixed variable production deeds breaking upkeep
* Added some extra markers to mark production increase /decrease. Use these to set the production of your variable production deeds **(Remember to update you markers file!)**
* Upkeep now takes into account production markers and even the jailbroken marker.
* Playing the starting cards will now wipe your GR, CP, and Influence and play pretty much all cards from your hand so make sure you don't use this action by mistake in the middle of the game! This change was done to allow factions which start with cards other than dudes, like the Sweetrock, to automatically play those too.
* Created an unimplemented option to recalculate your total influence and Control Points. When implemented, this will count the number of influence and control you have on cards you control (including their any markers) and update your counters to be accurate. Should be useful in keeping track without mistakes.

### 0.2.6

After personal experimentation, I've changed the default layout as set by card setup and card play, to be left-right instead of top-bottom. Doomtown on OCTGN, without a way to have your own cards in front of you actually benefits tremendously from this setup. By having one player on the left and another on the right, no player is forced to use to very unintuitive and uncomfortable top position. Furthermore, by having your street setup vertically, you can actually setup your dudes much better, by placing them in a row behind each deed and with their items under each. The only thing I'm not liking a lot is the automatic placement of the out-of-town deeds. At the moment they default about 3 cards distance behind your home, starting from the top and being placed downwards. If anyone can figure out a better default placement, please let me know.

### 0.2.5


* Nightfall now refreshes your hand to your hand size. A new command has been added to set you hand size (For having the max inlfuence, or modified by cards like Eureka!)
* Setting up your starting cards now also shuffles your deck, gives you your initial hand of 5 and increases your initial Influence by your starting Dude's influence
* When playing cards from your hand with the "Play Card" command, their cost will be subtracted from your bank and their influence and CP will be added to your totals automatically.
* Added a new counter to the global area called "Phase" which I hope to use to track the phase for all the players simulataneously.


### 0.2.4


* Implemented automated Upkeep/Production. Selecting this option in the table will automatically fill your bank with the production of any GR producing cards you control in play and will bill you for any cards costing upkeep. It will also react appropriately if you don't have enough money to pay all your upkeep costs.
* Updated the "Setup Starting Cards" option to setup your starting GR as well and to also announce your outfit, starting dudes and starting GR.
* Behind the scenes, quite a lot of groundwork to enable me to manipulate your counters as you play and use card. More automation will come from this :)

### 0.2.3


* Added an Option to Inspect cards. This will provide a confirm pop-up window with the text of the card which should help with reading the low quality cards available. Once better, Higher Quality scans are available for most cards, this will be removed to unclutter the interface
* Improved the "Play Card" function. Now notification customized per card type. Deeds will be moved to appropriate locations. In town deeds will even be placed left or right of your home after a confirm option. Dudes will be played at your home. In future versions this will also pay the costs automatically or prevent you from playing the card if you don't have enough money.
* Added the Draw Hand function to setup your starting cards. Will place your home in your area and your starting dudes behind it. This will coordinate for 2 players. In the future I will try to implement a way for up to 4 players to be orientated.
* Orientated the reveal of Draw and Shootout Hands to be placed in each player's area.
* Implemented Posse creation actions that highlight defenders and attackers.
* The Shootout Phase will now clear Posse card highlights when it ends, so don't forget to use it with F10!

### 0.2.2


* Most actions except the more complex now have been imlemented.
* Added some extra markers for +/-1 control and +/-1 influence **so make sure you download the Markers package as well**
* Playing a card from hand works at a basic level atm but it's going to be significantly improved in the future.
* Added some extra actions such as trading items. Now you can select a whole dude and all his items and select "trade items" and it will show an appropriate info.


### 0.2.1


* Fixed discarding a card from hand
* Various small text changes
* Added an unimplemented action to ace all events in the discard pile.

### 0.2.0


* Created the action list I'm going to implement in the future. 
* Separated Core set and markers.
* Updated the python functions with some new options.
* *Now possible to jump to specific phase

### 0.1.4

*First version uploaded. Doomtown core functionality available (Pull cards, draw hand + reveal, table setup etc). Game playable but almost no automation.