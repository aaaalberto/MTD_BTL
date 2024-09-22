import ROOT

###################################
# CROSSTALK RATIO FITTING (alberto)
###################################
def fit_ct_ratio(h):
    """
    Fits the gaussian peak in ROOT histogram `h.
    Returns the fit parameters [mean, sigma, integral].
    """
    
    h_max = h.GetMaximum()
    h_mean = h.GetMean()
    h_RMS = h.GetRMS()
    
    # Gaussian fit
    f = ROOT.TF1(f"{h.GetName()}_fit",f"gaus", 0.0 , 1.0 )
    #f.SetNpx(10000)
    f.SetLineColor(ROOT.kViolet)
    f.SetParameter(0, h_max)
    f.SetParameter(1, h_mean)
    f.SetParameter(2, h_RMS / 2)
    f.SetParLimits(0, 0.5*h_max, 2.0*h_max) #Amplitude between 50% and 200% of the max
    f.SetParLimits(2, 0, 2*h_RMS)  # Constrain sigma to be non-negative


    r = h.Fit(f, 'QS',  '', h_mean - h_RMS, h_mean + h_RMS )
    
    
    # Secondary fit for better precision
    h_mean = f.GetParameter(1)
    h_RMS = f.GetParameter(2)
    
    r = h.Fit(f, 'QS', '', h_mean - 4*h_RMS, h_mean + 4*h_RMS )

    h.Write()
    
    if not r.IsValid() or r.Status() != 0:
        return None

    
    # (amplitude, mean, sigma)
    return [f.GetParameter(i) for i in range(3)], [f.GetParError(i) for i in range(3)]