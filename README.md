# skater-xl-mod-tools

Being that Blender has become the primary content creation tool for the SkaterXL community, skater-xl-mod-tools privides an entry into easing production workflow all while maintaining consistency in our assets.

## What you need to know

This tool set is open source and is to be used `AS-IS`. You are free to do with it as you please under the specifications given under the `GNU Public license`. View [LICENSE](LICENSE) to get more information.

### Prerequisites

```
Blender version 2.80.0 is the primary targeted version.
The codebase is built to support legacy versions, supporting both Python 2.7+ and Python 3.
```

### Installing

Open Blender's Preferences panel and select the add-ons sub menu:

```
Edit => Preferences => Add-ons
```

On the upper right-hand corner, select Install Add-on and browse to `skater-xl-mod-tools.zip` that you have downloaded from [RELEASES](https://github.com/Amatobahn/skater-xl-blender/releases). Enable the add-on by searching for `Skater XL`, or selecting the `Skater XL Category`.

## Running the add-on

### Grind Splines
The Grind Splines tool a simple and easy to use process for creating spline nodes for non-dreamtek splines (Hondune Method). You have two options when creating splines: 
+ Vertex Mode: 
	- Only supports `TWO` selected vertices. Intended for direct, linear splines.
+ Edge Mode: 
	- Selecting edges of grind edge to generate point nodes. Intended for complex grind surfaces

Before generating a grind spline, setting the `audio cue` will allow the operation to understand the context of the grind surface, and generate the node name appropriately. Options currently are: `Metal`, `Wood`, and `Concrete`.

On creation, Splines will become a child of the selected object, with proper structure for that grindable object. Splines are a child of the object for those content creators that build environments in a modular fasion, allowing the ability to freely move the asset and not have to regenerate grind splines.

At this point in time, you should only be generating `ONE` grind spline at a time. Support for handling multiple will hopefully come in a future update.

### EXPERIMENTAL
These tools are here as an early preview and a quick-start to generating content for assets. These tools are in a `WORK IN PROGRESS` state.

#### Level of Detail
Generate Mesh LODs based on surface properties. Retains Parent UVs and is non-destructive. Requires blender to be in `Object Mode` with a single asset selected.

#### Collision
Generating collision shape based on source mesh. Currently creating a single solid-body object. A good start for those that aren't comfortable creating their own collision shape content.

### Asset Exporter
This tool will help ease the burden of exporting assets. The exporter will automatically export all children of the `Scene` or `Selected Meshes`. Exporting animation will export the entire timeline into one file. 

## Authors

* **Greg Amato** - *Initial work* - [Website](https://gregamato.dev) | [GitHub](https://github.com/amatobahn)

## License

This project is licensed under the GNU Public License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

+ Tester(s)
	- SqueegeeDinoToy
	- ]=[Z]=[
