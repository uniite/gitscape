from operator import itemgetter

def branches(session, repo=None):
    return {
        "branches": ["origin/%s" % b.name for b in repo.branches] + [b.name for b in repo.branches],
        "branchA": "origin/master",
        "branchB": "origin/master"
    }

def branch_diff(session, branch_a="origin/master", branch_b="master", repo=None):
    diff = repo.git.cherry(branch_a, branch_b)

    commits = []
    for line in diff.splitlines():
        side, sha = line.split()
        if side == "-":
            branch = branch_a
        else:  # side == "+"
            branch = branch_b
        commit = repo.commit(sha)
        commit_dict = {}
        commit_dict["branch"] = branch
        for attr in ["authored_date", "committed_date", "message", "hexsha"]:
            commit_dict[attr] = getattr(commit, attr)
        for role in ["author", "committer"]:
            commit_dict[role] = {}
            for attr in ["email", "name"]:
                commit_dict[role][attr] = getattr(getattr(commit, role), attr)
        commits.append(commit_dict)

    commits.sort(key=itemgetter("authored_date"), reverse=True)


    return {
        "commits": commits,
        "branchA": branch_a,
        "branchB": branch_b
    }
