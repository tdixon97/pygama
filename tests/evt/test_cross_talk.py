import awkward as ak
from pygama.evt.modules import cross_talk
import pytest
def test_cross_talk_corrected_energy_awkard_slow():

    
    energies_test=ak.Array([[1000,200],[100],[500,3000,100]])
    rawid_test   =ak.Array([[1,2],[3],[1,2,3]])

    ## first check exceptions
    matrix={1:{1:1.00, 2:0.01, 3:0.02, 4:0.00},
            2:{1:0.01, 2:1.00, 3:0,    4:0.01},
            3:{1:0.02, 2:0.00, 3:1.00, 4:0.01},
            4:{1:0.00, 2:0.01, 3:0.01, 4:1.00}
            }  

    # if rawid and energies have different shapes (juts the first entry)
    with pytest.raises(ValueError):
        cross_talk.cross_talk_corrected_energy_awkard_slow(ak.Array([[1000,200]]),rawid_test,matrix,True)

    # filter some values from energy first so each event has a different size
    with pytest.raises(ValueError):
        cross_talk.cross_talk_corrected_energy_awkard_slow(energies_test[energies_test!=1000],rawid_test,matrix,True)

    ## checks on the matrix
    # first check if the matrix has empty elements an exception is raised if allow_non_existing is false
    matrix_not_full={1:{1:1.00, 2:0.01, 3:0.02, 4:0.00},
                    2:{1:0.01, 2:1.00, 3:0},
                    3:{1:0.02, 2:0.00, 3:1.00, 4:0.01},
                    4:{1:0.00, 3:0.01, 4:1.00}
                    }  
    
    with pytest.raises(ValueError):
        cross_talk.cross_talk_corrected_energy_awkard_slow(energies_test,rawid_test,matrix_not_full,False)
    
    matrix_not_sym={1:{1:1.00, 2:0.0, 3:0.02, 4:0.00},
                    2:{1:0.01, 2:1.00, 3:0,    4:0.01},
                    3:{1:0.02, 2:0.00, 3:1.00, 4:0.01},
                    4:{1:0.00, 2:0.01, 3:0.01, 4:1.00}
                    } 
    with pytest.raises(ValueError):  
        cross_talk.cross_talk_corrected_energy_awkard_slow(energies_test,rawid_test,matrix_not_sym,True)

    ## now check the result returned (given no exceptions)
    ### 1st event is two channels 1% cross talk and [1000,200] energy so we expect Ecorr  = [1002,210] 
    ### 2nd event one channel so the energy shouldnt change
    ### 3rd event  3 channels [500,3000,100] energy ch1 has 1% ct to ch2 and 2% to ch3 so we will have
    ### E=[500,3005,102] then ch2 has 1% cross talk to ch1 and  0 to ch3
    ### E= [503,3005,102] finally ch3 has 2% cross talk with ch1
    ### E=[505,3005,102]
 
    energy_corr =cross_talk.cross_talk_corrected_energy_awkard_slow(energies_test,rawid_test,matrix,True)   

    assert np.all(energy_corr[0].to_numpy()==np.array([1002,210]))
    assert np.all(energy_corr[1].to_numpy()==np.array([100]))
    assert np.all(energy_corr[2].to_numpy()==np.array([505,3005,102]))