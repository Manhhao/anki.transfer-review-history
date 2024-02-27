# Copy IDs and Review History from Kaishi 1.5k on Core2.3k/Tango

This was written in like 3 hours, I've never worked on Anki plugins before so I excuse the poor code. This code heavily relies on the repository it was forked on, so I thank Kagu-Chan for his code and hope they don't mind me building on top of their code. I won't upload this to AnkiWeb.

This plugin should probably be uninstalled after usage, as it doesn't have any prompts or confirmations before running and it also doesn't remove any functionality of the original code.

As I didn't use Tango, I can't confirm whether this would also work on it. I've tested this a few times on an old backup from before I imported Kaishi, and it seems to work well for Core2.3k atleast.

## Why
After merging the new Kaishi 1.5k deck on top of (in my case) Core 2.3k, you are not able to get updates by simply re-importing the new apkg files. This plugin should fix it, while also providing an option to handle the incorrect duplicates while overwriting the original deck.

## Usage
Delete Transfer Review History Add-On if you have it.

Create a backup of your Anki profile.

Copy contents of this repository into a new folder in your addons21 folder. 
(C:\Users\\<Username>\AppData\Roaming\Anki2\addons21 for most people)

Do steps as outlined in https://github.com/donkuri/Kaishi?tab=readme-ov-file#how-to-import-kaishi-15k-on-top-of-another-deck to import Kaishi ontop of Core2.3k (Delete cards not in Kaishi!).

Delete Duplicates: Notes -> Find Duplicates -> Search in: Word -> Tag Duplicates -> Go Back into the browser and search tag:duplicate -> CTRL + A and then CTRL + DEL to delete the cards. Progress on already reviewed cards will be reset, it's only a few cards and didn't really matter to me.

Re-import Kaishi 1.5k with the .apkg as a normal deck. Specify deck name under Tools->Add-ons->Transfer Review History->Config

```
"source_deck": "Kaishi 1.5k", 
"target_deck": "Core2.3k Version 3" // change this one to whatever your deck is called
```

Run using Tools->Update IDs. Your Anki will freeze, just don't touch it and let it run, you can run Anki with it's console using the bat file in Anki's installation directory to see an output. A pop up will appear when it is finished.

Delete Kaishi 1.5k and then import it using the apkg again.

If everything worked well it should say it updated 1,4xx⁩ cards, while importing the remaining cards (in case of using Core).

Those cards are the duplicates that are missing, you can simply move them to the correct deck by going into the browser, CTRL + A -> Change Deck -> Choose the Deck they should be moved into -> Move Cards. These cards will already have the correct IDs as they were moved over. You can delete the now empty Kaishi 1.5k deck.

That's it, if you now try to import the Kaishi apkg, it should say that 1501 were already present in the collection.

Original README below
# Transfer Review History

Transfers or copies the review history from one card to another

Allows transferring or copying the review history from one card to another, for example when you created a newer, better card, but don't want to update an existing card or relearn anything on this card.

You can either merge or replace the review history on the target and can also automatically let the old card get deleted.

## Compatibility

Tested with 23.10.0 / 23.10.1, earlier versions may work.

Please report issues or future requests on the linked github.

## Changelog

### 2024-01-03

- ADD: Review histories can now be copied instead of being moved
- UPD: A card which had review data moved from or to it will now be marked as modified, this ensures a proper sync
- FIX: Remove left over scheduling data from cards which had data transferred from them
- FIX: Keep the select option enabled when a card is already selected
- FIX: The tooltip in the top left corner of the browser showed the source card twice

### 2023-12-06

- FIX: Fixed an issue where notifications in the browser window would result in a crash

### 2023-11-25

- ADD: Added an option to merge or replace the review history on the targetet item
- FIX: Disallow selecting items without any review history as source
