#!/bin/bash
NAMESPACE="${1:-codebase_b856_app}"
docker build -t "$NAMESPACE" .