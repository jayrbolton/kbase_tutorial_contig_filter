# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from jayrboltonTest.contig_filter_util import contig_filter
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.KBaseReportClient import KBaseReport

from Bio import SeqIO
#END_HEADER


class jayrboltonTest:
    '''
    Module Name:
    jayrboltonTest

    Module Description:
    A KBase module: jayrboltonTest
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "a16976166f5c43238a2283b96fa94599ca09b833"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def jayrbolton_contig_filter(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN jayrbolton_contig_filter
        if not params.get('assembly_input_ref'):
            raise TypeError("`assembly_input_ref` is required")
        if not params.get('min_length') or not isinstance(params['min_length'], int):
            raise TypeError("`min_length` is required and needs to be an int")
        min_length = params['min_length']
        # Initialize the assembly util client
        assembly_util = AssemblyUtil(self.callback_url)
        # download the fasta file to local disk
        fasta_file = assembly_util.get_assembly_as_fasta({'ref': params['assembly_input_ref']})
        filtered_path = os.path.join(self.shared_folder, 'filtered.fasta')
        report_client = KBaseReport(self.callback_url)
        result = contig_filter(fasta_file['path'], filtered_path, min_length)
        assembly_obj = assembly_util.save_assembly_from_fasta({
            'workspace_name': params['workspace_name'],
            'file': {
                'path': filtered_path,
                'assembly_name': 'filtered_contigs'
            },
            'assembly_name': 'filtered_assembly'
        })
        report = report_client.create_extended_report({
            'workspace_name': params['workspace_name'],
            'objects_created': [{'ref': assembly_obj, 'description': 'filtered_assembly'}],
            'message': (
                f"Filtered out {result['n_total'] - result['n_remaining']} "
                f"records out of {result['n_total']} records."
            )
        })
        output = {'report_ref': report['ref'], 'report_name': report['name']}
        #END jayrbolton_contig_filter

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method jayrbolton_contig_filter return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
