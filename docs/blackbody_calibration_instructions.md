# Camera Calibration Instructions



##  Part 1: Setup

1. Turn on the blackbody (BB) so it can begin heating up
   - DO NOT turn the blackbody off until it has cooled to 50 deg C. (This process could take hours)
2. Put the black plate in the oven to heat up (faster integration times will need hotter plates)
3. Set BB and IR camera at the same distance used in the experiment
4. Ensure that the camera and the BB are at the same height, at the same level and square to each other
   - Focus the lens on the blackbody
   - The blackbody aperture will look like circles of different temperatures
   - These circles should be mostly concentric when lined up properly

## Part 2: Non Uniformity Correction (NUC)

1. Select/enter the integration time to be NUC'ed
   * Note: The integration time to be NUC'ed must be on top
2. Go to Camera>Control>Tools>User>Mode>Advanced>Advanced>Correction
3. Click Perform Correction Icon>Two Point>Next>Next> 
4. Type name of correction file to be created, then click next
   * Photon count should be in the range of 2000-3000
5. Place the low temperature plate against the front of the lens when instructed, then click next
6. Place the hot temperature plate against the front of the lens when instructed, then click next
   * Photon count should be in the range of 12000-13000
   * Adjust the plate temperatures accordingly for different integration times
   * NOTE: the order of the plates can be reversed
7. If there are only a few bad pixels accept the calibration. If there are many bad pixels discard the NUC and try again
   * It is preferable to have only the factory bad pixels in the calibration
8. Repeat for each integration time to be used
9. When done, match the integration times with the ones that the NUC presents in the same order
   * i.e. the top integration time matches to preset 0 in the camera control menu
   * We are assuming that this the correct method
10. For questions contact FLIR Instruments and Science Division at 1-866-477-3687

## Part 3: Collect Blackbody Data

1. Draw a circular region of interest (ROI) enclosing as much of the hot center as possible without getting too close to the edges
2. Repeat the following for 10-12 temperatures until the BB maximum or the camera saturates (16,383 counts)
   1. Try 100 degree increments with a filter or 25 degree increments without a filter
   2. Ensure that the BB has stabilized. This usually takes around 30-60 min for each temperature. The standard deviation is used to determine stability
   3. Adjust ROI as needed
   4. Record the 'Mean [counts]' for each filter/integration-time combination in (Tools>Stats Viewer)

## Part 4: Correlate the Photon Counts

1. Set preset 0 (the top one) to the integration time to be calibrated
2. Go to Camera>User Calibration>Perform>Advanced
3. Select Use File and browse for "ASCII for detector response" or whatever is most up to date
4. Skip Modtran for now
5. Add additional response files for the lens, filters and any other required items
   * Responses for the filters should match the plot included with the filters. The plot in the software does not render very accurately, but the values can be verified by opening the file in a text editor
   * Load response files for all the filters that will be calibrated
6. BB emissivity has a range of 0.97-0.99 so use -0.98
7. Do not compensate for reflected radiance
8. Add all the temperature calibration point values that were used for the calibration. Use the actual temperature the blackbody stabilizes at not the setpoint
9. If creating an external calibration file (this is the recommended method)
   * Record the radiance values, and plot them against the recorded counts. The trend should be linear
   * NOTE: the radiance values are a function of blackbody temperature, emissivity, and selected filter response files, but not integration time. The integration time and current sensor chemistry control the number of counts, which is correlated to the radiance by this procedure.
10. If creating a camera calibration file using the FLIR software
   * Click the additional response tab and make sure that the correct filter is selected
   * Click back to the Cal Points tab and enter the counts recorded under preset 0
   * Check that the plot at the bottom is linear
   * Save the calibration
     * Go to Camera>User Calibration
     * 'Save' will save a text file and a .cal file. The text file contains the coefficients of the curvefit