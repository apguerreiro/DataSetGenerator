DataSetGenerator
===========

Code for generating sets of nondominated points on fronts of different shapes in two and more dimensions.  The generated points have coordinate values in [0,1].





License
--------


This software is Copyright © 2016, 2017 Andreia P. Guerreiro.

This program is free software. You can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Appropriate reference to this software should be made when describing research in which it played a substantive role, so that it may be replicated and verified by others.



Usage
--------


**Execution**:

    python generateData.py outputFolder dim npoints frontType

where:

- `outputFolder`  : the root folder where the generated points will be saved
- `dim`                : number of dimensions
- `npoints`          : size of the set to be generated
- `frontType`        : name of the front type that determines the shape of the front. It has to be one of the following:  
    - linear
    - convex 
    - concave
    - cliff
    - wave-?

    For the front `wave-?`, the question mark must be replaced by a number greater than 0, which indicates the number of convex regions. For example: wave-1, wave-2, wave-10. 

     
Optionally, arguments `plot` and `plot-save` may be provided as the *fifth* parameter, in which case the set of generated points will be shown in a plot (available for any number of dimensions). If argument `plot-save` is given, the plot will also be saved.
     

**Output**:

Running the code will generate a file that will be saved in `outputFolder/frontType/` where the file name indicates the front type, number of dimensions and the number of points.
                      

Example
-------

    python generateData.py myDataSets 2 100000 linear
    

For this example, the file `linear.2d.100000` will be created under `myDataSets/linear/` and will contain `100000` points with `2` coordinates, over a straigth line between points (0,1) and (1,0).

Optinally, to see the generated points:

    python generateData.py myDataSets 2 100000 linear plot
    
or:

    python generateData.py myDataSets 2 100000 linear plot-save


In which case, the plot will be saved in `myDataSets/figures/linear.2d.100000.png`.
    
    
    
    
Data Sets
---------

Some example plots of the generated data sets for each front type available:


**linear**

<img src=dataset-plots-examples/linear.2d.100.png width="400">

**convex**

<img src=dataset-plots-examples/convex.2d.100.png width="400">

**concave**

<img src=dataset-plots-examples/concave.2d.100.png width="400">

**cliff** (Available for 3D and 4D only)

*3D*

<img src=dataset-plots-examples/cliff.3d.1000.png width="400">

*4D*

<img src=dataset-plots-examples/cliffFour.4d.100.png width="400">

**wave-?** (Available for 2D only)

*wave-1*

<img src=dataset-plots-examples/wave-1.2d.100.png width="400">

*wave-3*

<img src=dataset-plots-examples/wave-3.2d.100.png width="400">



References
-----------

- [ [Ciff 3D](http://dx.doi.org/10.1007/978-3-642-19893-9_9) ]
- [ [Wave](https://eden.dei.uc.pt/~cmfonsec/GreedyHSS-ECJ2016-authorVersion.pdf) ]



