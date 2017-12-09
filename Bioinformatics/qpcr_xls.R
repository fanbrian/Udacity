library(readxl)

qpcr_xls = function(folder = 'path to folder with xls files'){
  
  # create list of all .xls files in folder
  file_list <- list.files(path=folder, pattern="*.xls")
  
  #read in individual xls files, skipping first 46 rows
  raw_data <- lapply(file_list, function(x) read_xls(paste(folder, x, sep=''), skip=46))
  
  #selecting desired columns (variables) from each xls file
  clean_data <- lapply(raw_data, function(x) x[c(4:5,12:15,18:23)])
  
  #combining xls files
  data <- do.call("rbind", lapply(clean_data, function(x) x))
  
}