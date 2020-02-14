
class GromacsError(BaseException):
    pass

class IOGromacsError(GromacsError):
    '''Exception raised with "File input/output error" message'''
    def __init__(self, command, explain):
        self.command = command
        self.explain = explain

    def __str__(self):
        return "%s failed with '%s'" % (self.command, self.explain)

class GromacsMessages(object):
    '''Load an error message and split it along as many properties as 
    posible'''

    #Map the messages with the errors
    e = {"File input/output error": IOGromacsError,
         "Can not open file": IOGromacsError,
         #FIXME: Clearly the following is not IOError
         "srun: error: Unable to create job step": IOGromacsError,
        }

    def __init__(self, gro_err="", command="", *args, **kwargs):
        '''Pass the command and the output of that command in "command" and 
        "gro_err" kwargs. The check for "error" property'''
        self.error = False
        self.command = command
        self.gro_err = gro_err.split("\n")

        self.check()

    def check(self):
        '''Check if the GROMACS error message have any of the known error
        messages. Set the self.error to the value of the error'''

        for line in self.gro_err:
            for error in self.e.keys():
                if line.startswith(error):
                    raise self.e[error](self.command, error)

def test_run(command):
    import subprocess
    c = ["/opt/gromacs405/bin/" + command]
    p = subprocess.Popen(c,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        stdin = subprocess.PIPE)
    out, err = p.communicate("4\n")
    return err

if __name__ == "__main__":
    GromacsMessages(gro_err=test_run("eneconv"), command="eneconv")
