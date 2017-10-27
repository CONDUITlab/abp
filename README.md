# abp
Analytics and visualization for arterial blood pressure waveforms

## Get Started
It's recommended that you create a virtual environment to manage dependencies

```
conda create --name CONDUITlab python=3 

conda install --name CONDUITlab pandas

source activate CONDUITlab

pip install biosppy
```

In order to get bokeh integrated with JupyterLab, you'll also need to install

```
jupyter labextension install jupyterlab_bokeh
```

## Dependencies
Check out the documentation of these dependencies here
* [pandas](https://pandas.pydata.org/pandas-docs/)
* [biosppy](http://biosppy.readthedocs.io/en/stable/)
* [bokeh](https://bokeh.pydata.org/en/latest/docs/reference.html)
