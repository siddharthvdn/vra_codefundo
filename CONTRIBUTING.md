# Contributing guidelines

Please follow the following steps before adding a new feature.

## Create a new branch for each feature
Before you start adding a new feature make sure you do it in a new branch, and pull the latest master
```
$ git checkout -b feature-name
$ git pull origin master
```

Make your changes, add files and commit.
```
$ git add .
$ git commit -m "Commit message"
```

Before you push, pull from master again to make sure there aren't any merge conflicts
```
$ git pull origin master
```

If there are merge conflicts, fix them.
Then push to branch.

```
$ git push origin feature-name
```

Now create a new PR from this branch to master.

Once the PR is merged, delete the branch.
