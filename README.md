Six Thousand (But you can call me 6k)
========

*Fast TUI prototyping*

Quick usage overview:

```python
>>> from six_thousand import Menu
>>> content = range(100)
>>> menu = Menu(content)
```

![Menu screenshot](img/screenshot.png)

Why **6k**?
----------

That's a good question. **6k** takes inspiration from other projects like 
[Choose](https://github.com/geier/choose), 
[Pick](https://github.com/thoughtbot/pick) and
[Selecta](https://github.com/garybernhardt/selecta).  
However these tools only let you choose a option and do one thing with it.  

6k is a new alternative that is more extensible! You can:
    Set your own keybindings that act on the selected text, 
    Change the colorscheme to your own liking and a lot more.

The Basics
----------

```python
>>> from six_thousand import Menu
>>> content = range(100)
>>> menu = Menu(content=content,
                keybindings=keybindings
                colorscheme=colorscheme)
```
