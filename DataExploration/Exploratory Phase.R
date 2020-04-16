library(ggplot2)

Combined_data <- read.csv("New_CountyHospitalCombined.csv", sep = ",")
cov_data <- read.csv("CovCountyHospitalTimeSeries.csv", sep = ",")

t.v1 <- table(Combined_data$BEDS, Combined_data$HELIPADS)
t.v2 <- addmargins(A = t.v1, FUN = list(total=sum),quiet = TRUE)
t.v1.rnd <- round(prop.table(t.v1, margin = 2)*100,1)

##Plots to finds the frequency of beds, helipads, and size of population per county

Combined_data$BEDS <- cut(x=Combined_data$BEDS,breaks = c(0,91,250,1000),right = FALSE,
                          labels = c("0 to 90","91 to 250","over 1000"))
ggplot(Combined_data, aes(BEDS))+geom_bar()

Combined_data$HELIPADS <- cut(x=Combined_data$HELIPADS, breaks = c(0,1,3,5),right = FALSE, 
                          labels = c("0 to 1","1 to 3","over 3"))
ggplot(Combined_data, aes(HELIPADS))+geom_bar(aes(fill=GOVERNM))


Combined_data$POPEST2019 <- cut(x=Combined_data$POPEST2019,breaks = c(500,15000,35000,60000,100000),right = FALSE,
                                labels = c("500 to 15000","15001 to 35000","60000 to 1000000", "Over 100000"))
ggplot(Combined_data, aes(POPEST2019))+labs(x="Population estimate of 2019")+geom_bar()

##Plots beds vs New cases/deaths and population vs New cases/deaths
ggplot(aes(x=beds,y=c2020.04.12),data = cov_data)+labs(y="Number of cases on 4/12/2020",x="Number of Beds")+geom_point()

ggplot(aes(x=beds,y=d2020.04.12),data = cov_data)+labs(y="Number of deaths on 4/12/2020",x="Number of Beds")+geom_point()

ggplot(aes(x=population,y=c2020.04.12), data =cov_data)+labs(x="Population",y="Number of cases on 4/12/2020")+geom_point()

ggplot(aes(x=population,y=d2020.04.12), data =cov_data)+labs(x="Population",y="Number of Deaths on 4/12/2020")+geom_point()
