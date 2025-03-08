# gm-Id_CMOS_AnalogDesignTool
This a Python-based tool that takes simulation data exported from your favorite analog SPICE simulator (Spectre in my case) and lets access it and visualize it in the spot. It can really plot anything you want, but the intended use case is to make quick and precise CMOS design in sub-micron technologies using the gm/Id design approach. 

![gmId_Aplication](/img/gmId_App.png?raw=true "gmId_Aplication")

There is still work to do to this day:
- Add functionalities to the NMOS and PMOS Buttons
- Extract and add the last graph regarding noise data (Thermal Noise Coefficient)
- Add "Radio Buttons" for selecting the technology node you want to use
- Add markers that change dynamically among all the plots and give more information about the operating point
    - Extra information: Vsat, Flicker Noise Parameter, Slope Factor (n), etc...
