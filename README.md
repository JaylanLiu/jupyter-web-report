# jupyter-web-report

## Usage 
```
$python jupyter-web-report.py -h
usage: jupyter-web-report.py [-h] -i IPYNB [-c CLINICAL] -m MUTATION [-n CNV]
                             [-s SV]

jupyter-web-report

optional arguments:
  -h, --help            show this help message and exit
  -i IPYNB, --ipynb IPYNB
                        path to ipynb template
  -c CLINICAL, --clinical CLINICAL
                        path to clinical info file.
  -m MUTATION, --mutation MUTATION
                        path to mutation info file.
  -n CNV, --cnv CNV     path to cnv info file
  -s SV, --sv SV        path to sv info file
```
The output goes to stdout.

## Example
```
$python jupyter-web-report.py -i model.ipynb -m data_mutation.txt >out.html
```