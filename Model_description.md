# Process based approachvsimulation model
- Object/parameters names in python version in parethesis

## Arrivals: generate new patients
## Patient
- Time when patient enters system tStart (self.start_time)
- Time when patient exits system tEnd (self.end_time)
- Time when patient starts to wait to get to recovery tStartedWaiting (self.time_operation_done)
- Time when patient stops waiting to get to recovery tEndWaiting (self.time_recovery_start)
## Preparation service (queue)
## Operation service (queue with one slot)
## Recovery service (queue)
## Reporter (statistics)
- decide which components will be active processes (with own life cycles)
## Patient
- sketch the life-cycles (ordered (conditional) sequence of actions that change the system variables or manipulate other life-cycles
- arrivals
- create new patient 
- tStart = now()
- schedule arrival for new patient
- Operation service
- tStartedWaiting = now() + surgeryTime
- Recovery service
- tEndWaiting = now()
- tEnd = now() + timeInRecovery
## Additional feature
- During the preparation, some new information is found and the surgery needs to be cancelled
- cancelling probability needed (self.operation_cancelled)
- skip the operation and recovery phases
