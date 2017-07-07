import os
import re

class GitRepo:
    def __init__(self, url, path, cmd_execute):
        self._url = url
        self._path = path
        self._cmd_execute = cmd_execute
        self._repo_name = os.path.basename(url).replace('.git', '')
        self._repo_path = os.path.join(self._path, self._repo_name)

    def download(self):
        previous_dir = os.getcwd()
        os.chdir(self._path)
        try:
            self._cmd_execute.run(['git', 'clone', self._url])
        # don't complain if it's already there
        except RuntimeError, e:
            allow_error = 'fatal: destination path \'{}\' already exists and is not an empty directory.'.format(self._repo_name)
            if allow_error not in str(e):
                raise e
        os.chdir(previous_dir)

    def _get_git_stat(self, commit_hash):
        previous_dir = os.getcwd()
        os.chdir(self._repo_path)
        output = self._cmd_execute.run(['git', 'show', '--stat', commit_hash])
        os.chdir(previous_dir)

        return output

    def stat_commit(self, commit_hash):
        git_stat_output =  self._get_git_stat(commit_hash)
        pattern = re.compile(r'(\d+) file[s]? changed, ((\d+) insertion[s]?\(\+\))?[,]?[ ]?((\d+) deletion[s]?\(\-\))?')

        for line in git_stat_output.split('\n'):
            matched_stats = pattern.match(line.strip())
            if matched_stats:
                groups = matched_stats.groups()
                files_changed = int(groups[0]) if groups[0] is not None else 0
                insertions = int(groups[2]) if groups[2] is not None else 0
                deletions = int(groups[4]) if groups[4] is not None else 0

                return files_changed, insertions, deletions

        return None, None, None
