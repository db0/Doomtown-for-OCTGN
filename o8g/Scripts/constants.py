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
BulletPlusMarker = ("+1 Bullet", "5f740820-4c72-4042-b6eb-dcedc77c82ed")
BulletMinusMarker = ("-1 Bullet", "093166b4-fddb-4e67-b6e4-86277faedc91")
JailbreakMarker = ("jailbroken", "692a1ab1-9aa9-49da-aff5-114644da921f")
WinnerMarker = ("Winner", "eeb5f447-f9fc-46b4-846a-a9a40e575cbc")
FlightOfAngelsMarker = ("Flight of Angels", "8ba2d501-e8b7-4df0-a168-be2d16b26daf")

### Misc ###

loud = 'loud' # So that I don't have to use the quotes all the time in my function calls
silent = 'silent' # Same as above
lowball = 'lowball' # Same as above
shootout = 'shootout' # Same as above
Xaxis = 'x'  # Same as above
Yaxis = 'y'	 # Same as above
