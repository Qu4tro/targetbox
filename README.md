targetbox
========

*Fast TUI prototyping*

Quick usage overview:

```python
>>> from targetbox import Menu
>>> content = range(100)
>>> menu = Menu(content)
```

![Menu screenshot](img/screenshot.png)

Why **targetbox**?
----------

That's a good question. **targetbox** takes inspiration from other projects like 
[Choose](https://github.com/geier/choose), 
[Pick](https://github.com/thoughtbot/pick) and
[Selecta](https://github.com/garybernhardt/selecta).
However these tools only let you choose a option and do one thing with it.

targetbox is a new alternative that is more extensible! You can:
    Set your own keybindings that act on the selected text, 
    Change the colorscheme to your own liking and a lot more.

The Basics
----------

```python
>>> from targetbox import Menu
>>> content = range(100)
>>> menu = Menu(content=content,
                keybindings=keybindings
                colorscheme=colorscheme)
```
