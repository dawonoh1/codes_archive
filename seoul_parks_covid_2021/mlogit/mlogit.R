# Loading the required packages
library(foreign)
library(nnet)
library(stargazer)


# Getting the data
mydata = read.csv("E://Dropbox//Dropbox//covid//acsp//data//var_211021.csv")
mydata<-attach(mydata)
View(mydata)

#descriptive statistic
library(psych)
X <- cbind(area, BUS_500, SUB_500, parking, green.space, leisure.facility, playground, sports.facility, green.space.rate)
describe(X)


#Checking the output (dependent) variable
table(mydata$cluster)


# By default the first category is the reference.
# To change it so ‘middle’ is the reference type
mydata$cluster2 = relevel(mydata$cluster, ref = "cluster1")


factor(x = character(), levels, labels = levels,
       
       exclude = NA, ordered = is.ordered(x), nmax = NA)

#factors to categorical var
mydata$park.shape = as.factor(mydata$park.shape)
park.type = factor(park.type)

mydata$park.type = factor(mydata$park.type, levels = c('근린생활권근린공원', '광역권근린공원', '도시지역권근린공원', '도보권근린공원', '소공원/어린이공원', '기타공원', '수변공원'))
mydata$park.shape= factor(mydata$park.shape, levels = c('근린생활권근린공원', '광역권근린공원', '도시지역권근린공원',


#install.packages("mltools")
#library(mltools)
#library(data.table)

#mydata1 = one_hot(as.data.table(mydata$park.shape))
#mydata$type.park = one_hot(as.data.table(mydata$park.type))

#library(fastDummies)
#dummy_cols(.data=mydata, select_columns = c("park.shape", "park.type"), remove_first_dummy= FALSE)


# Running the multinomial logit model using the multinom() function
multi1 = multinom(cluster ~ area + BUS_100 + SUB_500 + parking +green.space..ha. + leisure.facility + playground..ha. + sports.facility +green.space.rate + park.type, data=mydata)

summary(multi1)


stargazer(multi1, type="text", out="multi1.htm")


# Relative risk ratios allow an easier interpretation of the logit coefficients. 
# They are the exponentiated value of the logit coefficients.
multi1.rrr = exp(coef(multi1))
multi1.rrr

stargazer(multi1, type="text", coef=list(multi1.rrr), p.auto=FALSE, out="multi1rrr.htm")
