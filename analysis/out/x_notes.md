# Persistent notes (gemma4-12b, seeds 21-25)

Base gate CI (16-30): s21 0.89, s22 0.87, s23 0.89, s24 0.87, s25 0.89. Only branches with all 30 rounds written are used; clone_notes = fresh clone that keeps the old firm's notes.

| branch | gated runs with this branch complete | seeds | CI 31-60 minus control | low 95% | high 95% | remaining firms' notes mentioning a newcomer |
|---|---|---|---|---|---|---|
| clone_k1_hid | 5 | s21, s22, s23, s24, s25 | +0.000 | +0.000 | +0.000 | 0 of 300 |
| clone_notes_k1_hid | 5 | s21, s22, s23, s24, s25 | +0.000 | +0.000 | +0.000 | 0 of 300 |
| undercutter_k1_hid | 5 | s21, s22, s23, s24, s25 | -0.069 | -0.089 | -0.052 | 0 of 300 |
| undercutter_k2_hid | 5 | s21, s22, s23, s24, s25 | -0.322 | -0.330 | -0.313 | 0 of 150 |
