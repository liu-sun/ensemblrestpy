from functools import singledispatch, singledispatchmethod, partialmethod, partial
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry

media_type = dict(json="application/json", xml="text/xml", nh="text/x-nh", phyloxml="text/x-phyloxml+xml",
                  orthoxml="text/x-orthoxml+xml", gff3="text/x-gff3", fasta="text/x-fasta", bed="text/x-bed",
                  seqxml="text/x-seqxml+xml", text="text/plain", yaml="text/x-yaml", jsonp="text/javascript")
server = 'https://rest.ensembl.org'
session = requests.Session()
adapter = HTTPAdapter(
    max_retries=Retry(backoff_factor=3600 / 55000, respect_retry_after_header=True, status_forcelist=[429],
                      allowed_methods=["GET", "POST"], backoff_jitter=0.1))
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
        return response.raise_for_status()


def post(endpoint, params, json, response_format):
    headers = {"Content-Type": media_type[response_format], 'Accept': media_type[response_format]}
    response = session.post(urljoin(server, endpoint), headers=headers, params=params, json=json)
    if response.ok:
        if headers["Content-Type"] == "application/json":
            return response.json()
        else:
            return response.text
    else:
        return response.raise_for_status()


@singledispatch
def archive(id: str, callback=None, response_format='json'):
    return get(f"archive/id/{id}", params=dict(callback=callback), response_format=response_format)


@archive.register
def _(id: list, callback=None, response_format='json'):
    return post(f"archive/id", params=dict(callback=callback), response_format=response_format, json={"id": id})


def cafe_tree(id: str, callback=None, compara=None, nh_format=None, response_format='json'):
    return get(f"cafe/genetree/id/{id}", params=dict(callback=callback, compara=compara, nh_format=nh_format),
               response_format=response_format)


def cafe_tree_member_symbol(species: str, symbol: str, callback=None, compara=None, db_type=None, external_db=None,
                            nh_format=None, object_type=None, response_format='json'):
    return get(f"cafe/genetree/member/symbol/{species}/{symbol}",
               params=dict(callback=callback, compara=compara, db_type=db_type, external_db=external_db,
                           nh_format=nh_format, object_type=object_type), response_format=response_format)


def cafe_tree_species_member_id(id: str, species: str, callback=None, compara=None, db_type=None, nh_format=None,
                                object_type=None, response_format='json'):
    return get(f"cafe/genetree/member/id/{species}/{id}",
               params=dict(callback=callback, compara=compara, db_type=db_type, nh_format=nh_format,
                           object_type=object_type), response_format=response_format)


def genetree(id: str, aligned=None, callback=None, cigar_line=None, clusterset_id=None, compara=None, nh_format=None,
             prune_species=None, prune_taxon=None, sequence=None, response_format='json'):
    return get(f"genetree/id/{id}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, clusterset_id=clusterset_id,
                           compara=compara, nh_format=nh_format, prune_species=prune_species, prune_taxon=prune_taxon,
                           sequence=sequence), response_format=response_format)


def genetree_member_symbol(species: str, symbol: str, aligned=None, callback=None, cigar_line=None, clusterset_id=None,
                           compara=None, db_type=None, external_db=None, nh_format=None, object_type=None,
                           prune_species=None, prune_taxon=None, sequence=None, response_format='json'):
    return get(f"genetree/member/symbol/{species}/{symbol}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, clusterset_id=clusterset_id,
                           compara=compara, db_type=db_type, external_db=external_db, nh_format=nh_format,
                           object_type=object_type, prune_species=prune_species, prune_taxon=prune_taxon,
                           sequence=sequence), response_format=response_format)


def genetree_species_member_id(id: str, species: str, aligned=None, callback=None, cigar_line=None, clusterset_id=None,
                               compara=None, db_type=None, nh_format=None, object_type=None, prune_species=None,
                               prune_taxon=None, sequence=None, response_format='json'):
    return get(f"genetree/member/id/{species}/{id}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, clusterset_id=clusterset_id,
                           compara=compara, db_type=db_type, nh_format=nh_format, object_type=object_type,
                           prune_species=prune_species, prune_taxon=prune_taxon, sequence=sequence),
               response_format=response_format)


def genomic_alignment_region(region: str, species: str, aligned=None, callback=None, compact=None, compara=None,
                             display_species_set=None, mask=None, method=None, species_set=None, species_set_group=None,
                             response_format='json'):
    return get(f"alignment/region/{species}/{region}",
               params=dict(aligned=aligned, callback=callback, compact=compact, compara=compara,
                           display_species_set=display_species_set, mask=mask, method=method, species_set=species_set,
                           species_set_group=species_set_group), response_format=response_format)


def homology_species_gene_id(id: str, species: str, aligned=None, callback=None, cigar_line=None, compara=None,
                             format=None, sequence=None, target_species=None, target_taxon=None, type=None,
                             response_format='json'):
    return get(f"homology/id/{species}/{id}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, compara=compara, format=format,
                           sequence=sequence, target_species=target_species, target_taxon=target_taxon, type=type),
               response_format=response_format)


def homology_symbol(species: str, symbol: str, aligned=None, callback=None, cigar_line=None, compara=None,
                    external_db=None, format=None, sequence=None, target_species=None, target_taxon=None, type=None,
                    response_format='json'):
    return get(f"homology/symbol/{species}/{symbol}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, compara=compara,
                           external_db=external_db, format=format, sequence=sequence, target_species=target_species,
                           target_taxon=target_taxon, type=type), response_format=response_format)


def xref_external(species: str, symbol: str, callback=None, db_type=None, external_db=None, object_type=None,
                  response_format='json'):
    return get(f"xrefs/symbol/{species}/{symbol}",
               params=dict(callback=callback, db_type=db_type, external_db=external_db, object_type=object_type),
               response_format=response_format)


def xref_id(id: str, all_levels=None, callback=None, db_type=None, external_db=None, object_type=None, species=None,
            response_format='json'):
    return get(f"xrefs/id/{id}",
               params=dict(all_levels=all_levels, callback=callback, db_type=db_type, external_db=external_db,
                           object_type=object_type, species=species), response_format=response_format)


def xref_name(name: str, species: str, callback=None, db_type=None, external_db=None, response_format='json'):
    return get(f"xrefs/name/{species}/{name}", params=dict(callback=callback, db_type=db_type, external_db=external_db),
               response_format=response_format)


def analysis(species: str, callback=None, response_format='json'):
    return get(f"info/analysis/{species}", params=dict(callback=callback), response_format=response_format)


def assembly_info(species: str, bands=None, callback=None, synonyms=None, response_format='json'):
    return get(f"info/assembly/{species}", params=dict(bands=bands, callback=callback, synonyms=synonyms),
               response_format=response_format)


def assembly_stats(region_name: str, species: str, bands=None, callback=None, synonyms=None, response_format='json'):
    return get(f"info/assembly/{species}/{region_name}", params=dict(bands=bands, callback=callback, synonyms=synonyms),
               response_format=response_format)


def biotypes(species: str, callback=None, response_format='json'):
    return get(f"info/biotypes/{species}", params=dict(callback=callback), response_format=response_format)


def biotypes_groups(callback=None, group=None, object_type=None, response_format='json'):
    return get(f"info/biotypes/groups/{group}/{object_type}",
               params=dict(callback=callback, group=group, object_type=object_type), response_format=response_format)


def biotypes_name(name: str, callback=None, object_type=None, response_format='json'):
    return get(f"info/biotypes/name/{name}/{object_type}", params=dict(callback=callback, object_type=object_type),
               response_format=response_format)


def compara_methods(callback=None, compara=None, response_format='json', **kwargs):
    return get(f"info/compara/methods", params=dict(kwargs, callback=callback, compara=compara),
               response_format=response_format)


def compara_species_sets(method: str, callback=None, compara=None, response_format='json'):
    return get(f"info/compara/species_sets/{method}", params=dict(callback=callback, compara=compara),
               response_format=response_format)


def comparas(callback=None, response_format='json'):
    return get(f"info/comparas", params=dict(callback=callback), response_format=response_format)


def data(callback=None, response_format='json'):
    return get(f"info/data", params=dict(callback=callback), response_format=response_format)


def eg_version(callback=None, response_format='json'):
    return get(f"info/eg_version", params=dict(callback=callback), response_format=response_format)


def external_dbs(species: str, callback=None, feature=None, filter=None, response_format='json'):
    return get(f"info/external_dbs/{species}", params=dict(callback=callback, feature=feature, filter=filter),
               response_format=response_format)


def info_divisions(callback=None, response_format='json'):
    return get(f"info/divisions", params=dict(callback=callback), response_format=response_format)


def info_genome(name: str, callback=None, expand=None, response_format='json'):
    return get(f"info/genomes/{name}", params=dict(callback=callback, expand=expand), response_format=response_format)


def info_genomes_accession(accession: str, callback=None, expand=None, response_format='json'):
    return get(f"info/genomes/accession/{accession}", params=dict(callback=callback, expand=expand),
               response_format=response_format)


def info_genomes_assembly(assembly_id: str, callback=None, expand=None, response_format='json'):
    return get(f"info/genomes/assembly/{assembly_id}", params=dict(callback=callback, expand=expand),
               response_format=response_format)


def info_genomes_division(division: str, callback=None, expand=None, response_format='json'):
    return get(f"info/genomes/division/{division}", params=dict(callback=callback, expand=expand),
               response_format=response_format)


def info_genomes_taxonomy(taxon_name: str, callback=None, expand=None, response_format='json'):
    return get(f"info/genomes/taxonomy/{taxon_name}", params=dict(callback=callback, expand=expand),
               response_format=response_format)


def ping(callback=None, response_format='json'):
    return get(f"info/ping", params=dict(callback=callback), response_format=response_format)


def rest(callback=None, response_format='json'):
    return get(f"info/rest", params=dict(callback=callback), response_format=response_format)


def software(callback=None, response_format='json'):
    return get(f"info/software", params=dict(callback=callback), response_format=response_format)


def species(callback=None, division=None, hide_strain_info=None, strain_collection=None, response_format='json'):
    return get(f"info/species", params=dict(callback=callback, division=division, hide_strain_info=hide_strain_info,
                                            strain_collection=strain_collection), response_format=response_format)


def variation(species: str, callback=None, filter=None, response_format='json'):
    return get(f"info/variation/{species}", params=dict(callback=callback, filter=filter),
               response_format=response_format)


def variation_consequence_types(callback=None, rank=None, response_format='json'):
    return get(f"info/variation/consequence_types", params=dict(callback=callback, rank=rank),
               response_format=response_format)


def variation_population_name(population_name: str, species: str, callback=None, response_format='json'):
    return get(f"info/variation/populations/{species}:/{population_name}", params=dict(callback=callback),
               response_format=response_format)


def variation_populations(species: str, callback=None, filter=None, response_format='json'):
    return get(f"info/variation/populations/{species}", params=dict(callback=callback, filter=filter),
               response_format=response_format)


def ld_id_get(id: str, population_name: str, species: str, attribs=None, callback=None, d_prime=None, r2=None,
              window_size=None, response_format='json'):
    return get(f"ld/{species}/{id}/{population_name}",
               params=dict(attribs=attribs, callback=callback, d_prime=d_prime, r2=r2, window_size=window_size),
               response_format=response_format)


def ld_pairwise_get(id1: str, id2: str, species: str, callback=None, d_prime=None, population_name=None, r2=None,
                    response_format='json'):
    return get(f"ld/{species}/pairwise/{id1}/{id2}",
               params=dict(callback=callback, d_prime=d_prime, population_name=population_name, r2=r2),
               response_format=response_format)


def ld_region_get(population_name: str, region: str, species: str, callback=None, d_prime=None, r2=None,
                  response_format='json'):
    return get(f"ld/{species}/region/{region}/{population_name}",
               params=dict(callback=callback, d_prime=d_prime, r2=r2), response_format=response_format)


@singledispatch
def lookup_id(id: str, callback=None, db_type=None, expand=None, format=None, mane=None, phenotypes=None, species=None,
              utr=None, response_format='json'):
    return get(f"lookup/id/{id}",
               params=dict(callback=callback, db_type=db_type, expand=expand, format=format, mane=mane,
                           phenotypes=phenotypes, species=species, utr=utr), response_format=response_format)


@lookup_id.register
def _(id: list, callback=None, db_type=None, expand=None, format=None, object_type=None, species=None,
      response_format='json'):
    return post(f"lookup/id",
                params=dict(callback=callback, db_type=db_type, expand=expand, format=format, object_type=object_type,
                            species=species), response_format=response_format, json={'id': id})


@singledispatch
def lookup_symbol(species: str, symbol: str, callback=None, expand=None, format=None, response_format='json'):
    return get(f"lookup/symbol/{species}/{symbol}", params=dict(callback=callback, expand=expand, format=format),
               response_format=response_format)


@lookup_symbol.register
def _(symbol: str, species: str, callback=None, expand=None, format=None, response_format='json'):
    return post(f"lookup/symbol/{species}/", params=dict(callback=callback, expand=expand, format=format),
                response_format=response_format, json={"symbols": symbol})


def assembly_cdna(id: str, region: str, callback=None, include_original_region=None, species=None,
                  response_format='json'):
    return get(f"map/cdna/{id}/{region}",
               params=dict(callback=callback, include_original_region=include_original_region, species=species),
               response_format=response_format)


def assembly_cds(id: str, region: str, callback=None, include_original_region=None, species=None,
                 response_format='json'):
    return get(f"map/cds/{id}/{region}",
               params=dict(callback=callback, include_original_region=include_original_region, species=species),
               response_format=response_format)


def assembly_map(asm_one: str, asm_two: str, region: str, species: str, callback=None, coord_system=None,
                 target_coord_system=None, response_format='json'):
    return get(f"map/{species}/{asm_one}/{region}/{asm_two}",
               params=dict(callback=callback, coord_system=coord_system, target_coord_system=target_coord_system),
               response_format=response_format)


def assembly_translation(id: str, region: str, callback=None, species=None, response_format='json'):
    return get(f"map/translation/{id}/{region}", params=dict(callback=callback, species=species),
               response_format=response_format)


def ontology_ancestors(id: str, callback=None, ontology=None, response_format='json'):
    return get(f"ontology/ancestors/{id}", params=dict(callback=callback, ontology=ontology),
               response_format=response_format)


def ontology_ancestors_chart(id: str, callback=None, ontology=None, response_format='json'):
    return get(f"ontology/ancestors/chart/{id}", params=dict(callback=callback, ontology=ontology),
               response_format=response_format)


def ontology_descendants(id: str, callback=None, closest_term=None, ontology=None, subset=None, zero_distance=None,
                         response_format='json'):
    return get(f"ontology/descendants/{id}",
               params=dict(callback=callback, closest_term=closest_term, ontology=ontology, subset=subset,
                           zero_distance=zero_distance), response_format=response_format)


def ontology_id(id: str, callback=None, relation=None, simple=None, response_format='json'):
    return get(f"ontology/id/{id}", params=dict(callback=callback, relation=relation, simple=simple),
               response_format=response_format)


def ontology_name(name: str, callback=None, ontology=None, relation=None, simple=None, response_format='json'):
    return get(f"ontology/name/{name}",
               params=dict(callback=callback, ontology=ontology, relation=relation, simple=simple),
               response_format=response_format)


def taxonomy_classification(id: str, callback=None, response_format='json'):
    return get(f"taxonomy/classification/{id}", params=dict(callback=callback), response_format=response_format)


def taxonomy_id(id: str, callback=None, simple=None, response_format='json'):
    return get(f"taxonomy/id/{id}", params=dict(callback=callback, simple=simple), response_format=response_format)


def taxonomy_name(name: str, callback=None, response_format='json'):
    return get(f"taxonomy/name/{name}", params=dict(callback=callback), response_format=response_format)


def overlap_id(feature: str, id: str, biotype=None, callback=None, db_type=None, logic_name=None, misc_set=None,
               object_type=None, so_term=None, species=None, species_set=None, variant_set=None,
               response_format='json'):
    return get(f"overlap/id/{id}",
               params=dict(biotype=biotype, callback=callback, db_type=db_type, logic_name=logic_name,
                           misc_set=misc_set, object_type=object_type, so_term=so_term, species=species,
                           species_set=species_set, variant_set=variant_set), response_format=response_format)


def overlap_region(feature: str, region: str, species: str, biotype=None, callback=None, db_type=None, logic_name=None,
                   misc_set=None, so_term=None, species_set=None, trim_downstream=None, trim_upstream=None,
                   variant_set=None, response_format='json'):
    return get(f"overlap/region/{species}/{region}",
               params=dict(feature=feature, biotype=biotype, callback=callback, db_type=db_type, logic_name=logic_name,
                           misc_set=misc_set, so_term=so_term, species_set=species_set, trim_downstream=trim_downstream,
                           trim_upstream=trim_upstream, variant_set=variant_set), response_format=response_format)


def overlap_translation(id: str, callback=None, db_type=None, feature=None, so_term=None, species=None, type=None,
                        response_format='json'):
    return get(f"overlap/translation/{id}",
               params=dict(callback=callback, db_type=db_type, feature=feature, so_term=so_term, species=species,
                           type=type), response_format=response_format)


def phenotype_accession(accession: str, species: str, callback=None, include_children=None, include_pubmed_id=None,
                        include_review_status=None, source=None, response_format='json'):
    return get(f"/phenotype/accession/{species}/{accession}",
               params=dict(callback=callback, include_children=include_children, include_pubmed_id=include_pubmed_id,
                           include_review_status=include_review_status, source=source), response_format=response_format)


def phenotype_gene(gene: str, species: str, callback=None, include_associated=None, include_overlap=None,
                   include_pubmed_id=None, include_review_status=None, include_submitter=None, non_specified=None,
                   trait=None, tumour=None, response_format='json'):
    return get(f"/phenotype/gene/{species}/{gene}",
               params=dict(callback=callback, include_associated=include_associated, include_overlap=include_overlap,
                           include_pubmed_id=include_pubmed_id, include_review_status=include_review_status,
                           include_submitter=include_submitter, non_specified=non_specified, trait=trait,
                           tumour=tumour), response_format=response_format)


def phenotype_region(region: str, species: str, callback=None, feature_type=None, include_pubmed_id=None,
                     include_review_status=None, include_submitter=None, non_specified=None, only_phenotypes=None,
                     trait=None, tumour=None, response_format='json'):
    return get(f"/phenotype/region/{species}/{region}",
               params=dict(callback=callback, feature_type=feature_type, include_pubmed_id=include_pubmed_id,
                           include_review_status=include_review_status, include_submitter=include_submitter,
                           non_specified=non_specified, only_phenotypes=only_phenotypes, trait=trait, tumour=tumour),
               response_format=response_format)


def phenotype_term(species: str, term: str, callback=None, include_children=None, include_pubmed_id=None,
                   include_review_status=None, source=None, response_format='json'):
    return get(f"/phenotype/term/{species}/{term}",
               params=dict(callback=callback, include_children=include_children, include_pubmed_id=include_pubmed_id,
                           include_review_status=include_review_status, source=source), response_format=response_format)


def get_binding_matrix(binding_matrix: str, species: str, callback=None, unit=None, response_format='json'):
    return get(f"species/{species}/binding_matrix/{binding_matrix}/", params=dict(callback=callback, unit=unit),
               response_format=response_format)


@singledispatch
def sequence_id(id: str, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None, format=None,
                mask=None, mask_feature=None, multiple_sequences=None, object_type=None, species=None, start=None,
                type=None, response_format='json'):
    return get(f"sequence/id/{id}",
               params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                           expand_5prime=expand_5prime, format=format, mask=mask, mask_feature=mask_feature,
                           multiple_sequences=multiple_sequences, object_type=object_type, species=species, start=start,
                           type=type), response_format=response_format)


@sequence_id.register
def _(id: list, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None, format=None, mask=None,
      mask_feature=None, object_type=None, species=None, start=None, type=None, response_format='json'):
    return post(f"sequence/id", params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                                            expand_5prime=expand_5prime, format=format, mask=mask,
                                            mask_feature=mask_feature, object_type=object_type, species=species,
                                            start=start, type=type), response_format=response_format, json={'ids': id})


@singledispatch
def sequence_region(region: str, species: str, callback=None, coord_system=None, coord_system_version=None,
                    expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=None,
                    response_format='json'):
    return get(f"sequence/region/{species}/{region}",
               params=dict(callback=callback, coord_system=coord_system, coord_system_version=coord_system_version,
                           expand_3prime=expand_3prime, expand_5prime=expand_5prime, format=format, mask=mask,
                           mask_feature=mask_feature), response_format=response_format)


@sequence_region.register
def _(region: list, species: str, callback=None, coord_system=None, coord_system_version=None, expand_3prime=None,
      expand_5prime=None, format=None, mask=None, mask_feature=None, response_format='json'):
    return post(f"sequence/region/{species}",
                params=dict(callback=callback, coord_system=coord_system, coord_system_version=coord_system_version,
                            expand_3prime=expand_3prime, expand_5prime=expand_5prime, format=format, mask=mask,
                            mask_feature=mask_feature), response_format=response_format, json={'regions': region})


def transcript_haplotypes(id: str, species: str, aligned_sequences=None, callback=None, samples=None, sequence=None,
                          response_format='json'):
    return get(f"transcript_haplotypes/{species}/{id}",
               params=dict(aligned_sequences=aligned_sequences, callback=callback, samples=samples, sequence=sequence),
               response_format=response_format)


@singledispatch
def vep_hgvs(hgvs_notation: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
             ClinPred=None, Conservation=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
             GeneSplicer=None, Geno2MP=None, IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None, NMD=None,
             OpenTargets=None, Paralogues=None, Argument=None, clinsig=None, clnsig_match=None, fields=None,
             min_perc_cov=None, min_perc_pos=None, Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None,
             UTRAnnotator=None, ambiguous_hgvs=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None,
             dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
             flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, gencode_primary=None, hgvs=None, mane=None,
             merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None,
             pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None,
             shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
             variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
    return get(f"vep/{species}/hgvs/{hgvs_notation}",
               params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                           ClinPred=ClinPred, Conservation=Conservation, DosageSensitivity=DosageSensitivity, EVE=EVE,
                           Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                           LOEUF=LOEUF, LoF=LoF, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                           Paralogues=Paralogues, Argument=Argument, clinsig=clinsig, clnsig_match=clnsig_match,
                           fields=fields, min_perc_cov=min_perc_cov, min_perc_pos=min_perc_pos, Phenotypes=Phenotypes,
                           REVEL=REVEL, RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                           ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback, canonical=canonical,
                           ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed,
                           flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                           flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                           gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs, mane=mane,
                           merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                           per_gene=per_gene, pick=pick, pick_allele=pick_allele, pick_allele_gene=pick_allele_gene,
                           pick_order=pick_order, protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                           shift_genomic=shift_genomic, transcript_id=transcript_id,
                           transcript_version=transcript_version, tsl=tsl, uniprot=uniprot, variant_class=variant_class,
                           vcf_string=vcf_string, xref_refseq=xref_refseq), response_format=response_format)


@vep_hgvs.register
def _(hgvs_notation: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
      ClinPred=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
      IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None,
      Argument=None, clinsig=None, clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None,
      Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None, appris=None,
      callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None,
      flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None,
      gencode_primary=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None,
      per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None,
      shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
      variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
    return post(f"vep/{species}/hgvs",
                params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                            ClinPred=ClinPred, DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                            GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LOEUF=LOEUF, LoF=LoF,
                            MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                            Paralogues=Paralogues, Argument=Argument, clinsig=clinsig, clnsig_match=clnsig_match,
                            fields=fields, min_perc_cov=min_perc_cov, min_perc_pos=min_perc_pos, Phenotypes=Phenotypes,
                            REVEL=REVEL, RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                            ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback, canonical=canonical,
                            ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains,
                            failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                            flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                            gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs, mane=mane,
                            merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                            per_gene=per_gene, pick=pick, pick_allele=pick_allele, pick_allele_gene=pick_allele_gene,
                            pick_order=pick_order, protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                            shift_genomic=shift_genomic, transcript_id=transcript_id,
                            transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                            variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                response_format=response_format, json={"hgvs_notations": hgvs_notation})


@singledispatch
def vep_id(id: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None, ClinPred=None,
           Conservation=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
           IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None,
           Argument=None, clinsig=None, clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None,
           Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None,
           canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None,
           flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None,
           gencode_primary=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None,
           numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None,
           protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
           transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
           response_format='json'):
    return get(f"vep/{species}/id/{id}",
               params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                           ClinPred=ClinPred, Conservation=Conservation, DosageSensitivity=DosageSensitivity, EVE=EVE,
                           Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                           LOEUF=LOEUF, LoF=LoF, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                           Paralogues=Paralogues, Argument=Argument, clinsig=clinsig, clnsig_match=clnsig_match,
                           fields=fields, min_perc_cov=min_perc_cov, min_perc_pos=min_perc_pos, Phenotypes=Phenotypes,
                           REVEL=REVEL, RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                           appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                           dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                           flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                           ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs,
                           mane=mane, merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                           per_gene=per_gene, pick=pick, pick_allele=pick_allele, pick_allele_gene=pick_allele_gene,
                           pick_order=pick_order, protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                           shift_genomic=shift_genomic, transcript_id=transcript_id,
                           transcript_version=transcript_version, tsl=tsl, uniprot=uniprot, variant_class=variant_class,
                           vcf_string=vcf_string, xref_refseq=xref_refseq), response_format=response_format)


@vep_id.register
def _(id: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None, ClinPred=None,
      DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LOEUF=None,
      LoF=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None, Argument=None, clinsig=None,
      clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None, Phenotypes=None, REVEL=None,
      RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None,
      dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
      flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, gencode_primary=None, hgvs=None, mane=None,
      merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
      pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
      transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
      xref_refseq=None, response_format='json'):
    return post(f"vep/{species}/id",
                params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                            ClinPred=ClinPred, DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                            GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LOEUF=LOEUF, LoF=LoF,
                            MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                            Paralogues=Paralogues, Argument=Argument, clinsig=clinsig, clnsig_match=clnsig_match,
                            fields=fields, min_perc_cov=min_perc_cov, min_perc_pos=min_perc_pos, Phenotypes=Phenotypes,
                            REVEL=REVEL, RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                            appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                            dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                            flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                            ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, gencode_primary=gencode_primary,
                            hgvs=hgvs, mane=mane, merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc,
                            numbers=numbers, per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                            pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein, refseq=refseq,
                            shift_3prime=shift_3prime, shift_genomic=shift_genomic, transcript_id=transcript_id,
                            transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                            variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                response_format=response_format, json={"ids": id})


@singledispatch
def vep_region(region: str, allele: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None,
               CADD=None, ClinPred=None, Conservation=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
               GeneSplicer=None, Geno2MP=None, IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None,
               NMD=None, OpenTargets=None, Paralogues=None, Argument=None, clinsig=None, clnsig_match=None, fields=None,
               min_perc_cov=None, min_perc_pos=None, Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None,
               UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
               distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
               flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, gencode_primary=None, hgvs=None,
               mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None,
               pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None,
               shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
               variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
    return get(f"vep/{species}/region/{region}/{allele}/",
               params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                           ClinPred=ClinPred, Conservation=Conservation, DosageSensitivity=DosageSensitivity, EVE=EVE,
                           Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                           LOEUF=LOEUF, LoF=LoF, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                           Paralogues=Paralogues, Argument=Argument, clinsig=clinsig, clnsig_match=clnsig_match,
                           fields=fields, min_perc_cov=min_perc_cov, min_perc_pos=min_perc_pos, Phenotypes=Phenotypes,
                           REVEL=REVEL, RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                           appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                           dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                           flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                           ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs,
                           mane=mane, merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                           per_gene=per_gene, pick=pick, pick_allele=pick_allele, pick_allele_gene=pick_allele_gene,
                           pick_order=pick_order, protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                           shift_genomic=shift_genomic, transcript_id=transcript_id,
                           transcript_version=transcript_version, tsl=tsl, uniprot=uniprot, variant_class=variant_class,
                           vcf_string=vcf_string, xref_refseq=xref_refseq), response_format=response_format)


@vep_region.register
def _(variants: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None, ClinPred=None,
      DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LOEUF=None,
      LoF=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None, Argument=None, clinsig=None,
      clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None, Phenotypes=None, REVEL=None,
      RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None,
      dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
      flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, gencode_primary=None, hgvs=None, mane=None,
      merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
      pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
      transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
      xref_refseq=None, response_format='json'):
    return post(f"vep/{species}/region",
                params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                            ClinPred=ClinPred, DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                            GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LOEUF=LOEUF, LoF=LoF,
                            MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                            Paralogues=Paralogues, Argument=Argument, clinsig=clinsig, clnsig_match=clnsig_match,
                            fields=fields, min_perc_cov=min_perc_cov, min_perc_pos=min_perc_pos, Phenotypes=Phenotypes,
                            REVEL=REVEL, RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                            appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                            dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                            flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                            ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, gencode_primary=gencode_primary,
                            hgvs=hgvs, mane=mane, merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc,
                            numbers=numbers, per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                            pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein, refseq=refseq,
                            shift_3prime=shift_3prime, shift_genomic=shift_genomic, transcript_id=transcript_id,
                            transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                            variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq),
                response_format=response_format, json={"variants": variants})


@singledispatch
def variant_recoder(id: str, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None,
                    gencode_primary=None, minimal=None, var_synonyms=None, vcf_string=None, response_format='json'):
    return get(f"variant_recoder/{species}/{id}",
               params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                           gencode_basic=gencode_basic, gencode_primary=gencode_primary, minimal=minimal,
                           var_synonyms=var_synonyms, vcf_string=vcf_string), response_format=response_format)


@variant_recoder.register
def _(id: list, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None,
      gencode_primary=None, minimal=None, var_synonyms=None, vcf_string=None, response_format='json'):
    return post(f"variant_recoder/{species}",
                params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                            gencode_basic=gencode_basic, gencode_primary=gencode_primary, minimal=minimal,
                            var_synonyms=var_synonyms, vcf_string=vcf_string), response_format=response_format,
                json={"ids": id})


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


def beacon_get(callback=None, response_format='json'):
    return get(f"ga4gh/beacon", params=dict(callback=callback), response_format=response_format)


def beacon_query_get(alternateBases: str, assemblyId: str, end: str, referenceBases: str, referenceName: str,
                     start: str, variantType: str, callback=None, datasetIds=None, includeResultsetResponses=None,
                     response_format='json'):
    return get(f"ga4gh/beacon/query", params=dict(callback=callback, datasetIds=datasetIds,
                                                  includeResultsetResponses=includeResultsetResponses),
               response_format=response_format)


def beacon_query_post(alternateBases: str, assemblyId: str, end: str, referenceBases: str, referenceName: str,
                      start: str, variantType: str, callback=None, datasetIds=None, includeResultsetResponses=None,
                      response_format='json'):
    return post(f"ga4gh/beacon/query", params=dict(callback=callback, datasetIds=datasetIds,
                                                   includeResultsetResponses=includeResultsetResponses),
                response_format=response_format)


def features_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/features/{id}", params=dict(callback=callback), response_format=response_format)


def features_post(end: str, referenceName: str, start: str, callback=None, featureTypes=None, featuresetId=None,
                  pageSize=None, pageToken=None, parentId=None, response_format='json'):
    return post(f"ga4gh/features/search",
                params=dict(callback=callback, featureTypes=featureTypes, featuresetId=featuresetId, pageSize=pageSize,
                            pageToken=pageToken, parentId=parentId), response_format=response_format)


def gacallSet(variantSetId: str, callback=None, name=None, pageSize=None, pageToken=None, response_format='json'):
    return post(f"ga4gh/callsets/search",
                params=dict(callback=callback, name=name, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format)


def gacallset_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/callsets/{id}", params=dict(callback=callback), response_format=response_format)


def gadataset(callback=None, pageSize=None, pageToken=None, response_format='json'):
    return post(f"ga4gh/datasets/search", params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format)


def gadataset_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/datasets/{id}", params=dict(callback=callback), response_format=response_format)


def gafeatureset(datasetId: str, callback=None, pageSize=None, pageToken=None, response_format='json'):
    return post(f"ga4gh/featuresets/search", params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format)


def gafeatureset_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/featuresets/{id}", params=dict(callback=callback), response_format=response_format)


def gavariant_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/variants/{id}", params=dict(callback=callback), response_format=response_format)


def gavariantannotations(variantAnnotationSetId: str, callback=None, effects=None, end=None, pageSize=None,
                         pageToken=None, referenceId=None, referenceName=None, start=None, response_format='json'):
    return post(f"ga4gh/variantannotations/search",
                params=dict(callback=callback, effects=effects, end=end, pageSize=pageSize, pageToken=pageToken,
                            referenceId=referenceId, referenceName=referenceName, start=start),
                response_format=response_format)


def gavariants(end: str, referenceName: str, start: str, variantSetId: str, callSetIds=None, callback=None,
               pageSize=None, pageToken=None, response_format='json'):
    return post(f"ga4gh/variants/search",
                params=dict(callSetIds=callSetIds, callback=callback, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format)


def gavariantset(datasetId: str, callback=None, pageSize=None, pageToken=None, response_format='json'):
    return post(f"ga4gh/variantsets/search", params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format)


def gavariantset_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/variantsets/{id}", params=dict(callback=callback), response_format=response_format)


def references(referenceSetId: str, accession=None, callback=None, md5checksum=None, pageSize=None, pageToken=None,
               response_format='json'):
    return post(f"ga4gh/references/search",
                params=dict(accession=accession, callback=callback, md5checksum=md5checksum, pageSize=pageSize,
                            pageToken=pageToken), response_format=response_format)


def references_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/references/{id}", params=dict(callback=callback), response_format=response_format)


def referenceSets(accession=None, callback=None, pageSize=None, pageToken=None, response_format='json'):
    return post(f"ga4gh/referencesets/search",
                params=dict(accession=accession, callback=callback, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format)


def referenceSets_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/referencesets/{id}", params=dict(callback=callback), response_format=response_format)


def VariantAnnotationSet(variantSetId: str, callback=None, pageSize=None, pageToken=None, response_format='json'):
    return post(f"ga4gh/variantannotationsets/search",
                params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken), response_format=response_format)


def VariantAnnotationSet_id(id: str, callback=None, response_format='json'):
    return get(f"ga4gh/variantannotationsets/{id}", params=dict(callback=callback), response_format=response_format)


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
                              allowed_methods=["GET", "POST"], backoff_jitter=0.1))
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
            return response.raise_for_status()

    def post(self, endpoint, params, json, response_format):
        headers = {"Content-Type": media_type[response_format], "Accept": media_type[response_format]}
        response = self.session.post(urljoin(self.server, endpoint), headers=headers, params=params, json=json)
        if response.ok:
            if headers["Content-Type"] == "application/json":
                return response.json()
            else:
                return response.text
        else:
            return response.raise_for_status()

    @singledispatchmethod
    def archive(self, id: str, callback=None, response_format='json'):
        return self.get(f"archive/id/{id}", params=dict(callback=callback), response_format=response_format)

    @archive.register
    def _(self, id: list, callback=None, response_format='json'):
        return self.post(f"archive/id", params=dict(callback=callback), response_format=response_format,
                         json={"ids": id})

    def cafe_tree(self, id: str, callback=None, compara=None, nh_format=None, response_format='json'):
        return self.get(f"cafe/genetree/id/{id}", params=dict(callback=callback, compara=compara, nh_format=nh_format),
                        response_format=response_format)

    def cafe_tree_member_symbol(self, species: str, symbol: str, callback=None, compara=None, db_type=None,
                                external_db=None, nh_format=None, object_type=None, response_format='json'):
        return self.get(f"cafe/genetree/member/symbol/{species}/{symbol}",
                        params=dict(callback=callback, compara=compara, db_type=db_type, external_db=external_db,
                                    nh_format=nh_format, object_type=object_type), response_format=response_format)

    def cafe_tree_species_member_id(self, id: str, species: str, callback=None, compara=None, db_type=None,
                                    nh_format=None, object_type=None, response_format='json'):
        return self.get(f"cafe/genetree/member/id/{species}/{id}",
                        params=dict(callback=callback, compara=compara, db_type=db_type, nh_format=nh_format,
                                    object_type=object_type), response_format=response_format)

    def genetree(self, id: str, aligned=None, callback=None, cigar_line=None, clusterset_id=None, compara=None,
                 nh_format=None, prune_species=None, prune_taxon=None, sequence=None, response_format='json'):
        return self.get(f"genetree/id/{id}", params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line,
                                                         clusterset_id=clusterset_id, compara=compara,
                                                         nh_format=nh_format, prune_species=prune_species,
                                                         prune_taxon=prune_taxon, sequence=sequence),
                        response_format=response_format)

    def genetree_member_symbol(self, species: str, symbol: str, aligned=None, callback=None, cigar_line=None,
                               clusterset_id=None, compara=None, db_type=None, external_db=None, nh_format=None,
                               object_type=None, prune_species=None, prune_taxon=None, sequence=None,
                               response_format='json'):
        return self.get(f"genetree/member/symbol/{species}/{symbol}",
                        params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line,
                                    clusterset_id=clusterset_id, compara=compara, db_type=db_type,
                                    external_db=external_db, nh_format=nh_format, object_type=object_type,
                                    prune_species=prune_species, prune_taxon=prune_taxon, sequence=sequence),
                        response_format=response_format)

    def genetree_species_member_id(self, id: str, species: str, aligned=None, callback=None, cigar_line=None,
                                   clusterset_id=None, compara=None, db_type=None, nh_format=None, object_type=None,
                                   prune_species=None, prune_taxon=None, sequence=None, response_format='json'):
        return self.get(f"genetree/member/id/{species}/{id}",
                        params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line,
                                    clusterset_id=clusterset_id, compara=compara, db_type=db_type, nh_format=nh_format,
                                    object_type=object_type, prune_species=prune_species, prune_taxon=prune_taxon,
                                    sequence=sequence), response_format=response_format)

    def genomic_alignment_region(self, region: str, species: str, aligned=None, callback=None, compact=None,
                                 compara=None, display_species_set=None, mask=None, method=None, species_set=None,
                                 species_set_group=None, response_format='json'):
        return self.get(f"alignment/region/{species}/{region}",
                        params=dict(aligned=aligned, callback=callback, compact=compact, compara=compara,
                                    display_species_set=display_species_set, mask=mask, method=method,
                                    species_set=species_set, species_set_group=species_set_group),
                        response_format=response_format)

    def homology_species_gene_id(self, id: str, species: str, aligned=None, callback=None, cigar_line=None,
                                 compara=None, format=None, sequence=None, target_species=None, target_taxon=None,
                                 type=None, response_format='json'):
        return self.get(f"homology/id/{species}/{id}",
                        params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, compara=compara,
                                    format=format, sequence=sequence, target_species=target_species,
                                    target_taxon=target_taxon, type=type), response_format=response_format)

    def homology_symbol(self, species: str, symbol: str, aligned=None, callback=None, cigar_line=None, compara=None,
                        external_db=None, format=None, sequence=None, target_species=None, target_taxon=None, type=None,
                        response_format='json'):
        return self.get(f"homology/symbol/{species}/{symbol}",
                        params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, compara=compara,
                                    external_db=external_db, format=format, sequence=sequence,
                                    target_species=target_species, target_taxon=target_taxon, type=type),
                        response_format=response_format)

    def xref_external(self, species: str, symbol: str, callback=None, db_type=None, external_db=None, object_type=None,
                      response_format='json'):
        return self.get(f"xrefs/symbol/{species}/{symbol}",
                        params=dict(callback=callback, db_type=db_type, external_db=external_db,
                                    object_type=object_type), response_format=response_format)

    def xref_id(self, id: str, all_levels=None, callback=None, db_type=None, external_db=None, object_type=None,
                species=None, response_format='json'):
        return self.get(f"xrefs/id/{id}",
                        params=dict(all_levels=all_levels, callback=callback, db_type=db_type, external_db=external_db,
                                    object_type=object_type, species=species), response_format=response_format)

    def xref_name(self, name: str, species: str, callback=None, db_type=None, external_db=None, response_format='json'):
        return self.get(f"xrefs/name/{species}/{name}",
                        params=dict(callback=callback, db_type=db_type, external_db=external_db),
                        response_format=response_format)

    def analysis(self, species: str, callback=None, response_format='json'):
        return self.get(f"info/analysis/{species}", params=dict(callback=callback), response_format=response_format)

    def assembly_info(self, species: str, bands=None, callback=None, synonyms=None, response_format='json'):
        return self.get(f"info/assembly/{species}", params=dict(bands=bands, callback=callback, synonyms=synonyms),
                        response_format=response_format)

    def assembly_stats(self, region_name: str, species: str, bands=None, callback=None, synonyms=None,
                       response_format='json'):
        return self.get(f"info/assembly/{species}/{region_name}",
                        params=dict(bands=bands, callback=callback, synonyms=synonyms), response_format=response_format)

    def biotypes(self, species: str, callback=None, response_format='json'):
        return self.get(f"info/biotypes/{species}", params=dict(callback=callback), response_format=response_format)

    def biotypes_groups(self, callback=None, group=None, object_type=None, response_format='json'):
        return self.get(f"info/biotypes/groups/{group}/{object_type}",
                        params=dict(callback=callback, group=group, object_type=object_type),
                        response_format=response_format)

    def biotypes_name(self, name: str, callback=None, object_type=None, response_format='json'):
        return self.get(f"info/biotypes/name/{name}/{object_type}",
                        params=dict(callback=callback, object_type=object_type), response_format=response_format)

    def compara_methods(self, callback=None, compara=None, response_format='json', **kwargs):

        return self.get(f"info/compara/methods", params=dict(kwargs, callback=callback, compara=compara),
                        response_format=response_format)

    def compara_species_sets(self, method: str, callback=None, compara=None, response_format='json'):
        return self.get(f"info/compara/species_sets/{method}", params=dict(callback=callback, compara=compara),
                        response_format=response_format)

    def comparas(self, callback=None, response_format='json'):
        return self.get(f"info/comparas", params=dict(callback=callback), response_format=response_format)

    def data(self, callback=None, response_format='json'):
        return self.get(f"info/data", params=dict(callback=callback), response_format=response_format)

    def eg_version(self, callback=None, response_format='json'):
        return self.get(f"info/eg_version", params=dict(callback=callback), response_format=response_format)

    def external_dbs(self, species: str, callback=None, feature=None, filter=None, response_format='json'):
        return self.get(f"info/external_dbs/{species}", params=dict(callback=callback, feature=feature, filter=filter),
                        response_format=response_format)

    def info_divisions(self, callback=None, response_format='json'):
        return self.get(f"info/divisions", params=dict(callback=callback), response_format=response_format)

    def info_genome(self, name: str, callback=None, expand=None, response_format='json'):
        return self.get(f"info/genomes/{name}", params=dict(callback=callback, expand=expand),
                        response_format=response_format)

    def info_genomes_accession(self, accession: str, callback=None, expand=None, response_format='json'):
        return self.get(f"info/genomes/accession/{accession}", params=dict(callback=callback, expand=expand),
                        response_format=response_format)

    def info_genomes_assembly(self, assembly_id: str, callback=None, expand=None, response_format='json'):
        return self.get(f"info/genomes/assembly/{assembly_id}", params=dict(callback=callback, expand=expand),
                        response_format=response_format)

    def info_genomes_division(self, division: str, callback=None, expand=None, response_format='json'):
        return self.get(f"info/genomes/division/{division}", params=dict(callback=callback, expand=expand),
                        response_format=response_format)

    def info_genomes_taxonomy(self, taxon_name: str, callback=None, expand=None, response_format='json'):
        return self.get(f"info/genomes/taxonomy/{taxon_name}", params=dict(callback=callback, expand=expand),
                        response_format=response_format)

    def ping(self, callback=None, response_format='json'):
        return self.get(f"info/ping", params=dict(callback=callback), response_format=response_format)

    def rest(self, callback=None, response_format='json'):
        return self.get(f"info/rest", params=dict(callback=callback), response_format=response_format)

    def software(self, callback=None, response_format='json'):
        return self.get(f"info/software", params=dict(callback=callback), response_format=response_format)

    def species(self, callback=None, division=None, hide_strain_info=None, strain_collection=None,
                response_format='json'):
        return self.get(f"info/species",
                        params=dict(callback=callback, division=division, hide_strain_info=hide_strain_info,
                                    strain_collection=strain_collection), response_format=response_format)

    def variation(self, species: str, callback=None, filter=None, response_format='json'):
        return self.get(f"info/variation/{species}", params=dict(callback=callback, filter=filter),
                        response_format=response_format)

    def variation_consequence_types(self, callback=None, rank=None, response_format='json'):
        return self.get(f"info/variation/consequence_types", params=dict(callback=callback, rank=rank),
                        response_format=response_format)

    def variation_population_name(self, population_name: str, species: str, callback=None, response_format='json'):
        return self.get(f"info/variation/populations/{species}:/{population_name}", params=dict(callback=callback),
                        response_format=response_format)

    def variation_populations(self, species: str, callback=None, filter=None, response_format='json'):
        return self.get(f"info/variation/populations/{species}", params=dict(callback=callback, filter=filter),
                        response_format=response_format)

    def ld_id_get(self, id: str, population_name: str, species: str, attribs=None, callback=None, d_prime=None, r2=None,
                  window_size=None, response_format='json'):
        return self.get(f"ld/{species}/{id}/{population_name}",
                        params=dict(attribs=attribs, callback=callback, d_prime=d_prime, r2=r2,
                                    window_size=window_size), response_format=response_format)

    def ld_pairwise_get(self, id1: str, id2: str, species: str, callback=None, d_prime=None, population_name=None,
                        r2=None, response_format='json'):
        return self.get(f"ld/{species}/pairwise/{id1}/{id2}",
                        params=dict(callback=callback, d_prime=d_prime, population_name=population_name, r2=r2),
                        response_format=response_format)

    def ld_region_get(self, population_name: str, region: str, species: str, callback=None, d_prime=None, r2=None,
                      response_format='json'):
        return self.get(f"ld/{species}/region/{region}/{population_name}",
                        params=dict(callback=callback, d_prime=d_prime, r2=r2), response_format=response_format)

    @singledispatchmethod
    def lookup(self, id: str, callback=None, db_type=None, expand=None, format=None, mane=None, phenotypes=None,
               species=None, utr=None, response_format='json'):
        return self.get(f"lookup/id/{id}",
                        params=dict(callback=callback, db_type=db_type, expand=expand, format=format, mane=mane,
                                    phenotypes=phenotypes, species=species, utr=utr), response_format=response_format)

    @lookup.register
    def _(self, id: list, callback=None, db_type=None, expand=None, format=None, object_type=None, species=None,
          response_format='json'):
        return self.post(f"lookup/id", params=dict(callback=callback, db_type=db_type, expand=expand, format=format,
                                                   object_type=object_type, species=species),
                         response_format=response_format, json={"ids": id})

    @singledispatchmethod
    def symbol_lookup(self, species: str, symbol: str, callback=None, expand=None, format=None, response_format='json'):
        return self.get(f"lookup/symbol/{species}/{symbol}",
                        params=dict(callback=callback, expand=expand, format=format), response_format=response_format)

    @symbol_lookup.register
    def _(self, symbol: list, species: str, callback=None, expand=None, format=None, response_format='json'):
        return self.post(f"lookup/symbol/{species}", params=dict(callback=callback, expand=expand, format=format),
                         response_format=response_format, json={"symbols": symbol})

    def assembly_cdna(self, id: str, region: str, callback=None, include_original_region=None, species=None,
                      response_format='json'):
        return self.get(f"map/cdna/{id}/{region}",
                        params=dict(callback=callback, include_original_region=include_original_region,
                                    species=species), response_format=response_format)

    def assembly_cds(self, id: str, region: str, callback=None, include_original_region=None, species=None,
                     response_format='json'):
        return self.get(f"map/cds/{id}/{region}",
                        params=dict(callback=callback, include_original_region=include_original_region,
                                    species=species), response_format=response_format)

    def assembly_map(self, asm_one: str, asm_two: str, region: str, species: str, callback=None, coord_system=None,
                     target_coord_system=None, response_format='json'):
        return self.get(f"map/{species}/{asm_one}/{region}/{asm_two}",
                        params=dict(callback=callback, coord_system=coord_system,
                                    target_coord_system=target_coord_system), response_format=response_format)

    def assembly_translation(self, id: str, region: str, callback=None, species=None, response_format='json'):
        return self.get(f"map/translation/{id}/{region}", params=dict(callback=callback, species=species),
                        response_format=response_format)

    def ontology_ancestors(self, id: str, callback=None, ontology=None, response_format='json'):
        return self.get(f"ontology/ancestors/{id}", params=dict(callback=callback, ontology=ontology),
                        response_format=response_format)

    def ontology_ancestors_chart(self, id: str, callback=None, ontology=None, response_format='json'):
        return self.get(f"ontology/ancestors/chart/{id}", params=dict(callback=callback, ontology=ontology),
                        response_format=response_format)

    def ontology_descendants(self, id: str, callback=None, closest_term=None, ontology=None, subset=None,
                             zero_distance=None, response_format='json'):
        return self.get(f"ontology/descendants/{id}",
                        params=dict(callback=callback, closest_term=closest_term, ontology=ontology, subset=subset,
                                    zero_distance=zero_distance), response_format=response_format)

    def ontology_id(self, id: str, callback=None, relation=None, simple=None, response_format='json'):
        return self.get(f"ontology/id/{id}", params=dict(callback=callback, relation=relation, simple=simple),
                        response_format=response_format)

    def ontology_name(self, name: str, callback=None, ontology=None, relation=None, simple=None,
                      response_format='json'):
        return self.get(f"ontology/name/{name}",
                        params=dict(callback=callback, ontology=ontology, relation=relation, simple=simple),
                        response_format=response_format)

    def taxonomy_classification(self, id: str, callback=None, response_format='json'):
        return self.get(f"taxonomy/classification/{id}", params=dict(callback=callback),
                        response_format=response_format)

    def taxonomy_id(self, id: str, callback=None, simple=None, response_format='json'):
        return self.get(f"taxonomy/id/{id}", params=dict(callback=callback, simple=simple),
                        response_format=response_format)

    def taxonomy_name(self, name: str, callback=None, response_format='json'):
        return self.get(f"taxonomy/name/{name}", params=dict(callback=callback), response_format=response_format)

    def overlap_id(self, feature: str, id: str, biotype=None, callback=None, db_type=None, logic_name=None,
                   misc_set=None, object_type=None, so_term=None, species=None, species_set=None, variant_set=None,
                   response_format='json'):
        return self.get(f"overlap/id/{id}",
                        params=dict(biotype=biotype, callback=callback, db_type=db_type, logic_name=logic_name,
                                    misc_set=misc_set, object_type=object_type, so_term=so_term, species=species,
                                    species_set=species_set, variant_set=variant_set), response_format=response_format)

    def overlap_region(self, feature: str, region: str, species: str, biotype=None, callback=None, db_type=None,
                       logic_name=None, misc_set=None, so_term=None, species_set=None, trim_downstream=None,
                       trim_upstream=None, variant_set=None, response_format='json'):
        return self.get(f"overlap/region/{species}/{region}",
                        params=dict(biotype=biotype, callback=callback, db_type=db_type, logic_name=logic_name,
                                    misc_set=misc_set, so_term=so_term, species_set=species_set,
                                    trim_downstream=trim_downstream, trim_upstream=trim_upstream,
                                    variant_set=variant_set), response_format=response_format)

    def overlap_translation(self, id: str, callback=None, db_type=None, feature=None, so_term=None, species=None,
                            type=None, response_format='json'):
        return self.get(f"overlap/translation/{id}",
                        params=dict(callback=callback, db_type=db_type, feature=feature, so_term=so_term,
                                    species=species, type=type), response_format=response_format)

    def phenotype_accession(self, accession: str, species: str, callback=None, include_children=None,
                            include_pubmed_id=None, include_review_status=None, source=None, response_format='json'):
        return self.get(f"/phenotype/accession/{species}/{accession}",
                        params=dict(callback=callback, include_children=include_children,
                                    include_pubmed_id=include_pubmed_id, include_review_status=include_review_status,
                                    source=source), response_format=response_format)

    def phenotype_gene(self, gene: str, species: str, callback=None, include_associated=None, include_overlap=None,
                       include_pubmed_id=None, include_review_status=None, include_submitter=None, non_specified=None,
                       trait=None, tumour=None, response_format='json'):
        return self.get(f"/phenotype/gene/{species}/{gene}",
                        params=dict(callback=callback, include_associated=include_associated,
                                    include_overlap=include_overlap, include_pubmed_id=include_pubmed_id,
                                    include_review_status=include_review_status, include_submitter=include_submitter,
                                    non_specified=non_specified, trait=trait, tumour=tumour),
                        response_format=response_format)

    def phenotype_region(self, region: str, species: str, callback=None, feature_type=None, include_pubmed_id=None,
                         include_review_status=None, include_submitter=None, non_specified=None, only_phenotypes=None,
                         trait=None, tumour=None, response_format='json'):
        return self.get(f"/phenotype/region/{species}/{region}",
                        params=dict(callback=callback, feature_type=feature_type, include_pubmed_id=include_pubmed_id,
                                    include_review_status=include_review_status, include_submitter=include_submitter,
                                    non_specified=non_specified, only_phenotypes=only_phenotypes, trait=trait,
                                    tumour=tumour), response_format=response_format)

    def phenotype_term(self, species: str, term: str, callback=None, include_children=None, include_pubmed_id=None,
                       include_review_status=None, source=None, response_format='json'):
        return self.get(f"/phenotype/term/{species}/{term}",
                        params=dict(callback=callback, include_children=include_children,
                                    include_pubmed_id=include_pubmed_id, include_review_status=include_review_status,
                                    source=source), response_format=response_format)

    def get_binding_matrix(self, binding_matrix: str, species: str, callback=None, unit=None, response_format='json'):
        return self.get(f"species/{species}/binding_matrix/{binding_matrix}/",
                        params=dict(callback=callback, unit=unit), response_format=response_format)

    @singledispatchmethod
    def sequence_id(self, id: str, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None,
                    format=None, mask=None, mask_feature=None, multiple_sequences=None, object_type=None, species=None,
                    start=None, type=None, response_format='json'):
        return self.get(f"sequence/id/{id}",
                        params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                                    expand_5prime=expand_5prime, format=format, mask=mask, mask_feature=mask_feature,
                                    multiple_sequences=multiple_sequences, object_type=object_type, species=species,
                                    start=start, type=type), response_format=response_format)

    @sequence_id.register
    def _(self, id: list, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None, format=None,
          mask=None, mask_feature=None, object_type=None, species=None, start=None, type=None, response_format='json'):
        return self.post(f"sequence/id",
                         params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                                     expand_5prime=expand_5prime, format=format, mask=mask, mask_feature=mask_feature,
                                     object_type=object_type, species=species, start=start, type=type),
                         response_format=response_format, json={"ids": id})

    @singledispatchmethod
    def sequence_region(self, region: str, species: str, callback=None, coord_system=None, coord_system_version=None,
                        expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=None,
                        response_format='json'):
        return self.get(f"sequence/region/{species}/{region}", params=dict(callback=callback, coord_system=coord_system,
                                                                           coord_system_version=coord_system_version,
                                                                           expand_3prime=expand_3prime,
                                                                           expand_5prime=expand_5prime, format=format,
                                                                           mask=mask, mask_feature=mask_feature),
                        response_format=response_format)

    @sequence_region.register
    def _(self, region: list, species: str, callback=None, coord_system=None, coord_system_version=None,
          expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=None, response_format='json'):
        return self.post(f"sequence/region/{species}", params=dict(callback=callback, coord_system=coord_system,
                                                                   coord_system_version=coord_system_version,
                                                                   expand_3prime=expand_3prime,
                                                                   expand_5prime=expand_5prime, format=format,
                                                                   mask=mask, mask_feature=mask_feature),
                         response_format=response_format, json={"regions": region})

    def transcript_haplotypes(self, id: str, species: str, aligned_sequences=None, callback=None, samples=None,
                              sequence=None, response_format='json'):
        return self.get(f"transcript_haplotypes/{species}/{id}",
                        params=dict(aligned_sequences=aligned_sequences, callback=callback, samples=samples,
                                    sequence=sequence), response_format=response_format)

    @singledispatchmethod
    def vep_hgvs(self, hgvs_notation: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None,
                 CADD=None, ClinPred=None, Conservation=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
                 GeneSplicer=None, Geno2MP=None, IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None,
                 NMD=None, OpenTargets=None, Paralogues=None, Argument=None, clinsig=None, clnsig_match=None,
                 fields=None, min_perc_cov=None, min_perc_pos=None, Phenotypes=None, REVEL=None, RiboseqORFs=None,
                 SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None, appris=None, callback=None, canonical=None,
                 ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None,
                 flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None,
                 gencode_primary=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None,
                 numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None,
                 protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
                 transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
                 response_format='json'):
        return self.get(f"vep/{species}/hgvs/{hgvs_notation}",
                        params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                    CADD=CADD, ClinPred=ClinPred, Conservation=Conservation,
                                    DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LOEUF=LOEUF, LoF=LoF,
                                    MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                                    Paralogues=Paralogues, Argument=Argument, clinsig=clinsig,
                                    clnsig_match=clnsig_match, fields=fields, min_perc_cov=min_perc_cov,
                                    min_perc_pos=min_perc_pos, Phenotypes=Phenotypes, REVEL=REVEL,
                                    RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                    ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback,
                                    canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance,
                                    domains=domains, failed=failed, flag_pick=flag_pick,
                                    flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                    ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, gencode_primary=gencode_primary,
                                    hgvs=hgvs, mane=mane, merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc,
                                    numbers=numbers, per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                    pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                    refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                    transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                    uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                    xref_refseq=xref_refseq), response_format=response_format)

    @vep_hgvs.register
    def _(self, hgvs_notation: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
          ClinPred=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
          IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None,
          Argument=None, clinsig=None, clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None,
          Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None,
          appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None,
          failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None,
          gencode_basic=None, gencode_primary=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None,
          mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None,
          pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
          transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
          response_format='json'):
        return self.post(f"vep/{species}/hgvs",
                         params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                     CADD=CADD, ClinPred=ClinPred, DosageSensitivity=DosageSensitivity, EVE=EVE,
                                     Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                                     LOEUF=LOEUF, LoF=LoF, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     OpenTargets=OpenTargets, Paralogues=Paralogues, Argument=Argument, clinsig=clinsig,
                                     clnsig_match=clnsig_match, fields=fields, min_perc_cov=min_perc_cov,
                                     min_perc_pos=min_perc_pos, Phenotypes=Phenotypes, REVEL=REVEL,
                                     RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                     ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback,
                                     canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance,
                                     domains=domains, failed=failed, flag_pick=flag_pick,
                                     flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                     ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, gencode_primary=gencode_primary,
                                     hgvs=hgvs, mane=mane, merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc,
                                     numbers=numbers, per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                     pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                     refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                     transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                     uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                     xref_refseq=xref_refseq), response_format=response_format,
                         json={"hgvs_notations": hgvs_notation})

    @singledispatchmethod
    def vep_id(self, id: str, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
               ClinPred=None, Conservation=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None,
               GeneSplicer=None, Geno2MP=None, IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None,
               NMD=None, OpenTargets=None, Paralogues=None, Argument=None, clinsig=None, clnsig_match=None, fields=None,
               min_perc_cov=None, min_perc_pos=None, Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None,
               UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
               distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
               flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, gencode_primary=None, hgvs=None,
               mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None,
               pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None,
               shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
               variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
        return self.get(f"vep/{species}/id/{id}",
                        params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                    CADD=CADD, ClinPred=ClinPred, Conservation=Conservation,
                                    DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LOEUF=LOEUF, LoF=LoF,
                                    MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                                    Paralogues=Paralogues, Argument=Argument, clinsig=clinsig,
                                    clnsig_match=clnsig_match, fields=fields, min_perc_cov=min_perc_cov,
                                    min_perc_pos=min_perc_pos, Phenotypes=Phenotypes, REVEL=REVEL,
                                    RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                    appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                                    dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed,
                                    flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                    flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                    gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs, mane=mane,
                                    merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                    per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                    pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                    refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                    transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                    uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                    xref_refseq=xref_refseq), response_format=response_format)

    @vep_id.register
    def _(self, id: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
          ClinPred=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
          IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None,
          Argument=None, clinsig=None, clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None,
          Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None,
          canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None,
          flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None,
          gencode_primary=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None,
          per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None,
          shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
          variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
        return self.post(f"vep/{species}/id",
                         params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                     CADD=CADD, ClinPred=ClinPred, DosageSensitivity=DosageSensitivity, EVE=EVE,
                                     Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                                     LOEUF=LOEUF, LoF=LoF, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     OpenTargets=OpenTargets, Paralogues=Paralogues, Argument=Argument, clinsig=clinsig,
                                     clnsig_match=clnsig_match, fields=fields, min_perc_cov=min_perc_cov,
                                     min_perc_pos=min_perc_pos, Phenotypes=Phenotypes, REVEL=REVEL,
                                     RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                     appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                                     dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed,
                                     flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                     flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                     gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs, mane=mane,
                                     merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                     per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                     pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                     refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                     transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                     uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                     xref_refseq=xref_refseq), response_format=response_format, json={"ids": id})

    @singledispatchmethod
    def vep_region(self, region: str, allele: str, species: str, AlphaMissense=None, AncestralAllele=None,
                   Blosum62=None, CADD=None, ClinPred=None, Conservation=None, DosageSensitivity=None, EVE=None,
                   Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LOEUF=None, LoF=None,
                   MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None, Argument=None,
                   clinsig=None, clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None, Phenotypes=None,
                   REVEL=None, RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None,
                   canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None,
                   flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None,
                   gencode_basic=None, gencode_primary=None, hgvs=None, mane=None, merged=None, minimal=None,
                   mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
                   pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None,
                   shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
                   variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
        return self.get(f"vep/{species}/region/{region}/{allele}/",
                        params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                    CADD=CADD, ClinPred=ClinPred, Conservation=Conservation,
                                    DosageSensitivity=DosageSensitivity, EVE=EVE, Enformer=Enformer, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LOEUF=LOEUF, LoF=LoF,
                                    MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, OpenTargets=OpenTargets,
                                    Paralogues=Paralogues, Argument=Argument, clinsig=clinsig,
                                    clnsig_match=clnsig_match, fields=fields, min_perc_cov=min_perc_cov,
                                    min_perc_pos=min_perc_pos, Phenotypes=Phenotypes, REVEL=REVEL,
                                    RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                    appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                                    dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed,
                                    flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                    flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                    gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs, mane=mane,
                                    merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                    per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                    pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                    refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                    transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                    uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                    xref_refseq=xref_refseq), response_format=response_format)

    @vep_region.register
    def _(self, variants: list, species: str, AlphaMissense=None, AncestralAllele=None, Blosum62=None, CADD=None,
          ClinPred=None, DosageSensitivity=None, EVE=None, Enformer=None, GO=None, GeneSplicer=None, Geno2MP=None,
          IntAct=None, LOEUF=None, LoF=None, MaveDB=None, MaxEntScan=None, NMD=None, OpenTargets=None, Paralogues=None,
          Argument=None, clinsig=None, clnsig_match=None, fields=None, min_perc_cov=None, min_perc_pos=None,
          Phenotypes=None, REVEL=None, RiboseqORFs=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None,
          canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None,
          flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None,
          gencode_primary=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None,
          per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None,
          shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
          variant_class=None, vcf_string=None, xref_refseq=None, response_format='json'):
        return self.post(f"vep/{species}/region",
                         params=dict(AlphaMissense=AlphaMissense, AncestralAllele=AncestralAllele, Blosum62=Blosum62,
                                     CADD=CADD, ClinPred=ClinPred, DosageSensitivity=DosageSensitivity, EVE=EVE,
                                     Enformer=Enformer, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                                     LOEUF=LOEUF, LoF=LoF, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     OpenTargets=OpenTargets, Paralogues=Paralogues, Argument=Argument, clinsig=clinsig,
                                     clnsig_match=clnsig_match, fields=fields, min_perc_cov=min_perc_cov,
                                     min_perc_pos=min_perc_pos, Phenotypes=Phenotypes, REVEL=REVEL,
                                     RiboseqORFs=RiboseqORFs, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                     appris=appris, callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP,
                                     dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed,
                                     flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                                     flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                                     gencode_basic=gencode_basic, gencode_primary=gencode_primary, hgvs=hgvs, mane=mane,
                                     merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                     per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                     pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                     refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                     transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                     uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                     xref_refseq=xref_refseq), response_format=response_format,
                         json={"variants": variants})

    @singledispatchmethod
    def variant_recoder(self, id: str, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None,
                        gencode_basic=None, gencode_primary=None, minimal=None, var_synonyms=None, vcf_string=None,
                        response_format='json'):
        return self.get(f"variant_recoder/{species}/{id}",
                        params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                                    gencode_basic=gencode_basic, gencode_primary=gencode_primary, minimal=minimal,
                                    var_synonyms=var_synonyms, vcf_string=vcf_string), response_format=response_format)

    @variant_recoder.register
    def _(self, id: list, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None,
          gencode_primary=None, minimal=None, var_synonyms=None, vcf_string=None, response_format='json'):
        return self.post(f"variant_recoder/{species}",
                         params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                                     gencode_basic=gencode_basic, gencode_primary=gencode_primary, minimal=minimal,
                                     var_synonyms=var_synonyms, vcf_string=vcf_string), response_format=response_format,
                         json={"ids": id})

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

    def beacon_get(self, callback=None, response_format='json'):
        return self.get(f"ga4gh/beacon", params=dict(callback=callback), response_format=response_format)

    def beacon_query_get(self, alternateBases: str, assemblyId: str, end: str, referenceBases: str, referenceName: str,
                         start: str, variantType: str, callback=None, datasetIds=None, includeResultsetResponses=None,
                         response_format='json'):
        return self.get(f"ga4gh/beacon/query", params=dict(callback=callback, datasetIds=datasetIds,
                                                           includeResultsetResponses=includeResultsetResponses),
                        response_format=response_format)

    def beacon_query_post(self, alternateBases: str, assemblyId: str, end: str, referenceBases: str, referenceName: str,
                          start: str, variantType: str, callback=None, datasetIds=None, includeResultsetResponses=None,
                          response_format='json'):
        return self.post(f"ga4gh/beacon/query", params=dict(callback=callback, datasetIds=datasetIds,
                                                            includeResultsetResponses=includeResultsetResponses),
                         response_format=response_format)

    def features_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/features/{id}", params=dict(callback=callback), response_format=response_format)

    def features_post(self, end: str, referenceName: str, start: str, callback=None, featureTypes=None,
                      featuresetId=None, pageSize=None, pageToken=None, parentId=None, response_format='json'):
        return self.post(f"ga4gh/features/search",
                         params=dict(callback=callback, featureTypes=featureTypes, featuresetId=featuresetId,
                                     pageSize=pageSize, pageToken=pageToken, parentId=parentId),
                         response_format=response_format)

    def gacallSet(self, variantSetId: str, callback=None, name=None, pageSize=None, pageToken=None,
                  response_format='json'):
        return self.post(f"ga4gh/callsets/search",
                         params=dict(callback=callback, name=name, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format)

    def gacallset_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/callsets/{id}", params=dict(callback=callback), response_format=response_format)

    def gadataset(self, callback=None, pageSize=None, pageToken=None, response_format='json'):
        return self.post(f"ga4gh/datasets/search",
                         params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format)

    def gadataset_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/datasets/{id}", params=dict(callback=callback), response_format=response_format)

    def gafeatureset(self, datasetId: str, callback=None, pageSize=None, pageToken=None, response_format='json'):
        return self.post(f"ga4gh/featuresets/search",
                         params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format)

    def gafeatureset_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/featuresets/{id}", params=dict(callback=callback), response_format=response_format)

    def gavariant_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/variants/{id}", params=dict(callback=callback), response_format=response_format)

    def gavariantannotations(self, variantAnnotationSetId: str, callback=None, effects=None, end=None, pageSize=None,
                             pageToken=None, referenceId=None, referenceName=None, start=None, response_format='json'):
        return self.post(f"ga4gh/variantannotations/search",
                         params=dict(callback=callback, effects=effects, end=end, pageSize=pageSize,
                                     pageToken=pageToken, referenceId=referenceId, referenceName=referenceName,
                                     start=start), response_format=response_format)

    def gavariants(self, end: str, referenceName: str, start: str, variantSetId: str, callSetIds=None, callback=None,
                   pageSize=None, pageToken=None, response_format='json'):
        return self.post(f"ga4gh/variants/search",
                         params=dict(callSetIds=callSetIds, callback=callback, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format)

    def gavariantset(self, datasetId: str, callback=None, pageSize=None, pageToken=None, response_format='json'):
        return self.post(f"ga4gh/variantsets/search",
                         params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format)

    def gavariantset_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/variantsets/{id}", params=dict(callback=callback), response_format=response_format)

    def references(self, referenceSetId: str, accession=None, callback=None, md5checksum=None, pageSize=None,
                   pageToken=None, response_format='json'):
        return self.post(f"ga4gh/references/search",
                         params=dict(accession=accession, callback=callback, md5checksum=md5checksum, pageSize=pageSize,
                                     pageToken=pageToken), response_format=response_format)

    def references_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/references/{id}", params=dict(callback=callback), response_format=response_format)

    def referenceSets(self, accession=None, callback=None, pageSize=None, pageToken=None, response_format='json'):
        return self.post(f"ga4gh/referencesets/search",
                         params=dict(accession=accession, callback=callback, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format)

    def referenceSets_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/referencesets/{id}", params=dict(callback=callback), response_format=response_format)

    def VariantAnnotationSet(self, variantSetId: str, callback=None, pageSize=None, pageToken=None,
                             response_format='json'):
        return self.post(f"ga4gh/variantannotationsets/search",
                         params=dict(callback=callback, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format)

    def VariantAnnotationSet_id(self, id: str, callback=None, response_format='json'):
        return self.get(f"ga4gh/variantannotationsets/{id}", params=dict(callback=callback),
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
