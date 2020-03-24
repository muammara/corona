install.packages("googleVis")
library(googleVis)
wd='C:/Users/muamma/Documents/python/Coronavirus'
setwd(wd)
flagfilename<-'coronafilename'  #Storing the name of the latest file
filename<- readChar(flagfilename, file.info(flagfilename)$size)

print(filename)

fieldsformat=c("numeric", "character","factor","factor","factor","numeric","numeric","factor","factor","numeric","numeric")

C<-read.csv(filename,sep=",",colClasses=fieldsformat)

C$DateRep <- as.Date(C$DateRep,format="%Y-%m-%d")
C2 <-gvisMotionChart(data=C,idvar="Countries.and.territories" ,xvar = "TotalDeath", yvar = "TotalCases",
                     sizevar = "TotalDeath",timevar="DateRep",options=list(width=1200,height=600))
plot(C2)
cat(C2$html$chart, file="tmp.html")

