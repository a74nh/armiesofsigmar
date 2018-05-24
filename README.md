# Armies Of Sigmar

Generate lists of every possible Age Of Sigmar army for a given set of official rules and personal restrictions.

Either use as a python module or run main.py with a yaml config file.

## TODO
* Add configs for missing factions (see armiesofsigmar/units/)
* No support for allies
* No support for battalions
* Maybe better support for special Battleline alligence (currently supported as two different unit types)
* Maybe better support for special cheaper maximum unit sizes (currently supported as two different unit types)


## Example

    python main.py sylvaneth_example.yaml

This generates all valid 1000 point (minimum 980) Sylvaneth armies using no more than two getting started boxes and no Branchwraiths or Spite Revenants.

    1000:  2*Branchwych(160), 2*Dryads(200), Spirit of Durthu(400), Treelord(240)
    980:  2*Branchwych(160), 2*Dryads(200), Treelord(240), Treelord Ancient(300), Tree-Revenants(80)
    980:  2*Branchwych(160), 2*Dryads(200), Kurnoth Hunters(220), Treelord(240), 2*Tree-Revenants(160)
    1000:  2*Branchwych(160), 2*Dryads(200), Treelord(240), 5*Tree-Revenants(400)
    1000:  Branchwych(80), 2*Dryads(200), Spirit of Durthu(400), Treelord(240), Tree-Revenants(80)
    980:  Branchwych(80), 2*Dryads(200), Treelord(240), Treelord Ancient(300), 2*Tree-Revenants(160)
    980:  Branchwych(80), 2*Dryads(200), Kurnoth Hunters(220), Treelord(240), 3*Tree-Revenants(240)
    1000:  Branchwych(80), 2*Dryads(200), Treelord(240), 6*Tree-Revenants(480)
    1000:  2*Dryads(200), Spirit of Durthu(400), Treelord(240), 2*Tree-Revenants(160)
    980:  2*Dryads(200), Treelord(240), Treelord Ancient(300), 3*Tree-Revenants(240)
    980:  2*Branchwych(160), 2*Dryads(200), Kurnoth Hunters(220), Spirit of Durthu(400)
    1000:  2*Branchwych(160), 2*Dryads(200), Spirit of Durthu(400), 3*Tree-Revenants(240)
    980:  2*Branchwych(160), 2*Dryads(200), Treelord Ancient(300), 4*Tree-Revenants(320)
    980:  2*Branchwych(160), 2*Dryads(200), Kurnoth Hunters(220), 5*Tree-Revenants(400)
    1000:  2*Branchwych(160), 2*Dryads(200), 8*Tree-Revenants(640)
    980:  Branchwych(80), 2*Dryads(200), Spirit of Durthu(400), Treelord Ancient(300)
    980:  Branchwych(80), 2*Dryads(200), Kurnoth Hunters(220), Spirit of Durthu(400), Tree-Revenants(80)
    1000:  Branchwych(80), 2*Dryads(200), Spirit of Durthu(400), 4*Tree-Revenants(320)
    980:  Branchwych(80), 2*Dryads(200), Treelord Ancient(300), 5*Tree-Revenants(400)
    980:  Branchwych(80), 2*Dryads(200), Kurnoth Hunters(220), 6*Tree-Revenants(480)
    1000:  Branchwych(80), 2*Dryads(200), 9*Tree-Revenants(720)
    980:  2*Dryads(200), Spirit of Durthu(400), Treelord Ancient(300), Tree-Revenants(80)
    980:  2*Dryads(200), Kurnoth Hunters(220), Spirit of Durthu(400), 2*Tree-Revenants(160)
    1000:  2*Dryads(200), Spirit of Durthu(400), 5*Tree-Revenants(400)
    980:  2*Dryads(200), Treelord Ancient(300), 6*Tree-Revenants(480)
    980:  2*Branchwych(160), Dryads(100), Spirit of Durthu(400), Treelord(240), Tree-Revenants(80)
    980:  2*Branchwych(160), Dryads(100), Treelord(240), 6*Tree-Revenants(480)
    980:  Branchwych(80), Dryads(100), Spirit of Durthu(400), Treelord(240), 2*Tree-Revenants(160)
    980:  Branchwych(80), Dryads(100), Treelord(240), 7*Tree-Revenants(560)
    980:  Dryads(100), Spirit of Durthu(400), Treelord(240), 3*Tree-Revenants(240)
    980:  2*Branchwych(160), Dryads(100), Spirit of Durthu(400), 4*Tree-Revenants(320)
    1000:  2*Branchwych(160), Dryads(100), 3*Kurnoth Hunters(660), Tree-Revenants(80)
    980:  2*Branchwych(160), Dryads(100), 9*Tree-Revenants(720)
    980:  Branchwych(80), Dryads(100), Spirit of Durthu(400), 5*Tree-Revenants(400)
    1000:  Branchwych(80), Dryads(100), 2*Kurnoth Hunters(440), Treelord Ancient(300), Tree-Revenants(80)
    1000:  Branchwych(80), Dryads(100), 3*Kurnoth Hunters(660), 2*Tree-Revenants(160)
    980:  Branchwych(80), Dryads(100), 10*Tree-Revenants(800)
    1000:  Alarielle the Everqueen(600), Dryads(100), Kurnoth Hunters(220), Tree-Revenants(80)
    980:  Dryads(100), Spirit of Durthu(400), 6*Tree-Revenants(480)
    1000:  Dryads(100), Kurnoth Hunters(220), 2*Treelord Ancient(600), Tree-Revenants(80)
    1000:  Dryads(100), 2*Kurnoth Hunters(440), Treelord Ancient(300), 2*Tree-Revenants(160)
    1000:  2*Branchwych(160), 2*Kurnoth Hunters(440), Treelord(240), 2*Tree-Revenants(160)
    1000:  Branchwych(80), Kurnoth Hunters(220), Treelord(240), Treelord Ancient(300), 2*Tree-Revenants(160)
    1000:  Branchwych(80), 2*Kurnoth Hunters(440), Treelord(240), 3*Tree-Revenants(240)
    1000:  Alarielle the Everqueen(600), Treelord(240), 2*Tree-Revenants(160)
    1000:  Kurnoth Hunters(220), Treelord(240), Treelord Ancient(300), 3*Tree-Revenants(240)
    1000:  Alarielle the Everqueen(600), 2*Branchwych(160), 3*Tree-Revenants(240)
    1000:  2*Branchwych(160), 2*Treelord Ancient(600), 3*Tree-Revenants(240)
    1000:  2*Branchwych(160), Kurnoth Hunters(220), Treelord Ancient(300), 4*Tree-Revenants(320)
    980:  2*Branchwych(160), 3*Kurnoth Hunters(660), 2*Tree-Revenants(160)
    1000:  2*Branchwych(160), 2*Kurnoth Hunters(440), 5*Tree-Revenants(400)
    1000:  Alarielle the Everqueen(600), Branchwych(80), 4*Tree-Revenants(320)
    1000:  Branchwych(80), 2*Treelord Ancient(600), 4*Tree-Revenants(320)
    980:  Branchwych(80), 2*Kurnoth Hunters(440), Treelord Ancient(300), 2*Tree-Revenants(160)
    1000:  Branchwych(80), Kurnoth Hunters(220), Treelord Ancient(300), 5*Tree-Revenants(400)
    980:  Branchwych(80), 3*Kurnoth Hunters(660), 3*Tree-Revenants(240)
    1000:  Branchwych(80), 2*Kurnoth Hunters(440), 6*Tree-Revenants(480)
    980:  Alarielle the Everqueen(600), Kurnoth Hunters(220), 2*Tree-Revenants(160)
    1000:  Alarielle the Everqueen(600), 5*Tree-Revenants(400)
    1000:  2*Kurnoth Hunters(440), Spirit of Durthu(400), 2*Tree-Revenants(160)
    980:  Kurnoth Hunters(220), 2*Treelord Ancient(600), 2*Tree-Revenants(160)
    1000:  2*Treelord Ancient(600), 5*Tree-Revenants(400)
    980:  2*Kurnoth Hunters(440), Treelord Ancient(300), 3*Tree-Revenants(240)
    1000:  Kurnoth Hunters(220), Treelord Ancient(300), 6*Tree-Revenants(480)


## Example 2

Using this config file will generate all 1000 point armies with Alarielle and some limited support:

    rulebook: ghb2017
    size: vanguard
    unitlists: [sylvaneth]
    keywords: [SYLVANETH]
    units:
      Alarielle the Everqueen : { min: 1, max: -1 }
      Dryads : { min: 0, max: -1 }
      Tree-Revenants : { min: 0, max: -1 }
      Kurnoth Hunters : { min: 0, max: -1 }
      __Others : { min: 0, max: 0 }

When run with the verbose option:

    python main.py --verbose alarielle.yaml

Will gives stats for each army:

    Points 1000
    Wounds: 56, Models: 41, Bravery/Unit: 6.10, Save/Wound: 4.43+
	1 Alarielle the Everqueen
		Points: 600
		Roles: Leader, Behemoth
		M/W/S/B: 16*/16/3+/10
	40 Dryads
		Points: 400
		Roles: Battleline
		M/W/S/B: 7/1(40)/5+/6
     
    Points 1000
    Wounds: 46, Models: 19, Bravery/Unit: 6.37, Save/Wound: 3.98+
	1 Alarielle the Everqueen
		Points: 600
		Roles: Leader, Behemoth
		M/W/S/B: 16*/16/3+/10
	10 Dryads
		Points: 100
		Roles: Battleline
		M/W/S/B: 7/1(10)/5+/6
	3 Kurnoth Hunters
		Points: 220
		Roles:
		M/W/S/B: 5/5(15)/4+/7
	5 Tree-Revenants
		Points: 80
		Roles: Battleline
		M/W/S/B: 5/1(5)/5+/6
     
     Points 1000
     Wounds: 41, Models: 26, Bravery/Unit: 6.15, Save/Wound: 4.22+
	1 Alarielle the Everqueen
		Points: 600
		Roles: Leader, Behemoth
		M/W/S/B: 16*/16/3+/10
	25 Tree-Revenants
		Points: 400
		Roles: Battleline
		M/W/S/B: 5/1(25)/5+/6

### Python Example

To generate the same using python directly:

	from armiesofsigmar import ArmyGenerator, load_restictions

	restrict_config = load_restictions("sylvaneth_example.yaml")
	gen = ArmyGenerator(restrict_config)
	armies = gen.generate_army()

	for army in armies:
	    print army
            print(army.fullstr())
