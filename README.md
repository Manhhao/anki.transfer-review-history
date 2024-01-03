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
