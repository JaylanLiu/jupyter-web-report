# jupyter_web_report
jwr, short for jupyter_web_report, is a command line interface tool for using jupyter`s ipynb file as a reusable template to generate analysis report with new data source.

It provides properties such as:
- passing command line parameters, 
- executing notebooks, 
- jupyter cell level output controlling.

It supports all the kernals like IR,Ipython, etc.

## Installation

### From pip
```
pip install jupyter_web_report
```

### From github
```
git clone https://github.com/JaylanLiu/jupyter-web-report
cd jupyter-web-report
python setup.py install
```

## Usage 

### Template notebook configuration
Cell with a parameters tag will recieve the arguments form jwr. Parameters cell would not present in the output html. 
![parameters](imgs/template_notebook_configuration.gif)
Cell with a hide tag would be executed but not present in the output html.
![hide](imgs/template_notebook_configuration2.gif)
Cell with a output tage would be executed and only present the 'Out' but the 'In' structure in the output html.
![output](imgs/template_notebook_configuration3.gif)
Untaged cell would be executed and present both 'In' and 'Out' structures in the output html.



### parameterize and execution
```
$jwr -h
usage: jwr [-h] -i IPYNB [-o OUTPUT]

jupyter-web-report

optional arguments:
  -h, --help            show this help message and exit
  -i IPYNB, --ipynb IPYNB
                        path to ipynb template
  -o OUTPUT, --output OUTPUT
                        path to output executed ipynb
  -t TIMEOUT, --timeout TIMEOUT
                        time for ipynb execuation
```
'-i' specifies the configured template ipynb file. '-o' can be a file name which ends with '.html' or '.ipynb', output would be consistent to the suffix. if '-o' is not specified, then the output goes to stdout as html. '-t' specifies the time limit for notebook execution, 6000 sec for default.

Any parameters can be passed in the template ipynb notebook\`s parameters cell using a `--key value` format attach to the command.

## Example
```
$jwr -i example/model.ipynb -o x.html --mutation example/data_mutation.txt 
2020-06-29 14:14:20,004 - jupyter_web_report.py[line:21] - INFO: loading template ipynb successfully
2020-06-29 14:14:20,004 - jupyter_web_report.py[line:24] - INFO: passed in args:{'mutation': 'example/data_mutation.txt'}
2020-06-29 14:14:20,004 - jupyter_web_report.py[line:31] - INFO: args in ipynb parameters cell['clinical', 'mutation', 'cnv', 'sv']
2020-06-29 14:14:20,004 - jupyter_web_report.py[line:34] - INFO: used args{'mutation'}
2020-06-29 14:14:20,004 - jupyter_web_report.py[line:42] - INFO: parameterizing successfully
2020-06-29 14:14:20,004 - jupyter_web_report.py[line:49] - INFO: starting executing
2020-06-29 14:14:34,175 - jupyter_web_report.py[line:52] - INFO: finished executing
2020-06-29 14:14:34,333 - jupyter_web_report.py[line:68] - INFO: output successfully
```

