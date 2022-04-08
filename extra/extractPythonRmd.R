library("knitr")

# New processing functions
process_tangle <- function (x) { 
  UseMethod("process_tangle", x)
}

process_tangle.block <- function (x) {
  params = opts_chunk$merge(x$params)
  
  # Suppress any code but python
  if (params$engine != 'python') {
    params$purl <- FALSE
  }
  if (isFALSE(params$purl)) 
    return("")
  label = params$label
  ev = params$eval
  code = if (!isFALSE(ev) && !is.null(params$child)) {
    cmds = lapply(sc_split(params$child), knit_child)
    one_string(unlist(cmds))
  }
  else knit_code$get(label)
  if (!isFALSE(ev) && length(code) && any(grepl("read_chunk\\(.+\\)", 
                                                code))) {
    eval(parse_only(unlist(stringr::str_extract_all(code, 
                                                    "read_chunk\\(([^)]+)\\)"))))
  }
  code = knitr:::parse_chunk(code)
  if (isFALSE(ev)) 
    code = knitr:::comment_out(code, params$comment, newline = FALSE)
  # Output only the code, no documentation
  return(knitr:::one_string(code))
}

# Reassign functions
assignInNamespace("process_tangle.block",
                  process_tangle.block,
                  ns="knitr")

# Purl
extractPythonRmd <- function(file)
{
  outputFile <- sub("Rmd","py",file)
  purl(file, output=outputFile)
}
