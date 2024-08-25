from functools import singledispatch, singledispatchmethod, partialmethod, partial
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry

media_type = dict(json="application/json", xml="text/xml", nh="text/x-nh", phyloxml="text/x-phyloxml+xml",
                  orthoxml="text/x-orthoxml+xml", gff3="text/x-gff3", fasta="text/x-fasta", bed="text/x-bed",
                  seqxml="text/x-seqxml+xml", text="text/plain", yaml="text/x-yaml", jsonp="text/javascript")

server = 'http://rest.ensembl.org'
session = requests.Session()
adapter = HTTPAdapter(
    max_retries=Retry(backoff_factor=3600 / 55000, respect_retry_after_header=True, status_forcelist=[429],
                      allowed_methods=["GET", "POST"]))
session.mount(server, adapter)


def get(endpoint, params, response_format):
    headers = {"Content-Type": media_type[response_format]}
    response = session.get(urljoin(server, endpoint), headers=headers, params=params)
    if response.ok:
        if headers["Content-Type"] == "application/json":
            return response.json()
        else:
            return response.text
    else:
        response.raise_for_status()


def post(endpoint, params, json, response_format):
    headers = {"Content-Type": media_type[response_format], 'Accept': media_type[response_format]}
    response = session.post(urljoin(server, endpoint), headers=headers, params=params, json=json)
    if response.ok:
        if headers["Accept"] == "application/json":
            return response.json()
        else:
            return response.text
    else:
        response.raise_for_status()


@singledispatch
def vep_hgvs(hgvs_notation: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
             Conservation=None, DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
             GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None,
             NMD=None, OpenTargets=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None,
             appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None,
             domains=None, failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None,
             ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None,
             mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None,
             pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
             transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
             response_format='json'):
    return get(f"vep/{species}/hgvs/{hgvs_notation}",
               params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                           Conservation=Conservation, DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE,
                           Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                           Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                           OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                           ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback, canonical=canonical,
                           ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed,
                           flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                           flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                           gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                           mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                           pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                           protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                           transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                           variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
               response_format=response_format)


@vep_hgvs.register
def _(hgvs_notation: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
      DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
      IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Phenotypes=None,
      SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None, appris=None, callback=None, canonical=None, ccds=None,
      dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
      flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None,
      mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None,
      pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
      transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
      response_format='json'):
    return post(f"vep/{species}/hgvs",
                params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                            DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                            GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF, Mastermind=Mastermind,
                            MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                            Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                            ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback, canonical=canonical,
                            ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains,
                            failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                            flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                            gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                            mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                            pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                            protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                            transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                            uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                            xref_refseq=xref_refseq), response_format=response_format,
                json={"hgvs_notations": hgvs_notation})


@singledispatch
def vep_id(id: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None, Conservation=None,
           DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
           IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None,
           Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None,
           dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
           flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None,
           minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
           pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
           transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
           xref_refseq=None, response_format='json'):
    return get(f"vep/{species}/id/{id}",
               params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                           Conservation=Conservation, DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE,
                           Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                           Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                           OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                           appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                           dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                           flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                           ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged,
                           minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                           pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                           protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                           transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                           variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
               response_format=response_format)


@vep_id.register
def _(id: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None,
      DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None,
      Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Phenotypes=None, SpliceAI=None,
      UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
      distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None,
      ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None,
      numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None,
      refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None,
      uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
    return post(f"vep/{species}/id",
                params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                            DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                            GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF, Mastermind=Mastermind,
                            MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                            Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                            callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                            distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                            flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                            ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged,
                            minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene,
                            pick=pick, pick_allele=pick_allele, pick_allele_gene=pick_allele_gene,
                            pick_order=pick_order, protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                            shift_genomic=shift_genomic, transcript_id=transcript_id,
                            transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                            variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                response_format=response_format, json={"ids": id})


@singledispatch
def vep_region(region: str, allele: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None,
               CADD=None, Conservation=None, DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
               GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None,
               NMD=None, OpenTargets=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None,
               callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None,
               failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None,
               gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None,
               numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None,
               protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
               transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
               response_format='json'):
    return get(f"vep/{species}/region/{region}/{allele}/",
               params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                           Conservation=Conservation, DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE,
                           Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                           Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                           OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                           appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                           dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                           flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                           ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged,
                           minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                           pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                           protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                           transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                           variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
               response_format=response_format)


@vep_region.register
def _(region: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None,
      DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None,
      Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Phenotypes=None, SpliceAI=None,
      UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
      distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None,
      ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None,
      numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None,
      refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None,
      uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
    return post(f"vep/{species}/region",
                params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                            DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                            GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF, Mastermind=Mastermind,
                            MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                            Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                            callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                            distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                            flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                            ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged,
                            minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene,
                            pick=pick, pick_allele=pick_allele, pick_allele_gene=pick_allele_gene,
                            pick_order=pick_order, protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                            shift_genomic=shift_genomic, transcript_id=transcript_id,
                            transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                            variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                response_format=response_format, json={"variants": region})


@singledispatch
def variant_recoder(id: str, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None,
                    minimal=None, var_synonyms=None, vcf_string=None, response_format='json'):
    return get(f"variant_recoder/{species}/{id}",
               params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                           gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                           vcf_string=vcf_string), response_format=response_format)


@variant_recoder.register
def _(id: list, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None, minimal=None,
      var_synonyms=None, vcf_string=None, response_format='json'):
    return post(f"variant_recoder/{species}",
                params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                            gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                            vcf_string=vcf_string), response_format=response_format, json={"ids": id})


@singledispatch
def variation_id(id: str, species: str, callback=None, genotypes=None, genotyping_chips=None, phenotypes=None,
                 pops=None, population_genotypes=None, response_format='json'):
    return get(f"variation/{species}/{id}",
               params=dict(callback=callback, genotypes=genotypes, genotyping_chips=genotyping_chips,
                           phenotypes=phenotypes, pops=pops, population_genotypes=population_genotypes),
               response_format=response_format)


@variation_id.register
def _(id: list, species: str, callback=None, genotypes=None, phenotypes=None, pops=None, population_genotypes=None,
      response_format='json'):
    return post(f"variation/{species}/",
                params=dict(callback=callback, genotypes=genotypes, phenotypes=phenotypes, pops=pops,
                            population_genotypes=population_genotypes), response_format=response_format,
                json={"ids": id})


def variation_pmcid(pmcid: str, species: str, callback=None, response_format='json'):
    return get(f"variation/{species}/pmcid/{pmcid}", params=dict(callback=callback), response_format=response_format)


def variation_pmid(pmid: str, species: str, callback=None, response_format='json'):
    return get(f"variation/{species}/pmid/{pmid}", params=dict(callback=callback), response_format=response_format)


variant_recoder_human = partial(variant_recoder, species="human")
variation_pmid_human = partial(variation_pmid, species="human")
variation_pmcid_human = partial(variation_pmcid, species="human")
variation_id_human = partial(variation_id, species="human")
vep_hgvs_human = partial(vep_hgvs, species="human")
vep_id_human = partial(vep_id, species="human")
vep_region_human = partial(vep_region, species="human")


class Ensembl:
    def __init__(self):
        self.server = "https://rest.ensembl.org/"
        self.session = requests.Session()
        self.adapter = HTTPAdapter(
            max_retries=Retry(backoff_factor=3600 / 55000, respect_retry_after_header=True, status_forcelist=[429],
                              allowed_methods=["GET", "POST"], ))
        self.session.mount(self.server, self.adapter)

    def get(self, endpoint, params, response_format):
        headers = {"Content-Type": media_type[response_format]}
        response = self.session.get(urljoin(self.server, endpoint), headers=headers, params=params)
        if response.ok:
            if headers["Content-Type"] == "application/json":
                return response.json()
            else:
                return response.text
        else:
            response.raise_for_status()

    def post(self, endpoint, params, json, response_format):
        headers = {"Content-Type": media_type[response_format], "Accept": media_type[response_format]}
        response = self.session.post(urljoin(self.server, endpoint), headers=headers, params=params, json=json)
        if response.ok:
            if headers["Accept"] == "application/json":
                return response.json()
            else:
                return response.text
        else:
            response.raise_for_status()

    @singledispatchmethod
    def vep_hgvs(self, hgvs_notation: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None,
                 CADD=None, Conservation=None, DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
                 GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None,
                 NMD=None, OpenTargets=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None,
                 appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None,
                 domains=None, failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None,
                 ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None,
                 mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None,
                 pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
                 transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
                 response_format='json'):

        return self.get(f"vep/{species}/hgvs/{hgvs_notation}",
                        params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                    CADD=CADD, Conservation=Conservation, DisGeNET=DisGeNET,
                                    DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                    Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                    OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI,
                                    UTRAnnotator=UTRAnnotator, ambiguous_hgvs=ambiguous_hgvs, appris=appris,
                                    callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                                    distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                                    flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                    ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                    merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                    per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                    pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                    refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                    transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                    uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                    xref_refseq=xref_refseq), response_format=response_format)

    @vep_hgvs.register
    def _(self, hgvs_notation: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
          DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
          IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None,
          Phenotypes=None, SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None, appris=None, callback=None,
          canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None,
          flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None,
          hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None,
          pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None,
          shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
          variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):

        return self.post(f"vep/{species}/hgvs",
                         params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                     CADD=CADD, DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE,
                                     Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                                     LoF=LoF, Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI,
                                     UTRAnnotator=UTRAnnotator, ambiguous_hgvs=ambiguous_hgvs, appris=appris,
                                     callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                                     distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                                     flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                     ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                     merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                     per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                     pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                     refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                     transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                     uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                     xref_refseq=xref_refseq), response_format=response_format,
                         json={"hgvs_notations": hgvs_notation})

    @singledispatchmethod
    def vep_id(self, id: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
               Conservation=None, DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
               GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None,
               NMD=None, OpenTargets=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None,
               callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None,
               failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None,
               gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None,
               numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None,
               protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
               transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
               response_format='json'):

        return self.get(f"vep/{species}/id/{id}",
                        params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                    CADD=CADD, Conservation=Conservation, DisGeNET=DisGeNET,
                                    DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                    Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                    OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI,
                                    UTRAnnotator=UTRAnnotator, appris=appris, callback=callback, canonical=canonical,
                                    ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains,
                                    failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                    flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                    gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                                    mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                                    pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                                    protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                                    shift_genomic=shift_genomic, transcript_id=transcript_id,
                                    transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                                    variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                        response_format=response_format)

    @vep_id.register
    def _(self, id: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
          DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
          IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None,
          Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None,
          dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
          flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None,
          minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
          pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
          transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
          xref_refseq=None, response_format='json'):

        return self.post(f"vep/{species}/id",
                         params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                     CADD=CADD, DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE,
                                     Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                                     LoF=LoF, Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI,
                                     UTRAnnotator=UTRAnnotator, appris=appris, callback=callback, canonical=canonical,
                                     ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains,
                                     failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                     flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                     gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                                     mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                                     pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                                     protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                                     shift_genomic=shift_genomic, transcript_id=transcript_id,
                                     transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                                     variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                         response_format=response_format, json={"ids": id})

    @singledispatchmethod
    def vep_region(self, region: str, allele: str, species: str, AlphaMissense=None, AncestralAllele=None,
                   Blosum62=None, CADD=None, Conservation=None, DisGeNET=None, DosageSensitivity=None, EVE=None,
                   Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None,
                   MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Phenotypes=None, SpliceAI=None,
                   UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
                   distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
                   flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None,
                   minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
                   pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None,
                   shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
                   variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):

        return self.get(f"vep/{species}/region/{region}/{allele}/",
                        params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                    CADD=CADD, Conservation=Conservation, DisGeNET=DisGeNET,
                                    DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                    Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                    OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI,
                                    UTRAnnotator=UTRAnnotator, appris=appris, callback=callback, canonical=canonical,
                                    ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains,
                                    failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                    flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                    gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                                    mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                                    pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                                    protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                                    shift_genomic=shift_genomic, transcript_id=transcript_id,
                                    transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                                    variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                        response_format=response_format)

    @vep_region.register
    def _(self, region: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
          DisGeNET=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
          IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None,
          Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None,
          dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
          flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None,
          minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
          pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
          transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
          xref_refseq=None, response_format='json'):

        return self.post(f"vep/{species}/region",
                         params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                     CADD=CADD, DisGeNET=DisGeNET, DosageSensitivity=DosageSensitivity, EVE=EVE,
                                     Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                                     LoF=LoF, Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     OpenTargets=OpenTargets, Phenotypes=Phenotypes, SpliceAI=SpliceAI,
                                     UTRAnnotator=UTRAnnotator, appris=appris, callback=callback, canonical=canonical,
                                     ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains,
                                     failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                     flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                     gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                                     mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                                     pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                                     protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                                     shift_genomic=shift_genomic, transcript_id=transcript_id,
                                     transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                                     variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                         response_format=response_format, json={"variants": region})

    @singledispatchmethod
    def variant_recoder(self, id: str, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None,
                        gencode_basic=None, minimal=None, var_synonyms=None, vcf_string=None, response_format='json'):

        return self.get(f"variant_recoder/{species}/{id}",
                        params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                                    gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                                    vcf_string=vcf_string), response_format=response_format)

    @variant_recoder.register
    def _(self, id: list, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None,
          minimal=None, var_synonyms=None, vcf_string=None, response_format='json'):

        return self.post(f"variant_recoder/{species}",
                         params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                                     gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                                     vcf_string=vcf_string), response_format=response_format, json={"ids": id})

    @singledispatchmethod
    def variation_id(self, id: str, species: str, callback=None, genotypes=None, genotyping_chips=None, phenotypes=None,
                     pops=None, population_genotypes=None, response_format='json'):

        return self.get(f"variation/{species}/{id}",
                        params=dict(callback=callback, genotypes=genotypes, genotyping_chips=genotyping_chips,
                                    phenotypes=phenotypes, pops=pops, population_genotypes=population_genotypes),
                        response_format=response_format)

    @variation_id.register
    def _(self, id: list, species: str, callback=None, genotypes=None, phenotypes=None, pops=None,
          population_genotypes=None, response_format='json'):

        return self.post(f"variation/{species}/",
                         params=dict(callback=callback, genotypes=genotypes, phenotypes=phenotypes, pops=pops,
                                     population_genotypes=population_genotypes), response_format=response_format,
                         json={"ids": id})

    def variation_pmcid(self, pmcid: str, species: str, callback=None, response_format='json'):

        return self.get(f"variation/{species}/pmcid/{pmcid}", params=dict(callback=callback),
                        response_format=response_format)

    def variation_pmid(self, pmid: str, species: str, callback=None, response_format='json'):

        return self.get(f"variation/{species}/pmid/{pmid}", params=dict(callback=callback),
                        response_format=response_format)

    variant_recoder_human = partialmethod(variant_recoder, species="human")
    variation_id_human = partialmethod(variation_id, species="human")
    variation_pmcid_human = partialmethod(variation_pmcid, species="human")
    variation_pmid_human = partialmethod(variation_pmid, species="human")
    vep_hgvs_human = partialmethod(vep_hgvs, species="human")
    vep_id_human = partialmethod(vep_id, species="human")
    vep_region_human = partialmethod(vep_region, species="human")


if __name__ == "__main__":
    import pprint

    pprint.pprint(vep_hgvs("NM_000410.4:c.845G>A", "human"))
    pprint.pprint(vep_hgvs_human('NM_000410.4:c.845G>A'))
    pprint.pprint(vep_hgvs(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"], "human"))
    pprint.pprint(vep_hgvs_human(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"]))
    pprint.pprint(vep_id("rs1800562", "human"))
    pprint.pprint(vep_id_human('rs1800562'))
    pprint.pprint(vep_id(["rs1800562", "rs1799945"], "human"))
    pprint.pprint(vep_id_human(["rs1800562", "rs1799945"]))
    pprint.pprint(variant_recoder("rs1800562", "human"))
    pprint.pprint(variant_recoder_human('rs1800562'))
    pprint.pprint(variant_recoder(["rs1800562", "rs1799945"], "human"))
    pprint.pprint(variant_recoder_human(["rs1800562", "rs1799945"]))
    pprint.pprint(variation_id("rs1800562", "human"))
    pprint.pprint(variation_id_human('rs1800562'))
    pprint.pprint(variation_id(["rs1800562", "rs1799945"], "human"))
    pprint.pprint(variation_id_human(["rs1800562", "rs1799945"]))
    pprint.pprint(variation_pmcid("PMC3104019", "human"))
    pprint.pprint(variation_pmcid_human('PMC3104019'))
    pprint.pprint(variation_pmid("18408718", "human"))
    pprint.pprint(variation_pmid_human('18408718'))
    pprint.pprint(vep_region("6:26092913", "A", "human"))
    pprint.pprint(vep_region_human('6:26092913', 'A'))
    pprint.pprint(vep_region(["6 26092913 rs1800562 G A ...", "6:26090951 rs1799945 C G ..."], "human"))
    pprint.pprint(vep_region_human(["6 26092913 rs1800562 G A ...", "6:26090951 rs1799945 C G ..."]))
    ensembl = Ensembl()
    pprint.pprint(ensembl.vep_hgvs("NM_000410.4:c.845G>A", "human"))
    pprint.pprint(ensembl.vep_hgvs_human('NM_000410.4:c.845G>A'))
    pprint.pprint(ensembl.vep_hgvs(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"], "human"))
    pprint.pprint(ensembl.vep_hgvs_human(['NM_000410.4:c.845G>A', "NM_000410.4:c.187C>G"]))
    pprint.pprint(ensembl.vep_id("rs1800562", "human"))
    pprint.pprint(ensembl.vep_id_human('rs1800562'))
    pprint.pprint(ensembl.vep_id(["rs1800562", "rs1799945"], "human"))
    pprint.pprint(ensembl.vep_id_human(["rs1800562", "rs1799945"]))
    pprint.pprint(ensembl.variant_recoder("rs1800562", "human"))
    pprint.pprint(ensembl.variant_recoder_human('rs1800562'))
    pprint.pprint(ensembl.variant_recoder(["rs1800562", "rs1799945"], "human"))
    pprint.pprint(ensembl.variant_recoder_human(["rs1800562", "rs1799945"]))
    pprint.pprint(ensembl.variation_id("rs1800562", "human"))
    pprint.pprint(ensembl.variation_id_human('rs1800562'))
    pprint.pprint(ensembl.variation_id(["rs1800562", "rs1799945"], "human"))
    pprint.pprint(ensembl.variation_id_human(["rs1800562", "rs1799945"]))
    pprint.pprint(ensembl.variation_pmcid("PMC3104019", "human"))
    pprint.pprint(ensembl.variation_pmcid_human('PMC3104019'))
    pprint.pprint(ensembl.variation_pmid("18408718", "human"))
    pprint.pprint(ensembl.variation_pmid_human('18408718'))
    pprint.pprint(ensembl.vep_region("6:26092913", "A", "human"))
    pprint.pprint(ensembl.vep_region_human('6:26092913', 'A'))
    pprint.pprint(ensembl.vep_region(["6 26092913 rs1800562 G A ...", "6:26090951 rs1799945 C G ..."], "human"))
    pprint.pprint(ensembl.vep_region_human(["6 26092913 rs1800562 G A ...", "6:26090951 rs1799945 C G ..."]))
