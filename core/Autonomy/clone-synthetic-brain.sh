#!/bin/bash

# Log file
LOGFILE="clone_synthetic_brain.log"

# Clear the log file at the start
> $LOGFILE

# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> $LOGFILE
}

# Directories to clone repositories into
FRAMEWORKS_DIR="frameworks"
LABORATORIES_DIR="laboratories"
ORACLES_DIR="oracles"
SUPPORT_DIR="support"
LEGACY_DIR="legacy"

# Create directories
mkdir -p $FRAMEWORKS_DIR $LABORATORIES_DIR $ORACLES_DIR $SUPPORT_DIR $LEGACY_DIR

# Clone functions for repositories
clone_repos() {
    local repo_urls=($1)
    local dir=$2
    
    for url in ${repo_urls[@]}; do
        log "Cloning $url to $dir"
        git clone $url $dir/$(basename $url) >> $LOGFILE 2>&1
        if [ $? -eq 0 ]; then
            log "Successfully cloned $url"
        else
            log "Failed to clone $url"
        fi
    done
}

# Repository URLs (replace these with actual repository URLs)
FRAMEWORKS_URLS=( "https://github.com/user/repo1.git" "https://github.com/user/repo2.git" )
LABORATORIES_URLS=( "https://github.com/user/repo3.git" "https://github.com/user/repo4.git" )
ORACLES_URLS=( "https://github.com/user/repo5.git" "https://github.com/user/repo6.git" )
SUPPORT_URLS=( "https://github.com/user/repo7.git" )
LEGACY_URLS=( "https://github.com/user/repo8.git" )

# Start cloning repositories
clone_repos ""); clone_repos "${FRAMEWORKS_URLS[@]}" $FRAMEWORKS_DIR
clone_repos "${LABORATORIES_URLS[@]}" $LABORATORIES_DIR
clone_repos "${ORACLES_URLS[@]}" $ORACLES_DIR
clone_repos "${SUPPORT_URLS[@]}" $SUPPORT_DIR
clone_repos "${LEGACY_URLS[@]}" $LEGACY_DIR

log "All cloning operations completed."