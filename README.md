# Twitch Chat Graph Generator

Run the `generate_graph.py` script to generate a chatter correlation graph 
based on all the json chat logs in the `data/` folder.

```bash
python generate_graph.py
```

The script will output the `.gexf` graph file in the generated `output/` folder.

The graph file can now be converted into a visualisation by [Gephi](https://gephi.org/).

1. Import the graph file into a new workspace
2. In the `Layout` tab, run the `ForceAtlas 2` layout until you are happy with how it looks
3. In the `Statistics` tab, run the `Community Detection` -> `Modularity` algorithm
4. Update `Appearance` -> `Nodes` -> `Color` -> `Partition` with the `Modularity Class` attribute and apply it
5. Update `Appearance` -> `Nodes` -> `Size` -> `Ranking` with the `count` attribute
    - Set the min and max size to a reasonable amount e.g. 3 and 15p
    - Go into the `Spline` menu and choose an appropriate scale e.g. the one with a horizontal inflection point
    - Apply the changes
6. Export the graph as a graph file (in JSON format)
    - You will need to install the `JSON Exporter` plugin from the `Tools` -> `Plugins` menu
    - Double check in the `Options` menu when exporting that the output format is `Graphology`

The generated `.json` file can now be used at 
[data.json](https://github.com/fourers/twitch-chat-atlas-react/blob/main/src/data.json)
in [Twitch Chat Atlas React](https://github.com/fourers/twitch-chat-atlas-react).
