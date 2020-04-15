##Enrique Cervantes cs 4331

cov_data <- read.csv("../data/us_states_covid19_daily.csv", sep = ",")
##Adding Index field 
n <- dim(cov_data)[1]
cov_data$Index <- c(1:n)
head(cov_data)

##Standardizing numeric fields, adding z value rows for each positive/negative tests, hospitalized patients, death toll, total test results
cov_data$positive_z <- scale(x = cov_data$positive)
cov_data_positive_outliers <- cov_data[which(cov_data$positive_z < -3 | cov_data$positive_z >3),]
cov_data_sort_positive <- cov_data[order(-cov_data$positive_z),]
cov_data_sort_positive[1:15,]
head(cov_data_sort_positive)
cov_data_sort_positive[1:15,c(1,3)]

cov_data$negative_z <- scale(x = cov_data$negative)
cov_data_negative_outliers <- cov_data[which(cov_data$negative_z < -3 | cov_data$negative_z > 3),]
cov_data_sort_negative <- cov_data[order(-cov_data$negative_z),]
cov_data_sort_negative[1:15]
head(cov_data_sort_negative)
cov_data_sort_negative[1:15, c(1,3)]

cov_data$hospitalized_z <- scale(x = cov_data$hospitalized)
cov_data_hospitalized_outliers <- cov_data[which(cov_data$hospitalized_z < -3 | cov_data$hospitalized_z > 3),]
cov_data_sort_hospitalized <- cov_data[order(-cov_data$hospitalized_z),]
cov_data_sort_hospitalized[1:15]
head(cov_data_sort_hospitalized)
cov_data_sort_hospitalized[1:15, c(1,3)]

cov_data$death_z <- scale(x = cov_data$death)
cov_data_death_outliers <- cov_data[which(cov_data$death_z < -3 | cov_data$death_z > 3),]
cov_data_sort_death <- cov_data[order(-cov_data$death_z),]
cov_data_sort_death[1:15]
cov_data_sort_death[1:15, c(1, 3)]

cov_data$total_z <- scale(x = cov_data$total)
cov_data_total_outliers <- cov_data[which(cov_data$total_z < -3 | cov_data$death_z > 3),]
cov_data_sort_total <- cov_data[order(-cov_data$total_z),]
cov_data_sort_total[1:15]
cov_data_sort_total[1:15, c(1,3)]

cov_data$totalTestResults_z <- scale(x = cov_data$totalTestResults)
cov_data_totalTestResults_outliers <- cov_data[which(cov_data$totalTestResults_z < -3 |cov_data$totalTestResults_z > 3),]
cov_data_sort_results <- cov_data[order(-cov_data$totalTestResults_z),]
cov_data_sort_results[1:15]
cov_data_sort_results[1:15, c(1,3)]


##write updated csv file
write.csv(cov_data,"../data/new_us_states_covid19_daily.csv",row.names = FALSE)
