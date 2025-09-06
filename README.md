# Fusion 360 Thread Profiles for 3D-Printed Threads

Fusion 360 comes with various thread standards, most of which are not a great fit for 3D printing because they are too fine to work well when printed.
This project defines thread profiles that are aimed at 3D printing so that they work, even when printed with lower detail settings.

## What's in the Box?

The provided `3DPrintedMetricV4.xml` file contains the thread profiles listed below.
Additional profiles can be easily generated from the included Python script.

**Shape:** 60° trapezoidal
<br>
**Size (OD):** 1-50mm
<br>
**Pitch:** Various, based on the ISO standard
<br>
**Classes:** O.0, O.1, O.2, 0.3, O.4, 0.5, 0.6, 0.7, O.8, 0.9


The classes specify tolerances.
O.0 has the tightest tolerances which are loosely based on ISO M30x3.5 6g/6H.
The number after the 'O.' specifies, in tenths of a millimeter, how much the major, minor and pitch diameters are offset compared to O.0.
For example, O.2 would have a 0.2mm looser tolerance than O.0.

If your goal is to use real metal bolts in 3D printed threaded holes, I find that **0.6** works well.
<p align="center">
    <img src="m4_thread_example_1.jpg" alt="M4 Thread Example 1" height="400">
    <img src="m4_thread_example_2.jpg" alt="M4 Thread Example 2" height="400">
</p>

## Install and Use

If you just want to use the profiles with no customization, download the file `3DPrintedMetricV4.xml`, save it in the following directory and then restart Fusion 360.

**On Windows:**
```
%localappdata%\Autodesk\webdeploy\Production\<version ID>\Fusion\Server\Fusion\Configuration\ThreadData
```

**On Mac OS:**
The easiest way to get to the ThreadData folder is to use the Terminal. Open a new Terminal window and paste in:
```
open ~/Library/Application\ Support/Autodesk/webdeploy/production/Autodesk\ Fusion.app/Contents/Libraries/Applications/Fusion/Fusion/Server/Fusion/Configuration/ThreadData
```
This will open the correct folder in the Finder

(see also [here](https://knowledge.autodesk.com/support/fusion-360/learn-explore/caas/sfdcarticles/sfdcarticles/Custom-Threads-in-Fusion-360.html))

When you now create or edit a *Thread* feature, you should be able to select the Thread Type *"3D-printed Metric Threads V4"*.

![Select Thread Type in Fusion 360](ss_fusion.png)

> Note: Profiles will need to be reinstalled after every Fusion 360 update. To do this automatically, check out the [ThreadKeeper](https://github.com/thomasa88/ThreadKeeper) plugin.

## Generating Customized Profiles

You can generate your own thread profile file using the `main.py` script.
To execute the script, **Python 3.9** or newer is required.
The script has no parameters and can be executed like so:

```bash
python main.py
```

This will create a file named `output.xml` in the working directory which you can then rename and install in Fusion as described above.

To customize the generated profiles, simply edit the values defined at the top of `main.py`.
