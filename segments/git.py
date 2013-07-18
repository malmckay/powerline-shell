import re
import os
import subprocess

def get_git_status():
    has_pending_commits = True
    has_untracked_files = False
    origin_position = ""
    output = subprocess.Popen(['git', 'status', '--ignore-submodules'],
            stdout=subprocess.PIPE).communicate()[0]
    for line in output.split('\n'):
        origin_status = re.findall(
                r"Your branch is (ahead|behind).*?(\d+) comm", line)
        if origin_status:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'
            if origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'

        if line.find('nothing to commit') >= 0:
            has_pending_commits = False
        if line.find('Untracked files') >= 0:
            has_untracked_files = True
    return has_pending_commits, has_untracked_files, origin_position

def is_git():
    p2 = subprocess.Popen(['git', 'rev-parse', '--is-inside-work-tree'], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
    is_git = p2.communicate()[0].strip()
    if is_git:
        return True
    else:
        return False


def add_git_segment():
    #cmd = "git rev-parse --abbrev-ref HEAD"
    p2 = subprocess.Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE)
    branch = p2.communicate()[0].strip()
    if not branch:
        return

    has_pending_commits, has_untracked_files, origin_position = get_git_status()
    branch += origin_position
    if has_untracked_files:
        branch += ' +'

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    if has_pending_commits:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    powerline.append(' %s ' % branch, fg, bg)

def is_build():
    p2 = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
    project_dir  = p2.communicate()[0].strip()
    build_script = os.path.join(project_dir, 'script', 'jenkins.sh')
    return os.path.isfile(build_script)

def add_git_build_status():
    if is_build():
        p2 = subprocess.Popen(['git', 'tag', '--contains', 'HEAD', '--list', 'green_*'], stdout=subprocess.PIPE)

        tags = p2.communicate()[0].strip()

        if tags:
            build_state = Character.BUILD_SUCCESS
            bg = Color.REPO_CLEAN_BG
            fg = Color.REPO_CLEAN_FG
        else:
            build_state = Character.BUILD_NOT_BUILT
            bg = Color.REPO_DIRTY_BG
            fg = Color.REPO_DIRTY_FG

        powerline.append(' %s ' % build_state, fg, bg)

try:
    if is_git():
        add_git_segment()
        add_git_build_status()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
