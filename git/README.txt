`git-blamed-diff` combines `git-blame` and `git-diff`. It prints the diff of
working directory or of a commit, on a particular file, but annotates the diff
lines with commit information, including removed lines, telling from which
commit they were removed.

This is useful when making multiple modifications to a patch series to amend,
to know which lines should be squashed in which commit.

It simply works by performing `git-blame` on a commit (or current working dir),
its parent commit, and diffing the 2 blames.

----

`git-recpbranch` will cherry-pick commits from a source branch to current branch.
It will not take all commits though. It will only take those which have
the same commit message title line as the commits in current branch.
Those from current branch matching the source branch are removed before.

This is useful to replace old commits of one branch by newer, amended commits
(revised history) from another branch.

----

`git-amend-author` modifies the author name and email of the last commit.
It also modifies the committer name/email.
It doesn't reset the author timestamp though.

Usage: `git amend-author <NAME> <EMAIL>`

----

`git-commit-with-mtime` calls git-commit but sets the date to a file's mtime.

----

`git-cherry-pick-on-path` is like git-cherry-pick but it can restrict to only
some path.

Sample: `git cherry-pick-on-path 0123456 modules/only_one/`

----

`git-combine-remotes` creates a new git remote with all the URLs of other specified
remotes. This is useful to push to multiple URLs in one git-push call.

Usage: `git combine-remotes NEW_REMOTE REMOTE1 REMOTE2...`

----

`git-midnight` commits (or amends a commit) to fake the commit date and force it
to midnight today. This can be used to hide the real commit date for privacy.

----

`git-edit-index` spawn an editor to edit the staged content of a file, but leaves
the working directory file untouched at the end.

Usage: `git edit-index FILE`
