import os
from storystats.pivotaltracker import PivotalTracker
from storystats.tools import AnalyseComments
from storystats.git import GitRepo
from storystats.tools import CommandExecute

def create_pivotal_tracker(args):
    return PivotalTracker(
        args.url,
        args.token,
        args.project_id
    )

def print_bugs(args, filter_accepted=True):
    tracker = create_pivotal_tracker(args)
    for bug in tracker.get_project_bugs(filter_accepted):
        print('#{}: {}'.format(bug['id'], bug['name']))

def print_story_stats(args):
    tracker = create_pivotal_tracker(args)
    comments = tracker.get_story_comments(args.story_id)

    # hohoho stuff
    c_analyser = AnalyseComments(comments)
    total_files = 0
    total_insertions = 0
    total_deletions = 0
    for repo, commits in c_analyser.repos.items():
        ssh_repo = repo.replace(
            'github.com/', 'github.com:').replace('https://', 'git@')

        git = GitRepo(ssh_repo, args.repos_path, CommandExecute())
        git.download()
        print('# Repo: {}\n  Commits:'.format(repo))
        all_files = 0
        all_insertions = 0
        all_deletions = 0
        for commit in commits:
            files_changed, insertions, deletions = git.stat_commit(commit)
            all_files += files_changed
            all_insertions += insertions
            all_deletions += deletions
            print('\t{}'.format(commit))
        print('  Overall repo stats: files changed: {}, insertions: {}, '
              'deletions {}'.format(all_files, all_insertions, all_deletions))
        print('')
        total_files += all_files
        total_insertions += all_insertions
        total_deletions += all_deletions

    print('')
    print('Total story stats: files changed: {}, insertions: {}, '
          'deletions {}'.format(total_files, total_insertions, total_deletions))
