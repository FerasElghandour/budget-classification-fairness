# Input contract

The CLI reads a predictions CSV containing label, prediction, and privileged, each encoded 0/1. Both group values must be present. privileged defines the reference cohort chosen by the analyst. reweighing_weights accepts aligned target/group arrays. Undefined rates are returned as null rather than silently treated as fair. No original demographic or activity records are included.
