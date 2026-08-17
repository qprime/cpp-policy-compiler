# C++ Core Guidelines coverage ledger

Every normative rule in the C++ Core Guidelines, with this corpus's
disposition. Generated from the upstream document on 2026-08-16 and verified
total: no rule is unmarked.

Rule identifiers only. The upstream licence permits copying for personal or
internal business use, and this repository is public, so rule titles are not
reproduced here — look an identifier up upstream to read its title.

Five dispositions:

- **covered** — an existing policy answers it, named here
- **adopt** — no policy answers it yet; the italic text names the policy to be written
- **declined** — considered and rejected, with the reason
- **diverges** — this corpus holds the opposite position, with the reason
- **out of scope** — outside what this corpus governs, with the reason

A rule marked *adopt* is an open gap. A rule marked *declined* was decided and
needs no further thought. A rule marked *diverges* is a position a reader may
need to see, and belongs with the divergences the captured convention already
records. Without the distinction a gap and a decision look identical, which is
how casts went missing through two rounds of derivation.

## Philosophy (P)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| P.1 | covered | POL-0006 |
| P.2 | covered | POL-0158 |
| P.3 | covered | POL-0006 |
| P.4 | covered | POL-0001, POL-0019 |
| P.5 | covered | POL-0001, POL-0008, POL-0036 |
| P.6 | covered | POL-0002, POL-0009, POL-0036 |
| P.7 | covered | POL-0002, POL-0005, POL-0036 |
| P.8 | covered | POL-0003 |
| P.9 | declined | too general to act on at generation time; performance-criticality is code-local, which the ontology keeps as content rather than a rule |
| P.10 | covered | POL-0020, POL-0026 |
| P.11 | covered | POL-0025 |
| P.12 | covered | POL-0089, POL-0090, POL-0091, POL-0092 |
| P.13 | covered | POL-0109 |

## Interfaces (I)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| I.1 | covered | POL-0124 |
| I.2 | covered | POL-0124 |
| I.3 | covered | POL-0124 |
| I.4 | covered | POL-0017 |
| I.5 | covered | POL-0027, POL-0031 |
| I.6 | covered | POL-0027 |
| I.7 | diverges | the corpus makes a precondition a type (POL-0027) rather than a stated assertion, and sends postconditions the same way |
| I.8 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| I.9 | covered | POL-0129 |
| I.10 | covered | POL-0031, POL-0039 |
| I.11 | covered | POL-0014 |
| I.12 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| I.13 | covered | POL-0035, POL-0046 |
| I.22 | covered | POL-0124 |
| I.23 | covered | POL-0016, POL-0023 |
| I.24 | covered | POL-0016, POL-0023 |
| I.25 | covered | POL-0037 |
| I.26 | declined | binary interface stability is a project architecture choice, not a decision made while writing a file |
| I.27 | declined | binary interface stability is a project architecture choice, not a decision made while writing a file |
| I.30 | covered | POL-0064 |

## Functions (F)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| F.1 | covered | POL-0030 |
| F.2 | covered | POL-0030 |
| F.3 | covered | POL-0030 |
| F.4 | covered | POL-0036 |
| F.5 | declined | performance-criticality is code-local; the ontology keeps it as content rather than a rule |
| F.6 | covered | POL-0051 |
| F.7 | covered | POL-0035 |
| F.8 | covered | POL-0030 |
| F.9 | covered | POL-0054 |
| F.10 | covered | POL-0030 |
| F.11 | covered | POL-0116 |
| F.15 | covered | POL-0035 |
| F.16 | covered | POL-0035 |
| F.17 | covered | POL-0035 |
| F.18 | covered | POL-0035 |
| F.19 | covered | POL-0151 |
| F.20 | covered | POL-0035 |
| F.21 | covered | POL-0023, POL-0035 |
| F.60 | covered | POL-0009, POL-0024, POL-0031, POL-0035 |
| F.22 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| F.23 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| F.24 | covered | POL-0035 |
| F.25 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| F.26 | covered | POL-0014 |
| F.27 | covered | POL-0048 |
| F.42 | covered | POL-0135 |
| F.43 | covered | POL-0035 |
| F.44 | covered | POL-0135 |
| F.45 | covered | POL-0135 |
| F.46 | declined | the compiler already rejects the alternative |
| F.47 | covered | POL-0021 |
| F.48 | covered | POL-0151 |
| F.49 | covered | POL-0135 |
| F.50 | covered | POL-0116 |
| F.51 | covered | POL-0159 |
| F.52 | covered | POL-0115 |
| F.53 | covered | POL-0115 |
| F.54 | covered | POL-0114 |
| F.55 | covered | POL-0154 |
| F.56 | covered | POL-0030 |

## Classes and class hierarchies (C)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| C.1 | covered | POL-0042 |
| C.2 | covered | POL-0015, POL-0022, POL-0034, POL-0042 |
| C.3 | covered | POL-0028 |
| C.4 | covered | POL-0029 |
| C.5 | covered | POL-0029 |
| C.7 | declined | a declaration form a generator does not produce, with no cost when it appears |
| C.8 | covered | POL-0022 |
| C.9 | covered | POL-0022 |
| C.10 | covered | POL-0040 |
| C.11 | covered | POL-0126 |
| C.12 | covered | POL-0126 |
| C.13 | covered | POL-0136 |
| C.20 | covered | POL-0021, POL-0025 |
| C.21 | covered | POL-0021 |
| C.22 | covered | POL-0021 |
| C.30 | covered | POL-0021 |
| C.31 | covered | POL-0025 |
| C.32 | covered | POL-0014 |
| C.33 | covered | POL-0021 |
| C.35 | covered | POL-0037 |
| C.36 | covered | POL-0144 |
| C.37 | covered | POL-0144 |
| C.40 | covered | POL-0015 |
| C.41 | covered | POL-0015, POL-0022 |
| C.42 | covered | POL-0015, POL-0022 |
| C.43 | covered | POL-0126 |
| C.44 | covered | POL-0126 |
| C.45 | covered | POL-0022 |
| C.46 | covered | POL-0022 |
| C.47 | covered | POL-0136 |
| C.48 | covered | POL-0136 |
| C.49 | covered | POL-0022 |
| C.50 | covered | POL-0022 |
| C.51 | covered | POL-0148 |
| C.52 | covered | POL-0148 |
| C.60 | covered | POL-0125 |
| C.61 | covered | POL-0125 |
| C.62 | covered | POL-0125 |
| C.63 | covered | POL-0125 |
| C.64 | covered | POL-0125 |
| C.65 | covered | POL-0125 |
| C.66 | covered | POL-0021, POL-0051 |
| C.67 | covered | POL-0120 |
| C.80 | covered | POL-0147 |
| C.81 | covered | POL-0147 |
| C.82 | covered | POL-0037 |
| C.83 | covered | POL-0145 |
| C.84 | covered | POL-0145 |
| C.85 | covered | POL-0145 |
| C.86 | covered | POL-0146 |
| C.87 | covered | POL-0146 |
| C.89 | covered | POL-0146 |
| C.90 | covered | POL-0095 |
| C.100 | declined | writing a new container is off the ordinary path; the standard library supplies them (POL-0109) |
| C.101 | declined | writing a new container is off the ordinary path; the standard library supplies them (POL-0109) |
| C.102 | declined | writing a new container is off the ordinary path; the standard library supplies them (POL-0109) |
| C.103 | declined | writing a new container is off the ordinary path; the standard library supplies them (POL-0109) |
| C.104 | declined | writing a new container is off the ordinary path; the standard library supplies them (POL-0109) |
| C.109 | declined | writing a new resource handle is off the ordinary path; POL-0025 governs the case that does arise |
| C.120 | covered | POL-0037 |
| C.121 | covered | POL-0149 |
| C.122 | covered | POL-0037 |
| C.126 | covered | POL-0149 |
| C.127 | covered | POL-0120 |
| C.128 | covered | POL-0037 |
| C.129 | covered | POL-0037, POL-0044 |
| C.130 | covered | POL-0120 |
| C.131 | covered | POL-0166 |
| C.132 | covered | POL-0037 |
| C.133 | covered | POL-0120 |
| C.134 | covered | POL-0126 |
| C.135 | covered | POL-0037 |
| C.136 | declined | the corpus routes variation to std::variant (POL-0044); inheritance for implementation attributes is the case POL-0037 already rejects |
| C.137 | declined | virtual bases follow from multiple implementation inheritance, which POL-0037 already rejects |
| C.138 | covered | POL-0159 |
| C.139 | declined | a sparing-use rule with no decision procedure a generator can apply |
| C.140 | covered | POL-0159 |
| C.145 | covered | POL-0121 |
| C.146 | covered | POL-0150 |
| C.147 | covered | POL-0150 |
| C.148 | covered | POL-0150 |
| C.149 | covered | POL-0014 |
| C.150 | covered | POL-0128 |
| C.151 | covered | POL-0128 |
| C.152 | covered | POL-0121 |
| C.153 | covered | POL-0037 |
| C.160 | covered | POL-0122 |
| C.161 | covered | POL-0123 |
| C.162 | covered | POL-0122 |
| C.163 | covered | POL-0122 |
| C.164 | covered | POL-0123 |
| C.165 | covered | POL-0123 |
| C.166 | covered | POL-0122 |
| C.167 | covered | POL-0122 |
| C.168 | covered | POL-0123 |
| C.170 | covered | POL-0116 |
| C.180 | covered | POL-0156 |
| C.181 | covered | POL-0033 |
| C.182 | covered | POL-0033 |
| C.183 | covered | POL-0095 |

## Enumerations (Enum)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| Enum.1 | covered | POL-0103 |
| Enum.2 | covered | POL-0103 |
| Enum.3 | covered | POL-0103 |
| Enum.4 | covered | POL-0160 |
| Enum.5 | covered | POL-0084 |
| Enum.6 | covered | POL-0160 |
| Enum.7 | covered | POL-0104 |
| Enum.8 | covered | POL-0104 |

## Resource management (R)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| R.1 | covered | POL-0003 |
| R.2 | covered | POL-0035 |
| R.3 | covered | POL-0014, POL-0024 |
| R.4 | covered | POL-0014, POL-0024 |
| R.5 | covered | POL-0024 |
| R.6 | covered | POL-0124 |
| R.10 | covered | POL-0127 |
| R.11 | covered | POL-0014 |
| R.12 | covered | POL-0127 |
| R.13 | covered | POL-0127 |
| R.14 | covered | POL-0046 |
| R.15 | declined | follows from POL-0021 and no naked new and delete; a matched pair only arises where an override was already written |
| R.20 | covered | POL-0014, POL-0024 |
| R.21 | covered | POL-0014, POL-0024, POL-0048 |
| R.22 | covered | POL-0128 |
| R.23 | covered | POL-0128 |
| R.24 | covered | POL-0168 |
| R.30 | covered | POL-0035 |
| R.31 | declined | a non-standard smart pointer is off the ordinary path; POL-0109 sends the author to the standard one |
| R.32 | covered | POL-0014 |
| R.33 | covered | POL-0132 |
| R.34 | covered | POL-0132 |
| R.35 | covered | POL-0132 |
| R.36 | covered | POL-0132 |
| R.37 | covered | POL-0132 |

## Expressions and statements (ES)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| ES.1 | covered | POL-0109 |
| ES.2 | covered | POL-0006 |
| ES.3 | covered | POL-0056 |
| ES.5 | covered | POL-0097 |
| ES.6 | covered | POL-0097 |
| ES.7 | covered | POL-0152 |
| ES.8 | covered | POL-0152 |
| ES.9 | covered | POL-0084 |
| ES.10 | covered | POL-0153 |
| ES.11 | covered | POL-0050 |
| ES.12 | covered | POL-0165 |
| ES.20 | covered | POL-0019, POL-0096 |
| ES.21 | covered | POL-0097 |
| ES.22 | covered | POL-0097 |
| ES.23 | covered | POL-0096 |
| ES.24 | covered | POL-0014 |
| ES.25 | covered | POL-0026 |
| ES.26 | covered | POL-0165 |
| ES.27 | covered | POL-0155 |
| ES.28 | covered | POL-0116 |
| ES.30 | covered | POL-0157 |
| ES.31 | covered | POL-0157 |
| ES.32 | covered | POL-0084 |
| ES.33 | covered | POL-0157 |
| ES.34 | covered | POL-0154 |
| ES.40 | covered | POL-0134 |
| ES.41 | covered | POL-0134 |
| ES.42 | covered | POL-0014 |
| ES.43 | covered | POL-0134 |
| ES.44 | covered | POL-0134 |
| ES.45 | covered | POL-0010 |
| ES.46 | covered | POL-0101 |
| ES.47 | covered | POL-0110 |
| ES.48 | covered | POL-0094 |
| ES.49 | covered | POL-0094 |
| ES.50 | covered | POL-0095 |
| ES.55 | covered | POL-0098 |
| ES.56 | covered | POL-0151 |
| ES.60 | covered | POL-0127 |
| ES.61 | covered | POL-0127 |
| ES.62 | covered | POL-0133 |
| ES.63 | covered | POL-0121 |
| ES.64 | covered | POL-0096 |
| ES.65 | covered | POL-0133 |
| ES.70 | covered | POL-0117 |
| ES.71 | covered | POL-0098, POL-0099 |
| ES.72 | covered | POL-0117 |
| ES.73 | covered | POL-0117 |
| ES.74 | covered | POL-0097 |
| ES.75 | covered | POL-0117 |
| ES.76 | covered | POL-0118 |
| ES.77 | covered | POL-0117 |
| ES.78 | covered | POL-0119 |
| ES.79 | covered | POL-0119 |
| ES.84 | declined | a declaration form a generator does not produce, and the compiler warns on it |
| ES.85 | covered | POL-0117 |
| ES.86 | covered | POL-0098 |
| ES.87 | covered | POL-0134 |
| ES.100 | covered | POL-0102 |
| ES.101 | covered | POL-0169 |
| ES.102 | covered | POL-0101 |
| ES.103 | covered | POL-0101 |
| ES.104 | covered | POL-0101 |
| ES.105 | covered | POL-0170 |
| ES.106 | covered | POL-0101 |
| ES.107 | covered | POL-0101 |

## Performance (Per)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| Per.1 | declined | an instruction not to act, with no decision a generator makes differently for having read it |
| Per.2 | declined | an instruction not to act, with no decision a generator makes differently for having read it |
| Per.3 | declined | an instruction not to act, with no decision a generator makes differently for having read it |
| Per.4 | declined | an instruction not to act, with no decision a generator makes differently for having read it |
| Per.5 | declined | an instruction not to act, with no decision a generator makes differently for having read it |
| Per.6 | covered | POL-0172 |
| Per.7 | declined | too general to act on; the specific cases are POL-0036 and the real-time topic |
| Per.10 | covered | POL-0008 |
| Per.11 | covered | POL-0036 |
| Per.12 | declined | an optimizer concern, not a decision made while writing a file |
| Per.13 | declined | an optimizer concern, not a decision made while writing a file |
| Per.14 | covered | POL-0012 |
| Per.15 | covered | POL-0012 |
| Per.16 | declined | layout tuning is code-local and measured; the ontology keeps performance-criticality as content |
| Per.17 | declined | layout tuning is code-local and measured; the ontology keeps performance-criticality as content |
| Per.18 | declined | layout tuning is code-local and measured; the ontology keeps performance-criticality as content |
| Per.19 | declined | layout tuning is code-local and measured; the ontology keeps performance-criticality as content |
| Per.30 | covered | POL-0079 |

## Concurrency and parallelism (CP)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| CP.1 | diverges | POL-0049 takes the opposite default: single-threaded by contract until a threading model is declared |
| CP.2 | covered | POL-0107 |
| CP.3 | covered | POL-0105 |
| CP.4 | covered | POL-0138 |
| CP.8 | covered | POL-0107 |
| CP.9 | covered | POL-0090 |
| CP.20 | covered | POL-0106 |
| CP.21 | covered | POL-0106 |
| CP.22 | covered | POL-0140 |
| CP.23 | covered | POL-0139 |
| CP.24 | covered | POL-0139 |
| CP.25 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| CP.26 | covered | POL-0139 |
| CP.31 | covered | POL-0142 |
| CP.32 | covered | POL-0142 |
| CP.40 | covered | POL-0079 |
| CP.41 | covered | POL-0138 |
| CP.42 | covered | POL-0107 |
| CP.43 | covered | POL-0140 |
| CP.44 | covered | POL-0140 |
| CP.50 | covered | POL-0141 |
| CP.51 | covered | POL-0081 |
| CP.52 | covered | POL-0080 |
| CP.53 | covered | POL-0080 |
| CP.60 | covered | POL-0138 |
| CP.61 | covered | POL-0138 |
| CP.100 | covered | POL-0143 |
| CP.101 | covered | POL-0143 |
| CP.102 | covered | POL-0143 |
| CP.110 | covered | POL-0105 |
| CP.111 | covered | POL-0107 |
| CP.200 | covered | POL-0107 |
| CP.201 | out of scope | an unwritten placeholder upstream, with no rule to disposition |

## Error handling (E)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| E.1 | covered | POL-0031 |
| E.2 | covered | POL-0031, POL-0039 |
| E.3 | covered | POL-0053 |
| E.4 | covered | POL-0015 |
| E.5 | covered | POL-0015 |
| E.6 | covered | POL-0003 |
| E.7 | covered | POL-0027 |
| E.8 | diverges | the corpus makes a precondition a type (POL-0027) rather than a stated assertion, and sends postconditions the same way |
| E.12 | covered | POL-0051 |
| E.13 | covered | POL-0163 |
| E.14 | covered | POL-0031 |
| E.15 | covered | POL-0031 |
| E.16 | covered | POL-0144 |
| E.17 | covered | POL-0053 |
| E.18 | covered | POL-0053 |
| E.19 | covered | POL-0163 |
| E.25 | covered | POL-0039, POL-0076 |
| E.26 | covered | POL-0039, POL-0076 |
| E.27 | covered | POL-0039, POL-0076 |
| E.28 | covered | POL-0124 |
| E.30 | covered | POL-0031 |
| E.31 | covered | POL-0164 |

## Constants and immutability (Con)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| Con.1 | covered | POL-0020, POL-0026 |
| Con.2 | covered | POL-0020, POL-0022 |
| Con.3 | covered | POL-0020, POL-0035 |
| Con.4 | covered | POL-0020 |
| Con.5 | covered | POL-0020, POL-0026, POL-0036 |

## Templates and generic programming (T)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| T.1 | covered | POL-0040 |
| T.2 | covered | POL-0040 |
| T.3 | covered | POL-0040 |
| T.4 | declined | syntax tree manipulation is a domain this corpus does not govern |
| T.5 | declined | the corpus routes variation to std::variant (POL-0044) rather than combining generic and object-oriented mechanisms |
| T.10 | covered | POL-0040, POL-0052 |
| T.11 | covered | POL-0040 |
| T.12 | covered | POL-0129 |
| T.13 | covered | POL-0129 |
| T.20 | declined | authoring a concept library is the case POL-0052 makes rare enough not to rule on |
| T.21 | declined | authoring a concept library is the case POL-0052 makes rare enough not to rule on |
| T.22 | declined | axioms have no language support and nothing checks them |
| T.23 | declined | authoring a concept library is the case POL-0052 makes rare enough not to rule on |
| T.24 | declined | a mechanism for distinguishing concepts that differ only semantically, which POL-0052 makes rare enough not to rule on |
| T.25 | declined | a mechanism for distinguishing concepts that differ only semantically, which POL-0052 makes rare enough not to rule on |
| T.26 | declined | authoring a concept library is the case POL-0052 makes rare enough not to rule on |
| T.40 | covered | POL-0116 |
| T.41 | covered | POL-0129 |
| T.42 | covered | POL-0130 |
| T.43 | covered | POL-0130 |
| T.44 | covered | POL-0130 |
| T.46 | out of scope | withdrawn upstream, with no rule to disposition |
| T.47 | covered | POL-0129 |
| T.48 | covered | POL-0110 |
| T.49 | declined | type erasure is the runtime-typed interface POL-0040 already rejects |
| T.60 | covered | POL-0130 |
| T.61 | declined | a parameterization tuning concern that POL-0052 makes rare enough not to rule on |
| T.62 | declined | a parameterization tuning concern that POL-0052 makes rare enough not to rule on |
| T.64 | declined | tag dispatch and specialization serve the hierarchy POL-0040 routes away from, and concepts supersede them on C++20 |
| T.65 | declined | tag dispatch and specialization serve the hierarchy POL-0040 routes away from, and concepts supersede them on C++20 |
| T.67 | declined | tag dispatch and specialization serve the hierarchy POL-0040 routes away from, and concepts supersede them on C++20 |
| T.68 | covered | POL-0096 |
| T.69 | covered | POL-0130 |
| T.80 | covered | POL-0052 |
| T.81 | covered | POL-0121 |
| T.82 | declined | a hierarchy-flattening technique for avoiding virtual calls, which is the performance-local case the ontology keeps as content |
| T.83 | declined | the compiler already rejects it |
| T.84 | declined | binary interface stability is a project architecture choice, not a decision made while writing a file |
| T.100 | declined | a variadic template is past the second caller POL-0052 already declines to templatize for |
| T.101 | out of scope | an unwritten placeholder upstream, with no rule to disposition |
| T.102 | declined | a variadic template is past the second caller POL-0052 already declines to templatize for |
| T.103 | declined | a variadic template is past the second caller POL-0052 already declines to templatize for |
| T.120 | covered | POL-0040, POL-0052 |
| T.121 | declined | template metaprogramming beyond constraints is the complexity POL-0040 and POL-0052 route away from |
| T.122 | declined | template metaprogramming beyond constraints is the complexity POL-0040 and POL-0052 route away from |
| T.123 | covered | POL-0036 |
| T.124 | covered | POL-0109 |
| T.125 | declined | template metaprogramming beyond constraints is the complexity POL-0040 and POL-0052 route away from |
| T.140 | covered | POL-0030 |
| T.141 | covered | POL-0116 |
| T.142 | declined | a notation convenience with no correctness consequence |
| T.143 | covered | POL-0130 |
| T.144 | declined | tag dispatch and specialization serve the hierarchy POL-0040 routes away from, and concepts supersede them on C++20 |
| T.150 | covered | POL-0129 |

## C-style programming (CPL)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| CPL.1 | covered | POL-0158 |
| CPL.2 | covered | POL-0064 |
| CPL.3 | covered | POL-0064 |

## Source files (SF)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| SF.1 | covered | POL-0084 |
| SF.2 | covered | POL-0028 |
| SF.3 | covered | POL-0028 |
| SF.4 | covered | POL-0137 |
| SF.5 | covered | POL-0028 |
| SF.6 | covered | POL-0162 |
| SF.7 | covered | POL-0028 |
| SF.8 | covered | POL-0028 |
| SF.9 | covered | POL-0018 |
| SF.10 | covered | POL-0137 |
| SF.11 | covered | POL-0028 |
| SF.12 | covered | POL-0137 |
| SF.13 | covered | POL-0137 |
| SF.20 | covered | POL-0028 |
| SF.21 | covered | POL-0028 |
| SF.22 | covered | POL-0028 |

## Standard library (SL)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| SL.1 | covered | POL-0109 |
| SL.2 | covered | POL-0109 |
| SL.3 | covered | POL-0162 |
| SL.4 | covered | POL-0109 |
| SL.con.1 | covered | POL-0098 |
| SL.con.2 | covered | POL-0161 |
| SL.con.3 | covered | POL-0046 |
| SL.con.4 | covered | POL-0095 |
| SL.str.1 | covered | POL-0131 |
| SL.str.2 | covered | POL-0035 |
| SL.str.3 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| SL.str.4 | covered | POL-0131 |
| SL.str.5 | covered | POL-0131 |
| SL.str.10 | covered | POL-0131 |
| SL.str.11 | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |
| SL.str.12 | covered | POL-0131 |
| SL.io.1 | covered | POL-0171 |
| SL.io.2 | covered | POL-0005 |
| SL.io.3 | diverges | POL-0111 routes formatting to std::format and POL-0073 forbids stream output from library code |
| SL.io.10 | declined | a global performance switch set once per program, not a decision made while writing a file |
| SL.io.50 | covered | POL-0110 |
| SL.C.1 | covered | POL-0154 |

## Non-rules and myths (NR)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| NR.1 | covered | POL-0097 |
| NR.2 | covered | POL-0117 |
| NR.3 | covered | POL-0039 |
| NR.4 | covered | POL-0028 |
| NR.5 | covered | POL-0015 |
| NR.6 | covered | POL-0117 |
| NR.7 | covered | POL-0120 |

## Guidelines Support Library (GSL)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| GSL.ptr | out of scope | Guidelines Support Library declined wholesale in the captured Divergences table |

## Naming and layout (NL)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| NL.1 | covered | POL-0006, POL-0112 |
| NL.2 | covered | POL-0113 |
| NL.3 | covered | POL-0112 |
| NL.4 | covered | POL-0092 |
| NL.5 | covered | POL-0084 |
| NL.7 | covered | POL-0152 |
| NL.8 | covered | POL-0084 |
| NL.9 | covered | POL-0084 |
| NL.10 | covered | POL-0084 |
| NL.11 | covered | POL-0153 |
| NL.15 | covered | POL-0092 |
| NL.16 | covered | POL-0167 |
| NL.17 | covered | POL-0092 |
| NL.18 | covered | POL-0153 |
| NL.19 | covered | POL-0017 |
| NL.20 | covered | POL-0092 |
| NL.21 | covered | POL-0153 |
| NL.25 | covered | POL-0153 |
| NL.26 | covered | POL-0026 |
| NL.27 | covered | POL-0084 |

## Type safety profile (Type)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| Type.1 | covered | POL-0094, POL-0095 |
| Type.2 | covered | POL-0150 |
| Type.3 | covered | POL-0095 |
| Type.4 | covered | POL-0094 |
| Type.5 | covered | POL-0096 |
| Type.6 | covered | POL-0136 |
| Type.7 | covered | POL-0156 |
| Type.8 | covered | POL-0154 |

## Bounds safety profile (Bounds)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| Bounds.1 | covered | POL-0133 |
| Bounds.2 | covered | POL-0133 |
| Bounds.3 | covered | POL-0155 |
| Bounds.4 | covered | POL-0046 |

## Lifetime safety profile (Lifetime)

| Rule | Disposition | Policy or reason |
|------|-------------|------------------|
| Lifetime.1 | covered | POL-0133 |

## Totals

| Disposition | Rules |
|-------------|-------|
| covered | 413 |
| adopt | 0 |
| declined | 57 |
| diverges | 4 |
| out of scope | 12 |
| **total** | **486** |

No rule is marked *adopt*. The corpus answers every Core Guidelines rule it
has not declined, diverged from, or placed out of scope.

