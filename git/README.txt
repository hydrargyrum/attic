git-blamed-diff combines git-blame and git-diff. It prints the diff of
working directory or of a commit, on a particular file, but annotates the diff
lines with commit information, including removed lines, telling from which
commit they were removed.

This is useful when making multiple modifications to a patch series to amend,
to know which lines should be squashed in which commit.

It simply works by performing git-blame on a commit (or current working dir),
its parent commit, and diffing the 2 blames.

----

git-recpbranch will cherry-pick commits from a source branch to current branch.
It will not take all commits though. It will only take those which have
the same commit message title line as the commits in current branch.
Those from current branch matching the source branch are removed before.

This is useful to replace old commits of one branch by newer, amended commits
(revised history) from another branch.
