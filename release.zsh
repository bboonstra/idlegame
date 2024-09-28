#!/bin/zsh

# Check if a version argument is provided
if [ -z "$1" ]; then
  echo "Usage: ./release.zsh <version>"
  exit 1
fi

VERSION="$1"

# Push the deletion of the remote tag, delete local tag, create a new tag, and push changes
git push origin --delete release && \
git tag -d release && \
git tag -a release -m "Release version $VERSION" && \
git push origin main && \
git push origin release