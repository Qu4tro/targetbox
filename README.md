Six Thousand (But you can call me 6k)
========

Remmeber to bold all 6k

*Fast TUI prototyping*

Quick usage overview:

```python
>>> from six_thousand import Menu
>>> content = range(100)
>>> menu = Menu(content)
```

![Menu screenshot](img/screenshot.png)

Why 6k?
----------

That's a good question. 6k takes inspiration from other projects like 
[Choose](https://github.com/geier/choose), 
[Pick](https://github.com/thoughtbot/pick) and
[Selecta](https://github.com/garybernhardt/selecta).  
However these tools only let you choose a option and do one thing with it.  

6k is a new alternative that 
allows you to set your own keybindings that act on the selected text, 
change the colorscheme to your own liking and a lot more.

But why it is it called 6k??
----------

While I was starting this project, there were two *TUI-building* toolkits
that I was considering: 
[blessings](https://pypi.python.org/pypi/blessings) or 
[curses](https://docs.python.org/2/library/curses.html).
Two sides of the same coin.

Well, I picked neither and went with [termbox](https://github.com/nsf/termbox).
According to
[wikipedia](https://en.wikipedia.org/wiki/Coin_flipping#Coin_landing_on_its_edge_in_fiction),
whenever you flip a coin there is a 1 in 6000 chance that it lands on its side. 

So there, 6k.


The Basics
----------

```python
>>> from six_thousand import Menu
>>> content = range(100)
>>> menu = Menu(content=content,
                keybindings=keybindings
                colorscheme=colorscheme)
```
