import argparse
import re
import sys
import logging
from traitlets.config import Config
import nbformat as nbf
from nbconvert.exporters import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from collections import defaultdict


class jupyter_web_report(object):
    """
    Create an instance of the jupyter_web_report.

    Args:
        object ([type]): [description]
    """
    def __init__(self, template: str):
        self.nn = nbf.read(template, as_version=nbf.NO_CONVERT)
        logger.info('loading template ipynb successfully')

    def parameterize(self, args_dict: dict = {}):
        logger.info('passed in args:' + str(args_dict))
        for cell in self.nn["cells"]:
            if (cell["metadata"].hasattr("tags")
                    and "parameters" in cell["metadata"]["tags"]):
                source_cell_str = cell["source"].strip()
                paras_str = re.split(r"\n", source_cell_str)
                paras_dict = {
                    re.split("=", para)[0].strip(): re.split("=",
                                                             para)[1].strip()
                    for para in paras_str if '=' in para
                }

                logger.info('args in ipynb parameters cell' + str(paras_dict))
                logger.info(
                    'used args' +
                    str(set(args_dict.keys()).intersection(set(paras_dict))))

                source_str = ""
                for para in paras_dict.keys():
                    if para in args_dict:
                        target = args_dict[para].strip('\'\"')
                        source_str += f"{para}='{target}'\n"
                    else:
                        source_str += f"{para}={paras_dict[para]}\n"

                cell["source"] = source_str
        logger.info('parameterizing successfully')

    def output_notebook(self, output: str):
        nbf.write(self.nn, output, version=nbf.NO_CONVERT)
        logger.info('output successfully')

    def execute(self, timeout: int = 6000):
        """Execute notebook and generate cell level log record

        Args:
            timeout (int, optional): max time limit to run each cell. Defaults to 6000.
        """
        logger.info('starting executing')
        ep = ExecutePreprocessor(timeout=timeout)
        with ep.setup_preprocessor(self.nn, {"metadata": {"path": "."}}):
            for i,cell in enumerate(self.nn['cells']):

                logger.info(f'executing cell {i}...')
                try:
                    ep.preprocess_cell(cell,{},cell_index=i)
                except Exception:
                    msg=f'error occurred in cell {i}\n'
                    msg=msg+cell.source
                    logger.error(msg, exc_info=True)
        # ep.preprocess(self.nn, {"metadata": {"path": "."}})
        logger.info('finished execution')

    def export(self, stream=sys.stdout):
        c = Config()
        c.TagRemovePreprocessor.enabled = True
        c.TagRemovePreprocessor.remove_cell_tags = (
            "parameters",
            "hide",
        )
        c.TagRemovePreprocessor.remove_input_tags = ("output", )

        c.HTMLExporter.preprocessors = [
            "nbconvert.preprocessors.TagRemovePreprocessor"
        ]
        out = HTMLExporter(config=c).from_notebook_node(self.nn)
        print(out[0], file=stream)
        logger.info('output successfully')


def interface():
    """
    jupyter-web-report accepts a mandatory arg of ipynb file path and any other unknow args with the format of '--key value' which would be passed to the ipynb parameters cell.

    Returns:
        tuple: (ipynb_path,dict_of_parameters_to_ipynb_parameters_cell) 
    """
    parser = argparse.ArgumentParser(description="jupyter-web-report")
    parser.add_argument("-i",
                        "--ipynb",
                        type=str,
                        required=True,
                        help="path to ipynb template")
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        default='',
                        help="path to output executed ipynb")
    parser.add_argument("-t",
                        "--timeout",
                        type=int,
                        default=6000,
                        help="time for ipynb execuation")
    parser.add_argument("--dryrun",
                        action='store_true',
                        help="skip execution, generate report directly from input notebook")
    parser, unparsed = parser.parse_known_args()

    # return unparsed args as a dict
    args_to_ipynb = {x.strip('-'): y for x, y in zip(*[iter(unparsed)] * 2)}
    return parser, args_to_ipynb


def main():
    parser, args = interface()

    jwr = jupyter_web_report(parser.ipynb)
    jwr.parameterize(args)

    if not parser.dryrun:
        jwr.execute(timeout=parser.timeout)

    if parser.output:
        if parser.output.endswith('html'):
            with open(parser.output, 'w') as outf:
                jwr.export(outf)
        elif parser.output.endswith('ipynb'):
            jwr.output_notebook(parser.output)
        else:
            raise RuntimeError('Unsupport output file type')
    else:
        jwr.export()


# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

if __name__ == "__main__":
    main()
