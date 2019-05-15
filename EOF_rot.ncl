; ==============================================================
; eof_5.ncl
;
; Concepts illustrated:
;   - Calculating standard EOFs
;   - Rotate EOFs via varimax method
;   - Reorder the varimax EOFs to be is descending order
;   - Using coordinate subscripting to read a specified geographical region
;   - Calculating symmetric contour intervals
;   - Drawing filled bars above and below a given reference line
;   - Drawing subtitles at the top of a plot
;
; ==============================================================
; NCL V6.4.0 has new functions eofunc_n_Wrap and 
; eofunc_ts_n_Wrap that allow you to calculate the EOFs without 
; first having to first reorder the data. See eof_3_640.ncl.
; ==============================================================
; Calculate Northern Hemisphere 500 hPa EOFs 
; ==============================================================
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

; ==============================================================
; User defined parameters that specify region of globe and
; ==============================================================
; ==============================================================
; User defined parameters that specify region of globe and
; ==============================================================

  vname  = "msl"               ; variable name
  yrStrt =1979 
  yrLast = 2018
;  season = "DJF"               ; choose Dec-Jan-Feb seasonal mean

  neof   =  30                  ; number of standard EOFs to calculate
  optEOF = False      
  optETS = False

; ==============================================================
; Open the file: Read only the user specified period
; ==============================================================
   fils = systemfunc ("ls *.nc") ; file paths
   f    = addfiles (fils, "r")   

   ListSetType (f, "cat")        ; concatenate (=default)
  TIME   = f[:]->time
  YYYY   = cd_calendar(TIME,-1)                 ; entire file
; iYYYY  = ind(YYYY.ge.yrStrt .and. YYYY.le.yrLast)
;print(iYYYY)
;return
;print(iYYYY)
VAR    = short2flt(f[:]->$vname$(:,:,:))
printVarSummary(VAR)                              ; variable overview
;print(zAvgLon)
sst = rmMonAnnCycTLL(VAR) 
sst1 = dtrend_msg_n(ispan(0,dimsizes(sst&time)-1,1),sst,True,False,0) ; detrend the data 

;zAvgLon = dim_avg_n_Wrap( sst1, (/1,2/) )
;asciiwrite (""+vname+"-"+unit+"-2004-2016-daily", zAvgLon)
;return
printVarSummary(sst1)
copy_VarCoords(sst,sst1) 
printVarSummary(sst1)
; ==============================================================
; compute desired global seasonal mean: month_to_season (contributed.ncl) 
; ==============================================================
; =================================================================
; create weights:  sqrt(cos(lat))   [or sqrt(gw) ] for covariance
; =================================================================
  rad    = 4.0*atan(1.0)/180.0
  clat   = cos(rad*sst1&latitude)           
  clat   = where(clat.lt.0, 0.0, clat)  ; avoid a potential numerical issue at pole
  clat   = sqrt( clat )  ; avoid a potential numerical issue at pole

; =================================================================
; weight all observations 
; =================================================================
  wvar   = VAR                                   ; copy meta data
  wvar   = VAR*conform(sst1, clat, 1)
  wvar@long_name = "Wgt: "+wvar@long_name

; =================================================================
; EOF
; Reorder (lat,lon,time) the *weighted* input data
; Access the area of interest via coordinate subscripting
; =================================================================
  x      = wvar(latitude|:,time|:,longitude|:)

;printVarSummary(x)
x    = lonFlip(x)
printVarSummary(x)  
x1    = x(latitude|:,longitude|:,time|:)
printVarSummary(x1)  
;x1=x1- Kelvin  ;;;;"deg C"
;x1=x1*100  ;;;;"deg C"
  eof    = eofunc_Wrap(x1, neof, optEOF)      
  eof_ts = eofunc_ts_Wrap (x1, eof, optETS)
; =================================================================
; Perform varimax rotation
; =================================================================

eof_rot = eofunc_varimax_Wrap( eof, 1 )
  eofrot_ts = eofunc_ts_Wrap (x1, eof_rot, optETS)
printVarSummary( eof_rot )        
print("eof_rot: min="+min(eof_rot)+"   max="+max(eof_rot) )
printVarSummary( eof_rot )        
prinfo=True
sig_pcv = eofunc_north(eof@pcvar, neof, prinfo)
; =================================================================
; put into descending order
; =================================================================

  eofunc_varimax_reorder( eof_rot )
  printVarSummary( eof_rot )        

printMinMax(eof_rot(0,:,:),0)
; =================================================================
; Normalize time series: Sum spatial weights over the area of used
; =================================================================
do gg = 0,neof-1
eofrot_ts(gg,:) = dim_standardize(eofrot_ts(gg,:),0) ; standardize PC1 
print(eof_ts)
asciiwrite ("eof_ts-"+vname+"-"+gg+"", eofrot_ts(gg,:))
asciiwrite ("eof_MaxAbsValue-"+vname+"_"+gg+"", max(abs(eof_rot(gg,:,:))))
end do

printMinMax(eof_ts(0,:),0)
; =================================================================
; Extract the YYYYMM from the time coordinate 
; associated with eof_ts [same as var&time] 
; =================================================================

  yyyymm = cd_calendar(eof_ts&time,-2)/1  
;;yrfrac = yyyymm_to_yyyyfrac(yyyymm, 0.0); not used here
return
