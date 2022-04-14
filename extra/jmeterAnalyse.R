### Analyse function for the load tests from Jmeter

extractTests<-function(file)
{
  res<-read.table(file,sep=",",h=T)
  index<-as.numeric(sub(".*[0-9]{1,2}-([0-9]{1,2})$","\\1",res$threadName))
  res$index<-index
  res<-res[order(index),]
  #colnames(res)<- c("timestamp","elapsed","label","responseCode","responseMessage","threadName","dataType","success","bytes","grp_thread","allThreads","latency")
  return(res)
}


analyseJmeterTests<-function(tests){
  time0<-min(tests$timeStamp)
  timeStart <-tests$timeStamp-time0
  timeLat <- timeStart+tests$Latency
  timeEnd <- timeStart+tests$elapsed
  totalTime_sec <- (max(timeEnd)-min(timeStart))/1000
  success<- tests$success=='true'&tests$responseCode==200
  percentError <- (1-(sum(success)/nrow(tests)))*100
  meanElapsed <- mean(tests$elapsed)
  meanLatency <- mean(tests$Latency)
  meanElapsedSuccess <- mean(tests$elapsed[success])
  meanLatencySuccess <- mean(tests$Latency[success])
  nbUser <- nrow(tests)
  throughput <-nbUser/totalTime_sec
  return(list(nbUser = nbUser, time0 = time0, success = success, percentError =percentError, timeStart = timeStart, timeLat = timeLat, timeEnd = timeEnd, totalTime_sec = totalTime_sec, meanElapsed = meanElapsed, meanElapsedSuccess = meanElapsedSuccess, meanLatency = meanLatency, meanLatencySuccess = meanLatencySuccess, throughput = throughput))
}

#basicFacts<-function(tests,present_kable=T, kable_caption="Basic facts in JMeter test results", kable_label="basFactsJmeter")
#{
 
#}

plotanalysisJmeter<-function(analysisJmeter,timeMaxMs = NA,legend=T, legendPlacement="topright",...)
{
  if(is.na(timeMaxMs))
  {timeMaxMs <- max(analysisJmeter$timeEnd)}
  XLIM<-c(0,timeMaxMs)
  plot(x=range(c(analysisJmeter$timeStart, analysisJmeter$timeEnd)), y = c(analysisJmeter$nbUser,1),type="n",yaxt="n",axes=F,ylab=NA,xlab="Time (s.)",xlim=XLIM,...)
  segments(x0=analysisJmeter$timeStart, y0=analysisJmeter$nbUser - (0:(analysisJmeter$nbUser-1)), x1=analysisJmeter$timeEnd,col=ifelse(analysisJmeter$success, "blue", "red"))
  if(timeMaxMs<10000)
  {
    AT <-seq(0,timeMaxMs,length.out=4)
  }else{
    AT <-seq(0,timeMaxMs,by=5000)
  }
  axis(1,at=AT,labels = round(AT/1000,2))
  points(x=analysisJmeter$timeLat, y = analysisJmeter$nbUser-(0:(analysisJmeter$nbUser-1)),pch=4)
  if(legend){
  legend(legendPlacement,lwd=c(1,1,NA),col=c("blue","red","black"),pch=c(NA,NA,4),legend=c("success","failure","latency"),bty="n")
  }
}
