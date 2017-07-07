import os
import sys
import subprocess

class GroupDict(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = []
        return dict.__getitem__(self, key)

class AnalyseComments:
    def __init__(self, comments_list):
        self._comments_list = comments_list
        self._repos = GroupDict()
        self._already_processed = False

    def _filter_github_commits(self):
        for c in self._comments_list:
            try:
                if c['commit_type'] == 'github':
                    yield c
            except KeyError:
                pass

    def _process_repo_line(self, repo_line):
        # example line
        # https://github.com/<group>/<project_name>/commit/<commit_hash>
        repo_name = os.path.dirname(repo_line).replace('/commit', '')
        commit = os.path.basename(repo_line)

        return repo_name, commit

    def _process_comments(self):
        if self._already_processed:
            return

        for comment in self._filter_github_commits():
            repo_name, commit = self._process_repo_line(comment['text'].split('\n')[1])
            self._repos[repo_name].append(commit)

        self._already_processed = True

    @property
    def repos(self):
        self._process_comments()
        return self._repos

class CommandExecute:
    def run(self, cmd):
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        except OSError, e:
            raise RuntimeError('Failed in Popen: {}, exception: {}'.format(
                cmd, e
            ))

        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError('Failed in Popen.communicate: {}, '
                               'stdout: {}, stderr {}, exitcode {}'.format(
                                    cmd, stdout, stderr, proc.returncode
            ))

        return stdout
