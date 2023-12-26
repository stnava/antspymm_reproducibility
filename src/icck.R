
## Intraclass Correlation Coefficients with  95 % C.I.
##            Model         Measures  Type    ICC Lower CI Upper CI
## 1 one-way random        Agreement  ICC1 0.1286  0.05437   0.2936
## 2 two-way random        Agreement  ICC2 0.1672  0.07871   0.3408
## 3  two-way fixed      Consistency  ICC3 0.8266  0.72401   0.9177
## 4 one-way random   Avg. Agreement ICC1k 0.7264  0.50861   0.8821
## 5 two-way random   Avg. Agreement ICC2k 0.7832  0.60597   0.9030
## 6  two-way fixed Avg. Consistency ICC3k 0.9885  0.97926   0.9950

icck <- function( indf, outcome, k=6, lmeru=FALSE, agree=FALSE  ) {
  # see: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0219854&type=printable
  # see: QUANTIFYING TEST-RETEST RELIABILITY USING THE INTRACLASS CORRELATION COEFFICIENT AND THE SEM
  # RANDOM+AvgAgree+1-way
  # a. 1-way or 2-way model:
  # --- 1-way b/c not all sites do all subjects
  # b. fixed or random effect model:
  # --- random b/c sites are a random selection of possible models
  # c. include or exclude systematic error in the ICC:
  # --- include it to handle large systematic effects ... a model 2 style
  # d. single or mean score:
  # --- mean scores when considering statistical summary data e.g.
  # Purpose of Measurement: If you need to know that different raters or instruments give exactly the same score (e.g., blood pressure readings), use the agreement model. If you’re more interested in whether raters or instruments rank subjects similarly (e.g., ranking of performance), use the average agreement model.
  #
  # k = 6 for average consistency
  #
  # use agree when dealing with factors
  if ( agree ) {
    mick = agree_coef( wide=FALSE, 
      measure="outcome", item="Site", id="Subject", 
      data=dd )
    return( mick )
  }
  if ( lmeru ) mick = reli_stats( outcome, item="Site", id="Subject", data=indf )
  if ( !lmeru) mick = reli_aov( outcome, item="Site", id="Subject", data=indf )
  return(  mick$icc[k,'icc'] )
}

