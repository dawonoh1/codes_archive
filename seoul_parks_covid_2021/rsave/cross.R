#a look at the data frame containing our data

str(hox2010ch2)
---------------------------------------------------------
  
  #Model 0, null ('no predictors) model
  
  #call up 'lme4' package
  
  library(lme4)

M0<-lmer(popular~1+(1|l2id),data=hox2010ch2,REML=FALSE)
summary(M0)

#output in full table format using 'jtools' package

library(jtools)
summ(M0)

#test of random intercepts using 'lmerTest' package

library(lmerTest)

ranova(M0)

---------------------------------------------------------
  #Model 1 adding sex and extraversion as Level 1 predictors plus
  #teacher experience at Level 2; slopes for Level 1 predictors
  #modeled as randomly varying and correlated - model fails to converge 
  
M1<-lmer(popular~1+sex+extrav+texp+(1+sex+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M1)

summ(M1)
ranova(M1)


####

dt1 <- read.csv("E:/Dropbox/Dropbox/covid/icapps/변수/20192020dataset.csv")
attach(dt1)

Y19 <- 로그방문자수19
X19 <- cbind(로그거리미터, 로그면적제곱미터, 로그주차장면적,  버스100미터,  지하철100미터,  로그도로면적,  로그광장면적,  로그산책로면적, 로그식수대면적, 로그연못면적,  로그캠핑장면적,로그실외수영장면적, 로그운동장면적, 그늘정자수, 운동시설수,  놀이기구수, 야외음악당수, 문화회관수,  매점수, 휴게음식점수) 
Y20 <- 로그방문자수20
X20 <- cbind(로그거리미터, 로그면적제곱미터, 로그주차장면적,  버스100미터,  지하철100미터,  로그도로면적,  로그광장면적,  로그산책로면적, 로그식수대면적, 로그연못면적,  로그캠핑장면적,로그실외수영장면적, 로그운동장면적, 그늘정자수, 운동시설수,  놀이기구수, 야외음악당수, 문화회관수,  매점수, 휴게음식점수) 

M19<-lmer(Y19~X19+(1|공원)+(1|유입지),data=dt1)
M20<-lmer(Y20~X20+(1|공원)+(1|유입지),data=dt1)

summary(M19)
ranova(M19)
summary(M20)
ranova(M20)

####

M1<-lmer(Y~X+(1|공원)+(1|유입지),data=dt1,REML=FALSE)

M1<-lmer(Y~1+X+(1+lndist|ID),data=dt,REML=FALSE)
summary(M1)

summ(M1)
ranova(M1)

---------------------------------------------------------
  #Model 1A same as Model 1 except slope for sex is not treated as randomly varying
  #intercepts and slopes for extraverion are modeled as correlated
  
  M1A<-lmer(popular~1+sex+extrav+texp+(1+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M1A)

summ(M1A,digits=4)
ranova(M1A)
---------------------------------------------------------
  #Model 2 with interaction
  
  M2<-lmer(popular~1+sex+extrav+texp+extrav*texp+(1+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M2)

OR

M2<-lmer(popular~1+sex+extrav*texp+(1+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M2)

summ(M2,digits=4)
ranova(M2)

---------------------------------------------------------
  #probing interaction
  
  library(reghelper)

simple_slopes(M2)

graph_model(M2,y=popular,x=extrav,lines=texp)

---------------------------------------------------------
  #Additional model with Level 1 interaction and cross-level interaction
  #covariance of random slopes and intercepts are fixed to 0
  
  M3<-lmer(popular~1+sex*extrav+texp+extrav*texp+(1|l2id)+(0+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M3)

summ(M3,digits=4)
ranova(M3)

Note: We get an error message when using 'summary' that indicates that our results 
are singular. For more info on this topic, go here:
  
  http://127.0.0.1:29811/library/lme4/html/isSingular.html

Or simply type:
  ?isSingular

---------------------------------------------------------
  #when probing simple slopes using 'reghelper' with multiple interaction terms
  #the first interaction term is probed using 'simple_slopes' function
  #if you wish to probe the second term, you will need to re-order them
  #in the equation
  
  simple_slopes(M3)

graph_model(M3,y=popular,x=extrav,lines=sex)






############################################################################################

#Model 0, null ('no predictors) model

#call up 'lme4' package

library(lme4)

M0<-lmer(popular~1+(1|l2id),data=hox2010ch2,REML=FALSE)
summary(M0)

#output in full table format using 'jtools' package

library(jtools)
summ(M0)

#test of random intercepts using 'lmerTest' package

library(lmerTest)

ranova(M0)

---------------------------------------------------------
  #Model 1 adding sex and extraversion as Level 1 predictors plus
  #teacher experience at Level 2; slopes for Level 1 predictors
  #modeled as randomly varying and correlated - model fails to converge 
  
  M1<-lmer(popular~1+sex+extrav+texp+(1+sex+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M1)

summ(M1)
ranova(M1)

---------------------------------------------------------
  #Model 1A same as Model 1 except slope for sex is not treated as randomly varying
  #intercepts and slopes for extraverion are modeled as correlated
  
  M1A<-lmer(popular~1+sex+extrav+texp+(1+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M1A)

summ(M1A,digits=4)
ranova(M1A)
---------------------------------------------------------
  #Model 2 with interaction
  
  M2<-lmer(popular~1+sex+extrav+texp+extrav*texp+(1+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M2)

OR

M2<-lmer(popular~1+sex+extrav*texp+(1+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M2)

summ(M2,digits=4)
ranova(M2)

---------------------------------------------------------
  #probing interaction
  
  library(reghelper)

simple_slopes(M2)

graph_model(M2,y=popular,x=extrav,lines=texp)

---------------------------------------------------------
  #Additional model with Level 1 interaction and cross-level interaction
  #covariance of random slopes and intercepts are fixed to 0
  
  M3<-lmer(popular~1+sex*extrav+texp+extrav*texp+(1|l2id)+(0+extrav|l2id),data=hox2010ch2,REML=FALSE)
summary(M3)

summ(M3,digits=4)
ranova(M3)

Note: We get an error message when using 'summary' that indicates that our results 
are singular. For more info on this topic, go here:
  
  http://127.0.0.1:29811/library/lme4/html/isSingular.html

Or simply type:
  ?isSingular

---------------------------------------------------------
  #when probing simple slopes using 'reghelper' with multiple interaction terms
  #the first interaction term is probed using 'simple_slopes' function
  #if you wish to probe the second term, you will need to re-order them
  #in the equation
  
  simple_slopes(M3)

graph_model(M3,y=popular,x=extrav,lines=sex)

---------------------------------------------------------------

pupils_crossed = lmer(
  achievement ~ sex + ses 
  + (1|primary_school_id) + (1|secondary_school_id),
  data = pupils
)
## 
## summary(pupils_crossed, correlation = FALSE)



