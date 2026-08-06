#!/usr/bin/env bash
set -euo pipefail

read -r DISTRO

echo "Distro: $DISTRO"

printf "build only or run locally or stop running? (B/R/S) >"
read -r BR


if [[ $BR == "B" ]]; then
    # Step 1: Build the OCI image
    echo "==> Step 1: Building container image..."
    podman build -t "searxng-distros/$DISTRO:latest" --build-arg "distro=$DISTRO" .
elif [[ $BR == "R" ]]; then
    # Step 2: Run with podman-compose
    export distro_name="$DISTRO"
    echo "==> Step 2: Starting services with podman-compose..."
    podman-compose -f ./podman-compose.yml up
elif [[ $BR == "S" ]]; then
    # Step 2: Run with podman-compose
    export distro_name="$DISTRO"
    echo "==> Step 2: Stopping services with podman-compose..."
    podman-compose -f ./podman-compose.yml down
fi
