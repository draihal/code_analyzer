import argparse
import os


class ValidateGitURL(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if not values.startswith('https://github.com/') or not values.endswith('.git'):
            # logging.error('Exception occurred.  ValidateGitURL.')
            raise argparse.ArgumentError(
                self,
                '''Something wend wrong. Is your path correct?\n
                It should be like: "https://github.com/draihal/code_analyzer.git".\n''')
        setattr(args, self.dest, values)


class ValidatePositiveInt(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if values <= 0:
            # logging.error('Exception occurred. ValidatePositiveInt.')
            raise argparse.ArgumentError(
                self,
                '''Something wend wrong. Is your number is correct?\n
                It should be > 0.\n''')
        setattr(args, self.dest, values)


class ValidateOSPath(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if not os.path.exists(values):
            # logging.error('Exception occurred.  ValidateOSPath.')
            raise argparse.ArgumentError(
                self,
                f'''Something wend wrong. Is your path correct?\n
                'It should be like: "C:\\py\\". Your path is: "{values}".\n''')
        setattr(args, self.dest, values)
