/*
A KBase module: jayrboltonTest
*/

module jayrboltonTest {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef jayrbolton_contig_filter(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
