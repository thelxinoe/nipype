"""Grab documentation from spm."""

from nipype.interfaces import matlab

spm_config_doc = {'realign' : 'spm_config_realign',
                  'coreg' : 'spm_config_coreg',
                  'normalise' : 'spm_config_norm',
                  }
#                  'segment' : spm_config.values{2}.values{4}.help{1}, or spm_config_segment_old


spm_doc_names = {'realign' : 'Realign: Estimate & Reslice',
                 'coreg' : 'Coreg: Estimate & Reslice',
                 #'normalise' : '',
                 'segment' : 'Segment',
                 }

def grab_doc(funcname):
    """Grab the SPM documentation for the given function name `funcname`.
    
    Parameters
    ----------
    funcname : {'realign', 'coreg'}
        Function for which we are grabbing documentation.

    """
    cmd = matlab.MatlabCommandLine()
    func_map = {'realign' : 'spm_realign_doc',
                'coreg' : 'print_spm_docs',
                }

    #cmd.inputs.script_lines = 'print_spm_docs'
    try:
        #cmd.inputs.script_lines = func_map[funcname]
        name = spm_doc_names[funcname]
        mcmd = "spm_get_doc('%s')" % name
        print 'matlab command:\n', mcmd
        cmd.inputs.script_lines = mcmd
    except KeyError:
        raise KeyError('funcname must match one of the options listed')
    
    out = cmd.run()
    #return out.runtime.stdout
    doc = out.runtime.stdout
    return doc, _strip_header(doc)


def _strip_header(doc):
    """Strip Matlab header and splash info off doc.

    Searches for the tag 'NIPYPE' in the doc and returns everyting after that.

    """
    hdr = 'NIPYPE'
    cruft = '\x1b' # There's some weird cruft at the end of the
                   # docstring, almost looks like the hex for the
                   # escape character 0x1b.
    try:
        index = doc.index(hdr)
        index += len(hdr)
        index += 2
        doc = doc[index:]
        index = doc.index(cruft)
        return doc[:index]
    except KeyError:
        raise IOError('This docstring was not generated by Nipype!\n')
