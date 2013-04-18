from __future__ import division
import numpy as np
from matplotlib import pyplot as plt

import pyhsmm
pyhsmm.internals.states.use_eigen()

N = 4
T = 500
obs_dim = 2

obs_hypparams = {'mu_0':np.zeros(obs_dim),
                'sigma_0':np.eye(obs_dim),
                'kappa_0':0.3,
                'nu_0':obs_dim+5}

# Construct the true observation and duration distributions
true_obs_distns = [pyhsmm.distributions.Gaussian(**obs_hypparams) for state in range(N)]
true_dur_distns = [pyhsmm.distributions.NegativeBinomialIntegerRVariantDuration(np.r_[1.,0.,1.],100.,10.)
                        for state in range(N)]

# Build the true HSMM model
truemodel = pyhsmm.models.HSMM(
        alpha=6.,gamma=6.,
        init_state_concentration=10.,
        obs_distns=true_obs_distns,
        dur_distns=true_dur_distns)

# Sample data from the true model
data, labels = truemodel.generate(T)

### posterior

usualmodel = pyhsmm.models.HSMM(
        init_state_concentration=10.,
        obs_distns=true_obs_distns,
        dur_distns=true_dur_distns,
        trans_distn=truemodel.trans_distn)
usualmodel.add_data(data)

specialmodel = pyhsmm.models.HSMMIntNegBin(
        init_state_concentration=10., # pretty inconsequential
        obs_distns=true_obs_distns,
        dur_distns=true_dur_distns,
        trans_distn=truemodel.trans_distn)
specialmodel.add_data(data)

specialbetalslow, specialbetalslow2 = specialmodel.states_list[0].messages_backwards_python()
specialbetal, specialsuperbetal = specialmodel.states_list[0].messages_backwards()

plt.figure()
plt.plot(specialbetalslow[:,0],'bx-',label='slow 1')
plt.plot(specialbetalslow2[:,0],'r+-',label='slow 2')
plt.plot(specialbetal[:,0],'g--',label='good guys')
plt.legend(loc='best')

plt.show()

