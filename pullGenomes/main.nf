#!/usr/bin/env/Nextflow

nextflow.enable.dsl=2

genomeFiles = Channel
            .fromPath(params.filesFortSCAN)
            .splitCsv(header:false, sep:"\t")
            .map{ row -> file(row[3]) }

workflow{

  TRNASCAN( genomeFiles )
  TRANSFORM2CSV( TRNASCAN.out.tRNAs )

  COMPILECSV( TRANSFORM2CSV.out.tRNACSVS.collect() )

}


process TRNASCAN {
  // Given the paths to genomes, run TRNASCAN
  // and extract the ss and sequence information

  publishDir "${params.tRNAresults}", mode:'copy'

  input:
  file genome

  output:
  path "${genome.baseName}.ss" , emit: tRNAs

  script:
  def reference = params.reference
  def threads = ""
  if (params.max_cpus) { threads = "--thread ${params.max_cpus}"}
  """
  tRNAscan-SE \\
  ${threads} \\
  -q \\
  $params.domain \\
  -f "${genome.baseName}.ss" \\
  "${genome}"
  """

}


process TRANSFORM2CSV {
  //publishDir "${params.tRNAresults}/CSVs", mode:'copy'

  input:
  file tRNA_ss

  output:
  path "${tRNA_ss.baseName}.csv" , emit: tRNACSVS

  script:
  """
  python "$projectDir/bin/parseSS.py" $tRNA_ss
  """
}

process COMPILECSV {
  publishDir "${params.tRNAresults}/CSVs", mode:'copy'

  echo true

  input:
  file csvList

  output:
  path "organism_tRNAs.csv"

  script:
  """
  python "$projectDir/bin/concatCSV.py" $csvList

  """

}
