# Fusion 360 Thread Profiles for 3D-Printed Threads

Fusion 360 comes with various thread standards, most of which are not a great fit for 3D printing because they are too fine to work well when printed.
This project defines thread profiles that are aimed at 3D printing so that they work, even when printed with lower detail settings (e.g. 0.30mm layer height).

## What's in the Box?

The provided `3DPrintedMetricV3.xml` file contains the thread profiles listed below.
Additional profiles can be easily generated from the included Python script.

**Shape:** 60° trapezoidal  
**Size (OD):** 8-50mm  
**Pitch:** 3.5mm, 5mm  
**Classes:** O.0, O.1, O.2, O.4, O.8

The classes specify tolerances.
O.0 has the tightest tolerances which are loosely based on ISO M30x3.5 6g/6H. 
The number after the 'O.' specifies, in tenths of a millimeter, how much the major, minor and pitch diameters are offset compared to O.0.
For example, O.2 would have a 0.2mm looser tolerance than O.0.

`3DPrintedMetric.xml` contains old thread definitions and is provided for compatibility with older prints or models.

## Install and Use

If you just want to use the profiles with no customization, download the file `3DPrintedMetricV3.xml`, save it in the following directory and then restart Fusion 360.

**On Windows:**
```
%localappdata%\Autodesk\webdeploy\Production\<version ID>\Fusion\Server\Fusion\Configuration\ThreadData
```

**On Mac OS:**

*Macintosh HD> Users> [Username] > Library > Application Support > Autodesk > Webdeploy > production > [Version specific ID] > Then right click on "Autodesk Fusion 360" and choose Show Package Contents > Contents > Libraries > Applications > Fusion > Fusion > Server > Fusion > Configuration >ThreadData*

(see also [here](https://knowledge.autodesk.com/support/fusion-360/learn-explore/caas/sfdcarticles/sfdcarticles/Custom-Threads-in-Fusion-360.html))

When you now create or edit a *Thread* feature, you should be able to select the Thread Type *"3D-printed Metric Threads"*.

![Select Thread Type in Fusion 360](ss_fusion.png)

> Note: Profiles will need to be reinstalled after every Fusion 360 update. To do this automatically, check out the [ThreadKeeper](https://github.com/thomasa88/ThreadKeeper) plugin.

## Generating Customized Profiles

You can generate your own thread profile file using the `main.py` script.
To execute the script, **Python 3.9** or newer is required.
The script can be executed like so:

```bash
python main.py
```

This will create XML files for each configuration defined in the `config.json` file in the working directory, which you can then rename and install in Fusion as described above.

To customize the generated profiles, simply edit the values defined in the `config.json` file.

```json
{
  "profiles": [
    {
      "name": "3DPrintedMetricV3",
      "customName": "3D-printed Metric Threads V3",
      "unit": "mm",
      "angle": 60.0,
      "sizes": "8:50",
      "pitches": [3.5, 5.0],
      "offsets": [0.0, 0.1, 0.2, 0.4, 0.8]
    }
  ]
}
```

To use a custom JSON file for the configurations, specify the path to the custom JSON file when executing the script:

```bash
python main.py path/to/custom/config.json
```

For example, if your custom configuration file is located at `configs/new_config.json`, you can run the script like this:

```bash
python main.py configs/new_config.json
```

This will load the configurations from the specified JSON file and generate the corresponding XML files.



To see all available options and arguments for the script, you can use the `-h` or `--help` flag:

```bash
python main.py -h
```

This will display a help message with descriptions of all the available command-line arguments.