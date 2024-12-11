# Copy Review History from Core2.3k on Kaishi 1.5k

This was written in like 3 hours, I've never worked on Anki addons before so I excuse the poor code. This code heavily relies on the repository it was forked off, so I thank Kagu-Chan for his code and hope they don't mind me building on top of their code. I won't upload this to AnkiWeb.

This should probably be uninstalled after usage, as it doesn't have any prompts or confirmations before running and it also doesn't remove any functionality of the original code.

As I didn't use Tango, I can't confirm whether this would also work on it. I've tested this a few times on an old backup from before I imported Kaishi, and it seems to work well for Core2.3k atleast.

## Why
After merging the new Kaishi 1.5k deck on top of (in my case) Core 2.3k using the .txt method, you are not able to get updates by simply re-importing the new apkg files. There are also duplicates which are incorrectly overwritten, causing multiple pairs of cards to be identical.

This addon provides an option to simply transfer the review history of your existing Core2.3k deck on to a fresh Kaishi 1.5k deck, while also retaining their original sorting should you decide to reset the card. This works even if you've done the .txt method before to fix the ids and duplicates.

## Usage

Quick video of process: https://www.youtube.com/watch?v=TatE4Cfq-zM

Delete Transfer Review History Add-On if you have it.

__Create a backup of your Anki profile under File->Create Backup.__

Download addon from [here](https://github.com/Manhhao/anki.transfer-review-history/releases)

Extract addon folder into your addons21 folder. 
(```C:\Users\%username%\AppData\Roaming\Anki2\addons21``` for most people)

Import Kaishi 1.5k as a new deck (if you've renamed your Core deck to Kaishi 1.5k rename it to something different, otherwise Anki merges the deck in automatically).

Change Notetype of your original deck. From the .txt guide by Kuube
```
> Select the deck you want to import Kaishi on top of, select Browse, click any card, press ctrl + a, and select Notes > Change Note Type... on the top left menu.  
> Change to the Kaishi 1.5k note type. Make sure the Word field in the New column shows the field your deck uses for the word next to it. 
```
__Delete Duplicates in both decks:__  
Notes -> Find Duplicates ->   
Search in: Word, copy this into Optional filter ```"deck:Kaishi 1.5k"``` (including apostrophes)-> Tag Duplicates  
Repeat, but as optional filter use ```"deck:Core2.3k Version 3"``` (or whatever the name of your original deck is), Tag Duplicates again  
Go Back into the browser and search ```tag:duplicate``` ->  
CTRL + A and then CTRL + DEL to delete the cards. Progress on already reviewed duplicate cards will be reset, it's only a few cards and didn't really matter to me.

Specify deck name under Tools->Add-ons->Name of Folder you created->Config

```
"target_deck": "Kaishi 1.5k", 
"source_deck": "Core2.3k Version 3" // change this one to whatever your deck is called
```

Run using Tools->Review History to Kaishi 1.5k. Your Anki will freeze, just don't touch it and let it run, you can run Anki with it's console using the bat file in Anki's installation directory to see an output. A pop up will appear when it is finished.

You can now safely delete Core2.3k Version 3, if you want to keep the words which are not included in Kaishi, you need to manually move those over.

Import the Kaishi 1.5k apkg again, this should add the duplicates you've deleted before.

That's it, if you now try to import the Kaishi apkg, it should say that 1501 were already present in the collection and for updates you can simply import the new apkg file. If you use FSRS, change the preset of Kaishi to the correct one, alternatively you can just optimize the parameters again.

Thanks [TimTheBimLim](https://github.com/TimTheBimLim) for creating a GitHub account, just to create a PR that improves the addon's speed from a minute to 5 seconds.
