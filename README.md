# Armies Of Sigmar

Generate lists of every possible Age Of Sigmar army for a given set of official rules and personal restrictions.

Either use as a python module or run main.py with a yaml config file.

## TODO
* Add configs for missing factions (see armiesofsigmar/units/)
* No support for allies
* No support for battalions
* Better support for special Battleline alligence (currently supported as two different unit types)
* Better support for special cheaper maximum unit sizes (currently supported as two different unit types)


## Example

    python main.py sylvaneth_example.yaml

This generate all valid 1000 point (minimum 980) Sylvaneth armies using no more than two getting started boxes and no Branchwraiths or Spite Revenants.

    980:  2*Branchwych(80), 2*Dryads(100), Treelord(240), Treelord Ancient(300), Tree-Revenants(80)
    980:  Branchwych(80), 2*Dryads(100), Treelord(240), Treelord Ancient(300), 2*Tree-Revenants(80)
    980:  2*Dryads(100), Treelord(240), Treelord Ancient(300), 3*Tree-Revenants(80)
    980:  2*Branchwych(80), 2*Dryads(100), Treelord Ancient(300), 4*Tree-Revenants(80)
    980:  Branchwych(80), 2*Dryads(100), Spirit of Durthu(400), Treelord Ancient(300)
    980:  Branchwych(80), 2*Dryads(100), Treelord Ancient(300), 5*Tree-Revenants(80)
    1000:  2*Dryads(100), Drycha Hamadreth(280), Kurnoth Hunters(220), Treelord Ancient(300)
    980:  2*Dryads(100), Spirit of Durthu(400), Treelord Ancient(300), Tree-Revenants(80)
    980:  2*Dryads(100), Treelord Ancient(300), 6*Tree-Revenants(80)
    1000:  2*Branchwych(80), Dryads(100), Drycha Hamadreth(280), Treelord Ancient(300), 2*Tree-Revenants(80)
    1000:  Branchwych(80), Dryads(100), Drycha Hamadreth(280), Treelord Ancient(300), 3*Tree-Revenants(80)
    1000:  Branchwych(80), Dryads(100), 2*Kurnoth Hunters(220), Treelord Ancient(300), Tree-Revenants(80)
    980:  Dryads(100), Drycha Hamadreth(280), Kurnoth Hunters(220), Treelord Ancient(300), Tree-Revenants(80)
    1000:  Dryads(100), Drycha Hamadreth(280), Treelord Ancient(300), 4*Tree-Revenants(80)
    1000:  Dryads(100), Kurnoth Hunters(220), 2*Treelord Ancient(300), Tree-Revenants(80)
    1000:  Dryads(100), 2*Kurnoth Hunters(220), Treelord Ancient(300), 2*Tree-Revenants(80)
    1000:  Branchwych(80), Kurnoth Hunters(220), Treelord(240), Treelord Ancient(300), 2*Tree-Revenants(80)
    1000:  Kurnoth Hunters(220), Treelord(240), Treelord Ancient(300), 3*Tree-Revenants(80)
    980:  2*Branchwych(80), Drycha Hamadreth(280), Treelord Ancient(300), 3*Tree-Revenants(80)
    1000:  2*Branchwych(80), 2*Treelord Ancient(300), 3*Tree-Revenants(80)
    1000:  2*Branchwych(80), Kurnoth Hunters(220), Treelord Ancient(300), 4*Tree-Revenants(80)
    980:  Branchwych(80), Drycha Hamadreth(280), Treelord Ancient(300), 4*Tree-Revenants(80)
    1000:  Branchwych(80), 2*Treelord Ancient(300), 4*Tree-Revenants(80)
    980:  Branchwych(80), 2*Kurnoth Hunters(220), Treelord Ancient(300), 2*Tree-Revenants(80)
    1000:  Branchwych(80), Kurnoth Hunters(220), Treelord Ancient(300), 5*Tree-Revenants(80)
    980:  Drycha Hamadreth(280), Treelord Ancient(300), 5*Tree-Revenants(80)
    980:  Kurnoth Hunters(220), 2*Treelord Ancient(300), 2*Tree-Revenants(80)
    1000:  2*Treelord Ancient(300), 5*Tree-Revenants(80)
    980:  2*Kurnoth Hunters(220), Treelord Ancient(300), 3*Tree-Revenants(80)
    1000:  Kurnoth Hunters(220), Treelord Ancient(300), 6*Tree-Revenants(80)
