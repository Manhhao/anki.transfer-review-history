from typing import Optional
from aqt import gui_hooks, mw
from aqt.utils import tooltip, qconnect
from aqt.browser import Browser
from aqt.qt import QAction, QMenu
from aqt.operations.scheduling import forget_cards
from anki.cards import Card
from anki.lang import _

def truncateString(string, maxSize = 17) -> str:
  """Truncate a string to a desired length, default 17"""
  if len(string) > maxSize:
    return string[0:maxSize-1] + "..."
  else:
    return string

def run_on_configuration_change(function) -> None:
  """Add event listener to addon manager -> config updated"""
  mw.addonManager.setConfigUpdatedAction(__name__, lambda *_: function())

class Config:
  def __init__(self) -> None:
    config = mw.addonManager.getConfig(__name__)
    self._deleteSourceCard: bool = config["delete_source_card"]
    self._mergeHistories: bool = config["merge_histories"]


  def save(self):
    """Persist configuration changes back to plugin"""
    mw.addonManager.writeConfig(__name__, {
      "delete_source_card": self._deleteSourceCard,
      "merge_histories": self._mergeHistories
    })

  @property
  def deleteSourceCard(self) -> bool:
    """
    Wether or not to delete the original card after transferring the review history.
    Automatically saves on update
    """
    return self._deleteSourceCard

  @deleteSourceCard.setter
  def deleteSourceCard(self, value) -> None:
    self._deleteSourceCard = value
    self.save()

  @property
  def mergeHistories(self) -> bool:
    """
    If true, review histories of two cards will be merged.
    If false, review history of target crad will be wiped before update.
    Automatically saves on update
    """
    return self._mergeHistories

  @mergeHistories.setter
  def mergeHistories(self, value) -> None:
    self._mergeHistories = value
    self.save()

class ReviewHistory:
  def __init__(self) -> None:
    self.config = Config()

    self.createPluginMenu()

    self.browser: (Browser | None) = None
    self.current: (Card | None) = None
    self.menu: (QMenu | None) = None
    self.selectAction: (QAction | None) = None
    self.targetAction: (QAction | None) = None

  def initEvents(self) -> None:
    """
    Listen to proper events in anki ui life cycle:
    * browser_menus_did_init -> Create the menus
    * browser_did_change_row -> Update the menus
    """
    gui_hooks.browser_menus_did_init.append(self.createBrowserMenu)
    gui_hooks.browser_did_change_row.append(lambda _: self.updateMenus())

  def select(self) -> None:
    """Mark currently selected card in browser as selected"""
    self.current = self.selected()
    self.updateMenus()

    tooltip("Selected review history for %d" % self.current.id, self.browser)

  def transferTo(self) -> None:
    """Transfer review history of previously selected card to current card"""
    self.transferReviewHistory(self.current, self.selected())

    self.current = None
    self.updateMenus()

  def selected(self) -> Optional[Card]:
    """Return the currently selected card from browser, if only one is selected"""
    return self.browser.table.get_single_selected_card()

  def hasSelected(self) -> bool:
    """Check if only one card is selected in the browser"""
    return bool(self.selected())

  def updateMenus(self) -> None:
    """Enable or disable menu actions depending on current selection state"""
    if (self.hasSelected()):
      self.selectAction.setDisabled(self.selected().ivl == 0 or (self.selected().id == self.current.id if self.current else not self.hasSelected()))
      self.targetAction.setDisabled(self.selected().id == self.current.id if self.current else True)
    else:
      self.selectAction.setDisabled(True)
      self.targetAction.setDisabled(True)

    self.menu.setDisabled(not (self.selectAction.isEnabled() or self.targetAction.isEnabled()))

  def createBrowserMenu(self, browser: Browser) -> None:
    """Create menus in browser and attach its actions"""
    self.browser = browser

    self.menu = QMenu("Transfer review history", self.browser)
    self.selectAction = QAction("Select current selection for transfer", self.browser)
    self.targetAction = QAction(self.getTargetText(), self.browser)

    self.browser.form.menu_Cards.addMenu(self.menu)
    self.menu.addAction(self.selectAction)
    self.menu.addAction(self.targetAction)

    qconnect(self.selectAction.triggered, self.select)
    qconnect(self.targetAction.triggered, self.transferTo)

    self.updateMenus()

    run_on_configuration_change(self.updateTargetText)

  def updateTargetText(self) -> None:
    """Update target selection text according to delete configuration"""
    try:
      self.targetAction.setText(self.getTargetText())
    except:
      pass

  def getTargetText(self) -> str:
    """Return target selection text according to delete configuration"""
    text: str = "Merge review histories into current selection" if self.config.mergeHistories else "Transfer review history to current selection"

    if (self.config.deleteSourceCard):
      text = text + " and delete source afterwards"

    return text

  def createPluginMenu(self) -> None:
    """Create configuration menu in tools menu"""
    deleteCardsOption = QAction("Delete cards after transferring review history", mw, checkable=True, checked = self.config.deleteSourceCard)
    mergeHistoriesOption = QAction("Merge cards review history", mw, checkable=True, checked = self.config.mergeHistories)

    menu = mw.form.menuTools.addMenu('Transfer review history')
    menu.addAction(deleteCardsOption)
    menu.addAction(mergeHistoriesOption)

    qconnect(deleteCardsOption.triggered, lambda v: self.updateConfig('deleteSourceCard', v))
    qconnect(mergeHistoriesOption.triggered, lambda v: self.updateConfig('mergeHistories', v))

  def updateConfig(self, key: str, value: bool) -> None:
    """Update delete card configuration"""
    setattr(self.config, key, value)

    if (self.menu):
      self.updateTargetText()

  def transferReviewHistory(self, fromCard: Card, toCard: Card) -> None:
    """
    Transfer review history from one card to another.
    Delete the source afterwards if configured to do so.
    Search and reselect target card afterwards.
    """
    fromF1 = fromCard.note().fields[0]
    toF1 = fromCard.note().fields[0]

    mw.progress.start()

    toCard.type = fromCard.type
    toCard.queue = fromCard.queue
    toCard.ivl = fromCard.ivl
    toCard.factor = fromCard.factor
    toCard.lapses = fromCard.lapses
    toCard.left = fromCard.left
    toCard.due = fromCard.due
    toCard.odue = fromCard.odue
    toCard.desired_retention = fromCard.desired_retention
    toCard.memory_state = fromCard.memory_state

    mw.col.db.transact(lambda: self.transferInDb(fromCard, toCard))

    mw.progress.finish()

    self.browser.search()
    self.browser.table.select_single_card(toCard.id)

    toCard.load()

    tooltip("Transferred review history from '%s' to '%s'" % (truncateString(fromF1), truncateString(toF1)) )

  def transferInDb(self, fromCard: Card, toCard: Card) -> None:
    """
    Perform actual data transfer:
    * Persist card changes in database
    * Rewrite or Merge revlog
    * Delete card if requested

    Perform in transaction!
    """
    # As it is not easily doable to transfer the review data by anki itself
    # We do not allow undoing this action.
    # Deleting the card though will be undoable by default
    mw.col.update_card(toCard, skip_undo_entry=True)

    if not self.config.mergeHistories:
      mw.col.db.all("DELETE FROM revlog WHERE cid = ?", toCard.id)

    mw.col.db.all("UPDATE revlog SET cid = ? WHERE cid = ?", toCard.id, fromCard.id)

    if (self.config.deleteSourceCard):
      mw.col.remove_notes_by_card(card_ids=[fromCard.id])

review_history = ReviewHistory()
review_history.initEvents()
