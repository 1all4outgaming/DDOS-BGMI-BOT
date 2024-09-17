#!/bin/bash

# Download tmate binary
echo "Downloading tmate..."
curl -L https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-amd64.tar.xz -o tmate.tar.xz

# Extract the downloaded archive
echo "Extracting tmate..."
tar -xf tmate.tar.xz

# Make tmate executable
echo "Making tmate executable..."
chmod +x tmate-2.4.0-static-linux-amd64/tmate

# Run tmate
echo "Running tmate..."
./tmate-2.4.0-static-linux-amd64/tmate

# Keep the session alive for 24 hours (86400 seconds)
echo "Keeping session alive for 24 hours..."
sleep 86400
