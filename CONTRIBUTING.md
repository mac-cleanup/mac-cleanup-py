# Welcome to contributing guide 

Thank you for investing your time in contributing to the project!

Read repo's [Code of Conduct](./CODE_OF_CONDUCT.md) to keep community respectable.

## TL;DR

> #### 1. [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) the repo
> #### 2. [Checkout](https://www.atlassian.com/git/tutorials/using-branches/git-checkout) from `develop` branch
> #### 3. Install dependencies: `pip install poetry && poetry install`
> #### 3. Setup `pre-commit` hooks: `pre-commit install --hook-type pre-commit --hook-type pre-push`
> #### 4. [Commit](https://www.atlassian.com/git/tutorials/saving-changes/git-commit) your changes with [Conventional Commits](https://www.conventionalcommits.org)
> #### 5. Run tests: `poetry run tox`
> #### 6. [Push the changes](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push) to your fork 
> #### 7. [Open PR](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) to 'develop' branch
> #### Congrats :tada::sparkles:. CYA in your PRs 😉


## New contributor guide

To get an overview of the project, read the [README](README.md). 
Here are some resources to help you get started with open source contributions:

- [Finding ways to contribute to open source on GitHub](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
- [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
- [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests)

### Issues

#### Create a new issue

If you spot ant problems [search if an issue already exists](https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-issues-and-pull-requests#search-by-the-title-body-or-comments). 

If an issue doesn't exist, you can open a new issue using a relevant [issue form](https://github.com/Drugsosos/mac-cleanup-py/issues/new/choose). 

#### Solve an issue

View the [existing issues](https://github.com/mac-cleanup/mac-cleanup-py/issues) to find something interesting to you. 

In general, new issues will be assigned on [Drugsosos](https://github.com/Drugsosos).

If you find an issue to work on, just post a comment on the issue's page and you are welcome to open a PR with a fix.

### Make Changes

1. [Fork the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) so that you can make your changes without affecting the original project until you're ready to merge them.
2. Create a working branch out of 'develop' and start with your changes
3. Install dependencies
    ```bash
   pip install poetry && poetry install
   ```
4. Setup pre-commit hooks
    ```bash
   pre-commit install --hook-type pre-commit --hook-type pre-push
    ```
5. Run tests before pushing
    ```bash
   poetry run tox
    ```

### Commit your update

[Commit the changes](https://www.atlassian.com/git/tutorials/saving-changes/git-commit) once you are happy with them and [push](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push) them to your fork.

Once your changes are ready, don't forget to self-review to speed up the review process:zap:.

### Pull Request

When you're finished with the changes, create a pull request, also known as a [PR](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
- Fill the "Ready for review" template so that we can review your PR. This template helps reviewers understand your changes as well as the purpose of your pull request. 
- Don't forget to [link PR to issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) if you are solving one.
- Enable the checkbox to [allow maintainer edits](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so the branch can be updated for a merge.
Once you submit your PR, someone of collaborators will come and see your PR.
- You may be asked for changes to be made before a PR can be merged, either using [suggested changes](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/incorporating-feedback-in-your-pull-request) or pull request comments.\ 
- You can apply suggested changes directly through the UI. You can make any other changes in your fork, then commit them to your branch.
- As you update your PR and apply changes, mark each conversation as [resolved](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request#resolving-conversations).

### Your PR is merged!

Congratulations :tada::sparkles:

Once your PR is merged, your contributions will be publicly visible on the [mac-cleanup-py](https://github.com/mac-cleanup/mac-cleanup-py).
