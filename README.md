# discord-friends-graph
This is a script for a discord self-bot intended to create your discord friends graph, that is the set of your discord friends linked together if they are also friends !

This script is based on the [`discord.py-self`](https://github.com/dolfies/discord.py-self) library. Thanks dolfies!

**Warning!** Running this script on your computer will automate your discord account, thus being an act of self-botting which is forbidden by discord's ToS and your account may get banned. Use this at your own risk!

## How to use

### Setup

This script requires you to be able to run `python 3.8` or higher, and that you have installed two libraries on your computer :
- `discord.py-self`: The installation details can be found on the [github page](https://github.com/dolfies/discord.py-self). If you're already using `discord.py` you might need to install this library in a virtual environment in order for those not to conflict, but again, all details are given in the github page.
- `unidecode`: This is used to normalize discord accounts name, which may contain accents, emojis, and special characters. Those may compromise the rendering of the graph at the end.
- `networkx`: A graph-tools library, used to cluster friends.

This can be achieved by executing the following lines.

```bash
python -m venv venv
source venv/bin/activate # or .\venv\Scripts\activate for Windows
pip install -r requirements.txt
```

### Launching the script
Once those libraries are installed, you need to find your discord user token. On August 11th, 2025 [this tutorial](https://www.androidauthority.com/get-discord-token-3149920/) works quite well.

**Warning!** Do not share this token with *anyone*, since this would allow them to have entire control of your discord account. Then, you can write in your command line one of the following two commands (by replacing `token` with your actual token)

```bash
python friends.py [-t|--token] *token*
```
or
```bash
python friends.py [-t|--token] *token* --output *output_file*
```

It should print a line each time it is treating a new friend and warn you when it is done.

If you already used the script to generate a file containing all the useful data, you can use it to generate the graphs again without reusing the self-bot via the command:

``` bash
python friends.py [-i|--input] *input_file*
```


### Rendering the graph
Executing the code will produce one file, `friends.txt` (unless specified otherwise), and a folder `./dots/`. 
- `friends.txt` is a text file containing the text description of the graph with a neighborhood representation, in case you would want to do things with it without executing the script a second time.
- `./dots/` contains the `dot` representation of two graphs: the normal one, and another with a clustering of your discord friends using the [louvain method](https://en.wikipedia.org/wiki/Louvain_method). On linux, you can render it using the bash script `render_graphs.sh` which will provide the results in a generated `./graphs/` directory. On linux and windows, you can also use [`graphviz`](https://graphviz.org/).

**Warning!** Those files will overwrite any other file named identically. Change the names of your files if you don't want to lose your data.



## Potential errors

Some errors can happen during the execution of the script or when rendering the graph. Here are some I have noticed:
- If you don't want to use `unidecode`, the graph may not render properly because of weird discord names, or worse the parsing of their names can make the script crash. To solve the first issue, you can remove by hand the issuing special characters.
- In may/june 2023, discord changed the format of names and every username should be unique. However at the moment the change has not been totally made and some accounts still have the same username, causing them to be fused in the graph. I didn't do anything against it in the script because of the change, and if you are facing this problem you can solve it by hand.

Don't hesitate to contact me if you find any new error!
