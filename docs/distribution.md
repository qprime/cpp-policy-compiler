# Distribution

`polc` supports a tool-managed path and a text-only path. Both originate from
the same versioned compiler and canonical corpus.

## Installed tool

The Python wheel contains the compiler, stock configurations, policies,
standard entries, and exemplars. Pinning the package version therefore pins the
tool and canonical content together.

Projects that install the wheel can initialize local overlays, detect drift,
rebuild projections, preview upgrades, and accept a new release atomically. See
[Adopting and maintaining a harness](adopting.md).

## Text-only archives

Build deterministic archives for all stock configurations:

```text
polc release build --out dist/text
```

Each zip contains neutral generation and review projections plus a manifest of
the compiler version, projection format, corpus fingerprint, configuration, and
file hashes. Verify one or more archives with:

```text
polc release verify dist/text/*.zip
```

The text-only path requires no tool in the target project: extract the selected
archive, check the documents into the repository, and point agents at the two
entry documents. It does not provide local overlay compilation, drift checks,
or managed upgrades.

## Reproducibility and provenance

The corpus fingerprint covers every file under the canonical policies,
standard, and exemplars directories. Projection provenance also records an
independent projection-format version. Release archives use fixed metadata,
sorted members, and content hashes so identical inputs produce identical bytes.

These guarantees establish content identity and structural reproducibility.
They do not establish that the policies are semantically correct or that a
particular model will apply them well; those questions belong to corpus review
and opt-in correctness evaluation.
