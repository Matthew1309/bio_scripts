#!/usr/bin/env Nextflow

nextflow.enable.dsl=2

workflow{

  //ref_genome_ch = Channel.fromPath("$params.ref_genome")
  println([params.taxon, params.zipName, params.unzippedDir])
  DOWNLOAD_ZIP(params.taxon, params.zipName)
  UNZIP(DOWNLOAD_ZIP.out.zipFile)
  REHYDRATE(UNZIP.out.unzippedDir)
  COLLECT_NAMES(REHYDRATE.out.dataDir)

}

process DOWNLOAD_ZIP {
  errorStrategy 'ignore'

  input:
  val taxonName
  val zipName

  output:
  path "${zipName}" , emit: zipFile

  script:
  def reference = params.reference
  """
  datasets download genome \\
     taxon '${taxonName}' \\
     --dehydrated \\
     --filename ${zipName} \\
     ${reference} \\
     --exclude-genomic-cds
  """

}


process UNZIP {
  input:
  path zipFile

  output:
  path "${zipFile.baseName}" , emit: unzippedDir

  script:
  """
  unzip $zipFile -d ${zipFile.baseName}
  """

}


process REHYDRATE {
  publishDir params.results, mode:'copy'
  input:
  path unzippedDir

  output:
  path "$unzippedDir/ncbi_dataset/data" , emit: dataDir

  script:
  """
  datasets rehydrate \\
     --directory $unzippedDir
  """
}



process COLLECT_NAMES {
  publishDir params.results, mode: 'copy'

  //echo true

  input:
  path dataDir

  output:
  path "relations.tsv" , emit: org_names

  script:
  """
  python "$baseDir/bin/collect_org_names.py" $dataDir
  """

}
