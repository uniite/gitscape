from operator import itemgetter

def branches(session, repo=None):
    return {
        "branches": ["origin/%s" % b.name for b in repo.branches] + [b.name for b in repo.branches],
        "base": "origin/master",
        "upstream": "origin/master"
    }

def branch_diff(session, base="origin/master", upstream="master", repo=None):
    diff = repo.git.cherry(base, upstream)

    commits = []
    for line in diff.splitlines():
        side, sha = line.split()
        if side == "-":
            branch = base
        else:  # side == "+"
            branch = upstream
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
        "base": base,
        "upstream": upstream
    }
