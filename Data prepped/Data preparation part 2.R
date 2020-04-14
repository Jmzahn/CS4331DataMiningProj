hospital_data <- read.csv("Hospitals.csv",sep = ",")
combined_data <- read.csv("CountyHospitalCombined.csv",sep = ",")

##Adding index field to hospital data
n1 <- dim(hospital_data)[1]
hospital_data$Index <- c(1:n1)
head(hospital_data)
##Cleaning up the data, removing misleading values
hospital_data$BEDS[hospital_data$BEDS < 0] <- NA
hospital_data$POPULATION[hospital_data$POPULATION < 0] <- NA
hospital_data$TTL_STAFF[hospital_data$TTL_STAFF < 0] <- NA
##Writting updated data set
write.csv(hospital_data,"New_Hospital_data.csv", row.names = FALSE)


##Adding index field to combined data
n2 <- dim(combined_data)[1]
combined_data$Index <- c(1:n2)
head(combined_data)
##Standardizing numberic fields and adding z-values to combined data
combined_data$Beds_z <- scale(x = combined_data$BEDS)
combined_data_beds_outliers <- combined_data[which(combined_data$Beds_z < -3 | combined_data$Beds_z > 3),]
combined_data_sort_beds <- combined_data[order(-combined_data$Beds_z),]
combined_data_sort_beds[1:15,]
combined_data_sort_beds[1:15, c(1,3)]

combined_data$POPEST2019_z <- scale(x = combined_data$POPEST2019)
combined_data_pop_outliers <- combined_data[which(combined_data$POPEST2019_z < -3 | combined_data$POPEST2019_z > 3),]
combined_data_sort_pop <- combined_data[order(-combined_data$POPEST2019_z),]
combined_data_sort_pop[1:15,]
combined_data_sort_pop[1:15, c(1,3)]

combined_data$HELIPADS_z <- scale(x= combined_data$HELIPADS)
combined_data_heli_outliers <- combined_data[which(combined_data$HELIPADS_z < -3 | combined_data$HELIPADS_z > 3),]
combined_data_sort_heli <- combined_data[order(-combined_data$HELIPADS_z),]
combined_data_sort_heli[1:15,]
combined_data_sort_heli[1:15,c(1,3)]

combined_data$NONPROF_z <- scale(x= combined_data$NONPROF)
combined_data_non_outliers <- combined_data[which(combined_data$NONPROF_z < -3 | combined_data$NONPROF_z > 3),]
combined_data_sort_non <- combined_data[order(-combined_data$NONPROF_z),]
combined_data_sort_non[1:15,]
combined_data_sort_non[1:15,c(1,3)]

combined_data$PRIVATE_z <- scale(x= combined_data$PRIVATE)
combined_data_private_outliers <- combined_data[which(combined_data$PRIVATE_z < -3 | combined_data$PRIVATE_z > 3),]
combined_data_sort_private <- combined_data[order(-combined_data$PRIVATE_z),]
combined_data_sort_private[1:15,]
combined_data_sort_private[1:15,c(1,3)]

combined_data$GOVERNM_z <- scale(x= combined_data$GOVERNM)
combined_data_gov_outliers <- combined_data[which(combined_data$GOVERNM_z < -3 | combined_data$GOVERNM_z > 3),]
combined_data_sort_gov <- combined_data[order(-combined_data$GOVERNM_z),]
combined_data_sort_gov[1:15,]
combined_data_sort_gov[1:15,c(1,3)]


##Writting updated data set
write.csv(combined_data, "New_CountyHospitalCombined.csv", row.names = FALSE)

