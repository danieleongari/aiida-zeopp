from voluptuous import Schema, Any, ExactSequence
from aiida.orm.data.parameter import ParameterData


class NetworkParameters(ParameterData):
    """ Command line parameters for zeo++ network binary
    """

    schema = Schema({
        'cssr': bool,
        'v1': bool,
        'xyz': bool,
        'nt2': bool,
        'res': bool,
        'zvis': bool,
        'axs': float,
        'sa': ExactSequence([float, float, int]),
        'vol': ExactSequence([float, float, int]),
        'block': ExactSequence([float, int]),
        'psd': ExactSequence([float, float, int]),
        'chan': float,
        # radfile is optional
        'r': Any(basestring, bool),
    })

    # pylint: disable=redefined-builtin, too-many-function-args
    def __init__(self, dict, **kwargs):
        """
        Constructor for the data class

        Usage: ``MultiplyParameters(x1=3, x2=4)``

        .. note:: As of 2017-09, the constructor must also support a single dbnode
          argument (to reconstruct the object from a database node).
          For this reason, positional arguments are not allowed.
        """
        if 'dbnode' in kwargs:
            super(NetworkParameters, self).__init__(**kwargs)
        else:
            # set dictionary of ParameterData
            super(NetworkParameters, self).__init__(dict=dict, **kwargs)
            dict = self.validate(dict)
            self._OUTPUT_FILE_NAME = "out.{}"

    def validate(self, parameters_dict):
        """validate parameters"""
        return NetworkParameters.schema(parameters_dict)

    @property
    def cmdline_params(self, input_file_name=None):
        """Synthesize command line parameters
        
        e.g. [['-r'], ['-axs', 0.4, 'out.axs']]
        """
        pm_dict = self.get_dict()

        parameters = []
        for k, v in pm_dict.iteritems():

            parameter = ['-{}'.format(k)]
            if isinstance(v, bool):
                pass
            elif isinstance(v, list):
                parameter += v
            else:
                parameter += [v]

            # specify output file name (except for -r)
            if k != 'r':
                parameter += " {}".format(self.OUTPUT_FILE_NAME.format(k))

        if input_file_name is not None:
            parameters.append([input_file_name])

        return parameters

    @property
    def output_files(self):
        """Return list of output files to be retrieved"""
        pm_dict = self.get_dict()

        output_list = []
        for k in pm_dict.keys():
            output_list.append(self.OUTPUT_FILE_NAME.format(k))

        return output_list