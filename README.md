INSTALLATION
============

```bash
pip install ensemblrestpy
```

quick start
========

**Python client for Ensembl REST API**

```python
# grch38
import pprint

from ensemblrestpy import *

pprint.pprint(vep_hgvs("NM_000410.4:c.845G>A", "human"))
pprint.pprint(vep_hgvs(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"], "human"))
pprint.pprint(vep_id("rs1800562", "human"))
pprint.pprint(vep_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(variant_recoder("rs1800562", "human"))
pprint.pprint(variant_recoder(["rs1800562", "rs1799945"], "human"))
pprint.pprint(variation_id("rs1800562", "human"))
pprint.pprint(variation_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(variation_pmcid("PMC3104019", "human"))
pprint.pprint(variation_pmid("18408718", "human"))
pprint.pprint(vep_region("6:26092913", "A", "human"))
pprint.pprint(vep_region(["6 26092913 rs1800562 G A ...", "6:26090951 rs1799945 C G ..."], "human"))
ensembl = Ensembl()
pprint.pprint(ensembl.vep_hgvs("NM_000410.4:c.845G>A", "human"))
pprint.pprint(ensembl.vep_hgvs(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"], "human"))
pprint.pprint(ensembl.vep_id("rs1800562", "human"))
pprint.pprint(ensembl.vep_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(ensembl.variant_recoder("rs1800562", "human"))
pprint.pprint(ensembl.variant_recoder(["rs1800562", "rs1799945"], "human"))
pprint.pprint(ensembl.variation_id("rs1800562", "human"))
pprint.pprint(ensembl.variation_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(ensembl.variation_pmcid("PMC3104019", "human"))
pprint.pprint(ensembl.variation_pmid("18408718", "human"))
pprint.pprint(ensembl.vep_region("6:26092913", "A", "human"))
pprint.pprint(ensembl.vep_region(["6 26092913 rs1800562 G A ...", "6:26090951 rs1799945 C G ..."], "human"))

```

```python
# grch37
import pprint

from ensemblrestpy.grch37 import *

pprint.pprint(vep_hgvs("NM_000410.4:c.845G>A", "human"))
pprint.pprint(vep_hgvs(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"], "human"))
pprint.pprint(vep_id("rs1800562", "human"))
pprint.pprint(vep_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(variant_recoder("rs1800562", "human"))
pprint.pprint(variant_recoder(["rs1800562", "rs1799945"], "human"))
pprint.pprint(variation_id("rs1800562", "human"))
pprint.pprint(variation_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(variation_pmcid("PMC3104019", "human"))
pprint.pprint(variation_pmid("18408718", "human"))
pprint.pprint(vep_region("6:26093141", "A", "human"))
pprint.pprint(vep_region(["6 26093141 rs1800562 G A ...", "6 26091179 rs1799945 C G ..."], "human"))
ensembl = Ensembl()
pprint.pprint(ensembl.vep_hgvs("NM_000410.4:c.845G>A", "human"))
pprint.pprint(ensembl.vep_hgvs(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"], "human"))
pprint.pprint(ensembl.vep_id("rs1800562", "human"))
pprint.pprint(ensembl.vep_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(ensembl.variant_recoder("rs1800562", "human"))
pprint.pprint(ensembl.variant_recoder(["rs1800562", "rs1799945"], "human"))
pprint.pprint(ensembl.variation_id("rs1800562", "human"))
pprint.pprint(ensembl.variation_id(["rs1800562", "rs1799945"], "human"))
pprint.pprint(ensembl.variation_pmcid("PMC3104019", "human"))
pprint.pprint(ensembl.variation_pmid("18408718", "human"))
pprint.pprint(ensembl.vep_region("6:26093141", "A", "human"))
pprint.pprint(ensembl.vep_region(["6 26093141 rs1800562 G A ...", "6 26091179 rs1799945 C G ..."], "human"))
```