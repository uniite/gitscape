def branch_diff(session, branch_a, branch_b):
    diff = session.repo.git.cherry("origin/staging", "origin/live")

    commits = []
    for line in diff.splitlines():
        side, sha = line.split()
        if side == "-":
            branch = branch_a
        else:  # side == "+"
            branch = branch_b
        commit = session.repo.commit(sha)
        commit_dict = {}
        commit_dict["branch"] = branch
        for attr in ["authored_date", "committed_date", "message", "hexsha"]:
            commit_dict[attr] = getattr(commit, attr)
        for role in ["author", "committer"]:
            commit_dict[role] = {}
            for attr in ["email", "name"]:
                commit_dict[role][attr] = getattr(getattr(commit, role), attr)
        commits.append(commit_dict)

    return commits
