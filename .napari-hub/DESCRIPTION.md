<!-- This file is a placeholder for customizing description of your plugin 
on the napari hub if you wish. The readme file will be used by default if
you wish not to do any customization for the napari hub listing.

If you need some help writing a good description, check out our 
[guide](https://github.com/chanzuckerberg/napari-hub/wiki/Writing-the-Perfect-Description-for-your-Plugin)
-->

# Description
This plugin allows object annotation on 2/3D images using 4 assisted annotation methods arising from two napari plugins:

- [napari-annotatorj](https://github.com/spreka/napari-annotatorj)
- [napari-nD-annotator](https://github.com/bauerdavid/napari-nD-annotator)

## Installation

Installation is possible with [pip](#pip), [napari](#bundled-napari-app) or [scripts](#script).
### Pip
You can install `napari-biomag-annotator` via [pip]:

    pip install napari[all]
	pip install napari-biomag-annotator



To install latest development version :

    pip install git+https://github.com/biomag-lab/napari-biomag-annotator.git


On Linux distributions, the following error may arise upon napari startup after the installation of the plugin: `Could not load the Qt platform plugin “xcb” in “” even though it was found`. In this case, the manual install of `libxcb-xinerama0` for Qt is required:

	sudo apt install libxcb-xinerama0