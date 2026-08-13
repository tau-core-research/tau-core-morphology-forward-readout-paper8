# LITTLE THINGS OSCC-1 capacity scoring v02

Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`

The score transports only the frozen v02-minus-TPG correction through the source-native H I beam. Capacity is computed separately from the noise-whitened local Jacobian with water filling; it is not reused as an attenuation factor.

On the 14-galaxy primary lane, mean RMSE is `8.962 km/s`, versus `8.962` for raw v02 and `8.976` for TPG. Mean OSCC-minus-TPG is `-0.014 km/s`; mean OSCC-minus-v02 is `-0.000 km/s`. The nominal operational capacity is `0.790` bits per profile use on average, with `4.71` active modes.

The numerical capacity depends on the declared `G=I/n` source-cost convention and a diagonal noise approximation. It is not yet a parent-derived physical capacity.
