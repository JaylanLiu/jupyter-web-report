import argparse
import re
import logging
from traitlets.config import Config
import nbformat as nbf
from nbconvert.exporters import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from collections import defaultdict

class jupyter_web_report(object):
    def __init__(self,template:str):
        self.nn=nbf.read(template,as_version=nbf.NO_CONVERT)

    def parameterize(self,args_dict:dict={}):
        for cell in self.nn['cells']:
            if cell['metadata'].hasattr('tags') and 'parameters' in cell['metadata']['tags']:
                paras_str=re.split('\s+',cell['source'])
                paras=[re.split('=',para)[0].strip() for para in paras_str]
        
                source_str=''
                for para in paras:
                    if args_dict[para]:
                        source_str+=f"{para}='{args_dict[para]}'\n"
    
                cell['source']=source_str

    def output_notebook(self,output:str):
        nbf.write(self.nn,output,version=nbf.NO_CONVERT)

    def execute(self):
        ep = ExecutePreprocessor(timeout=6000)
        ep.preprocess(self.nn, {'metadata': {'path': '.'}})

    def export(self):
        c = Config()
        c.TagRemovePreprocessor.enabled=True
        c.TagRemovePreprocessor.remove_cell_tags = ('parameters','hide',)
        c.TagRemovePreprocessor.remove_input_tags = ('output',)

        c.HTMLExporter.preprocessors = ['nbconvert.preprocessors.TagRemovePreprocessor']
        out=HTMLExporter(config=c).from_notebook_node(self.nn)
        print(out[0])


def interface():
    parser = argparse.ArgumentParser(description='jupyter-web-report')
    parser.add_argument('-i',
                        '--ipynb',
                        type=str,
                        required=True,
                        help='path to ipynb template')
    parser.add_argument('-c',
                        '--clinical',
                        type=str,
                        default='',
                        help='path to clinical info file.')
    parser.add_argument('-m',
                        '--mutation',
                        type=str,
                        default='',
                        required=True,
                        help='path to mutation info file.')
    parser.add_argument('-n',
                        '--cnv',
                        type = str,
                        default='',
                        help='path to cnv info file')
    parser.add_argument('-s',
                        '--sv',
                        type=str,
                        default='',
                        help='path to sv info file')
    
    parser = parser.parse_args()
    return parser

def _args2dict(args:argparse.ArgumentParser):
    args_dict=defaultdict(str)

    args_dict['clinical']=args.clinical
    args_dict['mutation']=args.mutation
    args_dict['cnv']=args.cnv
    args_dict['sv']=args.sv

    return args_dict

if __name__ == "__main__":
    args=interface()
    args_dict=_args2dict(args)

    jwr=jupyter_web_report(args.ipynb)
    jwr.parameterize(args_dict)
    jwr.execute()
    jwr.export()